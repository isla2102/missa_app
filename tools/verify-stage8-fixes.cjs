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

    const pause = (ms = 300) => page.waitForTimeout(ms);

    await page.goto(pathToFileURL(path.resolve('prototype/index.html')).href);
    await pause();

    // 튜토리얼 닫기
    if (await page.locator('[data-js="tutorial"]').isVisible()) {
      await page.locator('[data-js="tutorial-later"]').click();
      await pause();
    }

    console.log('\n--- [1] 전례시기 모달 시스템 정규화 검증 ---');
    const seasonBodyClass = await page.locator('[data-js="season-modal-body"]').getAttribute('class');
    console.log('전례시기 모달 바디 class:', seasonBodyClass);
    if (!seasonBodyClass?.includes('overlay__body')) {
      throw new Error('전례시기 모달 바디에 overlay__body 클래스가 누락되었습니다.');
    }
    console.log('✅ PASS: 전례시기 모달 바디 overlay__body 적용 확인');

    await page.locator('[data-js="liturgical-season"]').click();
    await pause();

    const cardCount = await page.locator('[data-js="season-modal-body"] .reader__content-card').count();
    console.log('전례시기 카드 수:', cardCount);
    if (cardCount !== 6) throw new Error(`전례시기 카드 수가 6개가 아닙니다: ${cardCount}`);
    console.log('✅ PASS: 전례시기 카드 6개 생성 확인');

    const hasOverlayHeader = await page.locator('[data-js="season-modal-body"] .overlay__header').count();
    const hasItemTitle = await page.locator('[data-js="season-modal-body"] .reader__item-title').count();
    const hasItemText = await page.locator('[data-js="season-modal-body"] .reader__item-text').count();
    console.log(`overlay__header: ${hasOverlayHeader}, reader__item-title: ${hasItemTitle}, reader__item-text: ${hasItemText}`);
    if (hasOverlayHeader !== 6 || hasItemTitle !== 6 || hasItemText !== 6) {
      throw new Error('카드 내부 시스템 정규화 클래스(overlay__header, reader__item-title, reader__item-text) 불일치');
    }
    console.log('✅ PASS: 카드 내부 시스템 정규화 클래스 구조 확인');

    const currentCardCount = await page.locator('[data-js="season-modal-body"] [aria-current="true"]').count();
    if (currentCardCount < 1) throw new Error('현재 선택된 전례 시기 카드에 aria-current="true" 미적용');
    console.log('✅ PASS: 현재 선택된 전례 시기 aria-current="true" 적용 확인');

    await page.locator('[data-js="season-modal-close"]').click();
    await pause();

    console.log('\n--- [2] 복음 열 정렬 (1·2열 분리) 검증 ---');
    await page.locator('[data-js="part-next"]').click();
    await pause();
    await page.locator('[data-js="page-next"]').click();
    await pause();

    const gospelItem = page.locator('.reader__item--reading').filter({ hasText: '복음' });
    const isGospelReadingClass = await gospelItem.count() > 0;
    if (!isGospelReadingClass) throw new Error('복음 섹션에 reader__item--reading 클래스가 적용되지 않았습니다.');
    console.log('✅ PASS: 복음 섹션 reader__item--reading 클래스 적용 확인');

    const gospelSpeechRows = await page.locator('.reader__item--reading').filter({ hasText: '복음' }).locator('.reader__speech-row').count();
    console.log('복음 2열 그리드 행 수:', gospelSpeechRows);
    if (gospelSpeechRows < 5) throw new Error(`복음 그리드 행 수가 부족합니다: ${gospelSpeechRows}`);
    console.log('✅ PASS: 복음 절 번호 행별 분리 확인');

    const gospelMarkers = await page.locator('.reader__item--reading').filter({ hasText: '복음' }).locator('.reader__speech-marker').allTextContents();
    const validMarkers = gospelMarkers.filter(t => t.trim().length > 0);
    console.log('복음 마커 텍스트 샘플:', validMarkers.slice(0, 5));
    if (validMarkers.length < 3) throw new Error('복음 본문에서 절 번호 마커가 1열로 추출되지 않았습니다.');
    console.log('✅ PASS: 복음 절 번호가 1열 마커로 정확히 분리됨 확인');

    console.log('\n--- [3] 성가표 10월 및 11월 연결 검증 ---');
    const catalogDays = await page.evaluate(() => hymnScheduleCatalog?.days?.length);
    console.log('성가표 총 등록 일수:', catalogDays);
    if (catalogDays !== 61) throw new Error(`성가표 일수가 61일이 아닙니다: ${catalogDays}`);
    console.log('✅ PASS: 10월(31일) + 11월(30일) = 61일 성가표 연결 확인');

    // 11월 1일로 날짜 변경
    await page.evaluate(() => {
      const dateInput = document.querySelector('[data-js="date"]');
      dateInput.value = '2026-11-01';
      dateInput.dispatchEvent(new Event('change'));
    });
    await pause();

    // 성가 패널 열기
    await page.locator('button[data-panel="hymn"]').click();
    await pause();

    const hymnDrawerText = await page.locator('[data-js="drawer-body"]').textContent();
    console.log('11월 1일 성가 패널 텍스트 샘플:', hymnDrawerText.slice(0, 150).replace(/\s+/g, ' '));
    if (!hymnDrawerText.includes('38') || !hymnDrawerText.includes('238')) {
      throw new Error('11월 1일 성가 추천 번호(38, 238 등)가 성가 패널에 반영되지 않았습니다.');
    }
    console.log('✅ PASS: 11월 1일 성가 추천 번호(입당 38, 예물 238 등) 정상 노출 확인');

    // 성가 패널 닫기
    await page.locator('[data-js="close"]').click();
    await pause();

    // 12월 8일로 날짜 변경
    await page.evaluate(() => {
      const dateInput = document.querySelector('[data-js="date"]');
      dateInput.value = '2026-12-08';
      dateInput.dispatchEvent(new Event('change'));
    });
    await pause();

    // 성가 패널 다시 열기
    await page.locator('button[data-panel="hymn"]').click();
    await pause();

    const hymnDrawerDec = await page.locator('[data-js="drawer-body"]').textContent();
    console.log('12월 8일 성가 패널 텍스트:', hymnDrawerDec.replace(/\s+/g, ' '));
    if (!hymnDrawerDec.includes('선택 날짜 성가표 미등록')) {
      throw new Error('12월 날짜 선택 시 성가표 미등록 안내가 노출되지 않았습니다.');
    }
    console.log('✅ PASS: 12월 성가표 부재 시 "선택 날짜 성가표 미등록" 안내 정상 노출 확인');

    if (errors.length > 0) {
      throw new Error('브라우저 콘솔 오류 발생: ' + errors.join('; '));
    }
    console.log('✅ PASS: 브라우저 런타임 오류 0건 확인');

    console.log('\n🎉 [최종 결과] 전 항목 100% 검증 통과 (ALL PASS)');

  } finally {
    await browser.close();
  }
})();
