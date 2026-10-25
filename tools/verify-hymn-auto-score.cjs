const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('C:/Users/imsup/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true
  });

  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 768 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));

    const pause = (ms = 400) => page.waitForTimeout(ms);

    console.log('\n--- [1] review/08-integration-v1.html 대표일 전환 검증 ---');
    await page.goto(pathToFileURL(path.resolve('review/08-integration-v1.html')).href);
    await pause();

    const appFrame = page.frameLocator('#app-frame');

    // 11월 1일 버튼 클릭
    console.log('11월 1일 대표일 버튼 클릭...');
    await page.locator('button[data-date="2026-11-01"]').click();
    await pause(600);

    const frameDate = await appFrame.locator('[data-js="date"]').inputValue();
    console.log('iframe 내부 날짜 값:', frameDate);
    if (frameDate !== '2026-11-01') {
      throw new Error(`대표일 전환 실패: 기대값 2026-11-01, 실제값 ${frameDate}`);
    }
    console.log('✅ PASS: 대표일 전환 버튼 클릭 시 iframe 내부 날짜 즉시 2026-11-01로 전환 확인');

    console.log('\n--- [2] 성가 추천번호가 있을 때 본문 악보 자동 노출 검증 ---');
    // 11월 1일 시작 예식의 '입당 성가' 확인
    const entranceInput = await appFrame.locator('#hymn-number-entrance').inputValue();
    console.log('11월 1일 입당 성가 입력창 값:', entranceInput);
    if (!entranceInput.includes('38')) {
      throw new Error(`11월 1일 입당 성가 추천 번호(38)가 입력창에 기본 채워지지 않았습니다: ${entranceInput}`);
    }
    console.log('✅ PASS: 11월 1일 입당 성가 입력창에 추천 번호(38) 자동 반영 확인');

    const entranceImg = await appFrame.locator('[data-flow-key="part-0-item-0"] img.reader__score-photo').count();
    console.log('11월 1일 입당 성가 본문 악보 이미지 수:', entranceImg);
    if (entranceImg < 1) {
      throw new Error('성가표 추천 번호가 있음에도 입당 성가 악보가 바로 노출되지 않았습니다.');
    }
    const entranceImgSrc = await appFrame.locator('[data-flow-key="part-0-item-0"] img.reader__score-photo').first().getAttribute('src');
    console.log('악보 이미지 URL:', entranceImgSrc);
    if (!entranceImgSrc?.includes('0038.jpg')) {
      throw new Error(`38번 악보 이미지가 로드되지 않았습니다: ${entranceImgSrc}`);
    }
    console.log('✅ PASS: 성가 추천번호(38번) 악보 이미지가 본문에 즉시 자동 렌더링됨 확인');

    // 10월 18일(전교주일)로 전환
    console.log('\n10월 18일 대표일 버튼 클릭...');
    await page.locator('button[data-date="2026-10-18"]').click();
    await pause(600);

    const frameDate2 = await appFrame.locator('[data-js="date"]').inputValue();
    console.log('iframe 내부 날짜 값:', frameDate2);
    if (frameDate2 !== '2026-10-18') {
      throw new Error(`대표일 전환 실패: 기대값 2026-10-18, 실제값 ${frameDate2}`);
    }

    const entranceInput2 = await appFrame.locator('#hymn-number-entrance').inputValue();
    console.log('10월 18일 입당 성가 입력창 값:', entranceInput2);
    if (!entranceInput2.includes('416')) {
      throw new Error(`10월 18일 입당 성가 추천 번호(416)가 기본 채워지지 않았습니다: ${entranceInput2}`);
    }

    const entranceImg2 = await appFrame.locator('[data-flow-key="part-0-item-0"] img.reader__score-photo').count();
    console.log('10월 18일 입당 성가 본문 악보 이미지 수:', entranceImg2);
    if (entranceImg2 < 1) {
      throw new Error('10월 18일 입당 성가 악보가 바로 노출되지 않았습니다.');
    }
    console.log('✅ PASS: 10월 18일 성가 추천번호(416번) 악보 이미지 본문 자동 노출 확인');

    console.log('\n🎉 전 항목 검증 성공!');

  } finally {
    await browser.close();
  }
})();
