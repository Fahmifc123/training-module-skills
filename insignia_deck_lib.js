// insignia_deck_lib.js v2
// Komponen deck training Insignia untuk pptxgenjs.
// Geometri dan gaya mengikuti AI-DLC_Internal_Training_Insignia.pptx (deck terbaru),
// referensi visual: brand/slide-templates/Template_Training_Insignia.pdf
//
// API v1 tetap ada (newDeck, addDividerSlide, addAgendaSlide, addCardGridSlide,
// addComparisonTableSlide, addBeforeAfterSlide, addChecklistSlide, addTimelineSlide,
// addCodeSlide, addClosingSlide, addContentHeader) supaya script lama tetap jalan.
// Komponen baru v2: addCoverSlide, addSectionSlide, addContentSlide, addNumberedListSlide,
// addStatSlide, addTwoPanelSlide, addLabelRowsSlide, addStepsCheckpointSlide, addThankYouSlide, save.

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const colors = JSON.parse(fs.readFileSync(path.join(ROOT, "brand", "colors.json"), "utf-8"));
const LOGO_LIGHT_BG = path.join(ROOT, "brand", "logo-light-bg.png");
const LOGO_DARK_BG = path.join(ROOT, "brand", "logo-dark-bg.png");

function pngRatio(p) { const b = fs.readFileSync(p); return b.readUInt32BE(16) / b.readUInt32BE(20); }
const RATIO_LIGHT = pngRatio(LOGO_LIGHT_BG);
const RATIO_DARK = pngRatio(LOGO_DARK_BG);

const FONT = colors.font_heading || "Arial";
const FONT_CODE = colors.font_code || "Courier New";
const COPYRIGHT = `©${new Date().getFullYear()} INSIGNIA. All contents and materials in this presentation belong to INSIGNIA`;

function hex(key) { return colors[key].replace("#", ""); }
const K = {
  navy: hex("primary"), blue: hex("secondary"), red: hex("accent"), white: hex("background"),
  bg: hex("surface"), text: hex("text_primary"), text2: hex("text_secondary"), muted: hex("muted"),
  line: hex("surface_muted"), tintRed: hex("tint_accent"), tintBlue: hex("tint_secondary"),
  success: hex("success"), codeBg: hex("code_background"), codeText: hex("code_text"), onDark: hex("text_on_dark"),
};

const M_CONTENT = "INS_CONTENT";
const M_DARK = "INS_DARK";

// ---------- util ----------
const noLine = () => ({ type: "none" });
const shadow = () => ({ type: "outer", color: K.navy, blur: 8, offset: 2, angle: 90, opacity: 0.09 });
const pad2 = (n) => String(n).padStart(2, "0");

function txt(slide, t, opts) {
  slide.addText(t, Object.assign({ isTextBox: true, margin: 0, fontFace: FONT, fontSize: 14, color: K.text2, valign: "top" }, opts));
}

function card(slide, x, y, w, h, fill = K.white, radius = 0.08) {
  slide.addShape("roundRect", { x, y, w, h, rectRadius: radius, fill: { color: fill }, line: noLine(), shadow: shadow() });
}

// Ukuran font terbesar yang memuat teks dalam satu baris selebar w inci (perkiraan lebar Arial bold).
function fitSize(text, w, maxPt, minPt) {
  const perChar = 0.6 / 72; // inci per pt per karakter (konservatif untuk bold)
  for (let pt = maxPt; pt > minPt; pt -= 2) if (text.length * perChar * pt <= w) return pt;
  return minPt;
}

// Teks "Label: isi" -> label merah tebal + isi
function labeled(text, labelColor, bodyColor) {
  const i = text.indexOf(":");
  if (i > 0 && i < 40) {
    return [
      { text: text.slice(0, i + 1) + " ", options: { bold: true, color: labelColor } },
      { text: text.slice(i + 1).trim(), options: { color: bodyColor } },
    ];
  }
  return [{ text, options: { color: bodyColor } }];
}

function decor(pptx, slide) {
  slide.addShape(pptx.ShapeType.custGeom, { x: 0, y: 0, w: 3, h: 3, fill: { color: K.blue }, line: noLine(),
    points: [{ x: 0, y: 0 }, { x: 3, y: 0 }, { x: 0, y: 3 }, { close: true }] });
  slide.addShape(pptx.ShapeType.custGeom, { x: 0, y: 0, w: 1.3, h: 2.2, fill: { color: K.red }, line: noLine(),
    points: [{ x: 0, y: 0 }, { x: 0.25, y: 0 }, { x: 1.3, y: 1.0 }, { x: 0, y: 2.2 }, { close: true }] });
  slide.addShape(pptx.ShapeType.custGeom, { x: 10.93, y: 5.5, w: 2.4, h: 2.0, fill: { color: K.red }, line: noLine(),
    points: [{ x: 2.4, y: 0 }, { x: 2.4, y: 2.0 }, { x: 0, y: 2.0 }, { close: true }] });
}

