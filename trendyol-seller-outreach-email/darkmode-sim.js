/* darkmode-sim.js — approximate what Gmail's dark mode does to the merged sample:
   light backgrounds become dark, dark text becomes light, images are left alone.
   Run after render.js:  NODE_PATH=/opt/node22/lib/node_modules node darkmode-sim.js */
'use strict';
const fs = require('fs'); const path = require('path'); const { chromium } = require('playwright');
const ROOT = __dirname, OUT = path.join(ROOT, 'output');
const MAP = { '#F2F2F2':'#111111', '#FFFFFF':'#1F1F1F', '#FAFAFA':'#1A1A1A', '#FFF3EC':'#2A1F18', '#E6E6E6':'#3A3A3A',
              '#434343':'#D6D6D6', '#181818':'#F0F0F0', '#7A7A7A':'#A8A8A8', '#9A9A9A':'#8A8A8A' };
(async () => {
  let html = fs.readFileSync(path.join(OUT, 'email-okwan-sample.html'), 'utf8');
  html = html.replace(/^[ \t]*<link[^>]*fonts\.googleapis\.com[^>]*>\s*\n/gm, '');
  const fonts = fs.readFileSync(path.join(ROOT, 'assets/fonts/local-fonts.css'), 'utf8')
    .replace(/url\(([^)]+)\)/g, (m, f) => `url(file://${path.join(ROOT, 'assets/fonts', f.replace(/['"]/g, ''))})`);
  html = html.replace('</head>', `<style>${fonts}</style></head>`);
  for (const [from, to] of Object.entries(MAP)) html = html.split(from).join(to);
  html = html.replace(/src="assets\//g, `src="file://${path.join(ROOT, 'assets')}/`);
  const tmp = path.join(OUT, '.dark-tmp.html'); fs.writeFileSync(tmp, html);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage(); await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, 'trendyol-seller-email-phone-darkmode-sim.png'), fullPage: true });
  await browser.close(); fs.unlinkSync(tmp);
  console.log('dark-mode simulation written to output/trendyol-seller-email-phone-darkmode-sim.png');
})();
