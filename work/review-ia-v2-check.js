
'use strict';
const find = name => document.querySelector(`[data-js="${name}"]`);
const parts = [
 {title:'시작 예식', pages:[['입당 · 성호경과 인사','공식 본문을 연결할 첫 번째 쪽입니다.'],['참회 예식 · 자비송 · 대영광송 · 본기도','같은 시작 예식의 이어지는 두 번째 쪽입니다.']]},
 {title:'말씀 전례', pages:[['독서 · 화답송','말씀 전례의 첫 번째 쪽입니다.'],['복음 환호송 · 복음','말씀 전례의 두 번째 쪽입니다.'],['강론 · 신앙 고백','말씀 전례의 세 번째 쪽입니다.'],['보편 지향 기도','말씀 전례의 네 번째 쪽입니다.']]},
 {title:'성찬 전례', pages:[['예물 준비 · 예물 기도','성찬 전례의 첫 번째 쪽입니다.'],['감사 기도','성찬 전례의 두 번째 쪽입니다.'],['주님의 기도 · 평화 예식','성찬 전례의 세 번째 쪽입니다.'],['영성체 · 영성체 후 기도','성찬 전례의 네 번째 쪽입니다.']]},
 {title:'마침 예식', pages:[['공지 · 강복','마침 예식의 첫 번째 쪽입니다.'],['파견 · 파견 성가','마침 예식의 이어지는 두 번째 쪽입니다.']]}
];
let part = 0, spread = 0, opener = null;
const position = parts.map(() => 0);
const titles = {toc:'미사 목차',hymn:'회차별 성가',prayer:'주요 기도문',settings:'보기 설정',info:'안내 · 검토 v2'};
function context() { find('context').textContent = `${find('slot').value} · 공통 주일 문서 · 공식 본문 미연동 · 정보 구조 검토 v2`; }
function render() {
 const current = parts[part]; find('part-title').textContent = current.title;
 find('book').replaceChildren();
 current.pages.slice(spread * 2, spread * 2 + 2).forEach(([title, description], i) => {
  const page = document.createElement('article'); page.className = 'reader__page';
  page.setAttribute('aria-label', `${current.title} ${spread * 2 + i + 1}쪽`);
  const h = document.createElement('h3'); h.className = 'reader__page-title'; h.textContent = title;
  const p = document.createElement('p'); p.textContent = description;
  const note = document.createElement('p'); note.textContent = '조판 위치를 설명하는 자리표시자입니다. 공식 전례문이 아닙니다.';
  page.append(h,p,note);
  if (find('mode').value === 'beginner') { const hint = document.createElement('p'); hint.textContent = '예비신자 안내도 현재 예식의 본문 흐름 안에 포함됩니다.'; page.append(hint); }
  find('book').append(page);
 });
 find('part-current').textContent = `현재: ${current.title}`;
 find('part-prev').textContent = part ? `← ${parts[part-1].title}` : '미사 시작'; find('part-prev').disabled = part === 0;
 find('part-next').textContent = part < parts.length-1 ? `${parts[part+1].title} →` : '미사 마침'; find('part-next').disabled = part === parts.length-1;
 find('page-context').textContent = `${current.title} · ${spread*2+1}–${Math.min(spread*2+2,current.pages.length)}쪽`;
 find('page-prev').disabled = spread === 0; find('page-next').disabled = (spread+1)*2 >= current.pages.length;
 position[part] = spread;
}
function go(index) { part = index; spread = position[part]; render(); }
function showPanel(which, trigger) {
 opener = trigger; const body = find('drawer-body'); body.replaceChildren(); find('drawer-title').textContent = titles[which];
 const text = value => { const p = document.createElement('p'); p.textContent = value; body.append(p); };
 if (which === 'toc') parts.forEach((item,i) => { const p = document.createElement('p'); const b = document.createElement('button'); b.type = 'button'; b.textContent = item.title; if (part === i) b.setAttribute('aria-current','step'); b.onclick = () => { go(i); find('drawer').close(); }; p.append(b); body.append(p); });
 if (which === 'hymn') { text(`${find('slot').value} · 미등록`); ['입당','봉헌','영성체','파견'].forEach(role => text(`${role} 성가 · 미등록`)); }
 if (which === 'prayer') text('성호경 · 주님의 기도 · 성모송 · 영광송. 공식 원문은 아직 연결하지 않았습니다.');
 if (which === 'settings') {
  text('우측 하단에서 여는 e-book 보기 설정입니다. 이 단계는 항목 위치를 검토하며 실제 글자 크기·테마 적용은 후속 디자인 단계에서 구현합니다.');
  const size = document.createElement('label'); size.className = 'reader__field'; size.textContent = '글자 크기 (배치 예시)'; const range = document.createElement('input'); range.type = 'range'; range.disabled = true; size.append(range); body.append(size);
  const theme = document.createElement('label'); theme.className = 'reader__field'; theme.textContent = '배경 테마 (배치 예시)'; const select = document.createElement('select'); select.disabled = true; ['밝게','어둡게','종이'].forEach(name => { const option = document.createElement('option'); option.textContent = name; select.append(option); }); theme.append(select); body.append(theme);
 }
 if (which === 'info') {
  text('현재 예식의 내용이 왼쪽→오른쪽 두 페이지로 이어집니다. 길어지면 같은 예식 안에서 페이지를 넘깁니다. 아래 예식 이름 버튼은 이전·다음 예식으로 이동합니다.');
  text('날짜·전례력 자동 판별은 미구현입니다. 본문은 조판 위치를 보여주는 개발용 예시입니다. 실제 조판기는 이후 글자·화면 크기에 맞게 페이지를 나누고 문단 식별자로 위치를 복원해야 합니다.');
  text('목차 제안 A: 우측 Drawer(현재 체험). 대안 B: 목차 상시 고정(본문 가용 폭 감소). 두 페이지 공간을 확보하는 A를 추천합니다.');
  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');
 }
 find('drawer').showModal();
}
find('part-prev').onclick = () => go(Math.max(0,part-1));
find('part-next').onclick = () => go(Math.min(parts.length-1,part+1));
find('page-prev').onclick = () => { spread = Math.max(0,spread-1); render(); };
find('page-next').onclick = () => { spread = Math.min(Math.ceil(parts[part].pages.length/2)-1,spread+1); render(); };
find('mode').onchange = render; find('slot').onchange = context;
find('date').onchange = () => { context(); find('context').textContent += ' · 선택 날짜의 공식 전례는 미확인'; };
document.querySelectorAll('[data-panel]').forEach(button => button.onclick = () => showPanel(button.dataset.panel,button));
find('close').onclick = () => find('drawer').close();
find('drawer').addEventListener('close', () => opener?.focus());
context(); render();
