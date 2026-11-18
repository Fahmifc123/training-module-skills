---
name: insignia-ppt-deck
description: Buat slide deck PowerPoint (.pptx) untuk materi training Insignia memakai pptxgenjs dan library insignia_deck_lib.js, mengikuti design system deck Insignia terbaru (cover navy dengan aksen segitiga, slide konten abu terang dengan kartu putih, eyebrow merah, footer copyright). Pakai skill ini setiap kali diminta membuat atau mengupdate deck training Insignia.
---

# Insignia PPT Deck

Jika pengguna meminta paket lengkap atau menyebut Brief, gunakan `insignia-training-module` sebagai pintu masuk; skill ini dipanggil olehnya.

Deck dibuat dengan memanggil komponen di `insignia_deck_lib.js` (kit root). Jangan menulis ulang geometri slide dari nol. Library sudah meniru deck asli `AI-DLC_Internal_Training_Insignia.pptx`.

Acuan visual wajib dilihat sebelum menyusun deck:
- `brand/slide-templates/Template_Training_Insignia.pdf` (15 slide, satu komponen per slide)
- `generate_template_deck.js` (kode yang menghasilkan template itu, contoh pemakaian setiap fungsi)

## Aturan konten

- Tanpa emoji atau ikon dekoratif. Tanda silang dan centang di Before/After adalah simbol fungsional dan boleh dipakai.
- Copy ringkas: satu ide per slide, bullet pendek. Penjelasan panjang masuk `notes` (speaker notes).
- Istilah teknis tetap bahasa Inggris, narasi Bahasa Indonesia.
- Kode di code slide harus lengkap dan runnable, maksimal 18 baris.
- Judul slide tanpa titik di akhir.
- Konten tidak muat: pecah ke slide lain. Jangan menambah teks melebihi batas item di tiap komponen.
- Angka dan fakta di slide harus punya sumber (pakai `source` di stat slide atau caption).

## Setup

```bash
npm install
```
`package.json` sudah berisi `pptxgenjs`. Library membaca warna dari `brand/colors.json` dan logo dari `brand/logo-light-bg.png` serta `brand/logo-dark-bg.png`.

## Struktur deck standar sesi live (mode Live Session)

Durasi agenda mengikuti Brief (default 120 menit). Di mode Preparation, deck baru hanya dibuat jika Brief memintanya; deck lama cukup dirujuk.

1. `addCoverSlide`
2. `addAgendaSlide` (rentang waktu dan durasi, total 120 menit)
3. `addCardGridSlide` (tujuan pembelajaran, dengan `footerNote` target akhir sesi)
4. Per bagian: `addSectionSlide`, lalu 2-5 slide konten (pilih komponen yang bervariasi)
5. Hands-on: `addCodeSlide` dan `addStepsCheckpointSlide` untuk setiap blok hands-on
6. `addChecklistSlide`
7. `addClosingSlide` (ringkasan dan sesi berikutnya), lalu `addThankYouSlide`

## API

Semua fungsi menerima `pptx` dan satu objek opsi, mengembalikan `slide`. Semua opsi menerima `notes` (speaker notes). Teks dengan pola `"Label: isi"` pada `footerNote`, `note`, `conclusion` otomatis memberi label merah tebal.

