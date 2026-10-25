
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
function renderPrayerCard(title, prayerId, scoreSlot = true) {
 const card = document.createElement('div'); card.className = 'reader__content-card';
 card.setAttribute('data-content-source','ordinary+parishPrayerSetting');
 function fill() {
  card.replaceChildren();
  const mode = parishPrayerPresentation[prayerId] || 'recite';
  if (scoreSlot) {
   const group = document.createElement('div'); group.className = 'reader__prayer-option'; group.setAttribute('role','group'); group.setAttribute('aria-label',`${title} 표시 방식`);
   [['recite','낭송 · 본문'],['chant','성가 · 악보']].forEach(([value,text])=>{
    const button=document.createElement('button');button.type='button';button.className='reader__prayer-button';button.textContent=text;
    button.setAttribute('aria-pressed',String(mode===value));button.setAttribute('data-prayer-mode',value);
    button.onclick=()=>{parishPrayerPresentation[prayerId]=value;fill();card.querySelector(`[data-prayer-mode="${value}"]`)?.focus();};group.append(button);
   });card.append(group);
  }
  const p = document.createElement('p'); p.className='reader__item-text';p.lang='la';p.textContent=mockParagraph;card.append(p);
  if (mode==='chant' && scoreSlot) {
   const figure=document.createElement('figure');figure.className='reader__score';
   const caption=document.createElement('figcaption');caption.textContent='악보 자리 · 미등록 (mock, 실제 악보 아님)';
   const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 400 60');svg.setAttribute('class','reader__staff');svg.setAttribute('role','img');svg.setAttribute('aria-label','악보가 들어갈 위치를 나타내는 빈 오선');
   [10,20,30,40,50].forEach(y=>{const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1','0');line.setAttribute('x2','400');line.setAttribute('y1',String(y));line.setAttribute('y2',String(y));line.setAttribute('stroke','currentColor');svg.append(line);});
   figure.append(caption,svg);card.append(figure);
  }
 }
 fill(); return card;
}

function renderItem(item) {
 const spec = frameSpecs[item.title];
 const section = document.createElement('section'); section.className = 'reader__item'; section.id = item.id; section.tabIndex = -1;
 const heading = document.createElement('h3'); heading.className = 'reader__item-title'; heading.textContent = item.title;
 if (item.id === selectedItem) { section.setAttribute('aria-current','location'); heading.textContent += ' · 현재 위치'; }
 section.append(heading);
 if (spec.kind === 'prayer') {
  section.append(renderPrayerCard(item.title,spec.prayerId,spec.scoreSlot));
 } else if (spec.kind === 'choice') {
  const guide = document.createElement('p'); guide.className = 'reader__item-text'; guide.textContent = spec.guide; section.append(guide);
 } else {
  const container = spec.kind === 'fixed' ? section : document.createElement('div');
  if (spec.kind !== 'fixed') { container.className = 'reader__content-card'; container.setAttribute('data-content-source',spec.source); }
  const paragraph = document.createElement('p'); paragraph.className = 'reader__item-text'; paragraph.lang = 'la'; paragraph.textContent = mockParagraph;
  container.append(paragraph);
  if (spec.kind !== 'fixed') section.append(container);
 }
 return section;
}

let selectedItem = null;
function jumpToItem(partIndex, item) {
 part = partIndex; spread = Math.floor(item.page / 2); selectedItem = item.id;
 render(); const target=document.getElementById(item.id);target?.focus({preventScroll:true});target?.scrollIntoView({block:'nearest',inline:'nearest'});
}

let part = 0, spread = 0, opener = null;
const position = parts.map(() => 0);
const titles = {toc:'미사 목차',hymn:'회차별 성가',prayer:'주요 기도문',settings:'보기 설정',info:'안내 · 검토 v8'};
function context() { find('context').textContent = `${find('slot').value} · 공통 주일 문서 · MOCK 본문(Lorem ipsum) · 공식 자료 미연동 · 정보 구조 검토 v8`; }
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

function render() {
 if (!contents[part].some(item => item.id === selectedItem && Math.floor(item.page / 2) === spread)) {
  selectedItem = contents[part].find(item => item.page === spread * 2)?.id ?? null;
 }
 const current = parts[part]; find('part-title').textContent = current.title;
 find('book').replaceChildren();
 current.pages.slice(spread * 2, spread * 2 + 2).forEach(([title, description], i) => {
  const page = document.createElement('article'); page.className = 'reader__page';
  page.setAttribute('aria-label', `${current.title} ${spread * 2 + i + 1}쪽`);
  contents[part].filter(item => item.page === spread * 2 + i).forEach(item => page.append(renderItem(item)));
  find('book').append(page);
 });
 find('part-current').textContent = `현재: ${current.title}`;
 find('part-prev').textContent = part ? `← ${parts[part-1].title}` : '미사 시작'; find('part-prev').disabled = part === 0;
 find('part-next').textContent = part < parts.length-1 ? `${parts[part+1].title} →` : '미사 마침'; find('part-next').disabled = part === parts.length-1;
 find('page-context').textContent = `${current.title} · ${spread*2+1}–${Math.min(spread*2+2,current.pages.length)}쪽`;
 find('page-prev').disabled = spread === 0; find('page-next').disabled = (spread+1)*2 >= current.pages.length;
 position[part] = spread; renderToc();
}
function go(index) { selectedItem = null; part = index; spread = position[part]; render(); }
function showPanel(which, trigger) {
 opener = trigger; const body = find('drawer-body'); body.replaceChildren(); find('drawer-title').textContent = titles[which];
 const text = value => { const p = document.createElement('p'); p.textContent = value; body.append(p); };
 if (which === 'hymn') { text(`${find('slot').value} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`)); }
 if (which === 'prayer') {
  text('기도문 본문과 본당별 기도문 성가·악보를 카드에 표시합니다. 아래 선택은 mock 체험이며 실제 본당 편성·악보 등록은 미구현입니다.');
  ['성호경','주님의 기도','성모송','영광송'].forEach(title=>{const section=document.createElement('section');section.className='reader__item';const heading=document.createElement('h3');heading.className='reader__item-title';heading.textContent=title;section.append(heading,renderPrayerCard(title,title,title!=='성호경'));body.append(section);});
 }
 if (which === 'settings') {
  text('우측 하단에서 여는 e-book 보기 설정입니다. 이 단계는 항목 위치를 검토하며 실제 글자 크기·테마 적용은 후속 디자인 단계에서 구현합니다.');
  const size = document.createElement('label'); size.className = 'reader__field'; size.textContent = '글자 크기 (배치 예시)'; const range = document.createElement('input'); range.type = 'range'; range.disabled = true; size.append(range); body.append(size);
  const theme = document.createElement('label'); theme.className = 'reader__field'; theme.textContent = '배경 테마 (배치 예시)'; const select = document.createElement('select'); select.disabled = true; ['밝게','어둡게','종이'].forEach(name => { const option = document.createElement('option'); option.textContent = name; select.append(option); }); theme.append(select); body.append(theme);
 }
 if (which === 'info') {
  text('현재 예식의 내용이 왼쪽→오른쪽 두 페이지로 이어집니다. 길어지면 같은 예식 안에서 페이지를 넘깁니다. 아래 예식 이름 버튼은 이전·다음 예식으로 이동합니다.');
  text('날짜·전례력 자동 판별은 미구현입니다. 본문은 조판 위치를 보여주는 개발용 예시입니다. 실제 조판기는 이후 글자·화면 크기에 맞게 페이지를 나누고 문단 식별자로 위치를 복원해야 합니다.');
  text('목차는 뷰어 오른쪽 상시 레일입니다. 안내 문구 없이 세부 링크와 현재 위치를 표시합니다. 성가·기도문·보기 설정·안내는 보조 Drawer를 유지합니다.');
  text('프레임 규칙: 각 순서의 타이틀 아래에 변동 본문은 카드, 기도문은 본문·악보 카드, 선택 양식은 짧은 안내를 표시합니다. 모든 라틴어 본문은 Lorem ipsum mock입니다.');
  text('변동 본문 카드는 매일미사·전례집 자료 연결을 위한 자리입니다. 고정 본문은 통상문 자료를 사용합니다. 적용 여부와 선택 양식은 공식 데이터·본당 선택 확인 후 결정하며, 현재 분류는 프레임 검토용입니다.');
  text('입당·봉헌·영성체·파견 성가 편성은 회차별 HymnSet입니다. 매일미사의 입당송·영성체송 같은 공통 전례일 본문과 구분합니다. 현재 모든 자료 연동·성가 편집은 미구현입니다.');
  text('기도문 카드는 고정 공식 본문과 본당별 기도문 성가 악보 참조를 분리합니다. 본당 설정은 세 주일 회차에 공통 적용하며, 회차별 네 성가 배정을 변경하지 않습니다. 낭송/성가 선택은 mock 체험으로 새로고침 시 초기화됩니다. 악보는 출처·이용 조건 확인 후 이미지나 PDF를 연결할 자리이며 현재 빈 오선만 표시합니다.');
  text('영성체 프레임은 공통 본문 카드 위치를 보여줍니다. 세부 통상문·영성체송·회차별 성가의 내부 구성은 후속 프레임에서 나눌 수 있습니다.');
  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');
 }
 find('drawer').showModal();
}
find('part-prev').onclick = () => go(Math.max(0,part-1));
find('part-next').onclick = () => go(Math.min(parts.length-1,part+1));
find('page-prev').onclick = () => { selectedItem = null; spread = Math.max(0,spread-1); render(); };
find('page-next').onclick = () => { selectedItem = null; spread = Math.min(Math.ceil(parts[part].pages.length/2)-1,spread+1); render(); };
find('mode').onchange = render; find('slot').onchange = context;
find('date').onchange = () => { context(); find('context').textContent += ' · 선택 날짜의 공식 전례는 미확인'; };
document.querySelectorAll('[data-panel]').forEach(button => button.onclick = () => showPanel(button.dataset.panel,button));
find('close').onclick = () => find('drawer').close();
find('drawer').addEventListener('close', () => { render(); const target = selectedItem && document.getElementById(selectedItem); if (target) target.focus({preventScroll:true}); else opener?.focus(); });
context(); render();
