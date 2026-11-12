---
name: insignia-training-module
description: Orkestrasi pembuatan 1 paket modul training Insignia secara bertahap (outline, PPT, Modul Praktikum, Starter Kit Peserta, Instructor Only), mengikuti struktur folder yang sudah dipakai di modul-modul Insignia sebelumnya. Pakai skill ini saat diminta membuat paket modul training LENGKAP, bukan cuma satu file.
---

# Insignia Training Module — Orkestrator

Skill ini mengatur alur kerja bertahap untuk membuat satu paket modul training lengkap, mengikuti pola yang konsisten dipakai di modul Insignia sebelumnya (AI-DLC for DE, Prompt Engineering Fundamentals, Use Case Verona Chatbot, Use Case FIANA). Jangan generate semua file sekaligus dalam satu lompatan — kerjakan fase demi fase, berhenti di tiap decision gate untuk konfirmasi, supaya mudah di-review secara iteratif (sesuai gaya review Fahmi: detail, dan inkonsistensi langsung ditandai, bukan ditunggu sampai akhir).

## Struktur folder output standar

```
<nama-modul>/
├── 00_Materi/                      # atau "1_PPT" tergantung konvensi — tanya user di Fase 0
│   └── <Nama_Modul>.pptx
├── 0_Modul_Latihan_Bertingkat/     # opsional, hanya untuk modul use-case dengan beberapa level kesulitan
│   └── Modul_Praktikum_Latihan_<Nama>.docx
├── 2_Modul_Praktikum/
│   └── Modul_Praktikum_<Nama>.docx
├── 3_Starter_Kit_Peserta/
│   └── <file-file yang didownload peserta sebelum sesi>
└── 4_Instructor_Only/
    ├── Answer_Key_Expected_Output.md
    └── <kode referensi / jawaban yang TIDAK dibagikan ke peserta>
```

Catatan: penomoran folder di modul Insignia sebelumnya tidak 100% seragam (ada yang pakai `00_Materi` + `01_Starter_Peserta` + `02_Reference_Run_Trainer`, ada yang pakai `1_PPT` + `2_Modul_Praktikum` + `3_Starter_Kit_Peserta` + `4_Instructor_Only`). Di Fase 0, konfirmasi ke user konvensi mana yang mau dipakai untuk modul ini, atau pakai default `1_PPT` / `2_Modul_Praktikum` / `3_Starter_Kit_Peserta` / `4_Instructor_Only` kalau tidak disebutkan.

## Fase pengerjaan

Kerjakan fase 0 sampai 4 secara berurutan. Setiap fase diakhiri satu baris ringkas + pertanyaan konfirmasi sebelum lanjut ke fase berikutnya, kecuali user sudah bilang di awal untuk jalan terus tanpa konfirmasi per fase.

### Fase 0 — Intake & Outline

**Cek Brief dulu.** Sebelum bertanya apa pun, cari file Brief di folder `briefs/`:
- Jika user menyebut sesi (misal "Sesi 1"), baca `briefs/Brief_Sesi_01_*.md`. Jika user menyebut nama file, baca file itu.
- Jika ada lebih dari satu file yang cocok, tanya user mana yang dipakai.
- Brief dibuat di Project claude.ai dan sudah disetujui. Pakai isinya apa adanya: jangan mengubah tujuan belajar, agenda, dataset, atau angka checkpoint tanpa persetujuan user.
- Tanyakan hanya bidang yang kosong. Bidang "Bentuk notebook peserta" menentukan isi Starter Kit: "lengkap" berarti notebook peserta sama dengan SOLUTION tanpa bagian kosong, "ada bagian latihan yang dikosongkan" berarti pakai `___` dan solusinya di Instructor Only.
- Jika Brief bertentangan dengan dirinya sendiri (misal total agenda bukan 120 menit, atau istilah berbeda antar bagian), sebutkan dan tanya sebelum lanjut.
- Folder output default untuk program Big Data: `output/Big_Data/Sesi_NN_<Judul>/` dengan 4 folder standar.
- Rangkum Brief dalam 5-8 baris sebagai konfirmasi Fase 0, lalu lanjut ke Fase 1 setelah user setuju.

Tanpa Brief, kumpulkan dulu sebelum generate apa pun:
- Nama modul dan satu kalimat deskripsi.
- Track: Data Engineering / Data Science / lintas-track.
- Use case konkret yang dipakai sebagai konteks hands-on (kalau ada).
- Target durasi sesi dan rentang waktu tiap bagian (dipakai di agenda PPT).
- Tool yang dipakai peserta (Claude Code, Dify, dsb).
- Apakah modul butuh varian "Latihan Bertingkat" (beberapa level kesulitan) atau cukup satu level.