function bottomNote(slide, note, y = 5.85) {
  if (!note) return;
  txt(slide, labeled(note, K.red, K.text), { x: 0.6, y, w: 12.13, h: 0.6, fontSize: 16, bold: true, valign: "middle" });
}

function navyBar(slide, text, y = 5.85) {
  card(slide, 0.6, y, 12.13, 0.8, K.navy, 0.08);
  txt(slide, labeled(text, K.red, K.onDark), { x: 0.95, y, w: 11.5, h: 0.8, fontSize: 16, valign: "middle" });
}

function pill(slide, x, y, w, label) {
  const l = label.toLowerCase();
  const s = l.includes("hands") || l.includes("lab") || l.includes("praktik")
    ? { fill: K.red, color: K.white }
    : l.includes("konsep") || l.includes("teori") || l.includes("demo") ? { fill: K.tintBlue, color: K.navy } : { fill: K.line, color: K.text2 };
  slide.addShape("roundRect", { x, y, w, h: 0.3, rectRadius: 0.15, fill: { color: s.fill }, line: noLine() });
  txt(slide, label.toUpperCase(), { x, y, w, h: 0.3, fontSize: 10, bold: true, color: s.color, align: "center", valign: "middle", charSpacing: 1 });
  return s.fill === K.red;
}


// ---------- foto latar (opsional) ----------
// setPhotoDir(dir): cover memakai dir/cover.jpg, section divider ke-N memakai dir/section-N.jpg
// (urutan pemanggilan addSectionSlide). Kredit diambil dari dir/CREDITS.json (insignia-image-gen).
// File yang tidak ada dilewati, slide tampil polos seperti biasa.
let PHOTO = null;
function setPhotoDir(dir) {
  const cp = path.join(dir, "CREDITS.json");
  PHOTO = { dir, section: 0, credits: fs.existsSync(cp) ? JSON.parse(fs.readFileSync(cp, "utf-8")) : [] };
}
function photoBackdrop(slide, file) {
  if (!PHOTO) return;
  const p = path.join(PHOTO.dir, file);
  if (!fs.existsSync(p)) return;
  slide.addImage({ path: p, x: 0, y: 0, w: 13.333, h: 7.5, sizing: { type: "cover", w: 13.333, h: 7.5 } });
  slide.addShape("rect", { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: K.navy, transparency: 22 }, line: noLine() });
  slide.addImage({ path: LOGO_DARK_BG, x: 10.35, y: 0.55, w: 2.3, h: 2.3 / RATIO_DARK });
  const c = PHOTO.credits.find((x) => x.file === file);
  if (c) txt(slide, c.credit_text, { x: 0.9, y: 7.08, w: 6.0, h: 0.25, fontSize: 9, color: K.muted, valign: "middle" });
}

// Panel foto di slide konten: dir/<file> dipotong mengisi kotak, kredit kecil di bawahnya.
// Mengembalikan true bila foto benar-benar ada (layout boleh menyempit), false bila tidak.
function photoPanel(slide, file, x, y, w, h) {
  if (!PHOTO || !file) return false;
  const p = path.join(PHOTO.dir, file);
  if (!fs.existsSync(p)) return false;
  slide.addImage({ path: p, x, y, w, h, sizing: { type: "cover", w, h } });
  const c = PHOTO.credits.find((k) => k.file === file);
  if (c) txt(slide, c.credit_text, { x, y: y + h + 0.04, w, h: 0.22, fontSize: 8, color: K.muted, align: "right", valign: "middle" });
  return true;
}
const hasPhoto = (file) => !!(PHOTO && file && fs.existsSync(path.join(PHOTO.dir, file)));

// ---------- deck ----------
function newDeck(title, footerLabel) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
  pptx.author = "Insignia - Data & AI Mentor Team";
  pptx.company = "Insignia";
  pptx.title = title;
  if (footerLabel) pptx.subject = footerLabel;
  pptx.theme = { headFontFace: FONT, bodyFontFace: FONT };

  pptx.defineSlideMaster({
    title: M_CONTENT,
    background: { color: K.bg },
    objects: [
      { image: { path: LOGO_LIGHT_BG, x: 11.55, y: 0.3, w: 1.18, h: 1.18 / RATIO_LIGHT } },
      { text: { text: COPYRIGHT, options: { x: 0.6, y: 7.05, w: 9.0, h: 0.25, fontFace: FONT, fontSize: 9, color: K.muted, margin: 0 } } },
    ],
    slideNumber: { x: 12.23, y: 7.05, w: 0.5, h: 0.25, fontFace: FONT, fontSize: 9, color: K.muted, align: "right" },
  });
  pptx.defineSlideMaster({
    title: M_DARK,
    background: { color: K.navy },
    objects: [{ image: { path: LOGO_DARK_BG, x: 10.35, y: 0.55, w: 2.3, h: 2.3 / RATIO_DARK } }],
  });
  return pptx;
}

