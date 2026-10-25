from pathlib import Path
import re
s=Path('review/02-ia-v47.html').read_text(encoding='utf-8').replace('v47','v48')
s=s.replace(' .reader__staff {', ''' .reader__book--continuous { display: block; overflow: auto; }
 .reader__page--continuous { overflow: visible; }
 .reader__book--continuous .reader__item--reading { display: block; }
 .reader__book--continuous .reader__reading-content { display: block; }
 .reader__book--continuous .reader__reading-liturgy { display: grid; }
 .reader__book--continuous .reader__reading-body { overflow: visible; }
 .reader__book--continuous .reader__item--score { block-size: auto; display: block; }
 .reader__book--continuous .reader__item--compact-score { max-block-size: none; }
 .reader__book--continuous .reader__item--collect { block-size: auto; display: block; }
 .reader__book--continuous .reader__score-scroll { overflow: visible; }
 .reader__book--continuous .reader__text-scroll { overflow: visible; }
 .reader__book--continuous .reader__collect-scroll { overflow: visible; }
 .reader__book--continuous .reader__psalm-content { overflow: visible; }
 .reader__staff {''',1)
s=s.replace("function render(options={}) {","function render(options={}) {const previousReaderAnchor=readerAnchor;")
s=s.replace('layouts=composePages();if(!layouts.length)',"const continuous=viewerOrientation==='portrait';book.className='reader__book'+(continuous?' reader__book--continuous':'');layouts=continuous?[{blocks:flowBlocks(part),continuous:true}]:composePages();if(!layouts.length)")
s=s.replace("page.className=layout.reading?", "page.className=layout.continuous?'reader__page reader__page--continuous':layout.reading?")
s=s.replace('if(nodes.length===1){','if(!continuous&&nodes.length===1){',1)
s=s.replace("hintNextPart(turn.nextPart);renderToc();", "hintNextPart(turn.nextPart);if(continuous){find('page-context').textContent=parts[part].title+' · 세로 연속 보기';find('page-prev').disabled=part===0;find('page-next').disabled=part===parts.length-1;find('page-prev').textContent=part?'← '+parts[part-1].title:'미사 시작';find('page-next').textContent=part<parts.length-1?parts[part+1].title+' →':'미사 마침';find('page-prev').setAttribute('aria-label',find('page-prev').textContent);find('page-next').setAttribute('aria-label',find('page-next').textContent);find('page-prev').title=find('page-prev').textContent;find('page-next').title=find('page-next').textContent;hintNextPart(false);}renderToc();")
s=s.replace('function turnSpread(direction){',"function turnSpread(direction){if(viewerOrientation==='portrait'){const next=part+direction;if(next>=0&&next<parts.length)go(next);return;}")
s=s.replace("const list=Array.from(book.querySelectorAll('*'));const counts={};return list.map", "const list=Array.from(book.querySelectorAll('*'));const counts={};const result=list.map")
s=s.replace("}).filter(Boolean);}\nfunction captureReaderScroll", "}).filter(Boolean);if(book.classList.contains('reader__book--continuous'))result.push({node:book,key:'continuous-part-'+readerPart});return result;}\nfunction captureReaderScroll")
s=s.replace("function readerScrolled(event){if(restoringScroll)return;", "function readerScrolled(event){if(restoringScroll)return;if(viewerOrientation==='portrait'&&event.target===find('book')){const blocks=Array.from(find('book').querySelectorAll('[data-flow-key]'));const visible=blocks.find(node=>node.offsetTop+node.offsetHeight>find('book').scrollTop);if(visible){currentAnchor=visible.getAttribute('data-flow-key');readerAnchor=currentAnchor;}}")
s=s.replace("restoreReaderScroll();persistReader();find('part-title')", "restoreReaderScroll();if(continuous&&(options.anchorKey&&options.anchorKey!==previousReaderAnchor||!Number.isFinite(readerScrolls['continuous-part-'+part]))){const target=Array.from(book.querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===currentAnchor);if(target)book.scrollTop=target.offsetTop;}persistReader();find('part-title')")
Path('review/02-ia-v48.html').write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v48-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
t=Path('work/test-reader-v47.cjs').read_text(encoding='utf-8').replace('02-ia-v47.html','02-ia-v48.html');t=t.replace('const events={};','const realTurn48=run("turnSpread");const events={};');t+='''\nassert.ok(html.includes("blocks:flowBlocks(part),continuous:true"));assert.ok(html.includes("if(!continuous&&nodes.length===1)"));assert.ok(html.includes("reader__book--continuous .reader__score-scroll { overflow: visible; }"));run("viewerOrientation='portrait';part=1;go=(value)=>{part=value;}");realTurn48(1);assert.equal(run('part'),2);realTurn48(-1);assert.equal(run('part'),1);console.log('PASS v48 portrait uses complete continuous flow without blank page and navigates parts.');\n''';Path('work/test-reader-v48.cjs').write_text(t,encoding='utf-8')
