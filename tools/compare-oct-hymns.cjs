const fs = require('fs');
const path = require('path');

const hwp10Path = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 10월 성가표(수정보완판).json');
const raw10 = JSON.parse(fs.readFileSync(hwp10Path, 'utf8'));
const p10 = raw10.paragraphs.map(p => p.text.trim()).filter(Boolean);

console.log('10월 첫 40문단:');
console.log(p10.slice(0, 40));
