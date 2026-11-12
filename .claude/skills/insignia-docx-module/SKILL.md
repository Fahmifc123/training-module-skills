---
name: insignia-docx-module
description: Buat dokumen Modul Praktikum (.docx) untuk training Insignia — panduan step-by-step dengan checkpoint, mengikuti struktur dokumen modul praktikum Insignia yang sudah ada. Pakai skill ini saat diminta membuat Modul Praktikum, bukan slide.
---

# Insignia Modul Praktikum (DOCX)

Skill ini membuat dokumen `.docx` berisi panduan praktikum langkah-demi-langkah, mengikuti struktur yang sudah dipakai di modul praktikum Insignia yang ada (contoh: modul Feasibility Analyzer, modul AI-DLC for DE). Ini dokumen yang dibaca peserta sambil mengikuti instruktur atau belajar mandiri — beda dari PPT yang dipakai untuk presentasi.

## Struktur dokumen standar (urutan ini dipertahankan)

1. **Judul dokumen** — "MODUL PRAKTIKUM" + baris konteks modul/use case.
2. **Heading 1 — Tujuan Pembelajaran** — bullet list, 3-5 poin, tiap poin mulai dengan kata kerja ("Peserta mampu ...", "Peserta memahami ...").
3. **Heading 1 — Gambaran Alur** (nama section bisa disesuaikan, misal "Gambaran Alur Workflow" atau "Gambaran Arsitektur") — ringkasan alur end-to-end dalam 1 paragraf/diagram teks, plus catatan constraint penting.
4. **Heading 1 — Persiapan Sebelum Mulai** — checklist prasyarat (akun, tool, file yang harus sudah di-download).
5. **Heading 1 — Langkah [Membangun/Mengerjakan] (Detail)** — berisi beberapa **Heading 2 — Langkah N — <nama langkah>**. Tiap Langkah 2 punya:
   - Sub-langkah bernomor `N.1`, `N.2`, dst — instruksi aksi konkret, satu aksi per nomor.
   - Baris **CHECKPOINT —** di akhir tiap Langkah, menjelaskan kondisi yang harus terlihat kalau langkah berhasil, supaya peserta tahu kapan boleh lanjut.
6. **Heading 1 — Latihan Mandiri** — bullet list tugas tambahan yang dikerjakan sendiri setelah sesi dipandu selesai.

## Aturan konten

- Tanpa emoji/icon di body dokumen.
- Setiap sub-langkah adalah instruksi aksi fisik yang bisa diikuti tanpa ambigu (sebutkan nama tombol/menu persis, bukan deskripsi umum).
- Kode yang direferensikan di dalam modul (misal "salin dari file X") harus benar-benar lengkap dan ada di folder Instructor Only / Starter Kit — jangan rujuk file yang tidak dibuat.
- Istilah teknis/nama tool/nama tombol UI tetap bahasa Inggris sesuai tampilan aslinya; narasi instruksi Bahasa Indonesia.
- CHECKPOINT ditulis singkat dan bisa diverifikasi visual/angka (misal "pastikan output menunjukkan nilai sekitar X", bukan "pastikan sudah benar").

## Setup

```bash
pip install python-docx
```

## Kode referensi (lengkap, runnable)

Simpan sebagai `generate_modul_praktikum.py` di root project, jalankan `python generate_modul_praktikum.py`. Isi variabel `MODULE_TITLE`, `LEARNING_OBJECTIVES`, `PREP_CHECKLIST`, `STEPS`, dan `SELF_PRACTICE` sesuai modul yang diminta — jangan ubah struktur fungsi helper.

