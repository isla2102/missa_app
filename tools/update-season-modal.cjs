const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const readerJsPath = path.join(root, 'prototype', 'source', 'reader.js');
let readerJs = fs.readFileSync(readerJsPath, 'utf8');

// 정규식으로 showSeasonModal 교체
const seasonModalRegex = /function showSeasonModal\(trigger\)\s*\{[\s\S]*?find\('season-modal'\)\.showModal\(\);find\('season-modal-close'\)\.focus\(\);\s*\}/;

const newShowSeasonModal = `function showSeasonModal(trigger){
 seasonModalOpener=trigger;const body=find('season-modal-body');body.replaceChildren();const year=find('date').value.slice(0,4);find('season-modal-title').textContent=year+'년 전례 시기';
 if(year==='2026'){
  const current=currentSeason();seasonCalendar2026.periods.forEach(period=>{
   const card=document.createElement('section');card.className='reader__content-card';card.style.padding='var(--reader-content-inset)';
   if(current===period){card.setAttribute('aria-current','true');card.style.borderColor='var(--reader-theme-accent)';card.style.background='var(--state-selected-surface)';}
   const heading=document.createElement('div');heading.className='overlay__header';
   const h=document.createElement('h3');h.className='reader__item-title';h.textContent=period.title+(current===period?' · 현재 선택한 시기':'');
   if(current===period)h.style.color='var(--reader-theme-accent)';
   const help=createReaderButton('?');help.type='button';help.setAttribute('aria-label',period.title+' 의미 알아보기');help.setAttribute('aria-haspopup','dialog');help.setAttribute('aria-controls','season-help-dialog');help.title=period.title+'란?';help.onclick=()=>showSeasonHelp(period.key,help);help.hidden=!seasonMeanings[period.key];
   heading.append(h,help);
   const p=document.createElement('p');p.className='reader__item-text';p.textContent=period.description;
   card.append(heading,p);body.append(card);
  });
  const note=document.createElement('p');note.className='reader__guidance';note.textContent='성주간 목요일 저녁부터 부활 성야 전까지는 파스카 성삼일입니다. 현재 확인한 대림·성탄 범위는 2026년 말까지이며 다음 해 경계·상세 미사 선택은 별도 자료입니다.';body.append(note);
  const source=externalSourceLink(seasonCalendar2026.sourceUrl,'2026년 전례력 자료');body.append(source);
 }else{const p=document.createElement('p');p.className='reader__guidance';p.textContent='선택한 연도의 전례 시기 자료 연결 전입니다.';body.append(p);}
 find('season-modal').showModal();find('season-modal-close').focus();
}`;

if (!seasonModalRegex.test(readerJs)) {
  console.error('❌ 정규식 매칭 실패');
  process.exit(1);
}

readerJs = readerJs.replace(seasonModalRegex, newShowSeasonModal);
fs.writeFileSync(readerJsPath, readerJs, 'utf8');
console.log('✅ prototype/source/reader.js 내 showSeasonModal 시스템 정규화 완료');
