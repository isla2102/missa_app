from pathlib import Path
s=Path('review/02-ia-v20.html').read_text(encoding='utf-8').replace('검토 v20','검토 v21')
s=s.replace("if(key==='감사 기도')text=text.split", "if(key==='감사 기도')text=text.replace('(타대오와 요한보스코)','(타대오와 협력 주교들)');\n if(key==='감사 기도')text=text.split")
s=s.replace("const fullScorePage=mode==='chant' && assets.length>0;", "const compactScore=prayerId==='주님의 기도 맺음 환호';\n  const fullScorePage=mode==='chant' && assets.length>0 && !compactScore;")
s=s.replace("card.className=fullScorePage?'reader__content-card reader__content-card--score':'reader__content-card';", "card.className=fullScorePage?'reader__content-card reader__content-card--score':'reader__content-card';\n  if(compactScore)card.setAttribute('data-score-layout','compact');")
s=s.replace("const reengravedPrincipalScores =", "temporaryPrincipalScores['하느님의 어린양']=temporaryPrincipalScores['하느님의 어린양'].map(asset=>({...asset,crop:[360,1800,2460,1960],title:'하느님의 어린양'}));\n\nconst reengravedPrincipalScores =")
s=s.replace("const previousScroll=rail.scrollTop;nav.replaceChildren();", "const previousScroll=rail.scrollTop;let activeLink=null;nav.replaceChildren();")
s=s.replace("if(entry.id===selectedItem){link.setAttribute", "if(entry.id===selectedItem){activeLink=link;link.setAttribute")
s=s.replace("});rail.scrollTop=previousScroll;", "});rail.scrollTop=previousScroll;if(activeLink && rail.getBoundingClientRect){const r=rail.getBoundingClientRect(),a=activeLink.getBoundingClientRect();rail.scrollTop=Math.max(0,rail.scrollTop+a.top-r.top-rail.clientHeight*0.25);}")
s=s.replace("if(item.title==='보편 지향 기도')addPrayer('response','보편 지향 기도 응답');", "")
s=s.replace("}else if(item.title==='복음 환호송'){", "}else if(item.title==='보편 지향 기도'){\n   universalPrayerBlocks(item).forEach(block=>blocks.push(block));\n  }else if(item.title==='복음 환호송'){")
pos=s.index('function flowBlocks(partIndex)')
s=s[:pos]+'''const dailyIntercessions20261018=[
 '교회를 위하여 기도합시다.\\n거룩하신 주님, 주님의 교회에 그리스도의 빛을 비추시어, 교회가 구원의 신비를 깊이 깨닫고, 그 신비에 온전히 참여하며, 민족들의 복음화에 힘쓰게 하소서.',
 '세계 지도자들을 위하여 기도합시다.\\n자비하신 주님, 세계 지도자들에게 사랑과 절제의 영을 주시어, 자국의 이익만을 생각하기보다 고통을 겪는 나라들을 살피며 공동선을 실현하도록 이끌어 주소서.',
 '감옥에 갇힌 이들을 위하여 기도합시다.\\n위로의 샘이신 주님, 감옥에 갇힌 이들을 참된 회개로 이끌어 주시어, 죄를 진심으로 뉘우치며 새 삶을 준비하게 하시고, 그들의 범죄로 피해받은 이들에게 위로와 힘을 주소서.',
 '가정 공동체를 위하여 기도합시다.\\n사랑이신 주님, 어려움에 있는 가정들을 돌보아 주시어, 주님의 한결같은 사랑과 자비를 믿고 온전히 의탁하며, 어머니인 교회 안에서 힘을 얻게 하소서.'
];
function universalPrayerBlocks(item){
 const dated=find('date').value==='2026-10-18';const petitions=dated?dailyIntercessions20261018:['[매일미사 기도 지향 · mock · 선택 날짜 자료 연결 예정]'];const result=[];
 petitions.forEach((text,i)=>{
  result.push({key:i?item.id+'-petition-'+(i+1):item.id,tocId:item.id,variant:{title:'보편 지향 기도',text:'○ '+text},hideHeading:i>0,group:'보편 지향 기도 지향'});
  result.push({key:item.id+'-response-'+(i+1),tocId:item.id,variant:{title:'',text:'◎ 주님, 저희의 기도를 들어주소서.'},hideHeading:true,group:'보편 지향 기도 합송'});
 });
 result.push({key:item.id+'-conclusion',tocId:item.id,variant:{title:'사제 마침 기도',text:'[안내] 매일미사 사제 마침 기도 연결용 mock\\n+ [사제 마침 기도 본문] … 우리 주 그리스도를 통하여 비나이다.'},group:'보편 지향 기도 마침'});
 result.push({key:item.id+'-amen',tocId:item.id,variant:{title:'',text:'◎ 아멘.'},hideHeading:true,group:'보편 지향 기도 아멘'});return result;
}
'''+s[pos:]
Path('review/02-ia-v21.html').write_text(s,encoding='utf-8',newline='\r\n')
import re
Path('work/review-ia-v21-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v20.cjs').read_text(encoding='utf-8').replace('02-ia-v20.html','02-ia-v21.html')
t+='''\nconst universal=run("flowBlocks(1).filter(b=>b.group?.startsWith('보편 지향 기도'))");assert.equal(universal.filter(b=>b.group==='보편 지향 기도 합송').length,4);assert.equal(universal.at(-1).variant.text,'◎ 아멘.');assert.ok(universal.at(-2).variant.text.includes('mock'));assert.ok(run("ordinaryText('감사기도 제2양식')").includes('(타대오와 협력 주교들)'));const compact=run("renderPrayerFrame('주님의 기도 맺음 환호','주님의 기도 맺음 환호')");assert.ok(!compact.className.includes('item--score'));assert.ok(walk(compact).some(n=>n.attrs['data-score-layout']==='compact'));assert.ok(run("scoreAssets('하느님의 어린양')[0].crop[1]")>=1800);date.value='2026-10-19';assert.equal(run("universalPrayerBlocks(contents[1].at(-1)).filter(b=>b.group==='보편 지향 기도 합송').length"),1);date.value='2026-10-18';console.log('PASS: intercessions response per petition/conclusion/Amen, dated fallback, bishop override, compact doxology, Agnus crop.');\n'''
Path('work/test-reader-v21.cjs').write_text(t,encoding='utf-8',newline='\r\n')
