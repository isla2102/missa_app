
'use strict';
const find = name => document.querySelector(`[data-js="${name}"]`);
const parts = [
 {title:'시작 예식', pages:[['입당 · 성호경과 인사','공식 본문을 연결할 첫 번째 쪽입니다.'],['참회 예식 · 자비송 · 대영광송 · 본기도','같은 시작 예식의 이어지는 두 번째 쪽입니다.']]},
 {title:'말씀 전례', pages:[['독서 · 화답송','말씀 전례의 첫 번째 쪽입니다.'],['복음 환호송 · 복음','말씀 전례의 두 번째 쪽입니다.'],['강론 · 신앙 고백','말씀 전례의 세 번째 쪽입니다.'],['보편 지향 기도','말씀 전례의 네 번째 쪽입니다.']]},
 {title:'성찬 전례', pages:[['예물 준비 · 예물 기도','성찬 전례의 첫 번째 쪽입니다.'],['감사 기도','성찬 전례의 두 번째 쪽입니다.'],['주님의 기도 · 평화 예식','성찬 전례의 세 번째 쪽입니다.'],['영성체 · 영성체 후 기도','성찬 전례의 네 번째 쪽입니다.']]},
 {title:'마침 예식', pages:[['공지 · 강복','마침 예식의 첫 번째 쪽입니다.'],['파견 · 파견 성가','마침 예식의 이어지는 두 번째 쪽입니다.']]}
];

const contents = [
 [['입당 성가',0],['성호경',0],['인사',0],['참회 예식',1],['자비송',1],['대영광송',1],['본기도',1]],
 [['제1독서',0],['화답송',0],['제2독서',0],['복음 환호송',1],['복음',1],['강론',2],['신앙 고백',2],['보편 지향 기도',3]],
 [['예물 준비 · 봉헌 성가',0],['예물 기도',0],['감사 기도',1],['주님의 기도',2],['평화 예식',2],['영성체 예식 · 영성체 성가',3],['영성체 후 기도',3]],
 [['공지 사항',0],['강복',0],['파견',1],['파견 성가',1]]
].map((items, partIndex) => items.map(([title, page], index) => ({id:`part-${partIndex}-item-${index}`, title, page})));
const frameSpecs = {"입당 성가": {"kind": "hymn", "source": "hymnSet", "role": "entrance"}, "성호경": {"kind": "prayer", "source": "ordinary", "prayerId": "성호경", "scoreSlot": false}, "인사": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 인사 양식에 따라 참여합니다."}, "참회 예식": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 참회 예식 양식에 따라 참여합니다."}, "자비송": {"kind": "prayer", "source": "ordinary", "condition": "선택한 예식에 따라 적용", "prayerId": "자비송", "scoreSlot": true}, "대영광송": {"kind": "prayer", "source": "ordinary", "condition": "전례일에 따라 포함 여부 결정", "prayerId": "대영광송", "scoreSlot": true}, "본기도": {"kind": "proper", "source": "liturgicalDay"}, "제1독서": {"kind": "proper", "source": "liturgicalDay"}, "화답송": {"kind": "proper", "source": "liturgicalDay"}, "제2독서": {"kind": "proper", "source": "liturgicalDay", "condition": "전례일에 따라 적용"}, "복음 환호송": {"kind": "proper", "source": "liturgicalDay"}, "복음": {"kind": "proper", "source": "liturgicalDay"}, "강론": {"kind": "choice", "source": "celebrant", "guide": "사제 또는 부제의 강론을 듣습니다."}, "신앙 고백": {"kind": "prayer", "source": "celebrant", "guide": "적용되는 전례일에 선택된 신앙 고백 양식으로 참여합니다.", "prayerId": "신앙 고백", "scoreSlot": true}, "보편 지향 기도": {"kind": "choice", "source": "parish", "guide": "본당에서 준비한 기도 지향에 따라 함께 기도합니다."}, "예물 준비 · 봉헌 성가": {"kind": "hymn", "source": "hymnSet", "role": "offertory"}, "예물 기도": {"kind": "proper", "source": "liturgicalDay"}, "감사 기도": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 감사 기도 양식에 따라 참여합니다."}, "주님의 기도": {"kind": "prayer", "source": "ordinary", "prayerId": "주님의 기도", "scoreSlot": true}, "평화 예식": {"kind": "choice", "source": "celebrant", "guide": "사제의 안내에 따라 평화 예식에 참여합니다."}, "영성체 예식 · 영성체 성가": {"kind": "proper", "source": "liturgicalDay", "role": "communion"}, "영성체 후 기도": {"kind": "proper", "source": "liturgicalDay"}, "공지 사항": {"kind": "choice", "source": "parish", "guide": "본당 공지가 있으면 안내를 듣습니다."}, "강복": {"kind": "choice", "source": "celebrant", "guide": "사제가 선택한 강복 양식에 따라 참여합니다."}, "파견": {"kind": "choice", "source": "celebrant", "guide": "선택된 파견 양식에 따라 응답합니다."}, "파견 성가": {"kind": "hymn", "source": "hymnSet", "role": "recessional"}};
const mockParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.';

