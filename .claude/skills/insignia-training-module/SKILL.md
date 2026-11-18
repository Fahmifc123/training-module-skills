---
name: insignia-training-module
description: Pintu masuk utama untuk semua pembuatan materi training Insignia. Orkestrator yang membuat paket materi bertahap dari sebuah Brief dan memanggil skill lain (ppt-deck, docx-module, xlsx-tracker, html-to-png-render, image-gen, grill-me) sesuai kebutuhan, dengan dua mode. Mode Live Session untuk satu sesi yang dibawakan mentor (PPT, Modul Praktikum, Starter Kit, Instructor Only). Mode Preparation untuk modul self-study yang dibagikan (misalnya onboarding via HR), dengan output modul sheet Excel, materi baru, materi rujukan, dan Mentor Only. Pakai skill ini setiap kali pengguna menyebut Brief, paket materi, modul sheet, modul preparation, sesi training, atau meminta lebih dari satu jenis file training sekaligus.
---

# Insignia Training Module - Orkestrator

Aturan lintas skill ada di `references/aturan-bersama.md`. Baca file itu sebelum mulai, terutama bagian 0 (kit root dan project root), dan patuhi di setiap fase.

## Cek awal

1. Tentukan kit root (`TRAINING_KIT_HOME`) dan project root (folder kerja saat ini). Laporkan keduanya dalam satu baris.
2. Jika `node_modules/pptxgenjs` tidak ada di kit root dan mode butuh PPT, minta pengguna menjalankan `npm install` di kit root.
3. Jika project root belum punya folder `briefs/`, `materi_rujukan/`, dan `output/`, buat ketiganya.

## Fase 0 - Intake dan pemilihan mode

1. Cari Brief di `<project root>/briefs/` (termasuk subfolder). Jika pengguna menyebut nama file, baca file itu. Jika menyebut sesi atau nama modul, cari file yang cocok. Jika ada lebih dari satu yang cocok, tanya pengguna. Jika di folder yang sama ada `_GLOSARIUM_*.md`, baca juga. Bila glosarium bertentangan dengan kalimat di Brief, glosarium yang berlaku.
2. Tentukan mode dari baris pertama Brief:
   - `BRIEF LIVE SESSION` (atau format lama `BRIEF SESI`): baca `modes/live-session.md`.
   - `BRIEF PREPARATION`: baca `modes/preparation.md`.
   - Jika tidak ada header yang dikenali, tanya pengguna mode mana yang dipakai.
3. Brief dibuat di Project claude.ai dan sudah disetujui. Pakai isinya apa adanya. Jangan mengubah tujuan, struktur, dataset, atau angka tanpa persetujuan pengguna.
4. Tanyakan hanya bidang yang kosong. Jika Brief bertentangan dengan dirinya sendiri, sebutkan konfliknya dan selesaikan lewat `grill-me`.
5. Rangkum Brief dalam 5-8 baris (mode, judul, output, folder tujuan), lalu tunggu konfirmasi sebelum Fase 1.

Tanpa Brief: jangan generate apa pun. Minta pengguna menyusun Brief di Project claude.ai memakai template di `<kit root>/briefs/templates/`.

## Fase 1 dan seterusnya

Ikuti fase di file mode yang terpilih. Setiap fase diakhiri ringkasan satu baris dan pertanyaan konfirmasi, kecuali pengguna sudah meminta jalan terus.

## Skill yang dipanggil

Skill di bawah wajib dimuat lewat tool Skill sebelum dipakai (jangan menulis ulang isinya dari ingatan). Skill ini yang memutuskan kapan masing-masing dipanggil, jadi pengguna cukup memanggil orkestrator.

| Kebutuhan | Skill |
|---|---|
| Deck .pptx | `insignia-ppt-deck` |
| Dokumen .docx (Modul Praktikum, panduan bagian) | `insignia-docx-module` |
| Excel (tracker, modul sheet, data tabel) | `insignia-xlsx-tracker` |
| Diagram atau visual HTML ke PNG | `html-to-png-render` |
| Foto stok untuk slide | `insignia-image-gen` |
| Keputusan milik pengguna | `grill-me` |

## Prinsip lintas fase

- Semua file dalam satu paket konsisten (lihat aturan bersama bagian 5).
- Setiap checkpoint atau kriteria cek punya jawaban eksplisit di answer key.
- Revisi di satu fase setelah fase berikutnya selesai wajib diikuti pengecekan dampak ke semua folder paket.
