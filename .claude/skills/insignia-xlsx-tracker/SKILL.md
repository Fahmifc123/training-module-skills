---
name: insignia-xlsx-tracker
description: Buat atau update file Excel (.xlsx) Insignia memakai openpyxl dengan dua pola. Pola Tracker untuk operasional training (alokasi akun, kehadiran, progres peserta). Pola Modul Sheet untuk modul preparation self-study yang dibagikan ke HR (format DE: tab Training Modules 13 kolom dan tab Legend). Pakai skill ini setiap kali diminta membuat tracker Excel atau modul sheet Insignia.
---

# Insignia Excel (Tracker dan Modul Sheet)

Jika pengguna meminta paket lengkap atau menyebut Brief, gunakan `insignia-training-module` sebagai pintu masuk; skill ini dipanggil olehnya.

Generator ada di `generate_xlsx.py` (folder skill ini). Jangan menulis ulang helper styling. Cukup siapkan `spec.json`, lalu jalankan generator.

```bash
pip install openpyxl
python "$TRAINING_KIT_HOME/.claude/skills/insignia-xlsx-tracker/generate_xlsx.py" demo output/_demo          # uji cepat
python "$TRAINING_KIT_HOME/.claude/skills/insignia-xlsx-tracker/generate_xlsx.py" tracker spec.json output/<nama>.xlsx
python "$TRAINING_KIT_HOME/.claude/skills/insignia-xlsx-tracker/generate_xlsx.py" modul-sheet spec.json output/<Nama_Program>/1_Modul_Sheet/<Nama_Modul>.xlsx
```

Warna dan font dibaca otomatis dari `<kit root>/brand/colors.json`. Path output relatif terhadap project root.

## Aturan konten

- Header Title Case, tanpa singkatan ambigu.
- Status hanya `Belum Mulai`, `Sedang Berjalan`, `Selesai`, berupa dropdown dengan conditional formatting. Tanpa emoji.
- Kolom yang menghitung (persentase, total) memakai formula Excel asli, bukan nilai hasil hitung manual.
- Istilah teknis tetap bahasa Inggris, label lain Bahasa Indonesia.

## Pola 1 - Tracker

```json
{
  "sheets": [{
    "name": "Tracker",
    "headers": ["No", "Nama Peserta", "Track", "Status", "Selesai", "Total", "Progress (%)"],
    "status_column": "Status",
    "rows": [[1, "Peserta A", "Data Engineering", "Sedang Berjalan", 3, 10, null]],
    "formula_columns": [{"header": "Progress (%)", "formula": "=E{row}/F{row}*100"}]
  }]
}
```

Beberapa kategori data dipisah per sheet (misalnya "DE Track" dan "DS Track").

## Pola 2 - Modul Sheet (format Modul Preparation)

Dipakai oleh mode Preparation di `insignia-training-module`. Formatnya mengikuti modul sheet DE yang sudah dibagikan ke HR.

**Tab `Training Modules`**, 13 kolom tetap: Modul, Sub Modul, Materi, Category, Learning Objectives, Difficulty, Output / Deliverable, Material Source, Internal Link PPT, Video Course Internal Link, External Link (Udemy, dll), Referensi Section Udemy, Status.

Pola baris per modul: sub modul bernomor (1.1, 1.2, ...), Mini Project (kategori Project), lalu **Test Modul N** (kategori Test) sebagai baris terakhir, kemudian satu baris kosong sebelum modul berikutnya. Nama modul ditulis di setiap baris.

**Tab `Legend`**: Kategori, Status Progress, Difficulty, Material Source (selalu ada), lalu `legend_extra` dan Alur Belajar dari spec.

Nilai baku (divalidasi generator, spec yang melanggar ditolak):
- Category: Concept, Setup, Hands-on, Project, Use Case, Capstone, Test, Review / Tanya Jawab
- Difficulty: Beginner, Intermediate, Advanced, All Levels, TBD
- Material Source: Internal, External, Blended. Internal atau Blended wajib punya link PPT atau Video. External atau Blended wajib punya External Link.
- Status: Belum Mulai, Sedang Berjalan, Selesai

```json
{
  "judul": "MLE Program",
  "alur_belajar": ["Belajar mandiri", "Tanya jawab dengan mentor (on-demand)", "Mini project, lalu Test Modul"],
  "legend_extra": [{"title": "Mode Belajar", "rows": [["Self-study", "Belajar mandiri"]]}],
  "modul": [{
    "nama": "Modul 1: Dify Foundations",
    "sub_modul": [
      {"sub_modul": "1.1 Orientasi Dify", "materi": "Agentic workflow, 4 jenis app",
       "category": "Concept", "objectives": "Satu kalimat atau list", "difficulty": "Beginner",
       "deliverable": "Akun aktif", "source": "Internal", "ppt": "Pengenalan_Dify.pptx",
       "video": "", "external": "", "referensi": "", "status": "Belum Mulai"},
      {"sub_modul": "Test Modul 1", "materi": "Quiz Konsep (1.1-1.x) + Rubrik Mini Project",
       "category": "Test", "objectives": "Validasi pemahaman Modul 1", "difficulty": "Intermediate",
       "source": "Internal", "ppt": "MLE_Test_Modul1.pptx"}
    ]
  }]
}
```

- Nilai berupa list otomatis menjadi teks multi-baris dengan bullet di dalam satu sel.
- Link yang belum tersedia (misalnya video belum direkam) dibiarkan kosong, jangan diisi placeholder. Jika validasi menolak karena link wajib kosong, laporkan ke pengguna, jangan mengarang link.
- Nama file di kolom Internal Link PPT harus sama persis dengan file di `2_Materi_Baru/` atau `3_Materi_Rujukan/`.

## Checklist sebelum diserahkan

- Generator berjalan tanpa error.
- File dibuka (atau dirender ke PDF lewat LibreOffice) dan dicek: tidak ada teks terpotong, tinggi baris cukup.
- Status berupa dropdown dengan warna yang benar.
- Output ada di `<project root>/output/...` sesuai mode.

## Aturan bersama

Patuhi `insignia-training-module/references/aturan-bersama.md` (bahasa, kode runnable, data sintetis, brand, path output, dan keputusan manusia lewat `grill-me`).
