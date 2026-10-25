const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// 1. prototype/source/shell.html 수정
// 전례시기 모달 바디에 시스템 정규화 클래스 overlay__body 적용
const shellPath = path.join(root, 'prototype', 'source', 'shell.html');
let shellHtml = fs.readFileSync(shellPath, 'utf8');

shellHtml = shellHtml.replace(
  '<div data-js="season-modal-body"></div>',
  '<div class="overlay__body" data-js="season-modal-body"></div>'
);
shellHtml = shellHtml.replace(
  '<p id="season-help-text" data-js="season-help-text"></p><a data-js="season-help-source" target="_blank" rel="noopener noreferrer">전례 시기 설명 출처</a>',
  '<div class="overlay__body"><p id="season-help-text" data-js="season-help-text" class="reader__item-text"></p><a data-js="season-help-source" target="_blank" rel="noopener noreferrer">전례 시기 설명 출처</a></div>'
);
fs.writeFileSync(shellPath, shellHtml, 'utf8');
console.log('1. prototype/source/shell.html 시스템 클래스(overlay__body) 적용 완료');

// 2. prototype/source/reader.js 수정
const readerJsPath = path.join(root, 'prototype', 'source', 'reader.js');
let readerJs = fs.readFileSync(readerJsPath, 'utf8');

// (1) liturgyNode 기호 매칭에 ✠ 추가
readerJs = readerJs.replace(
  'const match=part.text.match(/^([+◎◆○●])\\s*/);',
  'const match=part.text.match(/^([+◎◆○●✠])\\s*/);'
);

// (2) showSeasonModal 함수: 시스템 정규화 클래스(reader__content-card, overlay__header, reader__item-title, reader__item-text, reader__guidance 등) 적용
const oldShowSeasonModal = `function showSeasonModal(trigger){
 seasonModalOpener=trigger;const body=find('season-modal-body');body.replaceChildren();const year=find('date').value.slice(0,4);find('season-modal-title').textContent=year+'년 전례 시기';
 if(year==='2026'){
  const current=currentSeason();seasonCalendar2026.periods.forEach(period=>{const card=document.createElement('section');card.className='reader__season-period';if(current===period)card.setAttribute('aria-current','true');const h=document.createElement('h3');h.textContent=period.title+(current===period?' · 현재 선택한 시기':'');const heading=document.createElement('div');heading.className='reader__modal-heading';const help=createReaderButton();help.type='button';help.classList.add('reader__season-help');help.textContent='?';help.setAttribute('aria-label',period.title+' 의미 알아보기');help.setAttribute('aria-haspopup','dialog');help.setAttribute('aria-controls','season-help-dialog');help.title=period.title+'란?';help.onclick=()=>showSeasonHelp(period.key,help);help.hidden=!seasonMeanings[period.key];heading.append(h,help);const p=document.createElement('p');p.textContent=period.description;card.append(heading,p);body.append(card);});
  const note=document.createElement('p');note.textContent='성주간 목요일 저녁부터 부활 성야 전까지는 파스카 성삼일입니다. 현재 확인한 대림·성탄 범위는 2026년 말까지이며 다음 해 경계·상세 미사 선택은 별도 자료입니다.';body.append(note);
  const source=document.createElement('a');source.href=seasonCalendar2026.sourceUrl;source.target='_blank';source.rel='noopener noreferrer';source.textContent='2026년 전례력 자료';body.append(source);
 }else{const p=document.createElement('p');p.textContent='선택한 연도의 전례 시기 자료 연결 전입니다.';body.append(p);}
 find('season-modal').showModal();find('season-modal-close').focus();
}`;

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

readerJs = readerJs.replace(oldShowSeasonModal, newShowSeasonModal);

// (3) renderBlock에서 복음도 2열 독서 본문 마커 그리드 분리 대상에 포함
readerJs = readerJs.replace(
  "if(['제1독서','제2독서'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>{child.classList.add('reader__reading-body');const paragraphs=Array.from(child.querySelectorAll('.reader__speech-text'));child.replaceChildren();let paragraphBody=null;paragraphs.forEach(p=>{const match=p.textContent.match(/^(▥|\\d{1,3})\\s+/);if(match||!paragraphBody){const row=document.createElement('div');row.className='reader__speech-row'+(match?'':' reader__speech-row--unmarked');paragraphBody=document.createElement('div');paragraphBody.className='reader__speech-body';if(match){const marker=document.createElement('span');marker.className='reader__speech-marker';marker.textContent=match[1];row.append(marker);p.textContent=p.textContent.slice(match[0].length);}row.append(paragraphBody);child.append(row);}paragraphBody.append(p);});child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');});}",
  "if(['제1독서','제2독서','복음'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>{child.classList.add('reader__reading-body');const paragraphs=Array.from(child.querySelectorAll('.reader__speech-text'));child.replaceChildren();let paragraphBody=null;paragraphs.forEach(p=>{const match=p.textContent.match(/^(▥|✠|\\d{1,3})\\s+/);if(match||!paragraphBody){const row=document.createElement('div');row.className='reader__speech-row'+(match?'':' reader__speech-row--unmarked');paragraphBody=document.createElement('div');paragraphBody.className='reader__speech-body';if(match){const marker=document.createElement('span');marker.className='reader__speech-marker';marker.textContent=match[1];row.append(marker);p.textContent=p.textContent.slice(match[0].length);}row.append(paragraphBody);child.append(row);}paragraphBody.append(p);});child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');});}"
);

fs.writeFileSync(readerJsPath, readerJs, 'utf8');
console.log('2. prototype/source/reader.js 복음 2열 정렬 및 전례모달 정규화 적용 완료');

// 3. build.json 바인딩 경로 업데이트
const buildJsonPath = path.join(root, 'prototype', 'source', 'build.json');
let buildJson = fs.readFileSync(buildJsonPath, 'utf8');
buildJson = buildJson.replace(
  '"path": "data/reference-sources/hymn-schedule-202610.json"',
  '"path": "data/reference-sources/hymn-schedule-2026q4.json"'
);
fs.writeFileSync(buildJsonPath, buildJson, 'utf8');
console.log('3. prototype/source/build.json 통합 성가표 바인딩 업데이트 완료');
