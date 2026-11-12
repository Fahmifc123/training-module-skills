---
name: insignia-image-gen
description: Cari dan unduh foto stok dari Unsplash API untuk slide training Insignia (cover, section divider, ilustrasi suasana), lengkap dengan atribusi fotografer, lalu sisipkan ke deck lewat insignia-ppt-deck. Pakai skill ini saat diminta mencari foto/gambar stok untuk slide atau materi training.
---

# Insignia Image (Foto Stok Unsplash)

Skill ini mengambil foto stok dari Unsplash untuk kebutuhan visual non-teknis di deck: cover, section divider, slide pembuka/penutup. Untuk diagram, alur pipeline, atau arsitektur, pakai `html-to-png-render`, bukan foto stok.

## Aturan konten

- Default orientasi `landscape`, lebar 1920 px (cocok slide 16:9).
- Query dalam bahasa Inggris, konkret dan visual (misal `server room`, `team collaboration laptop`), bukan istilah abstrak (`big data`).
- Hindari foto dengan teks/logo merek yang menonjol dan wajah close-up yang jadi fokus utama.
- Atribusi wajib (ketentuan Unsplash): tulis `credit_text` di pojok foto (ukuran kecil) atau kumpulkan di slide kredit akhir deck.
- Setelah unduh, cek visual tiap foto dengan Read sebelum dipakai; buang yang tidak cocok.

## Setup

Access Key Unsplash disimpan di env var `UNSPLASH_ACCESS_KEY` (sudah di-set via `setx`). Script juga membaca registry user Windows, jadi tidak perlu restart terminal. Mode Demo dibatasi 50 request/jam; satu foto = 2 request (search dihitung sekali per pemanggilan + 1 trigger download per foto).

Tidak ada dependency; cukup Python 3 standard library.

## Pemakaian

```bash
python .claude/skills/insignia-image-gen/unsplash_fetch.py "<query>" <output_dir> [--count 3] [--orientation landscape] [--prefix nama] [--width 1920]
```

Contoh, kandidat cover Sesi 6:

```bash
python .claude/skills/insignia-image-gen/unsplash_fetch.py "server room" output/sesi-6/assets/photos --count 4 --prefix cover-sesi6
```

Output:
- `<prefix>-01.jpg`, `<prefix>-02.jpg`, ...
- `CREDITS.json` (dipakai kode deck) dan `CREDITS.md` (dibaca manusia), di-merge kalau dijalankan berkali-kali di folder yang sama.

## Banyak slide sekaligus (hemat kuota)

Untuk mengisi satu deck atau lebih, pakai `unsplash_batch.py`. Preview diunduh dari CDN (tidak memotong kuota API), hanya foto terpilih yang di-trigger:

```bash
python .claude/skills/insignia-image-gen/unsplash_batch.py candidates plan.json <work_dir> --per 4   # 1 request per slot
# lihat <work_dir>/sheet_<grup>.jpg, isi "pick" di plan.json
python .claude/skills/insignia-image-gen/unsplash_batch.py finalize plan.json <work_dir>             # 1 request per foto
```

Keduanya aman diulang dan berhenti rapi saat kuota habis (HTTP 403); jalankan lagi setelah 1 jam.

## Cara cepat di deck: `setPhotoDir`

`insignia_deck_lib.js` punya `L.setPhotoDir(dir)`. Panggil sebelum `L.newDeck(...)`: cover memakai `dir/cover.jpg`, section divider ke-N memakai `dir/section-N.jpg`, dengan overlay navy, logo, dan kredit dari `CREDITS.json` otomatis. File yang tidak ada dilewati. Deck Big_Data_Rebuild menyimpan foto di `_build/photos/`.

## Menyisipkan manual ke deck (pptxgenjs)

```javascript
const credits = require("./output/sesi-6/assets/photos/CREDITS.json");
const c = credits.find((x) => x.file === "cover-sesi6-02.jpg");

slide.addImage({
  path: "output/sesi-6/assets/photos/" + c.file,
  x: 0, y: 0, w: 13.333, h: 7.5,
  sizing: { type: "cover", w: 13.333, h: 7.5 },
});
// Overlay navy semi-transparan supaya teks putih tetap terbaca
slide.addShape("rect", { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: "0B1F3A", transparency: 35 } });
slide.addText(c.credit_text, { x: 9.3, y: 7.05, w: 3.9, h: 0.3, fontSize: 8, color: "FFFFFF", align: "right" });
```

Sesuaikan warna overlay dengan `brand/colors.json` dan ukuran slide dengan layout di `insignia-ppt-deck`.

## Checklist sebelum mengirim

- Tiap foto sudah dicek visual dan relevan dengan slide.
- Atribusi tampil di slide atau di slide kredit akhir.
- Foto disimpan di `output/<nama-modul>/assets/photos/`, bukan di root.
- Foto yang tidak dipakai dihapus beserta entrinya di `CREDITS.json`.

## Keputusan manusia: wajib lewat grill-me

Setiap kali muncul keputusan yang menjadi hak Fahmi (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu kelas, gaya), jangan memutuskan sendiri dan jangan menumpuk pertanyaan di akhir laporan. Langsung panggil skill `grill-me` (Skill tool), selesaikan wawancara dan Decision Log-nya, baru lanjut bekerja. Pemilihan foto final untuk slide termasuk keputusan gaya milik Fahmi; tunjukkan kandidat, biarkan Fahmi memilih. Keputusan teknis murni tetap diputuskan sendiri dan cukup dilaporkan.
