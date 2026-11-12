# Mode Live Session

Untuk satu sesi yang dibawakan mentor secara live (dan direkam). Brief memakai header `BRIEF LIVE SESSION`, template di `briefs/templates/Brief_Live_Session_TEMPLATE.md`.

## Struktur output (baku)

```
output/<Workstream>/Sesi_NN_<Judul>/
  0_Modul_Latihan_Bertingkat/   hanya jika Brief: Latihan Bertingkat = ya
  1_PPT/                        <Judul>.pptx
  2_Modul_Praktikum/            Modul_Praktikum_<Judul>.docx
  3_Starter_Kit_Peserta/        dataset, notebook peserta, README_Setup.md
  4_Instructor_Only/            Answer_Key_Expected_Output.md, Catatan_Trainer.md,
                                notebook SOLUTION, skrip generator dataset
```

`<Workstream>` diambil dari Brief (misalnya `Big_Data`). Jangan memakai konvensi folder lain.

## Fase 1 - PPT

Panggil `insignia-ppt-deck` dan ikuti struktur deck sesi live di skill itu. Agenda mengikuti rentang waktu di Brief (total durasi sesuai Brief, default 120 menit). Komponen slide per bagian mengikuti bidang "Komponen slide yang disarankan" di Brief.

## Fase 2 - Modul Praktikum

Panggil `insignia-docx-module` dengan struktur Modul Praktikum. Setiap sub-langkah adalah aksi nyata (nama tombol atau menu persis). Setiap Langkah diakhiri CHECKPOINT yang bisa diverifikasi.

Jika Brief meminta Latihan Bertingkat, buat juga `0_Modul_Latihan_Bertingkat/Modul_Praktikum_Latihan_<Judul>.docx`: satu konsep baru per level, level terakhir merujuk ke Modul Praktikum utama.

## Fase 3 - Starter Kit Peserta

File yang disiapkan peserta sebelum sesi: dataset sintetis, notebook peserta, `README_Setup.md`. Bidang "Bentuk notebook peserta" di Brief menentukan isinya:
- `lengkap`: notebook peserta sama dengan SOLUTION.
- `ada bagian latihan yang dikosongkan`: bagian latihan memakai `___`, solusinya di Instructor Only.

Dataset tabel dibuat dengan skrip Python (pandas atau csv), bukan lewat skill tracker. Skrip generatornya disimpan di Instructor Only.

## Fase 4 - Instructor Only

- `Answer_Key_Expected_Output.md`: hasil atau angka yang diharapkan di setiap CHECKPOINT.
- `Catatan_Trainer.md`: pesan kunci, pertanyaan yang sering muncul, risiko teknis dari Brief.
- Notebook SOLUTION, dijalankan penuh dari awal tanpa error.
- Skrip generator dataset.

## Definition of Done

- Keempat folder terisi, nama file konsisten dengan rujukan di Modul Praktikum.
- Setiap CHECKPOINT punya jawaban di Answer Key.
- Notebook SOLUTION jalan penuh, angka cocok dengan Answer Key.
- Slide dirender dan dicek: tidak ada teks terpotong.
- Aturan bersama terpenuhi (tanpa emoji, tanpa TODO, fakta dicek).