// The prototype holds parish presentation choices in memory only, shared by all Sunday sessions.
const parishPrayerPresentation = Object.create(null);
const prayerSourceRefs = {textRef:null, scoreRef:null, sourceUrl:null, licenseStatus:'unverified'};
const temporaryPrincipalScores = {"자비송": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020.jpg", "title": "자비송", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "대영광송": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_01.jpg", "title": "대영광송 앞부분", "rotation": -90, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}, {"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_02.jpg", "title": "대영광송 이어지는 부분", "rotation": 180, "width": 4000, "height": 3000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "거룩하시도다 · 신앙의 신비여": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_03.jpg", "title": "거룩하시도다 · 신앙의 신비여 (함께 촬영)", "rotation": 180, "width": 4000, "height": 3000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "아멘": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_04.jpg", "title": "아멘", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "주님의 기도": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_05.jpg", "title": "주님의 기도 앞부분", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}, {"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_06.jpg", "title": "주님의 기도 이어지는 부분", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "주님의 기도 맺음 환호": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_07.jpg", "title": "주님의 기도 맺음 환호 · 하느님의 어린양 (함께 촬영)", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}], "하느님의 어린양": [{"path": "../docs/교중미사악보/KakaoTalk_20261018_172809020_07.jpg", "title": "하느님의 어린양 · 주님의 기도 맺음 환호 (함께 촬영)", "rotation": 0, "width": 3000, "height": 4000, "temporary": true, "source": "user-provided", "licenseStatus": "unverified"}]};

