const fs = require('fs');
const path = require('path');

const hwpJsonPath = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 11월 성가표(수정보완판).json');
const raw = JSON.parse(fs.readFileSync(hwpJsonPath, 'utf8'));

const paragraphs = raw.paragraphs.map(p => p.text.trim()).filter(Boolean);
console.log('총 문단 수:', paragraphs.length);
console.log('앞부분 30개 문단:');
console.log(paragraphs.slice(0, 30));
