const fs = require('fs');
const path = require('path');

const octPath = path.join(__dirname, '..', 'data', 'reference-sources', 'hymn-schedule-202610.json');
const novPath = path.join(__dirname, '..', 'data', 'reference-sources', 'hymn-schedule-202611.json');

const oct = JSON.parse(fs.readFileSync(octPath, 'utf8'));
const nov = JSON.parse(fs.readFileSync(novPath, 'utf8'));

const combined = {
  month: "2026-10~2026-11",
  edition: "수정보완판",
  sourceFilename: "2026년 10월·11월 성가표(수정보완판).hwp",
  sourceUrl: "https://bbs.catholic.or.kr/pdsm/bbs_view.asp?id=212615&menu=4807",
  status: "recommendation-not-parish-confirmed",
  slotAssignments: null,
  days: [...oct.days, ...nov.days]
};

const outPath = path.join(__dirname, '..', 'data', 'reference-sources', 'hymn-schedule-2026q4.json');
fs.writeFileSync(outPath, JSON.stringify(combined, null, 2), 'utf8');
console.log(`성공: 총 ${combined.days.length}일치 성가표 통합 완료 -> ${outPath}`);
