# Changelog

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
