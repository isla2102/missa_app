from pathlib import Path
import json,re
p=Path('review/02-ia-v43.html');s=p.read_text(encoding='utf-8').replace('v43','v44')
doc=json.loads(Path('data/days/2026-10-18.json').read_text(encoding='utf-8'));sources=json.loads(Path('data/sources.json').read_text(encoding='utf-8'))
api=Path('work/daily-document.cjs').read_text(encoding='utf-8-sig').replace("if(typeof module!=='undefined')module.exports={validateDocument,selectDocument,resolveAnchor};",'')
helper='''
function selectedMassDocument(){return selectDocument(dailyDocuments,find('date').value);}
function dailySection(title){return selectedMassDocument()?.sections.find(s=>s.title===title)||null;}
function dailyText(title){const section=dailySection(title);return section?.status==='verified'?section.paragraphs.map(p=>p.text).join('\\n'):null;}
function renderDailySection(title){const section=document.createElement('section');section.className='reader__item';const h=document.createElement('h3');h.className='reader__item-title';h.textContent=title;section.append(h);const card=document.createElement('div');card.className='reader__content-card reader__content-card--liturgy';const record=dailySection(title);card.setAttribute('data-content-source',record?.status==='verified'?'cbck-verified-snapshot':'daily-missing');if(record?.status==='verified'){card.append(liturgyNode(dailyText(title)+(title==='예물 기도'||title==='영성체 후 기도'?'\\n◎ 아멘.':'')));const link=document.createElement('a');link.href=dailySources['cbck-20261018'].url;link.target='_blank';link.rel='noopener noreferrer';link.textContent='출처 · 2026-10-18 매일미사';card.append(link);}else{const p=document.createElement('p');p.textContent='선택 날짜 자료 미연결';card.append(p);}if(title==='화답송'){const note=document.createElement('p');note.textContent='주보 화답송 악보 미등록 · 현재는 매일미사 텍스트를 표시합니다.';card.append(note);}section.append(card);return section;}
'''
payload='const dailyDocuments='+json.dumps([doc],ensure_ascii=False)+';\nconst dailySources='+json.dumps(sources,ensure_ascii=False)+';\n'+api+'\nif(validateDocument(dailyDocuments[0],dailySources).length)throw new Error("Invalid daily document");\n'+helper
s=s.replace('function selectedDailyData()',payload+'\nfunction selectedDailyData()',1)
s=s.replace("function readingFrameText(title){","""function readingFrameText(title){
 const actual=dailyText(title);
 if(actual){
  if(title==='복음'){const lines=actual.split('\\n');const intro=lines.find(line=>line.startsWith('✠'));const body=lines.filter(line=>!line.startsWith('✠'));return '+ 주님께서 여러분과 함께.\\n◎ 또한 사제의 영과 함께.\\n+ '+intro.slice(1).trim()+'\\n[안내] 이마와 입술과 가슴에 작은 십자 표시를 합니다.\\n◎ 주님, 영광 받으소서.\\n'+body.map(line=>line==='주님의 말씀입니다.'?'+ '+line:line).join('\\n');}
  return (title==='제1독서'?'[안내] 앉아서 말씀을 듣습니다.\\n':'')+actual.split('\\n').map(line=>line==='주님의 말씀입니다.'?'◆ '+line:line).join('\\n');
 }
 return '[선택 날짜 자료 미연결]';
 /* legacy mock retained only as archived reference below */""",1)
s=s.replace("function renderItem(item) {","function renderItem(item) {\n if(['예물 기도','영성체 후 기도','화답송'].includes(item.title))return renderDailySection(item.title);",1)
s=s.replace("card.setAttribute('data-content-source','cbck-daily-mock');const p=document.createElement('p');p.className='reader__item-text';p.textContent=readingFrameText", "card.setAttribute('data-content-source',dailyText(item.title)?'cbck-verified-snapshot':'daily-missing');const p=document.createElement('p');p.className='reader__item-text';p.textContent=readingFrameText")
s=s.replace("p.textContent=selectedDailyData()?'○ 주님이 말씀하신다. 너희는 가서 모든 민족들을 가르쳐라. 내가 세상 끝 날까지 언제나 너희와 함께 있으리라.':'[오늘의 복음 환호송 구절 · 매일미사 연결용 mock]\\n'+frameMock;","p.textContent=dailySection('복음 환호송')?.paragraphs.find(p=>p.text.startsWith('○'))?.text||'[선택 날짜의 복음 환호송 구절 미연결]';")
s=s.replace("text:'[안내] 매일미사 사제 마침 기도 연결용 mock\\n+ [사제 마침 기도 본문] … 우리 주 그리스도를 통하여 비나이다.'","text:'[사제 마침 기도 자료 미제공 · 본당에서 확인한 기도를 연결해 주세요.]'")
# Use the current daily source for intercessions rather than duplicated hardcoded date data.
s=s.replace("const dated=find('date').value==='2026-10-18';const petitions=dated?dailyIntercessions20261018:['[매일미사 기도 지향 · mock · 선택 날짜 자료 연결 예정]'];", "const record=dailySection('보편 지향 기도');const lines=record?.status==='verified'?record.paragraphs.map(p=>p.text):[];const petitions=[];for(let i=0;i<lines.length;i++){if(/^[1-4]\\. /.test(lines[i]))petitions.push(lines[i].replace(/^[1-4]\\. /,'')+'\\n'+(lines[i+1]||''));}if(!petitions.length)petitions.push('[선택 날짜 기도 지향 미연결]');")
# Collect has its existing variant UI; retain it but remove Lorem fallback.
s=s.replace('}else body.textContent=frameMock;',"}else body.textContent='선택 날짜 본기도 자료 미연결';")
start=s.index(" /* legacy mock retained only as archived reference below */")
end=s.index("\n}\n\nfunction ordinaryText",start)
s=s[:start]+s[end:]
s=s.replace("if(['예물 기도','영성체 후 기도'].includes(item.title))return renderMockTextCard(item.title,'cbck-daily-mock');",'')
s=s.replace("section.append(card);return section;}\n", "section.append(card);return section;}\n")
s=s.replace("const first=text.split('[거룩하시도다 · 별도 카드 참조]');", "const first=text.split('[거룩하시도다 · 별도 카드 참조]');const preface=dailyText('감사송');if(preface){const opening=first[0].split('+ 거룩하신 아버지')[0];first[0]=opening+'+ '+preface;}" )
s=s.replace("forEach(child=>child.classList.add('reader__reading-body'))", "forEach(child=>{child.classList.add('reader__reading-body');child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');})")
Path('review/02-ia-v44.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v44-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
print('Built self-contained v44 with validated source snapshot.')
