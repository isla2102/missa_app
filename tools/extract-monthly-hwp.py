"""Extract user-provided HWP 5 paragraph records; candidates are never verified app data.
Dependency: olefile 0.47 in scratch/hwp-deps. Run from the project root.
"""
from pathlib import Path
import sys, struct, zlib, hashlib, json, re, calendar
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scratch/hwp-deps'))
import olefile
EXTENDED=set(range(1,10))|{11,12}|set(range(14,24))
def paragraph_text(data):
    if len(data)%2: raise ValueError('odd UTF-16 record')
    units=struct.unpack('<'+'H'*(len(data)//2),data); out=bytearray(); i=0
    while i<len(units):
        c=units[i]
        if c in EXTENDED:
            if i+8>len(units): raise ValueError('truncated control')
            if c==9:out.extend(' '.encode('utf-16le'))
            i+=8;continue
        if c>=32:out.extend(struct.pack('<H',c))
        i+=1
    return out.decode('utf-16le').strip()
def extract(path):
    result=[]
    with olefile.OleFileIO(path) as doc:
        header=doc.openstream('FileHeader').read()
        if not header.startswith(b'HWP Document File'):raise ValueError('unsupported HWP')
        flags=struct.unpack_from('<I',header,36)[0]
        if flags&2:raise ValueError('encrypted HWP')
        streams=sorted((s for s in doc.listdir() if s[0]=='BodyText'),key=lambda s:int(s[-1].replace('Section','')))
        for stream in streams:
            raw=doc.openstream(stream).read()
            if flags&1:raw=zlib.decompress(raw,-15)
            pos=0;ordinal=0
            while pos<len(raw):
                if pos+4>len(raw):raise ValueError('truncated record header')
                offset=pos;h=struct.unpack_from('<I',raw,pos)[0];pos+=4;n=h>>20
                if n==4095:
                    if pos+4>len(raw):raise ValueError('truncated size')
                    n=struct.unpack_from('<I',raw,pos)[0];pos+=4
                if pos+n>len(raw):raise ValueError('truncated record body')
                data=raw[pos:pos+n];pos+=n
                if h&1023==67:
                    ordinal+=1;t=paragraph_text(data)
                    if t:result.append(dict(stream='/'.join(stream),recordOffset=offset,paragraph=ordinal,text=t))
    return result
DATE=re.compile(r'^(10|11|12)월\s*(\d{1,2})일(?:\s|$)')
TITLES=['영성체 후 기도','예물 기도','본기도','입당송','영성체송']
def catalogue(rows,month):
    groups=[];current=None
    for row in rows:
        m=DATE.match(row['text'])
        if m:
            date=f'2026-{int(m[1]):02}-{int(m[2]):02}'
            if int(m[1])!=month:raise ValueError('month mismatch')
            current=dict(date=date,heading=row['text'],paragraphs=[],sections=[],status='needs-review');groups.append(current)
        if current:current['paragraphs'].append(row)
    for group in groups:
        section=None
        for row in group['paragraphs'][1:]:
            title=next((t for t in TITLES if row['text'].startswith(t)),None)
            if title:
                section=dict(title=title,heading=row['text'],paragraphs=[]);group['sections'].append(section)
            elif section:section['paragraphs'].append(row)
        group['missingHeadings']=[t for t in TITLES if not any(s['title']==t for s in group['sections'])]
    return groups

def main():
    assert paragraph_text('가나다'.encode('utf-16le'))=='가나다'
    assert paragraph_text(struct.pack('<8H',2,123,456,0,0,0,0,2)+'기도'.encode('utf-16le'))=='기도'
    try:paragraph_text(b'\x00');raise AssertionError('bad record accepted')
    except ValueError:pass
    out=ROOT/'data/source-library/extracted-hwp';out.mkdir(exist_ok=True)
    files=[];days=[]
    for kind in ['monthly-propers','hymn-schedules']:
        for path in sorted((ROOT/'data/source-library'/kind/'originals').glob('*.hwp')):
            rows=extract(path);sha=hashlib.sha256(path.read_bytes()).hexdigest()
            item=dict(sourcePath=path.relative_to(ROOT).as_posix(),sha256=sha,kind=kind,status='extracted-not-proofread',paragraphs=rows)
            if kind=='monthly-propers':
                month=int(re.search(r'2026(\d{2})',path.name)[1]);item['dates']=catalogue(rows,month)
                item['missingDates']=[f'2026-{month:02}-{d:02}' for d in range(1,calendar.monthrange(2026,month)[1]+1) if not any(g['date']==f'2026-{month:02}-{d:02}' for g in item['dates'])]
                days.extend(dict(date=g['date'],heading=g['heading'],sourcePath=item['sourcePath'],sections=[s['title'] for s in g['sections']],missingHeadings=g['missingHeadings'],status=g['status']) for g in item['dates'])
            filename=path.stem+'.json'
            (out/filename).write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            files.append(dict(sourcePath=item['sourcePath'],sha256=sha,paragraphs=len(rows),extractedPath=(out/filename).relative_to(ROOT).as_posix(),dateGroups=len(item.get('dates',[])),missingDates=item.get('missingDates',[])))
    report=dict(status='extraction-candidates-only',files=files,dates=days,uniqueDates=len(set(d['date'] for d in days)),linkedAppDates=[p.stem for p in (ROOT/'data/days').glob('*.json')],limitations=['原문 서식·표 셀 배치는 미복원. 성가표 문단 순서는 배정 규칙으로 사용하지 않음.','고유기도문은 독서·복음 전체 자료가 아님.','각 section에는 후속 지시문이 포함될 수 있으므로 검증 없이 앱에 투입하지 않음.'])
    (out/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['uniqueDates','linkedAppDates']},ensure_ascii=False));print(json.dumps(files,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
