"""Generator Excel Insignia dengan dua pola: tracker dan modul sheet.

Pemakaian:
    python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py tracker <spec.json> <output.xlsx>
    python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py modul-sheet <spec.json> <output.xlsx>
    python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py demo <output_dir>

Format spec.json dijelaskan di SKILL.md. Warna dibaca dari <root repo>/brand/colors.json.
"""
import argparse
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

REPO_ROOT = Path(__file__).resolve().parents[3]
COLORS = json.loads((REPO_ROOT / "brand" / "colors.json").read_text(encoding="utf-8"))
FONT = COLORS.get("font_body", "Arial")
STATUS_VALUES = ["Belum Mulai", "Proses", "Selesai"]
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def hex_(name: str) -> str:
    return COLORS[name].replace("#", "")


def fill(name: str) -> PatternFill:
    return PatternFill(start_color=hex_(name), end_color=hex_(name), fill_type="solid")


def style_header(ws, row: int, n_cols: int) -> None:
    for col in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill("primary")
        cell.font = Font(name=FONT, color=hex_("text_on_dark"), bold=True, size=11)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.freeze_panes = f"A{row + 1}"


def style_body(ws, first_row: int, last_row: int, n_cols: int, wrap: bool) -> None:
    for r in range(first_row, last_row + 1):
        for c in range(1, n_cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = Font(name=FONT, size=10, color=hex_("text_primary"))
            cell.alignment = Alignment(vertical="top", wrap_text=wrap)
            cell.border = BORDER
        if r % 2 == 0:
            for c in range(1, n_cols + 1):
                ws.cell(row=r, column=c).fill = fill("surface")


def auto_width(ws, n_cols: int, max_width: int = 45) -> None:
    for col_idx in range(1, n_cols + 1):
        letter = get_column_letter(col_idx)
        longest = 0
        for cell in ws[letter]:
            if cell.value is not None:
                longest = max(longest, max(len(line) for line in str(cell.value).split("\n")))
        ws.column_dimensions[letter].width = max(10, min(longest + 3, max_width))


def fit_row_heights(ws, first_row: int, last_row: int, n_cols: int) -> None:
    """Perkirakan tinggi baris dari jumlah baris teks setelah wrap."""
    for r in range(first_row, last_row + 1):
        lines = 1
        for c in range(1, n_cols + 1):
            value = ws.cell(row=r, column=c).value
            if value is None:
                continue
            width = ws.column_dimensions[get_column_letter(c)].width or 10
            chars = max(int(width) - 2, 1)
            n = sum(max(1, -(-len(line) // chars)) for line in str(value).split("\n"))
            lines = max(lines, n)
        ws.row_dimensions[r].height = min(15 * lines + 4, 409)


def add_status_column(ws, col_letter: str, first_row: int, last_row: int) -> None:
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUS_VALUES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    rng = f"{col_letter}{first_row}:{col_letter}{last_row}"
    dv.add(rng)
    for status, color in zip(STATUS_VALUES, ["error", "warning", "success"]):
        ws.conditional_formatting.add(
            rng,
            CellIsRule(operator="equal", formula=[f'"{status}"'], fill=fill(color),
                       font=Font(name=FONT, color=hex_("text_on_dark"), bold=True)),
        )


def bullets(value) -> str:
    """List menjadi teks multi-baris dengan awalan bullet. String dibiarkan apa adanya."""
    if isinstance(value, list):
        return "\n".join(f"• {item}" for item in value)
    return "" if value is None else str(value)


def write_table(ws, headers, rows, status_header=None, wrap=False, widths=None) -> None:
    ws.append(headers)
    style_header(ws, 1, len(headers))
    for row in rows:
        ws.append([bullets(v) for v in row])
    last = ws.max_row
    style_body(ws, 2, last, len(headers), wrap)
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    else:
        auto_width(ws, len(headers))
    if wrap:
        fit_row_heights(ws, 2, last, len(headers))
    if status_header and status_header in headers and last >= 2:
        letter = get_column_letter(headers.index(status_header) + 1)
        add_status_column(ws, letter, 2, last)


# ---------- Pola 1: Tracker ----------

def build_tracker(spec: dict, output: Path) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    for sheet in spec["sheets"]:
        ws = wb.create_sheet(sheet["name"][:31])
        write_table(ws, sheet["headers"], sheet["rows"], status_header=sheet.get("status_column"))
        for formula_col in sheet.get("formula_columns", []):
            col = sheet["headers"].index(formula_col["header"]) + 1
            for r in range(2, ws.max_row + 1):
                ws.cell(row=r, column=col).value = formula_col["formula"].replace("{row}", str(r))
    save(wb, output)


# ---------- Pola 2: Modul Sheet ----------

DEFAULT_MODUL_COLUMNS = [
    ("No", "no", 6), ("Blok", "blok", 16), ("Bagian", "bagian", 24),
    ("Topics", "topics", 42), ("Objective", "objective", 36),
    ("Deliverable", "deliverable", 42), ("Bukti Selesai", "bukti", 30),
    ("Dataset / Sumber", "dataset", 28), ("Materi", "materi", 32),
    ("Kriteria Cek Mentor", "kriteria", 36), ("Status", "status", 14), ("Catatan", "catatan", 24),
]


def build_start_here(ws, info: dict) -> None:
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 90
    ws["A1"] = info.get("judul", "")
    ws["A1"].font = Font(name=FONT, size=18, bold=True, color=hex_("primary"))
    ws["A2"] = info.get("subjudul", "")
    ws["A2"].font = Font(name=FONT, size=11, italic=True, color=hex_("text_secondary"))
    row = 4
    for label, value in info.get("items", []):
        a, b = ws.cell(row=row, column=1, value=label), ws.cell(row=row, column=2, value=bullets(value))
        a.font = Font(name=FONT, size=10, bold=True, color=hex_("accent"))
        b.font = Font(name=FONT, size=10, color=hex_("text_primary"))
        a.alignment = Alignment(vertical="top")
        b.alignment = Alignment(vertical="top", wrap_text=True)
        n = sum(max(1, -(-len(line) // 85)) for line in bullets(value).split("\n"))
        ws.row_dimensions[row].height = 15 * n + 4
        row += 1


def build_modul_sheet(spec: dict, output: Path) -> None:
    wb = Workbook()
    build_start_here(wb.active, spec["start_here"])
    wb.active.title = "Start here"

    columns = DEFAULT_MODUL_COLUMNS
    if "columns" in spec:
        columns = [(c["header"], c["key"], c.get("width", 24)) for c in spec["columns"]]
    ws = wb.create_sheet("Modul")
    rows = []
    for i, bagian in enumerate(spec["bagian"], start=1):
        bagian.setdefault("no", i)
        bagian.setdefault("status", "Belum Mulai")
        rows.append([bagian.get(key, "") for _, key, _ in columns])
    write_table(ws, [h for h, _, _ in columns], rows, status_header="Status", wrap=True,
                widths=[w for _, _, w in columns])

    if spec.get("materi"):
        wm = wb.create_sheet("Materi")
        write_table(wm, ["File", "Jenis", "Lokasi", "Dipakai di Bagian"],
                    [[m["file"], m["jenis"], m["lokasi"], m["bagian"]] for m in spec["materi"]])
    save(wb, output)


def save(wb, output: Path) -> None:
    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"Tersimpan: {output}")


# ---------- Demo (data sintetis) ----------

DEMO_TRACKER = {
    "sheets": [{
        "name": "Tracker",
        "headers": ["No", "Nama Peserta", "Track", "Modul", "Status", "Progress (%)", "Catatan"],
        "status_column": "Status",
        "rows": [[1, "Peserta A", "Data Engineering", "Modul 1", "Selesai", 100, ""],
                 [2, "Peserta B", "Data Science", "Modul 1", "Proses", 60, ""],
                 [3, "Peserta C", "Data Engineering", "Modul 2", "Belum Mulai", 0, ""]],
    }]
}

DEMO_MODUL = {
    "start_here": {
        "judul": "Contoh Modul Preparation",
        "subjudul": "Data sintetis untuk menguji pola modul sheet",
        "items": [["Target peserta", "Junior dan intern"],
                  ["Cara mengerjakan", ["Kerjakan bagian berurutan", "Isi kolom Status di tab Modul", "Lampirkan bukti selesai ke mentor"]]],
    },
    "bagian": [{
        "blok": "Foundations", "bagian": "Orientasi",
        "topics": ["Konsep A", "Konsep B", "Navigasi tool"],
        "objective": "Menjelaskan konsep dasar dan menavigasi tool.",
        "deliverable": ["Akun aktif", "Latihan level 1 selesai"],
        "bukti": "Screenshot hasil latihan", "dataset": "Teks contoh sintetis",
        "materi": "Contoh_Materi.pptx", "kriteria": "Output sesuai checkpoint level 1",
    }],
    "materi": [{"file": "Contoh_Materi.pptx", "jenis": "Rujukan", "lokasi": "3_Materi_Rujukan/", "bagian": "1"}],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pola", choices=["tracker", "modul-sheet", "demo"])
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    if args.pola == "demo":
        out = Path(args.paths[0])
        build_tracker(DEMO_TRACKER, out / "demo_tracker.xlsx")
        build_modul_sheet(DEMO_MODUL, out / "demo_modul_sheet.xlsx")
        return
    if len(args.paths) != 2:
        parser.error("butuh <spec.json> <output.xlsx>")
    spec = json.loads(Path(args.paths[0]).read_text(encoding="utf-8"))
    builder = build_tracker if args.pola == "tracker" else build_modul_sheet
    builder(spec, Path(args.paths[1]))


if __name__ == "__main__":
    main()
