const fs = require('fs');
const path = require('path');

const hwpJsonPath = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 11월 성가표(수정보완판).json');
const raw = JSON.parse(fs.readFileSync(hwpJsonPath, 'utf8'));

const paragraphs = raw.paragraphs.map(p => p.text.trim()).filter(Boolean);

// '1(일)', '2(월)', ... 패턴 찾기
const dayPattern = /^(\d{1,2})\(([일월화수목금토])\)$/;

const days = [];
let currentDay = null;

for (let i = 0; i < paragraphs.length; i++) {
  const text = paragraphs[i];
  const m = text.match(dayPattern);
  if (m) {
    if (currentDay) {
      days.push(currentDay);
    }
    const dayNum = parseInt(m[1], 10);
    const dateStr = `2026-11-${String(dayNum).padStart(2, '0')}`;
    const observance = paragraphs[i + 1] || '';
    currentDay = {
      date: dateStr,
      observance,
      rawNumbers: []
    };
    i++; // observance 건너뜀
    continue;
  }
  if (currentDay && /^\d+$/.test(text)) {
    currentDay.rawNumbers.push(parseInt(text, 10));
  }
}
if (currentDay) {
  days.push(currentDay);
}

console.log('추출된 일수:', days.length);
days.forEach(d => {
  console.log(`${d.date} (${d.observance}): [${d.rawNumbers.join(', ')}] (개수: ${d.rawNumbers.length})`);
});
