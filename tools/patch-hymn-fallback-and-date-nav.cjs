const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// 1. prototype/source/reader.js 수정
const readerJsPath = path.join(root, 'prototype', 'source', 'reader.js');
let readerJs = fs.readFileSync(readerJsPath, 'utf8');

// (1) currentHymns()에 성가표 추천 번호 자동 fallback 추가
const oldCurrentHymns = `function currentHymns(){try{return readHymnSet(localStorage,find('date').value,find('slot').value);}catch{return cleanHymnSet(null);}}`;

const newCurrentHymns = `function defaultHymnsForDate(date=find('date').value){
 const day=hymnScheduleCatalog?.days?.find(d=>d.date===date);
 if(!day?.recommendations)return cleanHymnSet(null);
 return {
  entrance:day.recommendations.entrance?[...day.recommendations.entrance]:[],
  offertory:day.recommendations.offertory?[...day.recommendations.offertory]:[],
  communion:day.recommendations.communion?[...day.recommendations.communion]:[],
  recessional:day.recommendations.recessional?[...day.recommendations.recessional]:[]
 };
}
function currentHymns(){
 try{
  const saved=readHymnSet(localStorage,find('date').value,find('slot').value);
  const hasAny=hymnRoles.some(role=>saved[role]?.length>0);
  if(hasAny)return saved;
 }catch{}
 return defaultHymnsForDate(find('date').value);
}`;

readerJs = readerJs.replace(oldCurrentHymns, newCurrentHymns);

// (2) URL 쿼리 파라미터 date 지원
const oldDateInit = `try{const saved=localStorage.getItem('missa.reader.selected-date.v1');if(/^\\d{4}-\\d{2}-\\d{2}$/.test(saved||'')){const field=find('date'),fallback=field.value;field.value=saved;if(!field.value)field.value=fallback;}}catch{}`;

const newDateInit = `const urlDateParam=new URLSearchParams(location.search).get('date');
if(/^\\d{4}-\\d{2}-\\d{2}$/.test(urlDateParam||'')){
 find('date').value=urlDateParam;
}else{
 try{const saved=localStorage.getItem('missa.reader.selected-date.v1');if(/^\\d{4}-\\d{2}-\\d{2}$/.test(saved||'')){const field=find('date'),fallback=field.value;field.value=saved;if(!field.value)field.value=fallback;}}catch{}
}`;

readerJs = readerJs.replace(oldDateInit, newDateInit);

// (3) postMessage 리스너에 missa-set-date 핸들러 추가
const oldPostMessage = `if(parent!==window){window.addEventListener('message',event=>{if(event.source!==parent)return;`;
const newPostMessage = `if(parent!==window){window.addEventListener('message',event=>{if(event.source!==parent)return;
if(event.data?.type==='missa-set-date'&&/^\\d{4}-\\d{2}-\\d{2}$/.test(event.data.date)){
 find('date').value=event.data.date;
 find('date').dispatchEvent(new Event('change'));
 return;
}`;

readerJs = readerJs.replace(oldPostMessage, newPostMessage);
fs.writeFileSync(readerJsPath, readerJs, 'utf8');
console.log('✅ prototype/source/reader.js 성가 추천 fallback 및 날짜 연동 수정 완료');

// 2. prototype/source/shell.html에 태블릿 PWA 및 뷰포트 메타태그 추가
const shellPath = path.join(root, 'prototype', 'source', 'shell.html');
let shellHtml = fs.readFileSync(shellPath, 'utf8');
if (!shellHtml.includes('mobile-web-app-capable')) {
  shellHtml = shellHtml.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#70283F">`
  );
  fs.writeFileSync(shellPath, shellHtml, 'utf8');
  console.log('✅ prototype/source/shell.html 태블릿 PWA 메타태그 추가 완료');
}

// 3. review/08-integration-v1.html 수정
const reviewPath = path.join(root, 'review', '08-integration-v1.html');
let reviewHtml = fs.readFileSync(reviewPath, 'utf8');

const oldIframeClick = `        try {
          const frameDoc = appFrame.contentDocument || appFrame.contentWindow.document;
          const dateInput = frameDoc.querySelector('[data-js="date"]');
          if (dateInput) {
            dateInput.value = targetDate;
            dateInput.dispatchEvent(new Event('change'));
          }
        } catch (e) {
          console.warn('Frame interaction failed, falling back to reload parameter:', e);
        }`;

const newIframeClick = `        // 1. postMessage 전송 (안전한 교차 출처 및 file:// 지원)
        try {
          appFrame.contentWindow.postMessage({ type: 'missa-set-date', date: targetDate }, '*');
        } catch (e) {}

        // 2. iframe src 쿼리 파라미터 갱신 (확실한 리로드 및 날짜 보장)
        appFrame.src = '../prototype/index.html?date=' + targetDate;

        // 3. 동일 출처일 때 DOM 직접 조작 시도 (fallback)
        try {
          const frameDoc = appFrame.contentDocument || appFrame.contentWindow.document;
          const dateInput = frameDoc?.querySelector('[data-js="date"]');
          if (dateInput) {
            dateInput.value = targetDate;
            dateInput.dispatchEvent(new Event('change'));
          }
        } catch (e) {}`;

reviewHtml = reviewHtml.replace(oldIframeClick, newIframeClick);
fs.writeFileSync(reviewPath, reviewHtml, 'utf8');
console.log('✅ review/08-integration-v1.html 대표일 전환 스크립트 수정 완료');