```python
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent

# Warna brand (dari brand/colors.json) - hardcode di sini karena python-docx
# tidak membaca JSON secara native; sinkronkan manual kalau brand/colors.json berubah.
COLOR_PRIMARY = RGBColor(0x0E, 0x1F, 0x47)   # navy
COLOR_ACCENT = RGBColor(0xE3, 0x1E, 0x2B)    # merah
COLOR_TEXT_SECONDARY = RGBColor(0x4A, 0x52, 0x68)

FONT_NAME = "Arial"


def set_run_font(run, size=11, bold=False, color=None, italic=False):
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color


def add_title_block(doc, kicker, title, subtitle):
    p = doc.add_paragraph()
    r = p.add_run(kicker.upper())
    set_run_font(r, size=10, bold=True, color=COLOR_ACCENT)

    p2 = doc.add_paragraph()
    r2 = p2.add_run(title)
    set_run_font(r2, size=24, bold=True, color=COLOR_PRIMARY)

    p3 = doc.add_paragraph()
    r3 = p3.add_run(subtitle)
    set_run_font(r3, size=12, italic=True, color=COLOR_TEXT_SECONDARY)

    doc.add_paragraph()


def add_heading1(doc, number, text):
    h = doc.add_heading(level=1)
    r = h.add_run(f"{number}. {text}")
    set_run_font(r, size=16, bold=True, color=COLOR_PRIMARY)
    return h


def add_heading2(doc, text):
    h = doc.add_heading(level=2)
    r = h.add_run(text)
    set_run_font(r, size=13, bold=True, color=COLOR_PRIMARY)
    return h


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(item)
        set_run_font(r, size=11)


def add_substep(doc, number_label, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    r1 = p.add_run(f"{number_label}  ")
    set_run_font(r1, size=11, bold=True, color=COLOR_ACCENT)
    r2 = p.add_run(text)
    set_run_font(r2, size=11)


def add_checkpoint(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r1 = p.add_run("CHECKPOINT — ")
    set_run_font(r1, size=11, bold=True, color=COLOR_ACCENT)
    r2 = p.add_run(text)
    set_run_font(r2, size=11, italic=True, color=COLOR_TEXT_SECONDARY)


def build_modul(output_path: Path) -> None:
    doc = Document()

    # --- Ganti bagian di bawah ini sesuai modul yang diminta ---
    MODULE_TITLE = "Nama Modul"
    MODULE_SUBTITLE = "Deskripsi singkat satu baris tentang isi modul ini"

    LEARNING_OBJECTIVES = [
        "Peserta mampu menjelaskan konsep inti dari topik ini",
        "Peserta mampu menjalankan contoh end-to-end secara mandiri",
        "Peserta memahami cara memverifikasi hasil di tiap tahap",
    ]

    OVERVIEW_TEXT = (
        "Ringkasan alur end-to-end: Input -> Proses -> Output. "
        "Jelaskan di sini batasan atau asumsi penting yang perlu diketahui peserta sebelum mulai."
    )

    PREP_CHECKLIST = [
        "Akun/tool yang dibutuhkan sudah aktif",
        "Sudah memahami konsep dasar yang relevan (sebutkan referensi)",
        "File pendukung sudah di-download dari folder Starter Kit Peserta",
    ]

    STEPS = [
        {
            "title": "Langkah 1 - Nama Langkah Pertama",
            "substeps": [
                "1.1  Instruksi aksi pertama, sebutkan nama tombol/menu persis.",
                "1.2  Instruksi aksi kedua.",
            ],
            "checkpoint": "Pastikan kondisi X terlihat sebelum lanjut ke langkah berikutnya.",
        },
        {
            "title": "Langkah 2 - Nama Langkah Kedua",
            "substeps": [
                "2.1  Instruksi aksi pertama.",
                "2.2  Instruksi aksi kedua.",
            ],
            "checkpoint": "Pastikan output menunjukkan nilai yang sesuai ekspektasi.",
        },
    ]

    SELF_PRACTICE = [
        "Ulangi langkah di atas dengan data/kasus yang berbeda.",
        "Diskusikan hasil yang tidak sesuai ekspektasi dengan rekan atau mentor.",
    ]
    # --- Akhir bagian yang perlu diganti ---

    add_title_block(doc, kicker="Modul Praktikum", title=MODULE_TITLE, subtitle=MODULE_SUBTITLE)

    add_heading1(doc, 1, "Tujuan Pembelajaran")
    add_bullets(doc, LEARNING_OBJECTIVES)

    add_heading1(doc, 2, "Gambaran Alur")
    p = doc.add_paragraph()
    set_run_font(p.add_run(OVERVIEW_TEXT), size=11)

    add_heading1(doc, 3, "Persiapan Sebelum Mulai")
    add_bullets(doc, PREP_CHECKLIST)

    add_heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    for step in STEPS:
        add_heading2(doc, step["title"])
        for substep in step["substeps"]:
            add_substep(doc, substep.split("  ")[0], "  ".join(substep.split("  ")[1:]))
        add_checkpoint(doc, step["checkpoint"])

    add_heading1(doc, 5, "Latihan Mandiri")
    add_bullets(doc, SELF_PRACTICE)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"Modul praktikum tersimpan di: {output_path}")


if __name__ == "__main__":
    build_modul(ROOT / "output" / "Modul_Praktikum.docx")
```

## Checklist sebelum mengirim modul ke user

- Semua 6 section ada sesuai urutan standar (Tujuan, Gambaran Alur, Persiapan, Langkah Detail, Latihan Mandiri).
- Setiap Langkah 2 diakhiri CHECKPOINT yang bisa diverifikasi konkret.
- Tidak ada sub-langkah yang menyebut file/kode yang tidak benar-benar dibuat di Starter Kit / Instructor Only.
- File output ditulis ke `output/<nama-modul>/Modul_Praktikum_<nama>.docx`.

## Keputusan manusia: wajib lewat grill-me

Setiap kali muncul keputusan yang menjadi hak Fahmi (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu kelas, gaya), jangan memutuskan sendiri dan jangan menumpuk pertanyaan di akhir laporan. Langsung panggil skill `grill-me` (Skill tool), selesaikan wawancara dan Decision Log-nya, baru lanjut bekerja. Keputusan teknis murni tetap diputuskan sendiri dan cukup dilaporkan.
