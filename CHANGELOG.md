# Changelog

## v3.2.1 - 2026-11-18

### Diubah
- Orkestrator menyiapkan project root otomatis dari folder kosong: membuat `briefs/`, `materi_rujukan/`, `output/`, menyalin `CLAUDE.md`, `README.md`, `.gitignore` dari template, memindahkan Brief di root ke `briefs/` dan materi lama ke `materi_rujukan/`.
- Alur project di README dan file 06: cukup folder kosong, file Brief, lalu prompt.

## v3.2.0 - 2026-11-18

Skill global dan project terpisah dari repo skill.

### Ditambahkan
- `install_skills.bat`: memasang semua skill ke level user Claude Code lewat junction, set `TRAINING_KIT_HOME`, dan `npm install`.
- `new_project.bat`: membuat folder project selevel repo (`briefs/`, `materi_rujukan/`, `output/`, `CLAUDE.md`).
- `project-template/` dan `.gitattributes` (file .bat memakai CRLF).
- Aturan bersama bagian 0: kit root (aset) vs project root (Brief dan output).

### Diubah
- Orkestrator menjadi pintu masuk utama: deskripsi diperluas, cek awal kit root dan project root, skill turunan wajib dimuat lewat tool Skill.
- Skill ppt-deck, docx-module, xlsx-tracker merujuk ke orkestrator jika diminta paket lengkap.
- Generator docx dan xlsx mencari kit root lewat `TRAINING_KIT_HOME`, dengan cadangan lokasi asli skill.
- Path output menjadi `<project root>/output/<Paket>/`; script dipanggil dengan path lengkap dari kit root.
- Deck library di-require dari kit root.

## v3.1.0 - 2026-11-18

### Diubah
- Nama repo menjadi `training-module-skills`.
- Pola Modul Sheet mengikuti format modul sheet DE: tab Training Modules (13 kolom: Modul sampai Status) dan tab Legend. Pola baris: sub modul, Mini Project, Test Modul, baris kosong antar modul.
- Generator memvalidasi Category, Difficulty, Material Source, Status, link wajib per Material Source, dan Test Modul di akhir setiap modul.
- Status baku di kedua pola: Belum Mulai, Sedang Berjalan, Selesai (menggantikan `done` dan `Proses`). Kategori `Test` ditambahkan ke Legend.
- Template Brief Preparation disusun per Modul dan Sub Modul sesuai kolom sheet.
- Orkestrator mencari Brief di subfolder `briefs/<Workstream>/` dan membaca `_GLOSARIUM_*.md` bila ada.

### Ditambahkan
- File root dari kit v2: `insignia_deck_lib.js`, `generate_template_deck.js`, `package.json`, `package-lock.json`.
- Brief Big Data v3 revisi dan glosarium di `briefs/Big_Data/`.
- Arsip generator per sesi Big Data di `examples/Big_Data/generators/`.

## v3.0.0 - 2026-11-12

Perapian kit dan pindah ke repo Git.

### Ditambahkan
- Mode Preparation di `insignia-training-module` (modul sheet, materi baru, materi rujukan, Mentor Only).
- `references/aturan-bersama.md` sebagai satu sumber aturan lintas skill.
- Pola Modul Sheet dan generator `generate_xlsx.py` (dropdown status, wrap text, layout cetak landscape).
- Struktur Panduan Bagian dan generator `generate_docx.py` (warna dan logo dibaca dari `brand/`).
- Template `Brief_Live_Session_TEMPLATE.md` dan `Brief_Preparation_TEMPLATE.md`.
- README, CHANGELOG, `.gitignore`, dan teks pengganti file 03 dan 06 untuk Project claude.ai.

### Diubah
- Orkestrator: mode dipilih dari header Brief, struktur folder dibakukan per mode, path `output/<Workstream>/` menggantikan hardcode Big Data.
- Live Session: data dummy Starter Kit tidak lagi memakai skill tracker.
- Blok "Keputusan manusia" yang disalin di 6 skill diganti satu rujukan ke aturan bersama.
- Nama pengguna di skill dibuat generik.
- ppt-deck, image-gen: contoh dan path dibuat netral; durasi agenda mengikuti Brief.
- docx-module: jumlah section diperbaiki (5 heading), path output konsisten, warna tidak lagi di-hardcode.
- xlsx-tracker: path `colors.json` konsisten dengan kode.

### Diperbaiki
- Bug `freeze_panes` di generator xlsx yang membuat data mulai di baris 3.

### Dihapus
- `__pycache__` di image-gen.

## v2 - sebelum repo

Kit dibagikan sebagai `insignia-training-assets-v2.zip`. Isinya tersimpan di commit baseline.