async function save(pptx, filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  await pptx.writeFile({ fileName: filePath });
  return filePath;
}

// ---------- header konten ----------
function addContentHeader(slide, { eyebrow, title }) {
  if (eyebrow) txt(slide, eyebrow.toUpperCase(), { x: 0.6, y: 0.32, w: 9.5, h: 0.28, fontSize: 11, bold: true, color: K.red, charSpacing: 2, valign: "middle" });
  txt(slide, title, { x: 0.6, y: 0.64, w: 10.6, h: 0.72, fontSize: fitSize(title, 10.6, 28, 22), bold: true, color: K.text, valign: "middle" });
}

// Slide konten kosong (header + logo + footer). Pakai untuk layout custom.
function addContentSlide(pptx, { eyebrow, title, notes }) {
  const slide = pptx.addSlide({ masterName: M_CONTENT });
  addContentHeader(slide, { eyebrow, title });
  if (notes) slide.addNotes(notes);
  return slide;
}

// ---------- 1. Cover ----------
// meta: maks 4 [{label, value}]
function addCoverSlide(pptx, { eyebrow = "Internal Training", title, subtitle, description, meta = [], notes }) {
  const slide = pptx.addSlide({ masterName: M_DARK });
  photoBackdrop(slide, "cover.jpg");
  decor(pptx, slide);
  txt(slide, eyebrow.toUpperCase(), { x: 0.9, y: 2.3, w: 8.0, h: 0.4, fontSize: 18, bold: true, color: K.onDark, charSpacing: 6, valign: "middle" });
  txt(slide, title, { x: 0.9, y: 2.75, w: 9.2, h: 1.45, fontSize: fitSize(title, 9.2, 72, 40), bold: true, color: K.onDark, valign: "middle" });
  if (subtitle) txt(slide, subtitle, { x: 0.9, y: 4.2, w: 9.5, h: 0.5, fontSize: fitSize(subtitle, 9.5, 24, 18), bold: true, color: K.red, valign: "middle" });
  if (description) txt(slide, description, { x: 0.9, y: 4.85, w: 8.6, h: 0.8, fontSize: 17, color: K.onDark });
  meta.slice(0, 4).forEach((m, i) => {
    const x = 0.9 + i * 2.55;
    if (i > 0) slide.addShape("line", { x: x - 0.15, y: 6.15, w: 0, h: 0.65, line: { color: K.muted, width: 0.75 } });
    txt(slide, m.label.toUpperCase(), { x, y: 6.15, w: 2.3, h: 0.28, fontSize: 11, bold: true, color: K.red, charSpacing: 1, valign: "middle" });
    txt(slide, m.value, { x, y: 6.45, w: 2.3, h: 0.35, fontSize: 14, bold: true, color: K.onDark, valign: "middle" });
  });
  if (notes) slide.addNotes(notes);
  return slide;
}

// ---------- 2. Section divider ----------
// items: 0-4 topik untuk panel "Di bagian ini"
function addSectionSlide(pptx, { number, title, subtitle, items = [], panelTitle = "Di bagian ini", notes }) {
  const slide = pptx.addSlide({ masterName: M_DARK });
  if (PHOTO) photoBackdrop(slide, `section-${++PHOTO.section}.jpg`);
  decor(pptx, slide);
  const wide = items.length === 0;
  const tw = wide ? 9.0 : 6.8;
  if (number !== undefined && number !== null && number !== "") {
    txt(slide, pad2(number), { x: 0.9, y: 1.6, w: 3.0, h: 1.1, fontSize: 72, bold: true, color: K.red, valign: "middle" });
    slide.addShape("rect", { x: 0.95, y: 2.72, w: 0.6, h: 0.06, fill: { color: K.red }, line: noLine() });
  }
  txt(slide, title, { x: 0.9, y: 2.95, w: tw, h: 1.4, fontSize: fitSize(title, tw, 40, 30), bold: true, color: K.onDark, valign: "middle" });
  if (subtitle) txt(slide, subtitle, { x: 0.9, y: 4.5, w: tw - 0.4, h: 0.9, fontSize: 18, color: K.onDark });
  if (!wide) {
    slide.addShape("roundRect", { x: 8.1, y: 1.9, w: 4.4, h: 3.9, rectRadius: 0.1, fill: { color: K.blue }, line: noLine() });
    txt(slide, panelTitle.toUpperCase(), { x: 8.45, y: 2.2, w: 3.8, h: 0.26, fontSize: 11, bold: true, color: K.muted, charSpacing: 2, valign: "middle" });
    items.slice(0, 4).forEach((t, i) => {
      const y = 2.65 + i * 0.6;
      txt(slide, pad2(i + 1), { x: 8.45, y, w: 0.5, h: 0.45, fontSize: 14, bold: true, color: K.red, valign: "middle" });
      txt(slide, t, { x: 9.0, y, w: 3.3, h: 0.45, fontSize: 15, color: K.onDark, valign: "middle" });
      if (i < Math.min(items.length, 4) - 1) slide.addShape("line", { x: 8.45, y: y + 0.53, w: 3.8, h: 0, line: { color: K.text2, width: 0.75 } });
    });
  }
  if (notes) slide.addNotes(notes);
  return slide;
}