| Fungsi | Opsi | Batas |
|---|---|---|
| `newDeck(title, footerLabel)` | membuat deck LAYOUT_WIDE dengan 2 layout (konten terang, gelap) | panggil sekali per file |
| `save(pptx, filePath)` | menulis file dan membuat folder | |
| `addCoverSlide` | `eyebrow, title, subtitle, description, meta[{label,value}]` | meta maks 4 |
| `addSectionSlide` | `number, title, subtitle, items[]` | items 0-4 |
| `addAgendaSlide` | `title, items[{time, text, tag, duration}], note` | maks 8 baris. tag berisi "hands-on" merah, "konsep" abu biru |
| `addCardGridSlide` | `eyebrow, title, cards[{number, heading, body}], footerNote` | 2-4 kartu |
| `addNumberedListSlide` | `eyebrow, title, items[{heading, body}], quote, note` | 2-4 item |
| `addStatSlide` | `eyebrow, title, stats[{value, label, body, highlight}], conclusion, source` | 2-4 angka |
| `addComparisonTableSlide` | `eyebrow, title, headers[], rows[][], note` | maks 6 baris, 2-4 kolom |
| `addTwoPanelSlide` | `eyebrow, title, panels[{label, title, body, listLabel, items, code}], note` | 2 panel, panel kedua navy |
| `addBeforeAfterSlide` | `eyebrow, title, before{label, items}, after{label, items}, note` | maks 5 item per panel |
| `addTimelineSlide` | `eyebrow, title, steps[{label, description}], note` | 3-5 langkah |
| `addLabelRowsSlide` | `eyebrow, title, rows[{term, body, highlight}], note` | 3-5 baris |
| `addCodeSlide` | `eyebrow, title, language, code, caption` | maks 18 baris |
| `addStepsCheckpointSlide` | `eyebrow, title, steps[{heading, body}], checkpoint{title, items}, note` | 3-4 langkah |
| `addChecklistSlide` | `eyebrow, title, items[], footerNote` | maks 8 item |
| `addClosingSlide` | `eyebrow, title, points[], nextStep` | 3-5 poin |
| `addThankYouSlide` | `eyebrow, title, subtitle, lines[], contact` | |
| `addContentSlide` | `eyebrow, title` | slide kosong berheader untuk layout custom |
| `addDividerSlide` | API v1. Dengan `meta` menjadi cover, tanpa `meta` menjadi section divider (nomor diambil dari eyebrow, misal "Bagian 2") | |

Untuk layout custom di atas `addContentSlide`, pakai util `L.card(slide, x, y, w, h, fill)` dan `L.txt(slide, text, opts)` serta warna `L.COLORS` (navy, red, blue, bg, text, text2, muted, line, tintRed, tintBlue). Area konten aman: x 0.6 sampai 12.73, y 1.6 sampai 6.7.

## Contoh minimal

```javascript
const path = require("path");
const KIT = process.env.TRAINING_KIT_HOME;  // kit root, lihat aturan bersama bagian 0
const L = require(path.join(KIT, "insignia_deck_lib.js"));

async function main() {
  const pptx = L.newDeck("Contoh Workstream - Sesi 1");
  L.addCoverSlide(pptx, {
    title: "Contoh Workstream",
    subtitle: "Sesi 1 - Judul Sesi",
    description: "Satu kalimat tentang isi sesi.",
    meta: [
      { label: "Hari", value: "Isi dari Brief" },
      { label: "Durasi", value: "120 menit" },
    ],
  });
  L.addThankYouSlide(pptx, { contact: "Kontak: Mentor Data & AI" });
  await L.save(pptx, path.join(process.cwd(), "output", "Sesi_01_Judul_Sesi", "1_PPT", "Judul_Sesi.pptx"));
}
main();
```

## Checklist sebelum mengirim deck

- Semua slide dibuat lewat fungsi library, tidak ada warna atau font di luar `brand/colors.json`.
- Variasi komponen: tidak ada lebih dari 2 slide berurutan dengan komponen yang sama.
- Total durasi agenda sama dengan Brief dan cocok dengan alur slide.
- Kode di code slide sudah dijalankan dan output-nya cocok dengan checkpoint dan Answer Key.
- Deck dirender ke gambar (LibreOffice ke PDF ke PNG) dan dicek: tidak ada teks terpotong, tumpang tindih, atau kata terpecah di dua baris.
- File output ditulis ke `<project root>/output/Sesi_NN_<Judul>/1_PPT/`. Script generator deck disimpan di project root, bukan di kit root.

## Aturan bersama

Patuhi `insignia-training-module/references/aturan-bersama.md` (bahasa, kode runnable, data sintetis, brand, path output, dan keputusan manusia lewat `grill-me`).