function scoreAssets(prayerId) { return find('slot').value === 'main' ? (temporaryPrincipalScores[prayerId] || []) : []; }
function selectedSlotName() { return find('slot').selectedOptions[0].textContent; }
function renderPhoto(asset) {
 const figure=document.createElement('figure');figure.className='reader__score';
 const caption=document.createElement('figcaption');caption.textContent=`교중미사 임시 악보 · ${asset.title} `;
 const link=document.createElement('a');link.href=encodeURI(asset.path);link.target='_blank';link.rel='noopener noreferrer';link.textContent='원본 열기';caption.append(link);
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','reader__score-photo');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${asset.title} · 사용자 제공 사진, 임시 배치`);
 const quarter=Math.abs(asset.rotation)===90;const width=quarter?asset.height:asset.width;const height=quarter?asset.width:asset.height;
 svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
 const image=document.createElementNS('http://www.w3.org/2000/svg','image');image.setAttribute('href',encodeURI(asset.path));image.setAttribute('width',String(asset.width));image.setAttribute('height',String(asset.height));
 if(asset.rotation===-90)image.setAttribute('transform',`translate(0 ${asset.width}) rotate(-90)`);
 if(asset.rotation===180)image.setAttribute('transform',`translate(${asset.width} ${asset.height}) rotate(180)`);
 image.addEventListener('error',()=>{caption.textContent=`${asset.title} · 이미지 로딩 실패. 프로젝트의 docs/교중미사악보 경로를 확인해 주세요.`;});
 svg.append(image);figure.append(caption,svg);return figure;
}
function renderPrayerFrame(title, prayerId, scoreSlot=true, level=3) {
 const frame=document.createElement('section');frame.className='reader__item';
 const headingRow=document.createElement('div');headingRow.className='reader__item-heading';
 const heading=document.createElement(`h${level}`);heading.className='reader__item-title';heading.textContent=title;headingRow.append(heading);
 const group=document.createElement('div');group.className='reader__prayer-option';group.setAttribute('role','group');group.setAttribute('aria-label',`${title} 표시 방식`);
 const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source','ordinary+temporaryPrincipalScores');
 if(scoreSlot)headingRow.append(group);frame.append(headingRow,card);
 function fill() {
  card.replaceChildren();group.replaceChildren();const assets=scoreAssets(prayerId);
  const mode=parishPrayerPresentation[prayerId] || (assets.length?'chant':'recite');
  if(scoreSlot)[['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([value,text])=>{
   const button=document.createElement('button');button.type='button';button.className='reader__prayer-button';button.textContent=text;button.setAttribute('aria-pressed',String(mode===value));button.setAttribute('data-prayer-mode',value);
   button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();group.querySelector(`[data-prayer-mode="${value}"]`)?.focus();
     if(frame.closest('.reader__book')){pendingPrayerFocus={key:frame.getAttribute('data-flow-key'),mode:value};scheduleReflow(frame.getAttribute('data-flow-key'));}
    };group.append(button);
  });
  if(mode==='chant' && scoreSlot){
   if(assets.length){
    const scoreWindow=document.createElement('div');scoreWindow.className='reader__score-scroll';scoreWindow.setAttribute('tabindex','0');scoreWindow.setAttribute('role','region');scoreWindow.setAttribute('aria-label',`${title} 악보 · 카드 안에서 스크롤`);
    assets.forEach(asset=>scoreWindow.append(renderPhoto(asset)));card.append(scoreWindow);
   }
   else{const p=document.createElement('p');p.textContent=`${selectedSlotName()} · 이 기도문의 임시 악보 미등록`;card.append(p);}
  } else {const p=document.createElement('p');p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);}
 }
 fill();return frame;
}
function renderItem(item) {
 const spec=frameSpecs[item.title];
 let section;
 if(spec.kind==='prayer') section=renderPrayerFrame(item.title,spec.prayerId,spec.scoreSlot);
 else {
  section=document.createElement('section');section.className='reader__item';
  const h=document.createElement('h3');h.className='reader__item-title';h.textContent=item.title;section.append(h);
  if(spec.kind==='choice'){const p=document.createElement('p');p.className='reader__item-text';p.textContent=spec.guide;section.append(p);}
  else {const card=document.createElement('div');card.className='reader__content-card';card.setAttribute('data-content-source',spec.source);const p=document.createElement('p');p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);section.append(card);}
 }
 section.id=item.id;section.tabIndex=-1;
 if(item.id===selectedItem){section.setAttribute('aria-current','location');}
 return section;
}

let selectedItem = null;
function jumpToItem(partIndex, item) {
 part=partIndex;selectedItem=item.id;render({anchorKey:item.id});
 const target=document.getElementById(item.id);target?.focus({preventScroll:true});
}

let part = 0, spread = 0, opener = null;
const position = parts.map(() => null);
const titles = {toc:'미사 목차',hymn:'회차별 성가',prayer:'주요 기도문',settings:'보기 설정',info:'안내 · 검토 v10'};
function context() { find('context').textContent = `${selectedSlotName()} · 공통 주일 문서 · MOCK 본문(Lorem ipsum) · 공식 자료 미연동 · 정보 구조 검토 v10`; }
function renderToc() {
 const nav=find('toc-rail');const rail=nav.parentElement;const previousScroll=rail.scrollTop;nav.replaceChildren();
 parts.forEach((item,partIndex)=>{
  const group=document.createElement('section');const heading=document.createElement('h3');heading.className='reader__toc-group-title';heading.textContent=item.title;
  const list=document.createElement('ol');list.className='reader__toc-list';
  contents[partIndex].forEach(entry=>{
   const li=document.createElement('li');const link=document.createElement('a');link.className='reader__toc-link';link.href=`#${entry.id}`;link.textContent=entry.title;
   if(entry.id===selectedItem){link.setAttribute('aria-current','location');link.setAttribute('aria-label',`${entry.title} · 현재 위치`);}
   link.onclick=event=>{event.preventDefault();jumpToItem(partIndex,entry);};li.append(link);list.append(li);
  });group.append(heading,list);nav.append(group);
 });rail.scrollTop=previousScroll;
}


