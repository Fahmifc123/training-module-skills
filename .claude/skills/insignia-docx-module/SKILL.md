---
name: insignia-docx-module
description: Buat dokumen .docx training Insignia dengan dua struktur. Modul Praktikum untuk sesi live (panduan langkah demi langkah dengan CHECKPOINT). Panduan Bagian untuk modul preparation self-study (tujuan, konsep singkat, langkah, bukti selesai). Pakai skill ini saat diminta membuat Modul Praktikum, panduan belajar mandiri, atau dokumen langkah demi langkah, bukan slide.
---

# Insignia DOCX (Modul Praktikum dan Panduan Bagian)

Jika pengguna meminta paket lengkap atau menyebut Brief, gunakan `insignia-training-module` sebagai pintu masuk; skill ini dipanggil olehnya.

Generator ada di `generate_docx.py` (folder skill ini). Jangan menulis ulang helper styling. Cukup siapkan `spec.json`, lalu jalankan generator.

```bash
pip install python-docx
python "$TRAINING_KIT_HOME/.claude/skills/insignia-docx-module/generate_docx.py" demo output/_demo
python "$TRAINING_KIT_HOME/.claude/skills/insignia-docx-module/generate_docx.py" modul-praktikum spec.json output/Sesi_NN_<Judul>/2_Modul_Praktikum/Modul_Praktikum_<Judul>.docx
python "$TRAINING_KIT_HOME/.claude/skills/insignia-docx-module/generate_docx.py" panduan-bagian spec.json output/<Nama_Program>/2_Materi_Baru/Panduan_Bagian_NN_<Judul>.docx
```

Warna, font, dan logo dibaca otomatis dari `<kit root>/brand/`. Path output relatif terhadap project root.

## Struktur 1 - Modul Praktikum (mode Live Session)

Urutan heading tetap (5 heading setelah blok judul):
1. Tujuan Pembelajaran: 3-5 bullet, diawali "Peserta mampu ..." atau "Peserta memahami ...".
2. Gambaran Alur (judul bisa diganti lewat `overview_heading`): alur end-to-end dan constraint penting.
3. Persiapan Sebelum Mulai: checklist akun, tool, dan file Starter Kit.
4. Langkah Mengerjakan (Detail): Langkah N dengan sub-langkah N.1, N.2, dan seterusnya, diakhiri CHECKPOINT.
5. Latihan Mandiri.

Spec: `title, subtitle, objectives[], overview, prep[], steps[], self_practice[]`, opsional `kicker, overview_heading, footer`.

## Struktur 2 - Panduan Bagian (mode Preparation)

Untuk satu bagian modul self-study. Peserta membaca tanpa mentor, jadi ada bagian konsep singkat:
1. Tujuan
2. Konsep Singkat: 2-5 subjudul, masing-masing satu paragraf pendek.
3. Persiapan
4. Langkah Mengerjakan: sama dengan Modul Praktikum, lengkap dengan CHECKPOINT.
5. Bukti Selesai: harus sama dengan kolom Output / Deliverable di modul sheet.
6. Latihan Mandiri

Spec: `title, subtitle, objectives[], concepts[{heading, body}], prep[], steps[], evidence[], self_practice[]`.

## Format langkah (kedua struktur)

```json
{"title": "Panggil Workflow API", "substeps": ["Buka menu API Access.", "Salin API key."],
 "code": "print('kode lengkap dan runnable')", "checkpoint": "Terminal menampilkan status 200."}
```

## Aturan konten

- Setiap sub-langkah adalah satu aksi nyata dengan nama tombol atau menu persis.
- CHECKPOINT bisa diverifikasi secara visual atau dengan angka ("output menunjukkan 5"), bukan "pastikan sudah benar".
- Kode di `code` dijalankan dulu sebelum dimasukkan. File yang dirujuk harus ada di Starter Kit, Materi Baru, Instructor Only, atau Mentor Only.

## Checklist sebelum diserahkan

- Semua heading struktur ada, sesuai urutan.
- Setiap Langkah diakhiri CHECKPOINT, dan setiap CHECKPOINT punya jawaban di answer key.
- Dokumen dirender (LibreOffice ke PDF) dan dicek visual.
- Output ada di folder sesuai mode.

## Aturan bersama

Patuhi `insignia-training-module/references/aturan-bersama.md` (bahasa, kode runnable, data sintetis, brand, path output, dan keputusan manusia lewat `grill-me`).