// v1: dengan meta -> cover; tanpa meta -> section divider (nomor diambil dari eyebrow, misal "Bagian 2")
function addDividerSlide(pptx, { eyebrow, title, subtitle, meta, items }) {
  if (meta && meta.length) return addCoverSlide(pptx, { eyebrow: eyebrow || "Internal Training", title, subtitle, meta });
  const m = (eyebrow || "").match(/(\d+)/);
  return addSectionSlide(pptx, { number: m ? Number(m[1]) : null, title, subtitle, items: items || [] });
}

// ---------- 3. Agenda ----------
// items: [{ time, text, tag, duration, number }]
function addAgendaSlide(pptx, { eyebrow = "Agenda", title, items, note, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const n = items.length, gap = 0.1, top = 1.6, avail = (note ? 5.4 : 5.9) - top;
  const rowH = Math.min(0.52, (avail - gap * (n - 1)) / n);
  items.forEach((it, i) => {
    const y = top + i * (rowH + gap);
    card(slide, 0.6, y, 12.13, rowH, K.white, 0.06);
    txt(slide, it.time || it.number || pad2(i + 1), { x: 0.85, y, w: 1.9, h: rowH, fontSize: 15, bold: true, color: K.text, valign: "middle" });
    const strong = it.tag ? pill(slide, 9.75, y + (rowH - 0.3) / 2, 1.6, it.tag) : false;
    txt(slide, it.text, { x: 2.9, y, w: 6.7, h: rowH, fontSize: 15, bold: strong, color: K.text, valign: "middle" });
    if (it.duration) txt(slide, it.duration, { x: 11.5, y, w: 1.0, h: rowH, fontSize: 14, color: K.text2, align: "right", valign: "middle" });
  });
  if (note) txt(slide, note, { x: 0.6, y: 5.55, w: 12.13, h: 0.4, fontSize: 14, color: K.text2, valign: "middle" });
  return slide;
}

// ---------- 4. Card grid (tujuan / poin kunci) ----------
// cards: 2-4 [{ number, heading, body }], footerNote: "Target akhir sesi: ..." -> bar navy
function addCardGridSlide(pptx, { eyebrow, title, cards, footerNote, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const n = cards.length, gap = 0.22, w = (12.13 - gap * (n - 1)) / n;
  cards.forEach((c, i) => {
    const x = 0.6 + i * (w + gap);
    card(slide, x, 1.7, w, 3.9);
    txt(slide, c.number || pad2(i + 1), { x: x + 0.3, y: 2.05, w: 1.6, h: 0.8, fontSize: 44, bold: true, color: K.red });
    txt(slide, c.heading, { x: x + 0.3, y: 3.15, w: w - 0.6, h: 0.45, fontSize: fitSize(c.heading, w - 0.6, 20, 16), bold: true, color: K.text });
    txt(slide, c.body, { x: x + 0.3, y: 3.7, w: w - 0.6, h: 1.75, fontSize: 15, color: K.text2 });
  });
  if (footerNote) navyBar(slide, footerNote);
  return slide;
}

// ---------- 5. List bernomor + kutipan ----------
// items: 2-4 [{ heading, body }], quote: string opsional, note: kalimat penutup
// photo: nama file di setPhotoDir (opsional, hanya tanpa quote) -> foto di panel kanan
// photoSide: "right" (bawaan) atau "left"
function addNumberedListSlide(pptx, { eyebrow, title, items, quote, note, notes, photo, photoSide = "right" }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const side = !quote && hasPhoto(photo), left = side && photoSide === "left";
  const listW = quote || side ? 7.6 : 12.13, n = items.length, gap = 0.17, lx = left ? 5.13 : 0.6;
  const h = Math.min(1.15, (3.95 - gap * (n - 1)) / n);
  items.forEach((it, i) => {
    const y = 1.7 + i * (h + gap);
    card(slide, lx, y, listW, h);
    slide.addShape("ellipse", { x: lx + 0.3, y: y + (h - 0.55) / 2, w: 0.55, h: 0.55, fill: { color: K.red }, line: noLine() });
    txt(slide, String(i + 1), { x: lx + 0.3, y: y + (h - 0.55) / 2, w: 0.55, h: 0.55, fontSize: 16, bold: true, color: K.white, align: "center", valign: "middle" });
    txt(slide, it.heading, { x: lx + 1.1, y: y + 0.16, w: listW - 1.4, h: 0.36, fontSize: 18, bold: true, color: K.text, valign: "middle" });
    if (it.body) txt(slide, it.body, { x: lx + 1.1, y: y + 0.54, w: listW - 1.3, h: h - 0.6, fontSize: 14, color: K.text2 });
  });
  if (quote) {
    card(slide, 8.55, 1.7, 4.18, 3.79, K.navy);
    txt(slide, "“", { x: 8.85, y: 1.85, w: 1.0, h: 0.9, fontSize: 60, bold: true, color: K.red });
    txt(slide, quote, { x: 8.85, y: 2.75, w: 3.6, h: 2.5, fontSize: 20, bold: true, color: K.onDark });
  }
  if (side) photoPanel(slide, photo, left ? 0.6 : 8.55, 1.7, 4.18, 3.79);
  bottomNote(slide, note);
  return slide;
}

// ---------- 6. Stat callout ----------
// stats: 2-4 [{ value, label, body, highlight }], conclusion: "Kesimpulan: ...", source: string
function addStatSlide(pptx, { eyebrow, title, stats, conclusion, source, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const n = stats.length, gap = 0.26, w = (12.13 - gap * (n - 1)) / n;
  stats.forEach((st, i) => {
    const x = 0.6 + i * (w + gap), dark = !!st.highlight;
    card(slide, x, 1.7, w, 3.3, dark ? K.navy : K.white);
    txt(slide, st.value, { x: x + 0.35, y: 2.0, w: w - 0.6, h: 1.1, fontSize: fitSize(st.value, w - 0.6, 54, 32), bold: true, color: dark ? K.red : K.text, valign: "middle" });
    txt(slide, st.label, { x: x + 0.35, y: 3.2, w: w - 0.6, h: 0.45, fontSize: 18, bold: true, color: dark ? K.onDark : K.text });
    if (st.body) txt(slide, st.body, { x: x + 0.35, y: 3.75, w: w - 0.6, h: 1.0, fontSize: 14, color: dark ? K.line : K.text2 });
  });
  if (conclusion) txt(slide, labeled(conclusion, K.red, K.text), { x: 0.6, y: 5.35, w: 12.13, h: 0.6, fontSize: 16, valign: "middle" });
  if (source) txt(slide, source, { x: 0.6, y: 6.05, w: 12.13, h: 0.3, fontSize: 11, color: K.muted, valign: "middle" });
  return slide;
}

// ---------- 7. Comparison table ----------
// headers: string[], rows: string[][] (maks 6 baris), note: kalimat di bawah tabel
function addComparisonTableSlide(pptx, { eyebrow, title, headers, rows, note, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const first = headers.length > 3 ? 2.4 : 2.9, other = (12.13 - first) / (headers.length - 1);
  const rowH = Math.min(0.62, 4.0 / (rows.length + 1));
  const head = headers.map((h) => ({ text: h, options: { bold: true, color: K.white, fill: { color: K.navy } } }));
  const body = rows.map((r, i) => r.map((t, j) => ({
    text: t, options: { fill: { color: i % 2 === 0 ? K.white : K.tintBlue }, bold: j === 0, color: j === 0 ? K.text : K.text2 },
  })));
  slide.addTable([head, ...body], {
    x: 0.6, y: 1.7, w: 12.13, colW: headers.map((_, i) => (i === 0 ? first : other)), rowH,
    fontFace: FONT, fontSize: rows.length > 5 ? 14 : 15, valign: "middle", margin: [0, 0.2, 0, 0.2],
    border: { type: "solid", color: K.line, pt: 0.75 },
  });
  bottomNote(slide, note, 1.7 + rowH * (rows.length + 1) + 0.35);
  return slide;
}

// ---------- 8. Dua panel kontras ----------
// panels: 2 [{ label, title, body, listLabel, items, code }], panel kedua navy (opsi yang ditekankan)
function addTwoPanelSlide(pptx, { eyebrow, title, panels, note, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  panels.slice(0, 2).forEach((p, i) => {
    const x = i === 0 ? 0.6 : 6.78, dark = i === 1;
    card(slide, x, 1.7, 5.95, 3.95, dark ? K.navy : K.white);
    if (p.label) txt(slide, p.label.toUpperCase(), { x: x + 0.4, y: 2.0, w: 5, h: 0.28, fontSize: 11, bold: true, color: K.red, charSpacing: 2, valign: "middle" });
    txt(slide, p.title, { x: x + 0.4, y: 2.35, w: 5.2, h: 0.5, fontSize: 22, bold: true, color: dark ? K.onDark : K.text, valign: "middle" });
    if (p.body) txt(slide, p.body, { x: x + 0.4, y: 3.0, w: 5.2, h: 0.9, fontSize: 15, color: dark ? K.line : K.text2 });
    if (p.items && p.items.length) {
      txt(slide, (p.listLabel || "Contoh").toUpperCase(), { x: x + 0.4, y: 4.05, w: 4, h: 0.26, fontSize: 11, bold: true, color: K.muted, charSpacing: 2, valign: "middle" });
      txt(slide, p.items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < p.items.length - 1 } })),
        { x: x + 0.4, y: 4.4, w: 5.2, h: 1.1, fontSize: 15, fontFace: p.code ? FONT_CODE : FONT, color: dark ? K.onDark : K.text, paraSpaceAfter: 4 });
    }
  });
  bottomNote(slide, note, 5.9);
  return slide;
}

// v1: before/after -> dua panel, item diberi tanda silang / centang
// marks: false menghapus tanda silang/centang untuk perbandingan netral (kedua panel benar atau setara).
function addBeforeAfterSlide(pptx, { eyebrow, title, before, after, note, notes, marks = true }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const panels = marks
    ? [[before, "BEFORE", "✗", K.red, K.tintRed], [after, "AFTER", "✓", K.success, K.white]]
    : [[before, "BEFORE", "•", K.navy, K.white], [after, "AFTER", "•", K.navy, K.white]];
  panels.forEach(([p, def, mark, markColor, fill], i) => {
    const x = i === 0 ? 0.6 : 6.78;
    card(slide, x, 1.7, 5.95, 3.95, fill);
    txt(slide, (p.label || def).toUpperCase(), { x: x + 0.4, y: 2.0, w: 5.2, h: 0.3, fontSize: 12, bold: true, color: markColor, charSpacing: 2, valign: "middle" });
    txt(slide, p.items.map((t, k) => [
      { text: `${mark}  `, options: { bold: true, color: markColor } },
      { text: t, options: { color: K.text, breakLine: k < p.items.length - 1 } },
    ]).flat(), { x: x + 0.4, y: 2.5, w: 5.2, h: 3.0, fontSize: 15, paraSpaceAfter: 10 });
  });
  bottomNote(slide, note, 5.9);
  return slide;
}

// ---------- 9. Timeline / process ----------
// steps: 3-5 [{ label, description }], langkah terakhir merah (atau highlightIndex, -1 tanpa sorotan)
function addTimelineSlide(pptx, { eyebrow, title, steps, note, notes, highlightIndex }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const n = steps.length, step = 12.13 / n, cy = 2.55, r = 0.36;
  card(slide, 0.6, 1.7, 12.13, 3.6);
  slide.addShape("line", { x: 0.6 + step / 2, y: cy, w: step * (n - 1), h: 0, line: { color: K.line, width: 2 } });
  steps.forEach((s, i) => {
    const cx = 0.6 + step / 2 + i * step, last = i === (highlightIndex ?? n - 1);
    slide.addShape("ellipse", { x: cx - r, y: cy - r, w: r * 2, h: r * 2, fill: { color: last ? K.red : K.navy }, line: noLine() });
    txt(slide, String(i + 1), { x: cx - r, y: cy - r, w: r * 2, h: r * 2, fontSize: 16, bold: true, color: K.white, align: "center", valign: "middle" });
    txt(slide, s.label, { x: cx - step / 2 + 0.1, y: 3.15, w: step - 0.2, h: 0.4, fontSize: 16, bold: true, color: K.text, align: "center", valign: "middle" });
    if (s.description) txt(slide, s.description, { x: cx - step / 2 + 0.15, y: 3.6, w: step - 0.3, h: 1.5, fontSize: 14, color: K.text2, align: "center" });
  });
  bottomNote(slide, note, 5.65);
  return slide;
}

// ---------- 10. Label rows ----------
// rows: 3-5 [{ term, body, highlight }]
// photo: nama file di setPhotoDir (opsional) -> baris menyempit, foto di kanan
function addLabelRowsSlide(pptx, { eyebrow, title, rows, note, notes, photo, photoSide = "right" }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const side = hasPhoto(photo), left = side && photoSide === "left", cw = side ? 8.0 : 12.13, ox = left ? 4.73 : 0.6;
  const n = rows.length, gap = 0.14, h = Math.min(side ? 1.05 : 0.72, (4.3 - gap * (n - 1)) / n);
  if (side) photoPanel(slide, photo, left ? 0.6 : 8.83, 1.7, 3.9, n * h + (n - 1) * gap);
  rows.forEach((r, i) => {
    const y = 1.7 + i * (h + gap);
    card(slide, ox, y, cw, h, K.white, 0.06);
    slide.addShape("rect", { x: ox, y, w: 0.95, h, fill: { color: r.highlight ? K.red : K.navy }, line: noLine() });
    txt(slide, r.label || pad2(i + 1), { x: ox, y, w: 0.95, h, fontSize: 18, bold: true, color: K.white, align: "center", valign: "middle" });
    txt(slide, r.term, { x: ox + 1.25, y, w: 2.2, h, fontSize: 16, bold: true, color: K.text, valign: "middle" });
    txt(slide, r.body, { x: ox + 3.6, y, w: cw - 3.8, h, fontSize: side ? 13 : 14, color: K.text2, valign: "middle" });
  });
  if (note) txt(slide, note, { x: 0.6, y: 6.15, w: 12.13, h: 0.45, fontSize: 14, color: K.text2, valign: "middle" });
  return slide;
}

// ---------- 10b. Teori + foto setengah halaman ----------
// Untuk konsep/analogi: foto di satu sisi, teks di sisi lain.
// lead: kalimat utama; points: 2-4 butir (string "Label: isi" diberi label merah); question: ajakan diskusi opsional.
function addPhotoSlide(pptx, { eyebrow, title, lead, points = [], question, photo, photoSide = "right", notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const side = hasPhoto(photo), left = side && photoSide === "left";
  const tx = left ? 6.55 : 0.6, tw = side ? 6.18 : 12.13;
  if (side) photoPanel(slide, photo, left ? 0.6 : 7.15, 1.7, 5.58, 4.6);
  let y = 1.7;
  if (lead) { txt(slide, lead, { x: tx, y, w: tw, h: 1.1, fontSize: 20, bold: true, color: K.text, valign: "top" }); y += 1.25; }
  points.slice(0, 4).forEach((p) => {
    card(slide, tx, y, tw, 0.72, K.white, 0.06);
    slide.addShape("rect", { x: tx, y, w: 0.09, h: 0.72, fill: { color: K.red }, line: noLine() });
    txt(slide, labeled(p, K.red, K.text), { x: tx + 0.3, y, w: tw - 0.5, h: 0.72, fontSize: 14, valign: "middle" });
    y += 0.84;
  });
  if (question) {
    card(slide, tx, y + 0.05, tw, 0.75, K.navy, 0.06);
    txt(slide, labeled(question, K.red, K.onDark), { x: tx + 0.3, y: y + 0.05, w: tw - 0.5, h: 0.75, fontSize: 14, bold: true, valign: "middle" });
  }
  return slide;
}

// ---------- 11. Code slide ----------
// code: string lengkap dan runnable (maks 18 baris)
function addCodeSlide(pptx, { eyebrow, title, language, code, caption, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  if (language) txt(slide, language, { x: 9.6, y: 1.35, w: 3.13, h: 0.3, fontSize: 12, italic: true, color: K.muted, align: "right", valign: "middle" });
  const lines = code.split("\n").length;
  card(slide, 0.6, 1.7, 12.13, 4.3, K.codeBg, 0.06);
  txt(slide, code, { x: 0.95, y: 1.95, w: 11.5, h: 3.85, fontSize: lines > 21 ? 9 : lines > 18 ? 10 : lines > 15 ? 12 : 14, fontFace: FONT_CODE, color: K.codeText, lineSpacingMultiple: 1.05 });
  if (caption) txt(slide, caption, { x: 0.6, y: 6.2, w: 12.13, h: 0.45, fontSize: 14, italic: true, color: K.text2, valign: "middle" });
  return slide;
}

// ---------- 12. Langkah hands-on + checkpoint ----------
// steps: 3-4 [{ heading, body }], checkpoint: { tag, title, items }, note: "Tertinggal? ..." -> bar navy
function addStepsCheckpointSlide(pptx, { eyebrow, title, steps, checkpoint, note, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  const n = steps.length, gap = 0.15, h = Math.min(0.85, (3.85 - gap * (n - 1)) / n);
  steps.forEach((s, i) => {
    const y = 1.7 + i * (h + gap);
    card(slide, 0.6, y, 7.2, h, K.white, 0.06);
    slide.addShape("ellipse", { x: 0.85, y: y + (h - 0.5) / 2, w: 0.5, h: 0.5, fill: { color: K.navy }, line: noLine() });
    txt(slide, String(i + 1), { x: 0.85, y: y + (h - 0.5) / 2, w: 0.5, h: 0.5, fontSize: 15, bold: true, color: K.white, align: "center", valign: "middle" });
    txt(slide, s.heading, { x: 1.6, y: y + 0.08, w: 6.0, h: 0.35, fontSize: 16, bold: true, color: K.text, valign: "middle" });
    if (s.body) txt(slide, s.body, { x: 1.6, y: y + 0.43, w: 6.0, h: h - 0.5, fontSize: 14, color: K.text2, valign: "middle" });
  });
  if (checkpoint) {
    card(slide, 8.15, 1.7, 4.58, 3.85);
    const tag = (checkpoint.tag || "Checkpoint").toUpperCase();
    slide.addShape("roundRect", { x: 8.5, y: 2.0, w: 1.8, h: 0.32, rectRadius: 0.16, fill: { color: K.tintRed }, line: noLine() });
    txt(slide, tag, { x: 8.5, y: 2.0, w: 1.8, h: 0.32, fontSize: 10, bold: true, color: K.red, align: "center", valign: "middle", charSpacing: 1 });
    txt(slide, checkpoint.title || "Expected output", { x: 8.5, y: 2.5, w: 3.9, h: 0.45, fontSize: 20, bold: true, color: K.text, valign: "middle" });
    txt(slide, checkpoint.items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < checkpoint.items.length - 1 } })),
      { x: 8.5, y: 3.1, w: 3.95, h: 2.3, fontSize: 15, color: K.text2, paraSpaceAfter: 8 });
  }
  if (note) navyBar(slide, note);
  return slide;
}

