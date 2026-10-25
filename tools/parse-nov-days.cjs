const fs = require('fs');
const path = require('path');

const hwpJsonPath = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 11월 성가표(수정보완판).json');
const raw = JSON.parse(fs.readFileSync(hwpJsonPath, 'utf8'));

// stream과 recordOffset 확인
console.log('문단 샘플:');
console.log(raw.paragraphs.slice(5, 20));
