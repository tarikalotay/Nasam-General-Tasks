/* eslint-disable no-console */
/**
 * render.js — merge sample data into email.html and render phone + desktop PNGs.
 *
 * Run:  NODE_PATH=/opt/node22/lib/node_modules node render.js
 *
 * Outputs (see DESIGN.md section 6):
 *   output/email-okwan-sample.html
 *   output/trendyol-seller-email-phone.png     (390x844, dsf 2, full page)
 *   output/trendyol-seller-email-desktop.png   (960x800, dsf 2, full page)
 *   output/render-report.json
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = __dirname;
const OUT_DIR = path.join(ROOT, 'output');
const ASSETS_DIR = path.join(ROOT, 'assets');
const FONTS_DIR = path.join(ASSETS_DIR, 'fonts');
const EMAIL_SRC = path.join(ROOT, 'email.html');
const DATA_SRC = path.join(ROOT, 'sample-data.json');
const MERGED_HTML = path.join(OUT_DIR, 'email-okwan-sample.html');
const TMP_HTML = path.join(OUT_DIR, '.render-tmp.html');
const PHONE_PNG = path.join(OUT_DIR, 'trendyol-seller-email-phone.png');
const DESKTOP_PNG = path.join(OUT_DIR, 'trendyol-seller-email-desktop.png');
const REPORT_JSON = path.join(OUT_DIR, 'render-report.json');

const READY_TIMEOUT_MS = 10000;

/* ---------------------------------------------------------------- helpers */

function escapeHtmlText(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function fileUrl(absPath) {
  return 'file://' + absPath.split(path.sep).join('/');
}

/** PNG width/height straight out of the IHDR header (bytes 16..24). */
function pngSize(file) {
  const fd = fs.openSync(file, 'r');
  const buf = Buffer.alloc(24);
  fs.readSync(fd, buf, 0, 24, 0);
  fs.closeSync(fd);
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

/* ------------------------------------------------------------------ merge */

function buildMergedHtml() {
  const template = fs.readFileSync(EMAIL_SRC, 'utf8');
  const data = JSON.parse(fs.readFileSync(DATA_SRC, 'utf8'));

  if (!data.seller_name) throw new Error('sample-data.json is missing "seller_name"');

  const values = Object.assign({}, data, {
    seller_name_url: encodeURIComponent(data.seller_name),
  });

  let html = template;
  for (const key of Object.keys(values)) {
    // seller_name_url is already percent-encoded and only ever lands in a URL.
    const replacement =
      key === 'seller_name_url' ? String(values[key]) : escapeHtmlText(values[key]);
    const re = new RegExp('\\{\\{\\s*' + escapeRegExp(key) + '\\s*\\}\\}', 'g');
    html = html.replace(re, replacement);
  }

  const leftovers = html.match(/\{\{[^}]*\}\}/g);
  if (leftovers && leftovers.length) {
    const unique = Array.from(new Set(leftovers));
    console.error('ERROR: unresolved merge tokens remain after substitution:');
    unique.forEach((t) => console.error('  ' + t));
    process.exit(1);
  }

  return html;
}

/* ------------------------------------------------- render-only transforms */

function buildRenderHtml(mergedHtml) {
  let css = fs.readFileSync(path.join(FONTS_DIR, 'local-fonts.css'), 'utf8');

  // Point every @font-face src at an absolute file:// URL so no network is needed.
  css = css.replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (match, quote, ref) => {
    if (/^(https?:|file:|data:)/i.test(ref)) return match;
    return "url('" + fileUrl(path.join(FONTS_DIR, ref)) + "')";
  });

  let html = mergedHtml;

  // No network during render: drop the Google Fonts @import.
  html = html.replace(/^[ \t]*@import\s+url\((['"]?)https:\/\/fonts\.googleapis\.com[^\n]*\n/gm, '');

  // The temp file lives in output/, so relative assets/... must become absolute.
  html = html.replace(/(src|href)="assets\/([^"]+)"/g, (m, attr, rel) => {
    return attr + '="' + fileUrl(path.join(ASSETS_DIR, rel)) + '"';
  });

  // Inject the offline font faces right after <head>.
  html = html.replace(/<head([^>]*)>/i, (m) => m + '\n<style type="text/css">\n' + css + '\n</style>');

  return html;
}

/* ----------------------------------------------------------------- render */

async function waitForReady(page) {
  await page.waitForFunction(
    () =>
      document.fonts.status === 'loaded' &&
      Array.from(document.images).every((i) => i.complete && i.naturalWidth > 0),
    undefined,
    { timeout: READY_TIMEOUT_MS }
  );
  await page.evaluate(() => document.fonts.ready);
}

async function shoot(browser, { width, height, out, label }) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  const consoleErrors = [];
  const failedRequests = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(`[${label}] ${msg.text()}`);
  });
  page.on('pageerror', (err) => consoleErrors.push(`[${label}] pageerror: ${err.message}`));
  page.on('requestfailed', (req) => {
    failedRequests.push(`[${label}] ${req.url()} — ${(req.failure() && req.failure().errorText) || 'failed'}`);
  });

  await page.goto(fileUrl(TMP_HTML), { waitUntil: 'load' });

  let readyError = null;
  try {
    await waitForReady(page);
  } catch (e) {
    readyError = `[${label}] ready-wait timed out: ${e.message}`;
  }

  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    scrollHeight: document.documentElement.scrollHeight,
    imagesTotal: document.images.length,
    imagesLoaded: Array.from(document.images).filter((i) => i.complete && i.naturalWidth > 0).length,
    imageDetail: Array.from(document.images).map((i) => ({
      src: i.currentSrc.split('/').pop(),
      loaded: i.complete && i.naturalWidth > 0,
      natural: i.naturalWidth + 'x' + i.naturalHeight,
      rendered: Math.round(i.getBoundingClientRect().width) + 'x' + Math.round(i.getBoundingClientRect().height),
    })),
    leftoverTokens: (document.documentElement.innerHTML.match(/\{\{[^}]*\}\}/g) || []).length,
  }));

  const fonts = await page.evaluate(() =>
    Array.from(document.fonts)
      .filter((f) => f.status === 'loaded')
      .map((f) => `${f.family} ${f.weight} ${f.style}`)
  );

  await page.screenshot({ path: out, fullPage: true });
  await context.close();

  if (readyError) consoleErrors.push(readyError);

  return { metrics, fonts: Array.from(new Set(fonts)).sort(), consoleErrors, failedRequests };
}