// ---------- 13. Checklist ----------
// items: maks 8 string, 2 kolom
function addChecklistSlide(pptx, { eyebrow = "Checklist", title, items, footerNote, notes }) {
  const slide = addContentSlide(pptx, { eyebrow, title, notes });
  items.slice(0, 8).forEach((t, i) => {
    const col = i % 2, row = Math.floor(i / 2), x = 0.6 + col * 6.17, y = 1.7 + row * 1.0;
    card(slide, x, y, 5.96, 0.8, K.white, 0.06);
    slide.addShape("roundRect", { x: x + 0.3, y: y + 0.25, w: 0.3, h: 0.3, rectRadius: 0.04, fill: { color: K.white }, line: { color: K.navy, width: 1.5 } });
    txt(slide, t, { x: x + 0.85, y, w: 4.9, h: 0.8, fontSize: 15, color: K.text, valign: "middle" });
  });
  const rows = Math.ceil(Math.min(items.length, 8) / 2);
  if (footerNote) txt(slide, footerNote, { x: 0.6, y: 1.7 + rows * 1.0 + 0.2, w: 12.13, h: 0.45, fontSize: 14, color: K.text2, valign: "middle" });
  return slide;
}

// ---------- 14. Closing ----------
// v1: ringkasan poin di background navy + next step
function addClosingSlide(pptx, { eyebrow = "Ringkasan", title, points = [], nextStep, nextLabel = "Sesi berikutnya", notes }) {
  const slide = pptx.addSlide({ masterName: M_DARK });
  decor(pptx, slide);
  txt(slide, eyebrow.toUpperCase(), { x: 0.9, y: 1.7, w: 8.0, h: 0.4, fontSize: 18, bold: true, color: K.onDark, charSpacing: 6, valign: "middle" });
  txt(slide, title, { x: 0.9, y: 2.15, w: 9.2, h: 1.1, fontSize: fitSize(title, 9.2, 40, 26), bold: true, color: K.onDark, valign: "middle" });
  if (points.length) txt(slide, points.map((p, k) => ({ text: p, options: { bullet: true, breakLine: k < points.length - 1 } })),
    { x: 0.9, y: 3.45, w: 9.6, h: 2.3, fontSize: 17, color: K.onDark, paraSpaceAfter: 8 });
  if (nextStep) txt(slide, labeled(`${nextLabel}: ${nextStep}`, K.red, K.onDark), { x: 0.9, y: 6.0, w: 10.8, h: 0.5, fontSize: 16, valign: "middle" });
  if (notes) slide.addNotes(notes);
  return slide;
}

