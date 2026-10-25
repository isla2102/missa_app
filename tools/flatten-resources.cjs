const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

function flattenDir(parentRel, subRel) {
  const sub = path.join(root, parentRel, subRel);
  if (!fs.existsSync(sub) || !fs.statSync(sub).isDirectory()) return;

  const parent = path.join(root, parentRel);
  fs.readdirSync(sub).forEach(file => {
    const src = path.join(sub, file);
    const dest = path.join(parent, file);
    if (!fs.existsSync(dest)) {
      fs.renameSync(src, dest);
    }
  });
  // 빈 폴더 제거
  try {
    fs.rmdirSync(sub);
    console.log(`중첩 폴더 정리 완료: ${path.relative(root, sub)}`);
  } catch (e) {
    console.warn(`폴더 삭제 불가(파일 잔여): ${sub}`);
  }
}

flattenDir('resources/roman-missal', '로마미사경본');
flattenDir('resources/daily-propers', '매일미사고유기도문');
flattenDir('resources/hymn-schedules', '굿뉴스성가번호표');
flattenDir('resources/catholic-enc-scores', '가톨릭성가');

console.log('✅ 리소스 폴더 중첩 해제 완료');
