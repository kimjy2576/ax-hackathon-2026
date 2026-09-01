const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2000, height: 1200 }, deviceScaleFactor: 1 });
  await page.goto('file:///home/claude/AX_구조도_와이드상세.html');
  await page.waitForTimeout(1200);
  for (const [id, name] of [['c1','EXACYCLE_구조도_와이드상세'], ['c2','CYCLE-Master_구조도_와이드상세']]) {
    const el = await page.$('#'+id);
    await el.screenshot({ path: name + '.jpg', type: 'jpeg', quality: 92 });
  }
  await browser.close(); console.log('done');
})();
