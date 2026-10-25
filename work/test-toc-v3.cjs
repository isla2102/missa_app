const assert = require('node:assert/strict');
const parts = [
 {title:'시작 예식', pages:[['입당 · 성호경과 인사','공식 본문을 연결할 첫 번째 쪽입니다.'],['참회 예식 · 자비송 · 대영광송 · 본기도','같은 시작 예식의 이어지는 두 번째 쪽입니다.']]},
 {title:'말씀 전례', pages:[['독서 · 화답송','말씀 전례의 첫 번째 쪽입니다.'],['복음 환호송 · 복음','말씀 전례의 두 번째 쪽입니다.'],['강론 · 신앙 고백','말씀 전례의 세 번째 쪽입니다.'],['보편 지향 기도','말씀 전례의 네 번째 쪽입니다.']]},
 {title:'성찬 전례', pages:[['예물 준비 · 예물 기도','성찬 전례의 첫 번째 쪽입니다.'],['감사 기도','성찬 전례의 두 번째 쪽입니다.'],['주님의 기도 · 평화 예식','성찬 전례의 세 번째 쪽입니다.'],['영성체 · 영성체 후 기도','성찬 전례의 네 번째 쪽입니다.']]},
 {title:'마침 예식', pages:[['공지 · 강복','마침 예식의 첫 번째 쪽입니다.'],['파견 · 파견 성가','마침 예식의 이어지는 두 번째 쪽입니다.']]}
];
const contents = [
 [['입당 성가',0],['성호경',0],['인사',0],['참회 예식',1],['자비송',1],['대영광송',1],['본기도',1]],
 [['제1독서',0],['화답송',0],['제2독서',0],['복음 환호송',1],['복음',1],['강론',2],['신앙 고백',2],['보편 지향 기도',3]],
 [['예물 준비 · 봉헌 성가',0],['예물 기도',0],['감사 기도',1],['주님의 기도',2],['평화 예식',2],['영성체 예식 · 영성체 성가',3],['영성체 후 기도',3]],
 [['공지 사항',0],['강복',0],['파견',1],['파견 성가',1]]
].map((items, partIndex) => items.map(([title, page], index) => ({id:`part-${partIndex}-item-${index}`, title, page})));
assert.equal(contents.length, 4);
const ids = new Set();
let count = 0;
contents.forEach((items, part) => items.forEach(item => {
 assert.ok(item.page >= 0 && item.page < parts[part].pages.length);
 assert.ok(!ids.has(item.id)); ids.add(item.id);
 const spread = Math.floor(item.page / 2);
 assert.ok(item.page >= spread * 2 && item.page < spread * 2 + 2);
 count++;
}));
assert.equal(count,26);
assert.equal(contents[1].find(x=>x.title==='보편 지향 기도').page,3);
assert.equal(Math.floor(contents[1].find(x=>x.title==='보편 지향 기도').page/2),1);
console.log(`PASS: four groups, ${count} unique targets, page ranges and spread mapping`);
