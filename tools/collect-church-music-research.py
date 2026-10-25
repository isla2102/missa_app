"""Public category metadata + transient reading text; originals preserved."""
from pathlib import Path
import urllib.request, urllib.parse, re, json, html, time, hashlib, zipfile, shutil
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/research/church-music'; OUT.mkdir(parents=True,exist_ok=True)
WORK=ROOT/'scratch/church-music-research-20261023'; WORK.mkdir(parents=True,exist_ok=True)
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8')
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
posts=[]; total=None
for page in range(1,8):
 s=get(f'https://blog.naver.com/PostTitleListAsync.naver?blogId=kelijah&currentPage={page}&categoryNo=1&countPerPage=30')
 s=re.sub(r'\\(?!["\\/bfnrtu])',r'\\\\',s);j=json.loads(s,strict=False);total=int(j['totalCount'])
 for x in j['postList']:
  posts.append({'id':x['logNo'],'title':html.unescape(urllib.parse.unquote_plus(x['title'])),'url':'https://m.blog.naver.com/kelijah/'+x['logNo'],'date':x.get('addDate',''),'readStatus':'indexed'})
 if len(posts)>=total:break
focus={'221190975541','221584939834','221282687527','221591322012','221262274935','221158413083','221158933731','221158924777','221366691773','221364931465','221210365609','221210362874','221299757861','221269598895','221313238293','221305778365'}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
  if tag in ['p','br','tr','h1','h2','h3']:self.out.append('\n')
 def handle_endtag(self,tag):
  if tag in ['script','style'] and self.skip:self.skip-=1
 def handle_data(self,data):
  if not self.skip:self.out.append(data)
for item in posts:
 if item['id'] not in focus:continue
 try:
  s=get(item['url']);start=s.find('<div class="se-main-container">');end=s.find('<!-- // SE_DOC_HEADER_END -->',start)
  if start<0:start=s.find('id="postViewArea"')
  fragment=s[start:] if start>=0 else s
  cut=fragment.find('<!-- // SE_DOC_FOOTER_START -->')
  if cut>=0:fragment=fragment[:cut]
  parser=Text();parser.feed(fragment);text='\n'.join(re.sub(r'\s+',' ',line).strip() for line in ''.join(parser.out).splitlines());text='\n'.join(line for line in text.splitlines() if line)
  (WORK/(item['id']+'.txt')).write_text(text,encoding='utf-8');item['readStatus']='body-retrieved';item['retrievedAt']='2026-10-23';item['bodyChars']=len(text)
  print(item['id'],item['title'],len(text),flush=True)
 except Exception as e:item['readStatus']='failed';item['error']=str(e)
 time.sleep(.25)
save(OUT/'category-index.json',{'category':'교회음악 알아가기','blogId':'kelijah','categoryNo':1,'retrievedAt':'2026-10-23','totalReported':total,'count':len(posts),'posts':posts})
LIB=ROOT/'data/source-library';inventory=[]
for folder,kind in [('매일미사고유기도문','monthly-propers'),('굿뉴스성가번호표','hymn-schedules'),('가톨릭성가','catholic-hymns')]:
 for src in sorted((ROOT/folder).iterdir()):
  if not src.is_file():continue
  dest=LIB/kind/'originals'/src.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
  inventory.append({'originalPath':str(src.relative_to(ROOT)).replace('\\','/'),'libraryPath':str(dest.relative_to(ROOT)).replace('\\','/'),'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'kind':kind,'contentStatus':'user-provided-not-yet-parsed'})
z=zipfile.ZipFile(ROOT/'가톨릭성가/가톨릭성가(ENC).zip');enc=[];base=LIB/'catholic-hymns/enc';base.mkdir(parents=True,exist_ok=True)
for info in z.infolist():
 if info.is_dir():continue
 name=info.filename if info.flag_bits&2048 else info.filename.encode('cp437').decode('cp949')
 if '/' in name or '\\' in name or name in ['.','..']:raise ValueError('Unexpected ZIP path '+name)
 if not name.lower().endswith('.enc'):raise ValueError('Unexpected format '+name)
 dest=base/name;data=z.read(info);dest.write_bytes(data);enc.append({'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'path':str(dest.relative_to(ROOT)).replace('\\','/')})
save(LIB/'inventory.json',{'createdAt':'2026-10-23','originalFiles':inventory,'encCount':len(enc),'encFiles':enc,'policy':'Original locations preserved; library copies SHA256 verified; ENC not converted or executed.'})
print('DONE',len(posts),'posts',len(inventory),'originals',len(enc),'ENC')
