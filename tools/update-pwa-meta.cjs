const fs = require('fs');
const path = require('path');

const shellPath = path.join(__dirname, '..', 'prototype', 'source', 'shell.html');
let html = fs.readFileSync(shellPath, 'utf8');

const targetMeta = `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#70283F">`;

const replaceMeta = `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="매일미사">
<meta name="theme-color" content="#70283F">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<link rel="manifest" href="./manifest.webmanifest">`;

html = html.replace(targetMeta, replaceMeta);
fs.writeFileSync(shellPath, html, 'utf8');
console.log('✅ prototype/source/shell.html PWA 아이콘 및 타이틀 메타태그 추가 완료');
