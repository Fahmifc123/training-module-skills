# Mode Preparation

Untuk modul self-study yang dibagikan dan dikerjakan mandiri (misalnya modul onboarding yang diwajibkan HR). Tidak ada agenda per menit. Pengecekan dilakukan lewat deliverable dan kriteria cek per bagian. Brief memakai header `BRIEF PREPARATION`, template di `briefs/templates/Brief_Preparation_TEMPLATE.md`.

## Struktur output (baku)

```
output/<Workstream>/<Nama_Modul>/
  1_Modul_Sheet/      <Nama_Program>_Modul_Preparation_Self_Study.xlsx
  2_Materi_Baru/      Panduan_Bagian_NN_<Judul>.docx, skrip dan file pendukung per bagian
  3_Materi_Rujukan/   salinan materi lama yang dirujuk + Daftar_Materi_Rujukan.md
  4_Mentor_Only/      Answer_Key.md, Rubrik_Penilaian.md, referensi solusi (DSL, kode)
```

## Fase 1 - Modul Sheet

Panggil `insignia-xlsx-tracker` dengan **pola Modul Sheet** (format DE): tab `Training Modules` 13 kolom dan tab `Legend`. Struktur modul, sub modul, Mini Project, dan Test Modul diambil dari Brief apa adanya. Nilai Category, Difficulty, Material Source, dan Status mengikuti nilai baku di skill tersebut.

Kolom link (PPT, Video, External, Referensi Section) diisi hanya dengan link atau nama file yang disebut Brief. Link yang belum ada dibiarkan kosong dan dilaporkan di ringkasan fase.

## Fase 2 - Materi Baru

Untuk setiap bagian yang di Brief ditandai `Materi: baru`:
- Panggil `insignia-docx-module` dengan **struktur Panduan Bagian** (tujuan, konsep singkat, langkah dengan CHECKPOINT, latihan mandiri).
- Kode atau skrip ditulis lengkap, dijalankan, dan hasilnya dicatat untuk answer key.
- Diagram dibuat lewat `html-to-png-render`.

Nama file harus sama persis dengan isi kolom Internal Link PPT di modul sheet.

## Fase 3 - Materi Rujukan

Untuk setiap bagian yang ditandai `Materi: dipakai ulang`:
- Salin file yang disebut Brief ke `3_Materi_Rujukan/` (pengguna menyediakan filenya, jangan membuat ulang).
- Tulis `Daftar_Materi_Rujukan.md`: nama file, bagian modul yang memakainya, bagian file yang perlu dibaca, dan catatan penyesuaian (misalnya padanan istilah antar platform).
- Jika file rujukan memuat nama klien atau data yang menurut Brief harus disamarkan, laporkan lokasinya dan selesaikan lewat `grill-me`. Jangan mengedit materi lama tanpa persetujuan.

## Fase 4 - Mentor Only

- `Answer_Key.md`: hasil yang diharapkan untuk setiap deliverable, CHECKPOINT, dan soal Test Modul.
- `Rubrik_Penilaian.md`: kriteria dan skala untuk setiap Mini Project.
- Referensi solusi (DSL, kode) yang tidak dibagikan ke peserta.

## Definition of Done

- Setiap sub modul di modul sheet punya Learning Objectives dan Output / Deliverable yang bisa diverifikasi; setiap modul diakhiri Test Modul.
- Setiap file di kolom Internal Link PPT benar-benar ada di `2_Materi_Baru/` atau `3_Materi_Rujukan/`.
- Semua skrip baru dijalankan tanpa error, hasilnya cocok dengan Answer Key.
- Setiap deliverable dan Test Modul punya jawaban di Answer Key, dan setiap Mini Project punya rubrik.
- Modul sheet dibuka dan dicek: wrap text rapi, tidak ada sel terpotong.
- Aturan bersama terpenuhi.
