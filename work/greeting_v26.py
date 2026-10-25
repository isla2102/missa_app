from pathlib import Path
p=Path('review/02-ia-v26.html');s=p.read_text(encoding='utf-8')
s=s.replace("...variant,title:item.title==='인사'?'인사':variant.title", "...variant,text:variant.text+(index===2?'\\n◎ 또한 사제의 영과 함께.':''),title:item.title==='인사'?'인사':variant.title")
s=s.replace("   if(item.title==='인사')blocks.push({key:`${item.id}-response`,tocId:item.id,variant:{title:'',text:'◎ 또한 사제의 영과 함께.'},hideHeading:true,group:'인사 합송'});",'')
s=s.replace(" if(block.alternative){const card=", " if(block.group==='인사' && block.variant.text.includes('◎')){const lit=node.querySelector('.reader__liturgy');if(lit && lit.children.length===2){const pair=document.createElement('div');pair.className='reader__dialogue';const children=Array.from(lit.children);lit.append(pair);pair.append(...children);}}\n if(block.alternative){const card=")
p.write_text(s,encoding='utf-8',newline='\r\n')
import re
Path('work/review-ia-v26-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
p=Path('work/test-reader-v26.cjs');s=p.read_text(encoding='utf-8');s=s.replace("greetings.every(b=>!b.variant.text.includes('◎'))","greetings.slice(0,2).every(b=>!b.variant.text.includes('◎'))")
s=s.replace("assert.equal(common.length,1);assert.equal(common[0].variant.text,'◎ 또한 사제의 영과 함께.');", "assert.equal(common.length,0);assert.ok(greetings[2].variant.text.includes('◎ 또한 사제의 영과 함께.'));const greetingPair=run(\"renderBlock(flowBlocks(0).filter(b=>b.group==='인사')[2])\");assert.ok(walk(greetingPair).some(n=>n.className==='reader__dialogue'&&n.children.length===2));")
p.write_text(s,encoding='utf-8',newline='\r\n')
