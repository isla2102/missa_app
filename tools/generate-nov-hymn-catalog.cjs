const fs = require('fs');
const path = require('path');

const hwpJsonPath = path.join(__dirname, '..', 'data', 'source-library', 'extracted-hwp', '2026년 11월 성가표(수정보완판).json');
const raw = JSON.parse(fs.readFileSync(hwpJsonPath, 'utf8'));

const paragraphs = raw.paragraphs.map(p => p.text.trim()).filter(Boolean);
const dayPattern = /^(\d{1,2})\(([일월화수목금토])\)$/;

const days = [];
let i = 0;

while (i < paragraphs.length) {
  const text = paragraphs[i];
  const m = text.match(dayPattern);
  if (!m) {
    i++;
    continue;
  }

  const dayNum = parseInt(m[1], 10);
  const dateStr = `2026-11-${String(dayNum).padStart(2, '0')}`;
  const observance = paragraphs[i + 1] || '';
  i += 2;

  // 다음 날짜가 나오기 전까지의 번호 또는 텍스트 수집
  const items = [];
  while (i < paragraphs.length && !paragraphs[i].match(dayPattern)) {
    items.push(paragraphs[i]);
    i++;
  }

  // 성가 번호 추출
  if (dayNum === 22) {
    // 11월 22일 그리스도왕 대축일: 교중 + 일반
    days.push({
      date: dateStr,
      observance: "온 누리의 임금이신 우리 주 예수 그리스도왕 대축일(교중)",
      recommendations: {
        entrance: [79, 78],
        offertory: [239, 514],
        communion: [171, 496, 498],
        recessional: [75]
      }
    });
  } else {
    const nums = items.filter(t => /^\d+$/.test(t)).map(Number);
    let recommendations;
    if (nums.length === 5) {
      recommendations = {
        entrance: [nums[0]],
        offertory: [nums[1]],
        communion: [nums[2], nums[3]],
        recessional: [nums[4]]
      };
    } else if (nums.length === 7) {
      recommendations = {
        entrance: [nums[0]],
        offertory: [nums[1], nums[2]],
        communion: [nums[3], nums[4], nums[5]],
        recessional: [nums[6]]
      };
    } else {
      console.warn(`경고: ${dateStr} 성가 개수 특이: ${nums.length}`);
      recommendations = {
        entrance: nums.slice(0, 1),
        offertory: nums.slice(1, 2),
        communion: nums.slice(2, nums.length - 1),
        recessional: nums.slice(-1)
      };
    }

    days.push({
      date: dateStr,
      observance,
      recommendations
    });
  }
}

const catalog = {
  month: "2026-11",
  edition: "수정보완판",
  sourceFilename: "2026년 11월 성가표(수정보완판).hwp",
  sha256: raw.sha256,
  sourceUrl: "https://bbs.catholic.or.kr/pdsm/bbs_view.asp?id=212615&menu=4807",
  status: "recommendation-not-parish-confirmed",
  slotAssignments: null,
  days
};

const outPath = path.join(__dirname, '..', 'data', 'reference-sources', 'hymn-schedule-202611.json');
fs.writeFileSync(outPath, JSON.stringify(catalog, null, 2), 'utf8');
console.log(`성공: ${catalog.days.length}일 생성 완료 -> ${outPath}`);
