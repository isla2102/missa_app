
'use strict';
const find = name => document.querySelector(`[data-js="${name}"]`);
const sections = ['시작 예식', '말씀 전례', '성찬 전례', '마침 예식'];
let spread = 0;
let opener = null;
let scenario = 'sunday';
const titles = {toc:'미사 목차', hymn:'회차별 성가', prayer:'주요 기도문', settings:'보기 설정', info:'안내 · 개발용 예시'};
function context() {
  find('context').textContent = scenario === 'weekday' ? '개발용 평일 예시 · 주일 회차 미적용 · 날짜 자동 변경 없음' : `${find('slot').value} · 네 성가 배정만 변경 · 같은 주일 문서`;
}
function renderBook() {
  find('book').replaceChildren();
  sections.slice(spread * 2, spread * 2 + 2).forEach((title, i) => {
    const article = document.createElement('article'); article.className = 'review__card';
    const heading = document.createElement('h3'); heading.textContent = title;
    const p = document.createElement('p'); p.textContent = `연속 본문 ${spread * 2 + i + 1}쪽 · 공식 본문 연결 예정`;
    article.append(heading, p);
    if (find('mode').value === 'beginner') { const hint = document.createElement('p'); hint.textContent = '예비신자 안내가 본문 흐름 안에 표시되는 영역'; article.append(hint); }
    find('book').append(article);
  });
  find('page').textContent = `${spread + 1} / 2 펼침`; find('prev').disabled = spread === 0; find('next').disabled = spread === 1;
}
function closePanel() { find('drawer').close(); }
function showPanel(which, trigger) {
  opener = trigger; const body = find('drawer-body'); body.replaceChildren(); find('drawer-title').textContent = titles[which];
  const text = value => { const p = document.createElement('p'); p.textContent = value; body.append(p); };
  if (which === 'toc') sections.forEach((title, i) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = title; b.onclick = () => { spread = Math.floor(i / 2); renderBook(); closePanel(); }; const p = document.createElement('p'); p.append(b); body.append(p); });
  if (which === 'hymn') { text(scenario === 'weekday' ? '개발용 평일 예시: 주일 회차 성가 편집 미적용' : `${find('slot').value}의 성가 편성`); ['입당', '봉헌', '영성체', '파견'].forEach(role => text(`${role} 성가 · 미등록`)); text('번호·제목·개인 가사/메모·출처 URL 편집 기능은 후속 구현 대상입니다.'); }
  if (which === 'prayer') text('주요 기도문 목록 → 선택한 기도문. 공식 원문은 아직 연결되지 않았습니다.');
  if (which === 'settings') text('보기 설정에 글자 크기·다크 모드를 모읍니다. 이 단계에서는 항목 위치만 검토하며 값이나 테마를 제안하지 않습니다.');
  if (which === 'info') {
    text('공식 콘텐츠 미연동 · 아래 선택은 개발용 순서 예시입니다. 날짜 기반 전례 판별이 아닙니다.');
    const label = document.createElement('label'); label.className = 'review__field'; label.textContent = '개발용 예시';
    const select = document.createElement('select'); [['sunday','주일 공통 순서 예시'],['weekday','평일 예시 · 주일 회차 미적용']].forEach(([value, name]) => { const option = document.createElement('option'); option.value = value; option.textContent = name; select.append(option); }); select.value = scenario;
    select.onchange = () => { scenario = select.value; find('slot').disabled = scenario === 'weekday'; context(); }; label.append(select); body.append(label);
    text('평일 선택은 충돌 처리 정책 체험입니다. 본문 영역은 IA 검토용 구조이며 실제 평일 전례로 전환되지 않습니다.');
  }
  find('drawer').showModal();
}
find('prev').onclick = () => { spread = Math.max(0, spread - 1); renderBook(); };
find('next').onclick = () => { spread = Math.min(1, spread + 1); renderBook(); };
find('slot').onchange = context;
find('mode').onchange = renderBook;
find('date').onchange = () => { find('context').textContent = '선택 날짜의 공식 전례는 미연동입니다. 회차 선택으로 날짜는 바뀌지 않습니다.'; };
document.querySelectorAll('[data-panel]').forEach(button => button.onclick = () => showPanel(button.dataset.panel, button));
find('close').onclick = closePanel;
find('drawer').addEventListener('close', () => { if (opener) opener.focus(); });
context(); renderBook();