/* ------------------------------------------------------------------- main */

(async () => {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const merged = buildMergedHtml();
  fs.writeFileSync(MERGED_HTML, merged, 'utf8');

  const renderHtml = buildRenderHtml(merged);
  fs.writeFileSync(TMP_HTML, renderHtml, 'utf8');

  const browser = await chromium.launch();
  let phone;
  let desktop;
  try {
    phone = await shoot(browser, { width: 390, height: 844, out: PHONE_PNG, label: 'phone' });
    desktop = await shoot(browser, { width: 960, height: 800, out: DESKTOP_PNG, label: 'desktop' });
  } finally {
    await browser.close();
    if (fs.existsSync(TMP_HTML)) fs.unlinkSync(TMP_HTML);
  }

  const familiesOf = (list) =>
    Array.from(new Set(list.map((f) => f.replace(/\s+\S+\s+\S+$/, '').replace(/^['"]|['"]$/g, '')))).sort();

  const report = {
    generated_at: new Date().toISOString(),
    merged_html: path.relative(ROOT, MERGED_HTML),
    leftover_merge_tokens: phone.metrics.leftoverTokens + desktop.metrics.leftoverTokens,
    screenshots: [
      {
        label: 'phone',
        path: path.relative(ROOT, PHONE_PNG),
        viewport: '390x844 @2x',
        pixels: pngSize(PHONE_PNG),
        bytes: fs.statSync(PHONE_PNG).size,
        document_scroll_width: phone.metrics.scrollWidth,
        document_client_width: phone.metrics.clientWidth,
        horizontal_overflow: phone.metrics.scrollWidth > phone.metrics.clientWidth,
      },
      {
        label: 'desktop',
        path: path.relative(ROOT, DESKTOP_PNG),
        viewport: '960x800 @2x',
        pixels: pngSize(DESKTOP_PNG),
        bytes: fs.statSync(DESKTOP_PNG).size,
        document_scroll_width: desktop.metrics.scrollWidth,
        document_client_width: desktop.metrics.clientWidth,
        horizontal_overflow: desktop.metrics.scrollWidth > desktop.metrics.clientWidth,
      },
    ],
    images: desktop.metrics.imageDetail,
    fonts_loaded: Array.from(new Set([].concat(phone.fonts, desktop.fonts))).sort(),
    font_families_loaded: familiesOf([].concat(phone.fonts, desktop.fonts)),
    console_errors: [].concat(phone.consoleErrors, desktop.consoleErrors),
    failed_requests: [].concat(phone.failedRequests, desktop.failedRequests),
  };

  fs.writeFileSync(REPORT_JSON, JSON.stringify(report, null, 2), 'utf8');

  const p = report.screenshots[0];
  const d = report.screenshots[1];
  console.log('Merged HTML   : ' + report.merged_html + ' (no leftover {{ tokens })');
  console.log('Phone PNG     : ' + p.path + '  ' + p.pixels.width + 'x' + p.pixels.height + 'px  ' + Math.round(p.bytes / 1024) + ' KB');
  console.log('Desktop PNG   : ' + d.path + '  ' + d.pixels.width + 'x' + d.pixels.height + 'px  ' + Math.round(d.bytes / 1024) + ' KB');
  console.log('Phone width   : scrollWidth ' + p.document_scroll_width + ' / client ' + p.document_client_width + '  overflow=' + p.horizontal_overflow);
  console.log('Images        : ' + desktop.metrics.imagesLoaded + '/' + desktop.metrics.imagesTotal + ' loaded');
  console.log('Font families : ' + report.font_families_loaded.join(', '));
  console.log('Console errors: ' + report.console_errors.length + '   Failed requests: ' + report.failed_requests.length);
  if (report.console_errors.length) report.console_errors.forEach((e) => console.log('  ! ' + e));
  if (report.failed_requests.length) report.failed_requests.forEach((e) => console.log('  ! ' + e));
  console.log('Report        : ' + path.relative(ROOT, REPORT_JSON));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
