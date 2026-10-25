const fs = require('fs');
const path = require('path');

const hwpJsonPath = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 11월 성가표(수정보완판).json');
const raw = JSON.parse(fs.readFileSync(hwpJsonPath, 'utf8'));

const paragraphs = raw.paragraphs.map(p => p.text.trim()).filter(Boolean);
const idx = paragraphs.findIndex(t => t.includes('22(일)'));
console.log('11월 22일 전후 문단:');
console.log(paragraphs.slice(idx - 2, idx + 25));
