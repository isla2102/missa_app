from pathlib import Path
import re
root=Path('.')
s=(root/'review/02-ia-v12.html').read_text(encoding='utf-8').replace('검토 v12','검토 v13')
s=s.replace('--draft-toc-target:', '--draft-guide-ink: #244b66; --draft-guide-surface: #eef4f8; --draft-response-weight: 700; --draft-response-border: 2px; --draft-toc-target:',1)
s=s.replace(' .reader__score-photo {', ''' .reader__liturgy { display: grid; gap: var(--draft-item-gap); }
 .reader__content-card--liturgy { border: 0; padding: 0; }
 .reader__speech-card { border: 1px solid; padding: var(--draft-content-inset); }
 .reader__speech-card--assembly { border-width: var(--draft-response-border); font-weight: var(--draft-response-weight); }
 .reader__speaker { display: block; margin-block-end: var(--draft-toc-gap); }
 .reader__guidance { color: var(--draft-guide-ink); background: var(--draft-guide-surface); padding: var(--draft-content-inset); font-weight: normal; }
 .reader__speech-text { margin: 0; white-space: pre-line; }
 .reader__score-photo {''',1)
helper=r'''
// Printed ◎ starts the assembly response; guidance does not end that speech turn.
function spokenSegments(text, initial='text'){
 const segments=[];let role=initial,current=null;
 const add=(kind,value)=>{if(!current || current.kind!==kind){current={kind,parts:[]};segments.push(current);}current.parts.push(value);};
 for(const raw of text.split('\n')){
  const line=raw.trim();if(!line)continue;
  if(/^\[(?:안내|프레임 안내|자료 안내)/.test(line) || line.startsWith('인쇄본 안내:')){
   const part={kind:'guide',text:line};if(current && current.kind==='assembly')current.parts.push(part);else{segments.push({kind:'guide',parts:[part]});current=null;}continue;
  }
  if(line.startsWith('◎'))role='assembly';
  else if(line.startsWith('+'))role='priest';
  else if(line.startsWith('◆'))role='lector';
  else if(line.startsWith('[')){segments.push({kind:'guide',parts:[{kind:'guide',text:line}]});current=null;continue;}
  add(role,{kind:'text',text:line});
 }
 return segments;
}
function spokenRoleAt(text,offset,initial='text'){
 let role=initial;for(const line of text.slice(0,offset).split('\n')){if(line.trim().startsWith('◎'))role='assembly';else if(line.trim().startsWith('+'))role='priest';else if(line.trim().startsWith('◆'))role='lector';}return role;
}
function liturgyNode(text,initial='text'){
 const stack=document.createElement('div');stack.className='reader__liturgy';stack.__sourceText=text;stack.__initialRole=initial;
 spokenSegments(text,initial).forEach(segment=>{
  const parts=find('mode').value==='regular'?segment.parts.filter(part=>part.kind!=='guide'):segment.parts;if(!parts.length)return;
  const card=document.createElement('div');card.className=segment.kind==='guide'?'reader__guidance':`reader__speech-card reader__speech-card--${segment.kind}`;
  card.setAttribute('data-speech-role',segment.kind);
  if(segment.kind==='assembly'){const label=document.createElement('strong');label.className='reader__speaker';label.textContent='◎ 합송 · 함께 바칩니다';card.append(label);}
  parts.forEach(part=>{const p=document.createElement('p');p.className=part.kind==='guide' && segment.kind!=='guide'?'reader__speech-text reader__guidance':'reader__speech-text';p.textContent=part.kind==='guide'?'안내 · '+part.text.replace(/^\[(?:안내|프레임 안내|자료 안내)\]\s*|^인쇄본 안내:\s*/,''):part.text;card.append(p);});
  stack.append(card);
 });return stack;
}
function decorateLiturgy(root){
 Array.from(root.querySelectorAll('.reader__item-text')).forEach(p=>{
  const source=p.textContent;if(!source)return;
  const parent=p.parentElement;p.replaceWith(liturgyNode(source));
  if(parent?.classList.contains('reader__content-card') && !parent.classList.contains('reader__content-card--score'))parent.classList.add('reader__content-card--liturgy');
 });
}
function replaceLiturgyText(root,text,initial='text'){
 const target=root.querySelector('.reader__liturgy')||root.querySelector('.reader__item-text');
 if(target){const parent=target.parentElement;target.replaceWith(liturgyNode(text,initial));if(parent?.classList.contains('reader__content-card') && !parent.classList.contains('reader__content-card--score'))parent.classList.add('reader__content-card--liturgy');}
}
'''
helper=helper.replace("\\\\", "\\")
s=s.replace("const frameMock=",helper+"\nconst frameMock=",1)
s=s.replace('text:text.trim()}));','text:text.split("\\n").filter(line=>!line.trim().startsWith("◎")).join("\\n").trim()}));',1)
s=s.replace(" });blocks.push({key:`part-${partIndex}-transition`", " });blocks.push({key:`part-${partIndex}-transition`",1)
# Common greeting response follows all three celebrant alternatives.
s=s.replace("variant,group:item.title}));", "variant,group:item.title}));\n   if(item.title==='인사')blocks.push({key:`${item.id}-response`,tocId:item.id,variant:{title:'인사 · 공통 합송',text:'◎ 또한 사제의 영과 함께.'},group:'인사 합송'});",1)
s=s.replace(" } else {const p=document.createElement('p');p.className='reader__item-text';p.lang='ko';p.textContent=ordinaryText(prayerId,find('mode').value);card.append(p);}\n }", " } else {const p=document.createElement('p');p.className='reader__item-text';p.lang='ko';p.textContent=ordinaryText(prayerId,find('mode').value);card.append(p);}\n  decorateLiturgy(card);\n }",1)
s=s.replace(' sync();return frame;',' decorateLiturgy(frame);sync();return frame;',1)
s=s.replace("if(block.displayText!==undefined){const p=node.querySelector('.reader__item-text');if(p)p.textContent=block.displayText;}","if(block.displayText!==undefined)replaceLiturgyText(node,block.displayText);")
s=s.replace("if(block.fragmentText!==undefined){const p=node.querySelector('.reader__item-text');if(p)p.textContent=block.fragmentText;}","if(block.fragmentText!==undefined)replaceLiturgyText(node,block.fragmentText,block.fragmentRole||'text');")
s=s.replace(' return node;\n}\nfunction paginateFlow',' decorateLiturgy(node);return node;\n}\nfunction paginateFlow',1)
s=s.replace("const node=renderBlock(block);const paragraph=node.querySelector('.reader__item-text');", "const node=renderBlock(block);const paragraph=node.querySelector('.reader__liturgy');")
s=s.replace('paragraph.textContent.length<2','paragraph.__sourceText.length<2').replace('remaining=paragraph.textContent,index=0','remaining=paragraph.__sourceText,index=0,offset=0')
s=s.replace('fragmentText:remaining.slice(0,mid)',"fragmentRole:spokenRoleAt(paragraph.__sourceText,offset,paragraph.__initialRole),fragmentText:remaining.slice(0,mid)")
s=s.replace('fragmentText:remaining.slice(0,best)',"fragmentRole:spokenRoleAt(paragraph.__sourceText,offset,paragraph.__initialRole),fragmentText:remaining.slice(0,best)")
s=s.replace('remaining=remaining.slice(best);index++;','remaining=remaining.slice(best);offset+=best;index++;')
# Prefer line boundaries: avoid cutting ◎ marker away from its response.
s=s.replace("const boundary=remaining.lastIndexOf(' ',best);", "const newline=remaining.lastIndexOf('\\n',best);const boundary=newline>best/2?newline:remaining.lastIndexOf(' ',best);")
s=s.replace("  text('v12:","  text('v13: ◎ 합송은 별도 강조 카드로, 안내는 라벨과 임시 안내 색으로 구분합니다. 인사의 세 사제 선택지 뒤에는 공통 합송을 한 번 표시합니다.');\n  text('v12:",1)
(root/'review/02-ia-v13.html').write_text(s,encoding='utf-8',newline='\r\n')
(root/'work/review-ia-v13-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
print('Created v13')
