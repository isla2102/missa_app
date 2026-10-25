const fs = require('fs');
const path = require('path');

const hwp10Path = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 10월 성가표(수정보완판).json');
const raw10 = JSON.parse(fs.readFileSync(hwp10Path, 'utf8'));
const p10 = raw10.paragraphs.map(p => p.text.trim()).filter(Boolean);

const idx = p10.findIndex(t => t.includes('18(일)'));
console.log('10월 18일 전후 문단:');
console.log(p10.slice(idx - 2, idx + 25));
