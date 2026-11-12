---
name: insignia-xlsx-tracker
description: Buat atau update file Excel (.xlsx) tracker untuk operasional conversion training Insignia (misal alokasi akun Udemy, tracker kehadiran, tracker progress peserta) memakai openpyxl, dengan format konsisten. Pakai skill ini setiap kali diminta membuat/update tracker Excel Insignia.
---

# Insignia Excel Tracker

Skill ini membuat/mengupdate file `.xlsx` untuk kebutuhan operasional program training Insignia (tracker alokasi akun, tracker kehadiran, tracker progress peserta per modul, dsb) memakai `openpyxl`.

## Aturan konten

- Header kolom jelas dan konsisten (Title Case, tanpa singkatan ambigu).
- Tanpa emoji di header atau cell — kalau perlu indikator status, pakai teks singkat ("Selesai", "Proses", "Belum Mulai") atau conditional formatting warna, bukan emoji.
- Istilah teknis tetap dalam bahasa Inggris (misal nama track "Data Engineering", nama tool), label lain Bahasa Indonesia.
- Kolom formula (misal persentase progress, status otomatis) harus pakai formula Excel asli (openpyxl `cell.value = "=...")`, bukan nilai hardcode hasil hitung manual, supaya tracker tetap hidup saat data diupdate.

## Sumber brand

Baca `brand/colors.json` (relatif dari root project: `../../../brand/colors.json`) untuk warna header/accent supaya konsisten dengan PPT.

## Setup

```bash
pip install openpyxl
```

## Pola standar

1. **Header row** — background warna `primary` dari colors.json, font putih bold, freeze panes di bawah header.
2. **Kolom status** — pakai conditional formatting (fill warna `success`/`warning`/`error`) berdasarkan isi teks status.
3. **Auto-width kolom** — hitung dari panjang konten, jangan biarkan default sempit.
4. **Sheet terpisah** kalau ada beberapa kategori data (misal sheet "DE Track" dan "DS Track").

## Kode referensi (lengkap, runnable)

Simpan sebagai `generate_tracker.py` di root project, jalankan `python generate_tracker.py`. Sesuaikan `data` dan nama kolom sesuai tracker yang diminta.

```python
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
COLORS = json.loads((ROOT / "brand" / "colors.json").read_text(encoding="utf-8"))


def strip_hash(hex_color: str) -> str:
    return hex_color.replace("#", "")


def style_header(ws, row: int, n_cols: int) -> None:
    header_fill = PatternFill(
        start_color=strip_hash(COLORS["primary"]),
        end_color=strip_hash(COLORS["primary"]),
        fill_type="solid",
    )
    header_font = Font(
        color=strip_hash(COLORS["text_on_dark"]), bold=True, size=11
    )
    thin = Side(style="thin", color="D0D0D0")
    for col in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws.freeze_panes = ws.cell(row=row + 1, column=1).coordinate


def auto_width(ws, n_cols: int) -> None:
    for col_idx in range(1, n_cols + 1):
        letter = get_column_letter(col_idx)
        max_len = 0
        for cell in ws[letter]:
            if cell.value is not None:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[letter].width = max(12, min(max_len + 4, 45))


def add_status_conditional_formatting(ws, column_letter: str, first_row: int, last_row: int) -> None:
    rng = f"{column_letter}{first_row}:{column_letter}{last_row}"
    ws.conditional_formatting.add(
        rng,
        CellIsRule(
            operator="equal", formula=['"Selesai"'],
            fill=PatternFill(start_color=strip_hash(COLORS["success"]), end_color=strip_hash(COLORS["success"]), fill_type="solid"),
            font=Font(color=strip_hash(COLORS["text_on_dark"])),
        ),
    )
    ws.conditional_formatting.add(
        rng,
        CellIsRule(
            operator="equal", formula=['"Proses"'],
            fill=PatternFill(start_color=strip_hash(COLORS["warning"]), end_color=strip_hash(COLORS["warning"]), fill_type="solid"),
            font=Font(color=strip_hash(COLORS["text_on_dark"])),
        ),
    )
    ws.conditional_formatting.add(
        rng,
        CellIsRule(
            operator="equal", formula=['"Belum Mulai"'],
            fill=PatternFill(start_color=strip_hash(COLORS["error"]), end_color=strip_hash(COLORS["error"]), fill_type="solid"),
            font=Font(color=strip_hash(COLORS["text_on_dark"])),
        ),
    )


def build_tracker(output_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Tracker"

    headers = ["No", "Nama Peserta", "Track", "Modul", "Status", "Progress (%)", "Catatan"]
    ws.append(headers)
    style_header(ws, row=1, n_cols=len(headers))

    # Contoh data - ganti dengan data asli sesuai permintaan user
    sample_rows = [
        [1, "Contoh Nama 1", "Data Engineering", "Modul 1", "Selesai", 100, ""],
        [2, "Contoh Nama 2", "Data Science", "Modul 1", "Proses", 60, ""],
        [3, "Contoh Nama 3", "Data Engineering", "Modul 2", "Belum Mulai", 0, ""],
    ]
    for row in sample_rows:
        ws.append(row)

    last_row = ws.max_row
    add_status_conditional_formatting(ws, column_letter="E", first_row=2, last_row=last_row)
    auto_width(ws, n_cols=len(headers))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"Tracker tersimpan di: {output_path}")


if __name__ == "__main__":
    build_tracker(ROOT / "output" / "tracker.xlsx")
```

## Checklist sebelum mengirim tracker ke user

- Header pakai warna dari `brand/colors.json`.
- Kolom status pakai conditional formatting, bukan emoji.
- Kolom formula (kalau ada) pakai formula Excel asli, bisa diedit ulang di Excel.
- Lebar kolom sudah auto-fit, tidak ada teks terpotong.
- File output ditulis ke `output/<nama-tracker>.xlsx`.

## Keputusan manusia: wajib lewat grill-me

Setiap kali muncul keputusan yang menjadi hak Fahmi (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu kelas, gaya), jangan memutuskan sendiri dan jangan menumpuk pertanyaan di akhir laporan. Langsung panggil skill `grill-me` (Skill tool), selesaikan wawancara dan Decision Log-nya, baru lanjut bekerja. Keputusan teknis murni tetap diputuskan sendiri dan cukup dilaporkan.