Tulis ringkasan ini sebagai outline singkat di awal respons (bukan file terpisah, cukup di chat/markdown block) dan konfirmasi ke user sebelum lanjut ke Fase 1. Kalau user sudah kasih semua info ini di prompt awal, boleh skip tanya ulang dan langsung rangkum untuk konfirmasi cepat.

### Fase 1 — PPT

Panggil skill `insignia-ppt-deck` dan ikuti struktur deck standar di skill itu: cover, agenda (rentang waktu dari Fase 0), tujuan pembelajaran, section divider per bagian, slide konsep dengan komponen yang bervariasi, code slide dan slide langkah + checkpoint untuk tiap hands-on block, checklist, ringkasan, dan penutup. Acuan visual: `brand/slide-templates/Template_Training_Insignia.pdf`.

Tulis output ke `<nama-modul>/1_PPT/<Nama_Modul>.pptx` (atau `00_Materi/` kalau user pilih konvensi itu di Fase 0).

### Fase 2 — Modul Praktikum

Panggil skill `insignia-docx-module`. Isi `STEPS` di kode referensi skill itu dengan langkah konkret sesuai use case dari Fase 0 — setiap sub-langkah harus instruksi aksi nyata (nama tombol/menu persis), bukan deskripsi umum, dan setiap Langkah diakhiri CHECKPOINT yang bisa diverifikasi.

Kalau Fase 0 menandai modul butuh "Latihan Bertingkat", buat juga versi kedua di `0_Modul_Latihan_Bertingkat/` dengan level kesulitan bertingkat (lebih banyak tugas mandiri, lebih sedikit instruksi step-by-step, dibanding versi utama di `2_Modul_Praktikum/`).

Tulis output ke `<nama-modul>/2_Modul_Praktikum/Modul_Praktikum_<Nama>.docx`.

### Fase 3 — Starter Kit Peserta

File yang peserta download/siapkan SEBELUM sesi dimulai — data dummy, template kosong, file requirement, atau starter code yang belum lengkap (bukan jawaban). Format file tergantung kebutuhan: bisa `.docx` (dokumen kasus/brief), `.csv`/`.xlsx` (data dummy), `.py`/`.md` (starter code/instruksi setup).

Kalau ada data dummy yang perlu dibuat, pakai skill `insignia-xlsx-tracker` sebagai basis kalau formatnya tabel, atau tulis langsung sebagai file data biasa kalau bukan tracker.

Tulis output ke `<nama-modul>/3_Starter_Kit_Peserta/`.

### Fase 4 — Instructor Only

Materi yang TIDAK dibagikan ke peserta: kunci jawaban/expected output, kode referensi lengkap yang jadi solusi (termasuk yang direferensikan di Modul Praktikum Fase 2, misal kode yang diminta peserta "copy dari file yang diberikan mentor"), catatan tambahan untuk trainer (pertanyaan yang sering muncul, perbedaan istilah antar tool, dsb).

Minimal satu file `Answer_Key_Expected_Output.md` berisi hasil/angka yang diharapkan di tiap CHECKPOINT dari Modul Praktikum Fase 2 — supaya trainer bisa verifikasi cepat hasil peserta.

Tulis output ke `<nama-modul>/4_Instructor_Only/`.

## Prinsip lintas fase

- Konsistensi penamaan use case, angka, dan istilah antara PPT (Fase 1), Modul Praktikum (Fase 2), Starter Kit (Fase 3), dan Instructor Only (Fase 4) harus persis sama — kalau Modul Praktikum merujuk file tertentu dari Starter Kit, pastikan file itu benar-benar dibuat di Fase 3 dengan nama yang sama persis.
- Checkpoint di Modul Praktikum (Fase 2) harus punya jawaban yang eksplisit di Answer Key (Fase 4) — jangan buat checkpoint yang tidak bisa diverifikasi.
- Semua file memakai `brand/colors.json` dan logo dari folder `brand/` yang sama (lihat skill `insignia-ppt-deck` dan `insignia-docx-module` untuk detail pemakaian).
- Kalau user minta revisi di satu fase setelah fase berikutnya sudah jadi, cek ulang dampaknya ke fase lain (misal ganti nama use case di Fase 0 setelah PPT jadi → ikut update Modul Praktikum, Starter Kit, dan Instructor Only) — jangan biarkan inkonsistensi antar file dalam satu paket.

## Keputusan manusia: wajib lewat grill-me

Setiap kali muncul keputusan yang menjadi hak Fahmi (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu kelas, gaya), jangan memutuskan sendiri dan jangan menumpuk pertanyaan di akhir laporan. Langsung panggil skill `grill-me` (Skill tool), selesaikan wawancara dan Decision Log-nya, baru lanjut bekerja. Keputusan teknis murni tetap diputuskan sendiri dan cukup dilaporkan.