let layouts=[],currentAnchor=null,pendingPrayerFocus=null,reflowFrame=null;
function flowBlocks(partIndex) {
 const blocks=[];
 contents[partIndex].forEach(item=>{
  blocks.push({key:item.id,tocId:item.id,item});
  const add=(suffix,title)=>blocks.push({key:`${item.id}-${suffix}`,tocId:item.id,prayerTitle:title});
  if(item.title==='감사 기도'){add('sanctus','거룩하시도다 · 신앙의 신비여');add('amen','아멘');}
  if(item.title==='주님의 기도')add('doxology','주님의 기도 맺음 환호');
  if(item.title==='영성체 예식 · 영성체 성가')add('agnus','하느님의 어린양');
 });return blocks;
}
function renderBlock(block) {
 const node=block.item?renderItem(block.item):renderPrayerFrame(block.prayerTitle,block.prayerTitle);
 node.id=block.key;node.tabIndex=-1;node.setAttribute('data-flow-key',block.key);
 if(block.fragmentText!==undefined){const p=node.querySelector('.reader__item-text');if(p)p.textContent=block.fragmentText;}
 if(block.continued){const heading=node.querySelector('h3');if(heading)heading.textContent+=' (계속)';}
 return node;
}
function paginateFlow(blocks,fits,split) {
 const pages=[];let current=[];
 const flush=()=>{if(current.length){pages.push({blocks:current,oversize:false});current=[];}};
 blocks.forEach(block=>{
  if(fits([...current,block])){current.push(block);return;}
  flush();
  if(fits([block])){current=[block];return;}
  const fragments=split(block);
  fragments.forEach(fragment=>{
   if(fits([...current,fragment]))current.push(fragment);
   else {flush();if(fits([fragment]))current=[fragment];else pages.push({blocks:[fragment],oversize:true});}
  });
 });flush();return pages;
}
function spreadForAnchor(pages,key) {
 const index=pages.findIndex(page=>page.blocks.some(block=>block.key===key));return index<0?0:Math.floor(index/2);
}
function composePages() {
 const probe=document.createElement('article');probe.className='reader__page reader__page--measure';probe.setAttribute('aria-hidden','true');probe.inert=true;find('book').append(probe);
 const fits=blocks=>{probe.replaceChildren(...blocks.map(renderBlock));return probe.scrollHeight<=probe.clientHeight+1;};
 const split=block=>{
  const node=renderBlock(block);const paragraph=node.querySelector('.reader__item-text');
  if(!paragraph || paragraph.textContent.length<2)return [block];
  const result=[];let remaining=paragraph.textContent,index=0;
  while(remaining.length){
   let low=1,high=remaining.length,best=0;
   const key=index?`${block.key}-continue-${index}`:block.key;
   while(low<=high){const mid=Math.floor((low+high)/2);const fragment={...block,key,continued:index>0,fragmentText:remaining.slice(0,mid)};if(fits([fragment])){best=mid;low=mid+1;}else high=mid-1;}
   if(!best)return [block];
   if(best<remaining.length){const boundary=remaining.lastIndexOf(' ',best);if(boundary>best/2)best=boundary+1;}
   result.push({...block,key,continued:index>0,fragmentText:remaining.slice(0,best)});remaining=remaining.slice(best);index++;
  }return result;
 };
 try{return paginateFlow(flowBlocks(part),fits,split);}finally{probe.remove();}
}
function render(options={}) {
 const book=find('book');if(book.clientWidth<2||book.clientHeight<2)return;
 const anchor=options.anchorKey||currentAnchor||contents[part][0].id;
 layouts=composePages();if(!layouts.length)return;
 spread=spreadForAnchor(layouts,anchor);
 const visible=layouts.slice(spread*2,spread*2+2);
 const anchorBlock=layouts.flatMap(page=>page.blocks).find(block=>block.key===anchor)||visible[0].blocks[0];
 currentAnchor=anchorBlock.key;selectedItem=anchorBlock.tocId;position[part]=currentAnchor;
 const nodes=visible.map((layout,index)=>{
  const page=document.createElement('article');page.className=layout.oversize?'reader__page reader__page--oversize':'reader__page';
  page.setAttribute('aria-label',`${parts[part].title} ${spread*2+index+1}쪽`);
  layout.blocks.forEach(block=>page.append(renderBlock(block)));return page;
 });
 if(nodes.length===1){const blank=document.createElement('article');blank.className='reader__page';blank.setAttribute('aria-label','빈 페이지');nodes.push(blank);}
 book.replaceChildren(...nodes);find('part-title').textContent=parts[part].title;
 find('part-current').textContent=`현재: ${parts[part].title}`;
 find('part-prev').textContent=part?`← ${parts[part-1].title}`:'미사 시작';find('part-prev').disabled=part===0;
 find('part-next').textContent=part<parts.length-1?`${parts[part+1].title} →`:'미사 마침';find('part-next').disabled=part===parts.length-1;
 find('page-context').textContent=`${parts[part].title} · ${spread*2+1}–${Math.min(spread*2+2,layouts.length)}쪽 / 총 ${layouts.length}쪽`;
 find('page-prev').disabled=spread===0;find('page-next').disabled=(spread+1)*2>=layouts.length;renderToc();
 if(pendingPrayerFocus){const request=pendingPrayerFocus;pendingPrayerFocus=null;const block=Array.from(book.querySelectorAll('[data-flow-key]')).find(node=>node.getAttribute('data-flow-key')===request.key);block?.querySelector(`[data-prayer-mode="${request.mode}"]`)?.focus({preventScroll:true});}
}
function scheduleReflow(anchorKey=currentAnchor) {
 if(reflowFrame!==null)cancelAnimationFrame(reflowFrame);
 reflowFrame=requestAnimationFrame(()=>{reflowFrame=null;render({anchorKey});});
}
function go(index){part=index;currentAnchor=position[index]||contents[index][0].id;render({anchorKey:currentAnchor});}
function turnSpread(direction){const page=layouts[(spread+direction)*2];if(page)render({anchorKey:page.blocks[0].key});}

