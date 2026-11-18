# Panduan Claude Code dengan Skill training-module-skills

Dipakai setelah Brief disetujui di Project. Claude Code membuat file jadi dari Brief. Kit disimpan di repo GitHub `training-module-skills`.

## 1. Setup satu kali
1. Clone repo `https://github.com/Fahmifc123/training-module-skills.git` ke `Documents\github\`.
2. Jalankan `install_skills.bat` dari folder repo: skill dipasang global (junction ke `%USERPROFILE%\.claude\skills\`), `TRAINING_KIT_HOME` di-set, dan `npm install` dijalankan.
3. `pip install python-docx openpyxl`, lalu buka ulang terminal.
4. Update skill: `git pull` di folder repo. Semua project otomatis memakai versi terbaru.

Repo skill (kit root) dan folder project (project root) selalu terpisah. Project dibuat dengan `new_project.bat <Nama>` dan berada di sebelah repo.

## 2. Isi skill

| Skill | Hasil |
|---|---|
| insignia-training-module | Pintu masuk utama. Orkestrator dua mode yang memanggil skill lain |
| insignia-ppt-deck | Deck .pptx dengan komponen Insignia |
| insignia-docx-module | .docx: Modul Praktikum (live) dan Panduan Bagian (preparation) |
| insignia-xlsx-tracker | .xlsx: Tracker operasional dan Modul Sheet |
| html-to-png-render | HTML ke PNG via Playwright |
| insignia-image-gen | Foto stok Unsplash dengan atribusi |
| grill-me | Wawancara keputusan milik pengguna sebelum file diubah |

## 3. Prompt untuk paket lengkap

1. Unduh Brief dari Project dan taruh di `<project>\briefs\`. Materi lama yang dipakai ulang taruh di `<project>\materi_rujukan\`.
2. Jalankan `claude` dari folder project, lalu kirim:

```
Pakai skill insignia-training-module dengan brief briefs/<nama_file>.md
```

Mode dipilih otomatis dari baris pertama Brief:
- `BRIEF LIVE SESSION`: output ke `<project>/output/Sesi_NN_<Judul>/` (1_PPT, 2_Modul_Praktikum, 3_Starter_Kit_Peserta, 4_Instructor_Only).
- `BRIEF PREPARATION`: output ke `<project>/output/<Nama_Program>/` (1_Modul_Sheet format DE, 2_Materi_Baru, 3_Materi_Rujukan, 4_Mentor_Only).

Setiap fase berhenti untuk konfirmasi.

## 4. Prompt per jenis file (revisi atau tambahan)

```
Pakai skill insignia-ppt-deck. Revisi deck di [path]: [daftar perubahan].
```
```
Pakai skill insignia-docx-module. Perbarui [Modul Praktikum | Panduan Bagian] di [path]: [daftar perubahan]. Pastikan semua checkpoint tetap punya jawaban di answer key.
```
```
Pakai skill insignia-xlsx-tracker pola modul sheet. Perbarui [path]: [daftar perubahan].
```

## 5. Setelah selesai
1. Jalankan skrip atau notebook SOLUTION dan cocokkan hasilnya dengan answer key.
2. Buka file hasil (PPT, docx, xlsx) dan cek tidak ada teks terpotong.
3. Bawa hasilnya ke Project untuk Mode Review.
4. Tempel revisi dari Project kembali ke Claude Code, ulangi sampai Definition of Done terpenuhi.
5. Minta blok Update Status di Project dan perbarui `04_Status_Tracker.md`.

## 6. Mengubah skill
Perubahan skill dilakukan lewat branch dan PR di repo, lalu dicatat di `CHANGELOG.md`. Aturan yang berlaku untuk semua skill diubah di `insignia-training-module/references/aturan-bersama.md`.
