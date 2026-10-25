from pathlib import Path
import re
s=Path('review/02-ia-v14.html').read_text(encoding='utf-8').replace('검토 v14','검토 v15')
s=s.replace('--draft-guide-ink:', '--draft-choice-card-z: 0; --draft-choice-marker-z: 1; --draft-choice-marker-space: 1.25rem; --draft-guide-ink:',1)
s=s.replace(' .reader__speaker { display: block; margin-block-end: var(--draft-toc-gap); }',' .reader__speech-card--alternative { position: relative; isolation: isolate; z-index: var(--draft-choice-card-z); padding-block-end: calc(var(--draft-content-inset) + var(--draft-choice-marker-space)); }\n .reader__alternative-marker { position: absolute; inset-inline-end: var(--draft-content-inset); inset-block-end: var(--draft-toc-gap); z-index: var(--draft-choice-marker-z); }\n .reader__tutorial { width: min(100%, var(--draft-panel)); padding: var(--draft-padding); }',1)
s=s.replace("  if(segment.kind==='assembly'){const label=document.createElement('strong');label.className='reader__speaker';label.textContent='◎ 합송 · 함께 바칩니다';card.append(label);}","  if(segment.kind==='assembly')card.setAttribute('aria-label','합송');",1)
s=s.replace('variant,group:item.title}',"variant:{...variant,title:item.title==='인사'?'인사':variant.title},hideHeading:item.title==='인사' && index>0,alternative:item.title==='인사' && index<2,group:item.title}",1)
s=s.replace("variant:{title:'인사 · 공통 합송',text:'◎ 또한 사제의 영과 함께.'},group:'인사 합송'", "variant:{title:'',text:'◎ 또한 사제의 영과 함께.'},hideHeading:true,group:'인사 합송'",1)
s=s.replace('node.append(h,card);',"if(!block.hideHeading)node.append(h);node.append(card);",1)
s=s.replace(' decorateLiturgy(node);return node;', ''' decorateLiturgy(node);
 if(block.alternative){const card=node.querySelector('.reader__speech-card');if(card){card.classList.add('reader__speech-card--alternative');card.setAttribute('aria-label',block.variant.key+' · 다른 양식 선택 가능');const marker=document.createElement('span');marker.className='reader__alternative-marker';marker.textContent='〈또는〉';marker.setAttribute('aria-hidden','true');card.append(marker);}}
 return node;''',1)
# On-demand guide starts from a button in the existing info drawer.
s=s.replace(" if (which === 'info') {", " if (which === 'info') {\n  const tutorialButton=document.createElement('button');tutorialButton.type='button';tutorialButton.textContent='기호와 사용법 튜토리얼 다시 보기';tutorialButton.onclick=()=>{find('drawer').close();requestAnimationFrame(()=>showTutorial(tutorialButton));};body.append(tutorialButton);",1)
dialog='''<dialog class="reader__tutorial" data-js="tutorial" aria-labelledby="tutorial-title"><h2 id="tutorial-title" data-js="tutorial-title">미사 뷰어 사용 안내</h2><p data-js="tutorial-step" role="status"></p><p data-js="tutorial-copy"></p><nav class="reader__row" aria-label="튜토리얼 단계"><button type="button" data-js="tutorial-prev">이전</button><button type="button" data-js="tutorial-next">다음</button><button type="button" data-js="tutorial-later">나중에 보기</button></nav></dialog>
'''
s=s.replace('<script>',dialog+'<script>',1)
helpers=r'''
const tutorialKey='missa.reader.symbol-tutorial.v1';
const tutorialSteps=[
 ['◎ 합송','동그라미 두 개(◎)는 신자가 함께 바치는 부분입니다. 굵은 글씨와 강조 테두리 카드의 본문을 함께 바칩니다.'],
 ['+ 사제의 부분','십자가 모양(+) 표시는 사제가 바치는 부분입니다. 신자는 듣고, 이어지는 ◎ 합송에 참여합니다.'],
 ['안내와 선택 양식','안내 색으로 구분된 문장은 자세나 행동에 대한 설명입니다. 〈또는〉은 사제가 선택할 수 있는 다른 양식이 이어진다는 뜻입니다.'],
 ['페이지와 악보','본문은 아래 페이지 버튼으로 넘깁니다. 긴 악보와 신앙 고백은 카드 안에서 스크롤합니다. 이 설명은 오른쪽 아래 안내에서 언제든 다시 볼 수 있습니다.']
];
let tutorialIndex=0,tutorialOpener=null,tutorialSeen=false;
function paintTutorial(){const step=tutorialSteps[tutorialIndex];find('tutorial-title').textContent=step[0];find('tutorial-step').textContent=`${tutorialIndex+1} / ${tutorialSteps.length}`;find('tutorial-copy').textContent=step[1];find('tutorial-prev').disabled=tutorialIndex===0;find('tutorial-next').textContent=tutorialIndex===tutorialSteps.length-1?'시작하기':'다음';}
function showTutorial(trigger=null){tutorialOpener=trigger;tutorialIndex=0;paintTutorial();find('tutorial').showModal();find('tutorial-next').focus();}
function hasSeenTutorial(){try{return localStorage.getItem(tutorialKey)==='done';}catch{return tutorialSeen;}}
function finishTutorial(){tutorialSeen=true;try{localStorage.setItem(tutorialKey,'done');}catch{}find('tutorial').close();}
function nextTutorial(){if(tutorialIndex===tutorialSteps.length-1)finishTutorial();else{tutorialIndex++;paintTutorial();}}
'''
s=s.replace("find('part-prev').onclick",helpers+"\nfind('part-prev').onclick",1)
s=s.replace("context(); render();\n</script>","find('tutorial-prev').onclick=()=>{tutorialIndex=Math.max(0,tutorialIndex-1);paintTutorial();};\nfind('tutorial-next').onclick=nextTutorial;\nfind('tutorial-later').onclick=()=>find('tutorial').close();\nfind('tutorial').addEventListener('close',()=>{const target=find('drawer').open?tutorialOpener:find('part-next');target?.focus();});\ncontext(); render();\nif(!hasSeenTutorial())showTutorial();\n</script>",1)
Path('review/02-ia-v15.html').write_text(s,encoding='utf-8',newline='\r\n')
Path('work/review-ia-v15-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S).group(1),encoding='utf-8')
