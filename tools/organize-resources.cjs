const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// 대상 디렉토리 구조 정의
const dirs = {
  missal: path.join(root, 'resources', 'roman-missal'),
  propers: path.join(root, 'resources', 'daily-propers'),
  hymnSchedules: path.join(root, 'resources', 'hymn-schedules'),
  encScores: path.join(root, 'resources', 'catholic-enc-scores'),
  legacySpecs: path.join(root, 'resources', 'legacy-v0.2-specs')
};

// 디렉토리 생성
Object.values(dirs).forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

function moveSafe(srcName, targetDir) {
  const src = path.join(root, srcName);
  if (!fs.existsSync(src)) return;

  const target = path.join(targetDir, srcName);
  // 만약 대상이 이미 존재하지 않으면 이동
  if (fs.existsSync(target)) {
    console.log(`대상 경로에 이미 존재: ${srcName}`);
    return;
  }

  try {
    fs.renameSync(src, target);
    console.log(`이동 완료: ${srcName} -> ${path.relative(root, target)}`);
  } catch (err) {
    // 디렉토리 간 이동 실패 시 복사 후 삭제
    console.warn(`이동 실패, 복사 방식으로 진행: ${srcName}`);
    copyRecursiveSync(src, target);
    fs.rmSync(src, { recursive: true, force: true });
    console.log(`복사 및 이동 완료: ${srcName} -> ${path.relative(root, target)}`);
  }
}

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach(childItemName => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

// 1. 로마미사경본 PDF 및 docx 이동
moveSafe('로마미사경본', dirs.missal);
moveSafe('미사통상문_서울대교구.docx', dirs.missal);
moveSafe('미사통상문_한국천주교주교회의.docx', dirs.missal);

// 2. 매일미사 고유기도문 HWP 이동
moveSafe('매일미사고유기도문', dirs.propers);

// 3. 굿뉴스 성가표 HWP 이동
moveSafe('굿뉴스성가번호표', dirs.hymnSchedules);

// 4. 가톨릭성가 ENC 이동
moveSafe('가톨릭성가', dirs.encScores);

// 5. 초기 v0.2 설계 문서 이동
moveSafe('개발_및_데이터연동_설계_v0.2.md', dirs.legacySpecs);
moveSafe('데이터_정규화_스키마_v0.2.json', dirs.legacySpecs);

console.log('\n🎉 모든 원본 리소스가 resources/ 하위 체계적 폴더로 정리 완료되었습니다.');
