from pathlib import Path
import json,re
s=Path('review/02-ia-v18.html').read_text(encoding='utf-8').replace('검토 v18','검토 v19')
registry=json.loads(Path('docs/교중미사악보/reengraved/registry.json').read_text(encoding='utf-8'))
s=re.sub(r'const reengravedPrincipalScores = .*?;\n','const reengravedPrincipalScores = '+json.dumps(registry,ensure_ascii=False)+';\n',s,count=1)
catalog=json.loads(Path('docs/references/score-source-catalog.json').read_text(encoding='utf-8'))['scores']
helpers='const scoreSourceCatalog = '+json.dumps(catalog,ensure_ascii=False)+';\n'+r'''
let sourceDialogOpener=null;
function sourceForAsset(asset){return scoreSourceCatalog[asset.sourceKey] || Object.values(scoreSourceCatalog).find(x=>asset.title.startsWith(x.title));}
function sourceButton(asset){
 const entry=sourceForAsset(asset);if(!entry)return null;const b=document.createElement('button');b.type='button';b.textContent=entry.confirmedNumber?'가톨릭성가 '+entry.confirmedNumber+'번':'출처 · 번호 미확인';b.setAttribute('aria-haspopup','dialog');b.onclick=()=>showSourceDialog(entry,b);return b;
}
function showSourceDialog(entry,trigger){
 sourceDialogOpener=trigger;find('source-dialog-title').textContent=entry.title+' · 출처';const body=find('source-dialog-body');body.replaceChildren();const note=document.createElement('p');note.textContent=entry.confirmedNumber?'가톨릭성가 '+entry.confirmedNumber+'번 · 본당 사용곡 사용자 확인 및 알렐루야 선율 대조':'동일 제목의 ZIP 수록 후보입니다. 사진 악보와 선율이 같은 번호는 아직 확인되지 않았습니다. 사진의 17·18 등은 인쇄물 번호이며 가톨릭성가 번호로 확정하지 않습니다.';body.append(note);
 if(entry.sourceUrl){const a=document.createElement('a');a.href=entry.sourceUrl;a.target='_blank';a.rel='noopener noreferrer';a.textContent='굿뉴스 · 지정 성가 출처';body.append(a);}
 const list=document.createElement('ul');entry.candidates.forEach(candidate=>{if(entry.confirmedNumber && !candidate.numbers.includes(entry.confirmedNumber))return;const li=document.createElement('li');const a=document.createElement('a');a.href=encodeURI(candidate.path);a.download=candidate.file;a.textContent=candidate.file;li.append(a);candidate.officialPages.forEach((url,i)=>{const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=' · '+candidate.numbers[i]+'번 정보';li.append(link);});list.append(li);});body.append(list);find('source-dialog').showModal();find('source-dialog-close').focus();
}
function renderAlleluia(part=null){
 const section=document.createElement('section');section.className='reader__item';const row=document.createElement('div');row.className='reader__item-heading';const h=document.createElement('h3');h.className='reader__item-title';h.textContent='복음 환호송';row.append(h);section.append(row);
 const mode=parishPrayerPresentation['복음 환호송']||'chant';const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','알렐루야 표시 방식');row.append(group);
 [['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([key,label])=>{const b=document.createElement('button');b.type='button';b.className='reader__prayer-button';b.textContent=label;b.setAttribute('aria-pressed',String(mode===key));b.onclick=()=>{parishPrayerPresentation['복음 환호송']=key;scheduleReflow(section.getAttribute('data-flow-key'));};group.append(b);});
 const response=()=>{const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-acclamation-role','assembly');if(mode==='chant')card.append(renderPhoto(reengravedPrincipalScores['복음 환호송'][0]));else card.append(liturgyNode('◎ 알렐루야, 알렐루야, 알렐루야.'));return card;};
 const first=response();const choir=document.createElement('div');choir.className='reader__content-card';choir.setAttribute('data-acclamation-role','choir');choir.setAttribute('data-content-source','daily-acclamation-verse');const label=document.createElement('p');label.textContent='성가대';const p=document.createElement('p');p.className='reader__item-text';p.textContent=selectedDailyData()?'○ 주님이 말씀하신다. 너희는 가서 모든 민족들을 가르쳐라. 내가 세상 끝 날까지 언제나 너희와 함께 있으리라.':'[오늘의 복음 환호송 구절 · 매일미사 연결용 mock]\n'+frameMock;choir.append(label,p);const last=response();section.append(first,choir,last);if(part==='first')section.replaceChildren(row,first);else if(part==='choir')section.replaceChildren(choir);else if(part==='last')section.replaceChildren(last);return section;
}
'''
s=s.replace('const frameMock=',helpers+'\nconst frameMock=',1)
s=s.replace("function scoreAssets(prayerId) {", "function scoreAssets(prayerId) { if(prayerId==='복음 환호송')return reengravedPrincipalScores[prayerId]||[];",1)
s=s.replace("if(!enlarged)caption.append(enlargeScoreButton(asset));figure.append(caption);", "if(!enlarged){caption.append(enlargeScoreButton(asset));const source=sourceButton(asset);if(source)caption.append(source);}figure.append(caption);",1)
s=s.replace("if(item.title==='복음 환호송')return renderPrayerFrame('복음 환호송 · 알렐루야','복음 환호송',true);", "if(item.title==='복음 환호송')return renderAlleluia();",1)
# This three-card response group is kept together, with internal scroll for very short viewports.
s=s.replace("['신앙 고백','본기도'].includes", "['신앙 고백','본기도','복음 환호송'].includes",1)
dialog='<dialog class="reader__tutorial" data-js="source-dialog" aria-labelledby="source-dialog-title"><div class="reader__modal-heading"><h2 id="source-dialog-title" data-js="source-dialog-title">악보 출처</h2><button type="button" data-js="source-dialog-close">닫기</button></div><div data-js="source-dialog-body"></div></dialog>\n'
s=s.replace('<script>',dialog+'<script>',1)
s=s.replace("context(); render();\nif(!hasSeenTutorial())", "find('source-dialog-close').onclick=()=>find('source-dialog').close();\nfind('source-dialog').addEventListener('close',()=>{(sourceDialogOpener?.isConnected?sourceDialogOpener:find('part-next'))?.focus();});\ncontext(); render();\nif(!hasSeenTutorial())",1)
s=s.replace("  }else if(item.title==='파견'){","  }else if(item.title==='복음 환호송'){\n   ['first','choir','last'].forEach((acclamationPart,i)=>blocks.push({key:i?`${item.id}-${acclamationPart}`:item.id,tocId:item.id,acclamationPart}));\n  }else if(item.title==='파견'){",1)
s=s.replace(" if(block.variant){"," if(block.acclamationPart)node=renderAlleluia(block.acclamationPart);\n else if(block.variant){",1)
Path('review/02-ia-v19.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v19-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
