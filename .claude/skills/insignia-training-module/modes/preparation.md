# Mode Preparation

Untuk modul self-study yang dibagikan dan dikerjakan mandiri (misalnya modul onboarding yang diwajibkan HR). Tidak ada agenda per menit. Pengecekan dilakukan lewat deliverable dan kriteria cek per bagian. Brief memakai header `BRIEF PREPARATION`, template di `briefs/templates/Brief_Preparation_TEMPLATE.md`.

## Struktur output (baku)

```
output/<Workstream>/<Nama_Modul>/
  1_Modul_Sheet/      <Nama_Modul>.xlsx
  2_Materi_Baru/      Panduan_Bagian_NN_<Judul>.docx, skrip dan file pendukung per bagian
  3_Materi_Rujukan/   salinan materi lama yang dirujuk + Daftar_Materi_Rujukan.md
  4_Mentor_Only/      Answer_Key.md, Rubrik_Penilaian.md, referensi solusi (DSL, kode)
```

## Fase 1 - Modul Sheet

Panggil `insignia-xlsx-tracker` dengan **pola Modul Sheet**. Satu baris per bagian. Kolom dan tab mengikuti bidang "Spesifikasi modul sheet" di Brief. Bila Brief tidak menyebut, pakai default:

- Tab `Start here`: tujuan modul, target peserta, cara mengerjakan, aturan (misalnya pemakaian AI assistant), kontak mentor.
- Tab `Modul`: No, Blok, Bagian, Topics, Objective, Deliverable, Bukti Selesai, Dataset / Sumber, Materi, Kriteria Cek Mentor, Status, Catatan.
- Tab `Materi`: daftar semua file materi (rujukan dan baru) beserta lokasi foldernya.

Isi sel Topics dan Deliverable memakai baris baru dengan awalan bullet, sama seperti contoh kurikulum yang ada.

## Fase 2 - Materi Baru

Untuk setiap bagian yang di Brief ditandai `Materi: baru`:
- Panggil `insignia-docx-module` dengan **struktur Panduan Bagian** (tujuan, konsep singkat, langkah dengan CHECKPOINT, latihan mandiri).
- Kode atau skrip ditulis lengkap, dijalankan, dan hasilnya dicatat untuk answer key.
- Diagram dibuat lewat `html-to-png-render`.

Nama file harus sama persis dengan isi kolom Materi di modul sheet.

## Fase 3 - Materi Rujukan

Untuk setiap bagian yang ditandai `Materi: dipakai ulang`:
- Salin file yang disebut Brief ke `3_Materi_Rujukan/` (pengguna menyediakan filenya, jangan membuat ulang).
- Tulis `Daftar_Materi_Rujukan.md`: nama file, bagian modul yang memakainya, bagian file yang perlu dibaca, dan catatan penyesuaian (misalnya padanan istilah antar platform).
- Jika file rujukan memuat nama klien atau data yang menurut Brief harus disamarkan, laporkan lokasinya dan selesaikan lewat `grill-me`. Jangan mengedit materi lama tanpa persetujuan.

## Fase 4 - Mentor Only

- `Answer_Key.md`: hasil yang diharapkan untuk setiap Bukti Selesai dan CHECKPOINT.
- `Rubrik_Penilaian.md`: kriteria dan skala untuk setiap deliverable proyek.
- Referensi solusi (DSL, kode) yang tidak dibagikan ke peserta.

## Definition of Done

- Setiap bagian di modul sheet punya Deliverable, Bukti Selesai, dan Kriteria Cek Mentor yang bisa diverifikasi.
- Setiap file yang disebut di kolom Materi benar-benar ada di `2_Materi_Baru/` atau `3_Materi_Rujukan/`.
- Semua skrip baru dijalankan tanpa error, hasilnya cocok dengan Answer Key.
- Setiap Bukti Selesai punya jawaban di Answer Key, dan setiap deliverable proyek punya rubrik.
- Modul sheet dibuka dan dicek: wrap text rapi, tidak ada sel terpotong.
- Aturan bersama terpenuhi.
