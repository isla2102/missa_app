from pathlib import Path
s=Path('review/02-ia-v24.html').read_text(encoding='utf-8').replace('검토 v24','검토 v25')
s=s.replace('grid-template-rows: auto auto minmax(0, 1fr) auto; padding:', 'grid-template-rows: auto auto minmax(0, 1fr); padding:',1)
s=s.replace('grid-template-columns: minmax(0, 1fr) fit-content(var(--draft-rail-max)); gap:', 'grid-template-columns: minmax(0, 1fr) fit-content(var(--draft-rail-max)); grid-template-rows: auto minmax(0, 1fr) auto; gap:',1)
s=s.replace(' .reader__body { min-width: 0; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr) auto; gap: var(--draft-gap); }',' .reader__body { display: contents; }\n .reader__section-heading { grid-column: 1; grid-row: 1; }\n .reader__tools { grid-column: 2; grid-row: 1; justify-content: flex-end; }\n .reader__turns { grid-column: 1; grid-row: 3; }')
# merge section heading rule to avoid duplicates
s=s.replace(' .reader__section-heading { display:', ' .reader__section-heading { grid-column: 1; grid-row: 1; display:',1).replace(' .reader__section-heading { grid-column: 1; grid-row: 1; }\n','')
s=s.replace(' .reader__book { position:', ' .reader__book { grid-column: 1; grid-row: 2; position:',1)
s=s.replace(' .reader__rail { min-height:', ' .reader__rail { grid-column: 2; grid-row: 2; min-height:',1)
s=s.replace(' .reader__liturgy {', ' .reader__dialogue { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); gap: var(--draft-item-gap); }\n .reader__liturgy {',1)
old='<div class="reader__section-heading"><h2 class="reader__title" id="part-title" data-js="part-title">시작 예식</h2></div>'
nav='<nav class="reader__row" aria-label="미사 순서 이동"><button type="button" data-js="part-prev"></button><button type="button" data-js="part-next"></button></nav>'
s=s.replace(old,old.replace('</div>',nav+'</div>'))
a=s.index('<footer class="reader__footer">');b=s.index('</footer>',a)+len('</footer>');s=s[:a]+s[b:]
s=s.replace('<aside class="reader__rail"','<nav class="reader__row reader__tools" aria-label="리더 도구"><button type="button" data-panel="settings">보기 설정</button><button type="button" data-panel="info">안내</button></nav>\n<aside class="reader__rail"',1)
s=s.replace("find('part-current').textContent=`현재: ${parts[part].title}`;",'')
s=s.replace('이마와 입술과 가슴에 십자 표시를 합니다.','이마와 입술과 가슴에 작은 십자 표시를 합니다.')
s=s.replace("function renderCreed(){", "let creedDate=null;\nfunction renderCreed(){\n const date=find('date').value;if(creedDate!==date){creedDate=date;creedView=['lent','easter'].includes(currentSeason()?.key)?'apostles':'nicene';}")
s=s.replace("note.textContent='양식 표시 미리보기 · 실제 미사 양식 자동 선택 아님';", "note.textContent='사순·부활에는 사도 신경을 기본 표시합니다. 사제의 선택에 따라 바꿀 수 있습니다.';")
a=s.index('function renderIntercessionResponse()');b=s.index('let penitentialView',a)
s=s[:a]+'''function intercessionControls(anchor){const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label','보편 지향 기도 응답 네 곳 표시');[['recite','낭송'],['chant','악보']].forEach(([value,label])=>{const b=document.createElement('button');b.type='button';b.className='reader__prayer-button';b.textContent=label;b.setAttribute('aria-pressed',String(intercessionView===value));b.onclick=()=>{intercessionView=value;scheduleReflow(anchor);};group.append(b);});return group;}
function renderIntercessionResponse(){const node=document.createElement('section');node.className='reader__item';const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','parish-response-card');card.setAttribute('data-response-view',intercessionView);if(intercessionView==='chant'){const p=document.createElement('p');p.textContent='악보 준비 중';card.append(p);}card.append(liturgyNode('◎ 주님, 저희의 기도를 들어주소서.'));node.append(card);return node;}
'''+s[b:]
s=s.replace("decorateLiturgy(node);\n if(block.alternative)", "decorateLiturgy(node);\n if(block.group==='보편 지향 기도 지향' && !block.hideHeading){const h=node.querySelector('h3');const row=document.createElement('div');row.className='reader__item-heading';h.replaceWith(row);row.append(h,intercessionControls(block.key));}\n if(block.item?.title==='복음'){const lit=node.querySelector('.reader__liturgy');if(lit?.children[0]?.textContent.includes('주님께서 여러분과 함께') && lit.children[1]?.textContent.includes('또한 사제의 영과 함께')){const pair=document.createElement('div');pair.className='reader__dialogue';const priest=lit.children[0],assembly=lit.children[1];lit.insertBefore(pair,priest);pair.append(priest,assembly);}}\n if(block.alternative)")
Path('review/02-ia-v25.html').write_text(s,encoding='utf-8',newline='\r\n')
