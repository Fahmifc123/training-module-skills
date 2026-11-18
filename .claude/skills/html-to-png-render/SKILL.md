---
name: html-to-png-render
description: Render file HTML (misal slide/visual/diagram custom) menjadi gambar PNG memakai Playwright, dengan resolusi dan branding konsisten untuk materi training Insignia. Pakai skill ini saat diminta mengubah HTML menjadi PNG/gambar.
---

# HTML to PNG Render

Skill ini merender file `.html` menjadi `.png` memakai `Playwright` (headless browser), untuk kebutuhan seperti: visual/diagram custom yang dibuat di HTML lalu dipakai sebagai gambar di PPT, atau snapshot halaman statis untuk materi training.

## Aturan konten

- Resolusi default mengikuti rasio slide 16:9 (1920x1080) kecuali diminta ukuran lain.
- Kalau HTML memuat font custom, pastikan font di-load dari `<kit root>/brand/fonts/` (lihat bagian embedding font di bawah) supaya render konsisten, bukan fallback ke font sistem.
- Tanpa emoji/icon dekoratif di hasil render untuk materi formal.
- Warna di HTML sumber sebaiknya mengacu ke `brand/colors.json` supaya hasil PNG konsisten dengan PPT dan Excel.

## Setup

```bash
npm install playwright --save
npx playwright install chromium
```

## Kode referensi (lengkap, runnable)

Simpan sebagai `render_html_to_png.js` di root project, jalankan dengan:

```bash
node render_html_to_png.js <path-ke-file.html> <path-output.png> [width] [height]
```

```javascript
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

async function renderHtmlToPng(htmlPath, outputPath, width = 1920, height = 1080) {
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`File HTML tidak ditemukan: ${htmlPath}`);
  }

  const outDir = path.dirname(outputPath);
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 2, // render tajam untuk kebutuhan print/zoom
  });

  const absoluteHtmlPath = path.resolve(htmlPath);
  await page.goto(`file://${absoluteHtmlPath}`);

  // Tunggu font custom selesai load sebelum screenshot
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);

  await page.screenshot({ path: outputPath, fullPage: false });
  await browser.close();

  console.log(`PNG tersimpan di: ${outputPath}`);
}

async function main() {
  const [, , htmlPathArg, outputPathArg, widthArg, heightArg] = process.argv;

  if (!htmlPathArg || !outputPathArg) {
    console.error("Pemakaian: node render_html_to_png.js <input.html> <output.png> [width] [height]");
    process.exit(1);
  }

  const width = widthArg ? parseInt(widthArg, 10) : 1920;
  const height = heightArg ? parseInt(heightArg, 10) : 1080;

  await renderHtmlToPng(htmlPathArg, outputPathArg, width, height);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

## Embedding font custom di HTML sumber

Kalau HTML yang akan dirender butuh font dari `<kit root>/brand/fonts/`, load lewat `@font-face` dengan path relatif/absolut ke file font tersebut:

```html
<style>
  @font-face {
    font-family: "Inter";
    src: url("file:///absolute/path/to/brand/fonts/Inter-Regular.ttf") format("truetype");
    font-weight: 400;
  }
  @font-face {
    font-family: "Inter";
    src: url("file:///absolute/path/to/brand/fonts/Inter-Bold.ttf") format("truetype");
    font-weight: 700;
  }
  body { font-family: "Inter", sans-serif; }
</style>
```

Gunakan path absolut (bukan relatif) untuk `file://` URL supaya tidak gagal resolve tergantung dari mana script dijalankan.

## Batch render (opsional)

Kalau perlu render banyak file HTML sekaligus (misal per slide custom dalam satu modul), loop folder input dan panggil `renderHtmlToPng` untuk tiap file, jalankan satu instance browser untuk semua render supaya lebih cepat:

```javascript
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

async function batchRender(inputDir, outputDir, width = 1920, height = 1080) {
  const browser = await chromium.launch();
  const files = fs.readdirSync(inputDir).filter((f) => f.endsWith(".html"));

  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  for (const file of files) {
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
    const absoluteHtmlPath = path.resolve(inputDir, file);
    await page.goto(`file://${absoluteHtmlPath}`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const outPath = path.join(outputDir, file.replace(".html", ".png"));
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`Rendered: ${outPath}`);
  }

  await browser.close();
}

module.exports = { batchRender };
```

## Checklist sebelum mengirim PNG ke user

- Resolusi sesuai kebutuhan (default 1920x1080 untuk slide).
- Font custom (kalau dipakai) ter-load sempurna, bukan fallback — cek hasil render secara visual.
- Warna di hasil render konsisten dengan `brand/colors.json`.
- File output ditulis ke `<project root>/output/<Paket>/`.

## Aturan bersama

Patuhi `insignia-training-module/references/aturan-bersama.md` (bahasa, kode runnable, data sintetis, brand, path output, dan keputusan manusia lewat `grill-me`).