// Terima kasih / Q&A
function addThankYouSlide(pptx, { eyebrow = "Q & A", title = "Terima Kasih", subtitle = "Pertanyaan dan diskusi", lines = [], contact, notes }) {
  const slide = pptx.addSlide({ masterName: M_DARK });
  decor(pptx, slide);
  txt(slide, eyebrow.toUpperCase(), { x: 0.9, y: 2.3, w: 8.0, h: 0.4, fontSize: 18, bold: true, color: K.onDark, charSpacing: 6, valign: "middle" });
  txt(slide, title, { x: 0.9, y: 2.75, w: 9.2, h: 1.45, fontSize: fitSize(title, 9.2, 72, 40), bold: true, color: K.onDark, valign: "middle" });
  if (subtitle) txt(slide, subtitle, { x: 0.9, y: 4.2, w: 9.2, h: 0.5, fontSize: 24, bold: true, color: K.red, valign: "middle" });
  lines.forEach((l, i) => txt(slide, labeled(l, K.onDark, K.onDark), { x: 0.9, y: 5.1 + i * 0.4, w: 9.6, h: 0.4, fontSize: 16, valign: "middle" }));
  if (contact) txt(slide, contact, { x: 0.9, y: 5.2 + Math.max(lines.length, 1) * 0.4 + 0.1, w: 8.0, h: 0.4, fontSize: 16, bold: true, color: K.onDark, valign: "middle" });
  if (notes) slide.addNotes(notes);
  return slide;
}

module.exports = {
  // deck
  newDeck, save, addContentSlide, addContentHeader, setPhotoDir,
  // komponen
  addCoverSlide, addSectionSlide, addDividerSlide, addAgendaSlide, addCardGridSlide,
  addNumberedListSlide, addStatSlide, addComparisonTableSlide, addTwoPanelSlide, addBeforeAfterSlide,
  addTimelineSlide, addLabelRowsSlide, addCodeSlide, addStepsCheckpointSlide, addChecklistSlide,
  addClosingSlide, addThankYouSlide, addPhotoSlide,
  // util
  hex, card, txt, COLORS: K, FONT, FONT_CODE,
};
