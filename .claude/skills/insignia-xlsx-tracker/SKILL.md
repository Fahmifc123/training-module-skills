---
name: insignia-xlsx-tracker
description: Buat atau update file Excel (.xlsx) Insignia memakai openpyxl dengan dua pola. Pola Tracker untuk operasional training (alokasi akun, kehadiran, progres peserta). Pola Modul Sheet untuk modul preparation self-study (satu baris per bagian berisi topics, objective, deliverable, bukti selesai, materi, kriteria cek mentor). Pakai skill ini setiap kali diminta membuat tracker Excel atau modul sheet Insignia.
---

# Insignia Excel (Tracker dan Modul Sheet)

Generator ada di `generate_xlsx.py` (folder skill ini). Jangan menulis ulang helper styling. Cukup siapkan `spec.json`, lalu jalankan generator.

```bash
pip install openpyxl
python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py demo output/_demo          # uji cepat
python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py tracker spec.json output/<Workstream>/<nama>.xlsx
python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py modul-sheet spec.json output/<Workstream>/<Nama_Modul>/1_Modul_Sheet/<Nama_Modul>.xlsx
```

Warna dan font dibaca otomatis dari `brand/colors.json` di root repo.

## Aturan konten

- Header Title Case, tanpa singkatan ambigu.
- Status hanya `Belum Mulai`, `Proses`, `Selesai`, berupa dropdown dengan conditional formatting. Tanpa emoji.
- Kolom yang menghitung (persentase, total) memakai formula Excel asli, bukan nilai hasil hitung manual.
- Istilah teknis tetap bahasa Inggris, label lain Bahasa Indonesia.

## Pola 1 - Tracker

```json
{
  "sheets": [{
    "name": "Tracker",
    "headers": ["No", "Nama Peserta", "Track", "Status", "Selesai", "Total", "Progress (%)"],
    "status_column": "Status",
    "rows": [[1, "Peserta A", "Data Engineering", "Proses", 3, 10, null]],
    "formula_columns": [{"header": "Progress (%)", "formula": "=E{row}/F{row}*100"}]
  }]
}
```

Beberapa kategori data dipisah per sheet (misalnya "DE Track" dan "DS Track").

## Pola 2 - Modul Sheet

Dipakai oleh mode Preparation di `insignia-training-module`. Hasilnya tiga tab:
- `Start here`: judul, subjudul, dan pasangan label-isi (tujuan, target peserta, cara mengerjakan, aturan, kontak).
- `Modul`: satu baris per bagian, wrap text, tinggi baris menyesuaikan isi, kolom Status berupa dropdown.
- `Materi` (opsional): daftar file materi dan lokasinya.

```json
{
  "start_here": {
    "judul": "Onboarding MLE - Dify",
    "subjudul": "Modul preparation self-study",
    "items": [["Target peserta", "Junior dan intern MLE"],
              ["Cara mengerjakan", ["Kerjakan berurutan", "Isi Status", "Kirim bukti ke mentor"]]]
  },
  "bagian": [{
    "blok": "Foundations", "bagian": "Orientasi Dify",
    "topics": ["Agentic workflow", "Chatflow vs Workflow"],
    "objective": "Satu kalimat.",
    "deliverable": ["Akun aktif", "Latihan L1 selesai"],
    "bukti": "Screenshot", "dataset": "Teks contoh", "materi": "Pengenalan_Dify.pptx",
    "kriteria": "Sesuai checkpoint L1"
  }],
  "materi": [{"file": "Pengenalan_Dify.pptx", "jenis": "Rujukan", "lokasi": "3_Materi_Rujukan/", "bagian": "1"}]
}
```

- Nilai berupa list otomatis menjadi teks multi-baris dengan bullet di dalam satu sel.
- Kolom default: No, Blok, Bagian, Topics, Objective, Deliverable, Bukti Selesai, Dataset / Sumber, Materi, Kriteria Cek Mentor, Status, Catatan. Jika Brief menentukan kolom lain, tambahkan `"columns": [{"header": "...", "key": "...", "width": 30}]`.
- Isi kolom Materi harus sama persis dengan nama file di `2_Materi_Baru/` atau `3_Materi_Rujukan/`.

## Checklist sebelum diserahkan

- Generator berjalan tanpa error.
- File dibuka (atau dirender ke PDF lewat LibreOffice) dan dicek: tidak ada teks terpotong, tinggi baris cukup.
- Status berupa dropdown dengan warna yang benar.
- Output ada di `output/<Workstream>/...` sesuai mode.

## Aturan bersama

Patuhi `insignia-training-module/references/aturan-bersama.md` (bahasa, kode runnable, data sintetis, brand, path output, dan keputusan manusia lewat `grill-me`).