function showPanel(which, trigger) {
 opener = trigger; const body = find('drawer-body'); body.replaceChildren(); find('drawer-title').textContent = titles[which];
 const text = value => { const p = document.createElement('p'); p.textContent = value; body.append(p); };
 if (which === 'hymn') { text(`${selectedSlotName()} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`)); }
 if (which === 'prayer') {
  text('기도문 본문과 본당별 기도문 성가·악보를 카드에 표시합니다. 교중미사 사진 악보를 임시로 배치했습니다. 본문은 mock이며 실제 본당 편성 확정 자료가 아닙니다.');
  ['성호경','자비송','대영광송','거룩하시도다 · 신앙의 신비여','아멘','주님의 기도','주님의 기도 맺음 환호','하느님의 어린양','성모송','영광송'].forEach(title=>body.append(renderPrayerFrame(title,title,title!=='성호경')));
 }
 if (which === 'settings') {
  text('우측 하단에서 여는 e-book 보기 설정입니다. 이 단계는 항목 위치를 검토하며 실제 글자 크기·테마 적용은 후속 디자인 단계에서 구현합니다.');
  const size = document.createElement('label'); size.className = 'reader__field'; size.textContent = '글자 크기 (배치 예시)'; const range = document.createElement('input'); range.type = 'range'; range.disabled = true; size.append(range); body.append(size);
  const theme = document.createElement('label'); theme.className = 'reader__field'; theme.textContent = '배경 테마 (배치 예시)'; const select = document.createElement('select'); select.disabled = true; ['밝게','어둡게','종이'].forEach(name => { const option = document.createElement('option'); option.textContent = name; select.append(option); }); theme.append(select); body.append(theme);
 }
 if (which === 'info') {
  text('현재 예식의 내용이 왼쪽→오른쪽 두 페이지로 이어집니다. 길어지면 같은 예식 안에서 페이지를 넘깁니다. 아래 예식 이름 버튼은 이전·다음 예식으로 이동합니다.');
  text('공식 전례력·본문은 미연동입니다. 현재 검토 화면은 실제 표시 높이를 측정하여 예식 안에서 다음 페이지로 내용을 넘깁니다. 긴 본문은 계속 페이지로 분리하고, 악보는 카드 안에서 스크롤합니다. 극도로 작은 화면 등에서 제목·조작부조차 한 쪽에 들어가지 않는 예외에만 해당 페이지의 스크롤을 허용합니다.');
  text('목차는 뷰어 오른쪽 상시 레일입니다. 안내 문구 없이 세부 링크와 현재 위치를 표시합니다. 성가·기도문·보기 설정·안내는 보조 Drawer를 유지합니다.');
  text('프레임 규칙: 각 순서의 타이틀 아래에 변동 본문은 카드, 기도문은 본문·악보 카드, 선택 양식은 짧은 안내를 표시합니다. 모든 라틴어 본문은 Lorem ipsum mock이며 사진 악보는 사용자가 제공한 임시 교중미사 자료입니다.');
  text('변동 본문 카드는 매일미사·전례집 자료 연결을 위한 자리입니다. 고정 본문은 통상문 자료를 사용합니다. 적용 여부와 선택 양식은 공식 데이터·본당 선택 확인 후 결정하며, 현재 분류는 프레임 검토용입니다.');
  text('입당·봉헌·영성체·파견 성가 편성은 회차별 HymnSet입니다. 매일미사의 입당송·영성체송 같은 공통 전례일 본문과 구분합니다. 현재 공식 자료 자동 연동·성가 편집은 미구현이며 사용자 제공 사진 악보만 임시로 연결했습니다.');
  text('기도문 카드는 고정 공식 본문과 본당별 기도문 성가 악보 참조를 분리합니다. 본당 설정은 세 주일 회차에 공통 적용하며, 회차별 네 성가 배정을 변경하지 않습니다. 낭송/성가 선택은 mock 체험으로 새로고침 시 초기화됩니다. 교중미사에 한해 사용자 제공 사진을 임시 표시합니다. 다른 회차에는 사진을 자동 배정하지 않습니다. 실제 기도문 본문·순서는 공통으로 유지하고 사진 리소스만 별도 참조합니다.');
  text('영성체 프레임은 공통 본문 카드 위치를 보여줍니다. 세부 통상문·영성체송·회차별 성가의 내부 구성은 후속 프레임에서 나눌 수 있습니다.');
  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');
 }
 find('drawer').showModal();
}
find('part-prev').onclick = () => go(Math.max(0,part-1));
find('part-next').onclick = () => go(Math.min(parts.length-1,part+1));
find('page-prev').onclick = () => turnSpread(-1);
find('page-next').onclick = () => turnSpread(1);
find('mode').onchange = render; find('slot').onchange = () => { context(); render(); };
find('date').onchange = () => { context(); find('context').textContent += ' · 선택 날짜의 공식 전례는 미확인'; };
document.querySelectorAll('[data-panel]').forEach(button => button.onclick = () => showPanel(button.dataset.panel,button));
find('close').onclick = () => find('drawer').close();
find('drawer').addEventListener('close', () => { render(); const target = selectedItem && document.getElementById(selectedItem); if (target) target.focus({preventScroll:true}); else opener?.focus(); });
let observedBookSize='';
if(typeof ResizeObserver!=='undefined')new ResizeObserver(entries=>{
 const rect=entries[0].contentRect;const size=`${Math.round(rect.width)}|${Math.round(rect.height)}`;
 if(size!==observedBookSize){observedBookSize=size;scheduleReflow();}
}).observe(find('book'));
window.addEventListener('resize',()=>scheduleReflow());
document.fonts?.ready.then(()=>scheduleReflow());
context(); render();
