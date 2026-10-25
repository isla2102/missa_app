from pathlib import Path
import re
s=Path('review/02-ia-v49.html').read_text(encoding='utf-8').replace('v49','v50')
s=s.replace(':root { ',':root { --draft-reading-note-z: 2; --draft-reading-note-size: .875rem; ',1)
s=s.replace('grid-template-rows: minmax(0, 3fr) minmax(0, 2fr)','grid-template-rows: minmax(0, 4fr) minmax(0, 1fr)')
s=s.replace(' .reader__staff {',''' .reader__reading-heading { display: flex; align-items: baseline; justify-content: space-between; gap: var(--draft-header-gap); }
 .reader__reading-note { position: relative; z-index: var(--draft-reading-note-z); font-size: var(--draft-reading-note-size); font-weight: normal; color: var(--draft-guide-ink); }
 .reader__bow-phrase { text-decoration: underline; text-underline-offset: .2em; }
 .reader__menu-toggle { display: none; }
 .reader[data-orientation="portrait"] .reader__header--navigation { flex-wrap: wrap; overflow: visible; }
 .reader[data-orientation="portrait"] .reader__header-controls { flex-basis: 100%; flex-wrap: wrap; order: 3; }
 .reader[data-orientation="portrait"] .reader__header-tools { display: none; }
 .reader[data-orientation="portrait"] .reader__menu-toggle { display: block; }
 .reader__staff {''',1)
s=s.replace('<div class="reader__header-group"><label class=', '<div class="reader__header-group reader__header-controls"><label class=',1).replace('<nav class="reader__header-group" aria-label="성가와 기도">','<button type="button" class="reader__menu-toggle" data-js="header-menu" aria-label="성가와 주요 기도문 메뉴" aria-haspopup="dialog">☰ 메뉴</button><nav class="reader__header-group reader__header-tools" aria-label="성가와 기도">',1)
# Explicit text reset avoids Gospel body inheriting assembly role.
s=s.replace("const line=raw.trim();if(!line)continue;", "const line=raw.trim();if(!line)continue;if(line==='[본문]'){role='text';current=null;continue;}")
s=s.replace("+'\\n[안내] 이마와 입술과 가슴에 작은 십자 표시를 합니다.\\n◎ 주님, 영광 받으소서.\\n'+body", "+'\\n◎ 주님, 영광 받으소서.\\n[안내] 이마와 입술과 가슴에 작은 십자 표시를 합니다.\\n[본문]\\n'+body")
s=s.replace("return (title==='제1독서'?'[안내] 앉아서 말씀을 듣습니다.\\n':'')+actual", "return actual")
# Direct liturgy recitation shells must not carry their own border.
s=s.replace("else card.append(liturgyNode('◎ 알렐루야, 알렐루야, 알렐루야.'));", "else {card.className+=' reader__content-card--liturgy';card.append(liturgyNode('◎ 알렐루야, 알렐루야, 알렐루야.'));}")
a=s.index("  if(asset.kind==='engraved'){",s.index('function showScoreModal'));b=s.index(" });find('score-modal')",a)
s=s[:a]+"  body.append(renderPhoto(asset,true));\n"+s[b:]
s=s.replace("caption.append(enlargeScoreButton(asset));", "caption.append(enlargeScoreButton(asset));")
s=s.replace("figure.append(caption);\n if(asset.kind", "if(!enlarged)figure.append(caption);\n if(asset.kind",1)
s=s.replace("p.textContent=match?part.text.slice(match[0].length):part.text;speechBody.append(p);", "p.textContent=match?part.text.slice(match[0].length):part.text;if(/성령으로 인하여|동정 마리아에게서 육신|사람이 되셨/.test(p.textContent))p.className+=' reader__bow-phrase';speechBody.append(p);")
# Add first reading note beside its heading only for beginner mode.
s=s.replace("if(['제1독서','제2독서'].includes(block.item?.title)){node.classList", "if(block.item?.title==='제1독서'&&find('mode').value==='beginner'){const heading=node.querySelector('h3');if(heading){const row=document.createElement('div');row.className='reader__reading-heading';heading.replaceWith(row);const note=document.createElement('span');note.className='reader__reading-note';note.textContent='앉아서 말씀을 듣습니다.';row.append(heading,note);}}\n if(['제1독서','제2독서'].includes(block.item?.title)){node.classList",1)
# In continuous mode, only the currently visible/selected item gets a TOC frame.
s=s.replace("const visibleIds=new Set(layouts.slice(spread*2,spread*2+2).flatMap(page=>page.blocks.map(block=>block.tocId)));", "const visibleIds=viewerOrientation==='portrait'?new Set([selectedItem]):new Set(layouts.slice(spread*2,spread*2+2).flatMap(page=>page.blocks.map(block=>block.tocId)));")
s=s.replace("currentAnchor=visible.getAttribute('data-flow-key');readerAnchor=currentAnchor;", "currentAnchor=visible.getAttribute('data-flow-key');readerAnchor=currentAnchor;const block=layouts.flatMap(page=>page.blocks).find(b=>b.key===currentAnchor);if(block&&selectedItem!==block.tocId){selectedItem=block.tocId;renderToc();}")
s=s.replace(" if (which === 'settings') {", " if(which==='menu'){[['hymn','성가'],['prayer','주요 기도문']].forEach(([panel,label])=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.onclick=()=>showPanel(panel,trigger);body.append(b);});}\n if (which === 'settings') {")
s=s.replace("settings:'보기 설정',", "menu:'메뉴',settings:'보기 설정',")
s=s.replace("find('viewport-rotate').onclick=", "find('header-menu').onclick=event=>showPanel('menu',event.currentTarget);\nfind('viewport-rotate').onclick=",1)
Path('review/02-ia-v50.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v50-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v49.cjs').read_text(encoding='utf-8').replace('02-ia-v49.html','02-ia-v50.html').replace('grid-template-rows: minmax(0, 3fr) minmax(0, 2fr)','grid-template-rows: minmax(0, 4fr) minmax(0, 1fr)')
t=t.replace("n.tagName==='object'&&n.type==='application/pdf'&&decodeURI(n.data).includes('amen.pdf')","n.tagName==='img'&&decodeURI(n.src).includes('amen.svg')");t+=Path('work/test-reader-v50-extra.cjs').read_text(encoding='utf-8');Path('work/test-reader-v50.cjs').write_text(t,encoding='utf-8')
