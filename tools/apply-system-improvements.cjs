const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// 1. build.json 수정
const buildJsonPath = path.join(root, 'prototype', 'source', 'build.json');
let buildJson = fs.readFileSync(buildJsonPath, 'utf8');
buildJson = buildJson.replace(
  '"path": "data/reference-sources/hymn-schedule-202610.json"',
  '"path": "data/reference-sources/hymn-schedule-2026q4.json"'
);
fs.writeFileSync(buildJsonPath, buildJson, 'utf8');
console.log('1. prototype/source/build.json 업데이트 완료');

// 2. reader.js 수정
const readerJsPath = path.join(root, 'prototype', 'source', 'reader.js');
let readerJs = fs.readFileSync(readerJsPath, 'utf8');

// (1) liturgyNode 기호에 ✠ 추가
readerJs = readerJs.replace(
  'const match=part.text.match(/^([+◎◆○●])\\s*/);',
  'const match=part.text.match(/^([+◎◆○●✠])\\s*/);'
);

// (2) renderBlock의 복음 2열 그리드 처리 확장
readerJs = readerJs.replace(
  "if(['제1독서','제2독서'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>{child.classList.add('reader__reading-body');const paragraphs=Array.from(child.querySelectorAll('.reader__speech-text'));child.replaceChildren();let paragraphBody=null;paragraphs.forEach(p=>{const match=p.textContent.match(/^(▥|\\d{1,3})\\s+/);if(match||!paragraphBody){const row=document.createElement('div');row.className='reader__speech-row'+(match?'':' reader__speech-row--unmarked');paragraphBody=document.createElement('div');paragraphBody.className='reader__speech-body';if(match){const marker=document.createElement('span');marker.className='reader__speech-marker';marker.textContent=match[1];row.append(marker);p.textContent=p.textContent.slice(match[0].length);}row.append(paragraphBody);child.append(row);}paragraphBody.append(p);});child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');});}",
  "if(['제1독서','제2독서','복음'].includes(block.item?.title)){node.classList.add('reader__item--reading');node.querySelector('.reader__content-card')?.classList.add('reader__reading-content');const lit=node.querySelector('.reader__liturgy');lit?.classList.add('reader__reading-liturgy');Array.from(lit?.children||[]).filter(child=>child.getAttribute('data-speech-role')==='text').forEach(child=>{child.classList.add('reader__reading-body');const paragraphs=Array.from(child.querySelectorAll('.reader__speech-text'));child.replaceChildren();let paragraphBody=null;paragraphs.forEach(p=>{const match=p.textContent.match(/^(▥|✠|\\d{1,3})\\s+/);if(match||!paragraphBody){const row=document.createElement('div');row.className='reader__speech-row'+(match?'':' reader__speech-row--unmarked');paragraphBody=document.createElement('div');paragraphBody.className='reader__speech-body';if(match){const marker=document.createElement('span');marker.className='reader__speech-marker';marker.textContent=match[1];row.append(marker);p.textContent=p.textContent.slice(match[0].length);}row.append(paragraphBody);child.append(row);}paragraphBody.append(p);});child.setAttribute('tabindex','0');child.setAttribute('aria-label',block.item.title+' 본문 스크롤');});}"
);

fs.writeFileSync(readerJsPath, readerJs, 'utf8');
console.log('2. prototype/source/reader.js 업데이트 완료');

// 3. reader.css 수정
const readerCssPath = path.join(root, 'prototype', 'source', 'reader.css');
let readerCss = fs.readFileSync(readerCssPath, 'utf8');

const seasonCss = `
.reader__season-period { margin-block: var(--reader-system-space-3); padding: var(--reader-system-space-3); border: var(--reader-card-border-width) solid var(--reader-card-border-color); border-radius: var(--reader-radius); background: var(--reader-theme-surface); }
.reader__season-period[aria-current="true"] { border-color: var(--reader-theme-accent); background: var(--state-selected-surface); }
.reader__season-period h3 { font-size: var(--reader-system-type-ui); margin: 0; color: var(--reader-theme-ink); }
.reader__season-period[aria-current="true"] h3 { color: var(--reader-theme-accent); }
.reader__season-period p { font-size: var(--reader-system-type-note); line-height: var(--reader-system-leading-body); color: var(--reader-theme-muted); margin-block-start: var(--reader-system-space-1); }
`;

if (!readerCss.includes('.reader__season-period')) {
  readerCss += seasonCss;
  fs.writeFileSync(readerCssPath, readerCss, 'utf8');
  console.log('3. prototype/source/reader.css 전례시기 모달 토큰 스타일 추가 완료');
} else {
  console.log('3. prototype/source/reader.css 이미 존재');
}
