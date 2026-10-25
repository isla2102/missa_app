const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
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

    const checks = [];
    const ok = (val, label) => checks.push({ label, pass: Boolean(val) });
    const pause = (ms = 250) => page.waitForTimeout(ms);

    // 1. review/08-integration-v1.html 검토 화면 로드 확인
    await page.goto(pathToFileURL(path.resolve('review/08-integration-v1.html')).href);
    await pause();
    ok(await page.locator('h1').textContent().then(t => t.includes('8단계 · 날짜별 자료 연결 및 통합 시각 검수')), 'review HTML loads with header');
    ok(await page.locator('.date-btn').count() === 6, 'review HTML has 6 date switch buttons');

    // 2. prototype/index.html 직접 테스트
    await page.goto(pathToFileURL(path.resolve('prototype/index.html')).href);
    await pause(300);
    if (await page.locator('[data-js="tutorial"]').isVisible()) {
      await page.locator('[data-js="tutorial-later"]').click();
      await pause();
    }

    const testDates = [
      {
        date: '2026-10-18',
        season: '연중',
        gloria: true,
        creed: true,
        reading2: true,
        prefaceKeyword: '저희는 주님 안에서 숨 쉬고 움직이며 살아가오니',
        intercessionType: 'present',
        screenshot: 'work/browser-qa/stage8-ordinary-20261018.png'
      },
      {
        date: '2026-10-24',
        season: '연중',
        gloria: false,
        creed: false,
        reading2: false,
        prefaceKeyword: '사랑하시는 성자 예수 그리스도를 통하여',
        intercessionType: 'missing',
        screenshot: null
      },
      {
        date: '2026-11-01',
        season: '연중',
        gloria: true,
        creed: true,
        reading2: true,
        prefaceKeyword: '아버지께서 오늘 저희 어머니인 천상 도읍 예루살렘을 보여 주시니',
        intercessionType: 'present',
        screenshot: null
      },
      {
        date: '2026-11-29',
        season: '대림',
        gloria: false,
        creed: true,
        reading2: true,
        prefaceKeyword: '선택 날짜 감사송 전문 미연결',
        intercessionType: 'present',
        screenshot: 'work/browser-qa/stage8-advent-20261129.png'
      },
      {
        date: '2026-12-08',
        season: '대림',
        gloria: true,
        creed: true,
        reading2: true,
        prefaceKeyword: '복되신 동정 마리아를 원죄에 물들지 않게 지켜 주시고',
        intercessionType: 'missing',
        screenshot: null
      },
      {
        date: '2026-12-25',
        season: '성탄',
        gloria: true,
        creed: true,
        reading2: true,
        prefaceKeyword: '선택 날짜 감사송 전문 미연결',
        intercessionType: 'guidance_only',
        screenshot: 'work/browser-qa/stage8-christmas-20261225.png'
      }
    ];

    for (const item of testDates) {
      await page.locator('[data-js="date"]').fill(item.date);
      await page.locator('[data-js="date"]').dispatchEvent('change');
      await pause(300);

      const dayCheck = await page.evaluate((target) => {
        const season = find('liturgical-season')?.textContent || '';
        const dayLabel = find('liturgical-day')?.textContent || '';
        const tocLinks = Array.from(document.querySelectorAll('.reader__toc-link')).map(n => n.textContent);
        
        const blocks2 = flowBlocks(2);
        const prefaceBlock = blocks2.find(b => b.displayText && b.item?.title === '감사기도 제2양식');
        const prefaceText = prefaceBlock?.displayText || '';

        const intercessionItem = contents[1].find(i => i.title === '보편 지향 기도');
        const intercessionBlocks = universalPrayerBlocks(intercessionItem);
        const petitionsCount = intercessionBlocks.filter(b => b.group === '보편 지향 기도 지향').length;
        const missingNotice = intercessionBlocks.length === 1 && intercessionBlocks[0].group === '보편 지향 기도 미수록';
        const missingText = intercessionBlocks[0]?.variant?.text || '';

        return {
          season,
          dayLabel,
          hasGloria: tocLinks.includes('대영광송'),
          hasCreed: tocLinks.includes('신앙 고백'),
          hasReading2: tocLinks.includes('제2독서'),
          prefaceText,
          hasDuplicateSanctus: prefaceText.includes('◎ 거룩하시도다!'),
          petitionsCount,
          missingNotice,
          missingText
        };
      }, item);

      ok(dayCheck.season.includes(item.season), `${item.date} season matches (${item.season})`);
      ok(dayCheck.hasGloria === item.gloria, `${item.date} Gloria TOC matches (${item.gloria})`);
      ok(dayCheck.hasCreed === item.creed, `${item.date} Creed TOC matches (${item.creed})`);
      ok(dayCheck.hasReading2 === item.reading2, `${item.date} Reading 2 TOC matches (${item.reading2})`);
      ok(dayCheck.prefaceText.includes(item.prefaceKeyword), `${item.date} preface contains keyword`);
      ok(!dayCheck.hasDuplicateSanctus, `${item.date} no duplicate Sanctus`);

      if (item.intercessionType === 'present') {
        ok(dayCheck.petitionsCount === 4, `${item.date} has 4 petitions (actual: ${dayCheck.petitionsCount})`);
      } else if (item.intercessionType === 'guidance_only') {
        ok(dayCheck.missingNotice && dayCheck.missingText.includes('공동체가 기도를 준비하라는 안내'), `${item.date} guidance only notice`);
      } else {
        ok(dayCheck.missingNotice && dayCheck.missingText.includes('수록되어 있지 않습니다'), `${item.date} missing notice`);
      }

      if (item.screenshot) {
        await page.screenshot({ path: item.screenshot, fullPage: true });
      }
    }

    // 본당 악보 자산 카탈로그 보존 검사
    const parishScoresOk = await page.evaluate(() => {
      const mainChants = ['자비송', '대영광송', '거룩하시도다', '신앙의 신비여', '아멘', '주님의 기도', '하느님의 어린양'];
      return mainChants.every(title => Boolean(scoreSourceCatalog?.[title]));
    });
    ok(parishScoresOk, 'Parish reengraved scores catalog is intact');

    const result = {
      timestamp: new Date().toISOString(),
      viewport: '1024x768',
      checks,
      failures: checks.filter(c => !c.pass),
      errors
    };

    fs.writeFileSync('work/browser-qa/stage8-integration.json', JSON.stringify(result, null, 2));
    console.log(JSON.stringify({ total: checks.length, failures: result.failures.length, errors: errors.length }));

    assert.equal(errors.length, 0, 'Browser error count must be 0');
    assert.equal(result.failures.length, 0, 'All checks must pass');
  } finally {
    await browser.close();
  }
})().catch(e => {
  console.error(e);
  process.exitCode = 1;
});
