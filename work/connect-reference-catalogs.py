from pathlib import Path
import json,shutil
for name in ['review/source/reader.js','review/source/build.json','tests/build-review.cjs']:
 shutil.copy2(name,Path('scratch')/(Path(name).name+'.before-reference-catalog'))
p=Path('review/source/build.json');c=json.loads(p.read_text(encoding='utf-8'));bindings={'majorPrayerCatalog':'major-prayers.json','bulletinProvider':'daegu-bulletin.json','hymnScheduleCatalog':'hymn-schedule-202610.json'}
for key,file in bindings.items():c['bindings'][key]={'path':'data/reference-sources/'+file,'array':False}
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('review/source/reader.js');s=p.read_text(encoding='utf-8');s='\n'.join('const '+key+' = {{'+key+'}};' for key in bindings)+'\n'+s
helper='''
function externalSourceLink(url,label){const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=label;return link;}
function appendMajorPrayerSources(body){const heading=document.createElement('h3');heading.textContent='굿뉴스 주요기도문';const list=document.createElement('ul');majorPrayerCatalog.items.forEach(item=>{const li=document.createElement('li');li.append(externalSourceLink(item.url,item.title+' · 원문'));list.append(li);});body.append(heading,list);}
function appendHymnRecommendations(body){const day=hymnScheduleCatalog.days.find(day=>day.date===find('date').value);if(!day)return;const heading=document.createElement('h3');heading.textContent='참고 성가표 · '+hymnScheduleCatalog.edition;const note=document.createElement('p');note.textContent='본당·회차별 확정 전 추천 번호입니다.';body.append(heading,note);[['entrance','입당'],['offertory','예물 준비'],['communion','영성체'],['recessional','파견']].forEach(([key,label])=>{const p=document.createElement('p');p.textContent=label+' · '+(day.recommendations[key].join(', ')||'미등록');body.append(p);});body.append(externalSourceLink(hymnScheduleCatalog.sourceUrl,'성가표 출처'));}
function appendBulletinSource(body){const issue=bulletinProvider.issues.find(issue=>issue.date===find('date').value);const p=document.createElement('p');p.append(externalSourceLink(issue?issue.viewUrl:bulletinProvider.indexUrl,'대구대교구 주보'+(issue?' · '+issue.date:'')));if(issue)p.append(externalSourceLink(issue.pdfUrl,' · PDF 열기'));body.append(p);}
'''
s=s.replace('function renderMockTextCard(',helper+'\nfunction renderMockTextCard(',1)
s=s.replace(" if(title!=='공지 사항')section.append(liturgyNode('◎ 아멘.'));return section;", " if(title==='공지 사항'){p.textContent='본당 공지 자료 미연결';appendBulletinSource(section);}else section.append(liturgyNode('◎ 아멘.'));return section;",1)
s=s.replace("if (which === 'hymn') { text(`${selectedSlotName()} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`)); }", "if (which === 'hymn') { text(`${selectedSlotName()} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`));appendHymnRecommendations(body); }")
s=s.replace("if (which === 'prayer') {", "if (which === 'prayer') {\n  appendMajorPrayerSources(body);",1)
p.write_text(s,encoding='utf-8',newline='\r\n')
