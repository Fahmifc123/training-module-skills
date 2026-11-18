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
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Nilai baku. Status dipakai di kedua pola agar konsisten dengan Legend.
STATUS = [
    ("Belum Mulai", "Module belum dimulai", "surface_muted"),
    ("Sedang Berjalan", "Module sedang dikerjakan", "warning"),
    ("Selesai", "Module selesai dan deliverable sudah dikumpulkan", "success"),
]
CATEGORY = [
    ("Concept", "Materi teori: baca, pahami konsep"),
    ("Setup", "Konfigurasi environment dan tools"),
    ("Hands-on", "Latihan praktek mandiri: ikuti langkah yang diberikan"),
    ("Project", "Mini project mandiri: implementasikan tanpa panduan step-by-step"),
    ("Use Case", "Hands-on lanjutan dengan use case industri"),
    ("Capstone", "Proyek akhir end-to-end"),
    ("Test", "Quiz konsep dan penilaian rubrik di akhir modul"),
    ("Review / Tanya Jawab", "Sesi diskusi on-demand dengan mentor setelah selesai modul"),
]
DIFFICULTY = [
    ("Beginner", "Tanpa prasyarat di luar modul sebelumnya"),
    ("Intermediate", "Butuh pemahaman sub modul sebelumnya"),
    ("Advanced", "Menggabungkan beberapa konsep, minim panduan"),
    ("All Levels", "Bisa diikuti semua level"),
    ("TBD", "Belum ditentukan"),
]
SOURCE = [
    ("Internal", "Materi dari mentor (PPT, video, modul)"),
    ("External", "Course atau dokumentasi luar (Udemy, docs resmi)"),
    ("Blended", "Gabungan materi internal dan external"),
]

# (header, key, lebar)
MODUL_COLUMNS = [
    ("Modul", "modul", 24), ("Sub Modul", "sub_modul", 28), ("Materi", "materi", 34),
    ("Category", "category", 14), ("Learning Objectives", "objectives", 54),
    ("Difficulty", "difficulty", 13), ("Output / Deliverable", "deliverable", 40),
    ("Material Source", "source", 15), ("Internal Link PPT", "ppt", 26),
    ("Video Course Internal Link", "video", 28), ("External Link (Udemy, dll)", "external", 40),
    ("Referensi Section Udemy", "referensi", 46), ("Status", "status", 16),
]


def hex_(name: str) -> str:
    return COLORS[name].replace("#", "")


def fill(name: str) -> PatternFill:
    return PatternFill(start_color=hex_(name), end_color=hex_(name), fill_type="solid")


def font(size=10, bold=False, color="text_primary", italic=False) -> Font:
    return Font(name=FONT, size=size, bold=bold, italic=italic, color=hex_(color))


def style_header(ws, row: int, n_cols: int) -> None:
    for col in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill("primary")
        cell.font = font(bold=True, color="text_on_dark")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 34
    ws.freeze_panes = f"A{row + 1}"  # string, agar tidak membuat sel kosong di baris data


def estimate_height(values, widths) -> float:
    lines = 1
    for value, width in zip(values, widths):
        if value in (None, ""):
            continue
        chars = max(int(width) - 2, 1)
        n = sum(max(1, -(-len(line) // chars)) for line in str(value).split("\n"))
        lines = max(lines, n)
    return min(14 * lines + 8, 409)


def add_list_validation(ws, values, rng: str) -> None:
    dv = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


def add_status_format(ws, rng: str) -> None:
    for status, _, color in STATUS:
        text_color = "text_primary" if color == "surface_muted" else "text_on_dark"
        ws.conditional_formatting.add(
            rng, CellIsRule(operator="equal", formula=[f'"{status}"'], fill=fill(color),
                            font=font(bold=True, color=text_color)))


def bullets(value) -> str:
    """List menjadi teks multi-baris dengan awalan bullet. String dibiarkan apa adanya."""
    if isinstance(value, list):
        return "\n".join(f"• {item}" for item in value)
    return "" if value is None else str(value)


def page_setup(ws) -> None:
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0


def save(wb, output: Path) -> None:
    for ws in wb.worksheets:
        page_setup(ws)
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)
    print(f"Tersimpan: {output}")


# ---------- Pola 1: Tracker ----------

def build_tracker(spec: dict, output: Path) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    for sheet in spec["sheets"]:
        ws = wb.create_sheet(sheet["name"][:31])
        headers = sheet["headers"]
        ws.append(headers)
        style_header(ws, 1, len(headers))
        for row in sheet["rows"]:
            ws.append([bullets(v) for v in row])
        last = ws.max_row
        for r in range(2, last + 1):
            for c in range(1, len(headers) + 1):
                cell = ws.cell(row=r, column=c)
                cell.font = font()
                cell.alignment = Alignment(vertical="top")
                cell.border = BORDER
                if r % 2 == 0:
                    cell.fill = fill("surface")
        for c in range(1, len(headers) + 1):
            letter = get_column_letter(c)
            longest = max(len(str(x.value)) for x in ws[letter] if x.value is not None)
            ws.column_dimensions[letter].width = max(10, min(longest + 3, 45))
        for formula_col in sheet.get("formula_columns", []):
            col = headers.index(formula_col["header"]) + 1
            for r in range(2, last + 1):
                ws.cell(row=r, column=col).value = formula_col["formula"].replace("{row}", str(r))
        status_header = sheet.get("status_column")
        if status_header in headers and last >= 2:
            letter = get_column_letter(headers.index(status_header) + 1)
            rng = f"{letter}2:{letter}{last}"
            add_list_validation(ws, [s for s, _, _ in STATUS], rng)
            add_status_format(ws, rng)
    save(wb, output)


# ---------- Pola 2: Modul Sheet (format DE - Modul Preparation) ----------

def validate_modul_spec(spec: dict) -> None:
    allowed = {
        "category": [c for c, _ in CATEGORY], "difficulty": [d for d, _ in DIFFICULTY],
        "source": [s for s, _ in SOURCE], "status": [s for s, _, _ in STATUS],
    }
    errors = []
    for modul in spec["modul"]:
        for row in modul["sub_modul"]:
            row.setdefault("status", "Belum Mulai")
            for key, values in allowed.items():
                if row.get(key) and row[key] not in values:
                    errors.append(f"{modul['nama']} / {row.get('sub_modul')}: {key} '{row[key]}' "
                                  f"tidak ada di {values}")
            for key in ("sub_modul", "materi", "category", "objectives", "difficulty", "source"):
                if not row.get(key):
                    errors.append(f"{modul['nama']} / {row.get('sub_modul')}: kolom {key} kosong")
            if row.get("source") in ("Internal", "Blended") and not (row.get("ppt") or row.get("video")):
                errors.append(f"{modul['nama']} / {row['sub_modul']}: source {row['source']} "
                              "tetapi Internal Link PPT dan Video kosong")
            if row.get("source") in ("External", "Blended") and not row.get("external"):
                errors.append(f"{modul['nama']} / {row['sub_modul']}: source {row['source']} "
                              "tetapi External Link kosong")
        if modul["sub_modul"][-1].get("category") != "Test":
            errors.append(f"{modul['nama']}: baris terakhir modul harus kategori Test")
    if errors:
        raise SystemExit("Spec modul sheet tidak valid:\n- " + "\n- ".join(errors))


def build_training_modules(ws, spec: dict) -> None:
    headers = [h for h, _, _ in MODUL_COLUMNS]
    widths = [w for _, _, w in MODUL_COLUMNS]
    ws.append(headers)
    style_header(ws, 1, len(headers))
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    data_rows = []
    for m_idx, modul in enumerate(spec["modul"]):
        if m_idx > 0:
            ws.append([])  # satu baris kosong antar modul
        for row in modul["sub_modul"]:
            values = [modul["nama"] if key == "modul" else bullets(row.get(key, ""))
                      for _, key, _ in MODUL_COLUMNS]
            ws.append(values)
            r = ws.max_row
            data_rows.append(r)
            is_test = row.get("category") == "Test"
            for c in range(1, len(headers) + 1):
                cell = ws.cell(row=r, column=c)
                cell.font = font(bold=(c <= 2 and is_test))
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = BORDER
                cell.fill = fill("tint_accent" if is_test else "tint_secondary" if c <= 2 else "background")
            ws.row_dimensions[r].height = estimate_height(values, widths)

    last = ws.max_row
    col = {key: get_column_letter(i) for i, (_, key, _) in enumerate(MODUL_COLUMNS, start=1)}
    add_list_validation(ws, [c for c, _ in CATEGORY], f"{col['category']}2:{col['category']}{last}")
    add_list_validation(ws, [d for d, _ in DIFFICULTY], f"{col['difficulty']}2:{col['difficulty']}{last}")
    add_list_validation(ws, [s for s, _ in SOURCE], f"{col['source']}2:{col['source']}{last}")
    status_rng = f"{col['status']}2:{col['status']}{last}"
    add_list_validation(ws, [s for s, _, _ in STATUS], status_rng)
    add_status_format(ws, status_rng)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{last}"


def build_legend(ws, spec: dict) -> None:
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 80
    row = 1

    def section(title: str, items, title_size=10) -> None:
        nonlocal row
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
        cell = ws.cell(row=row, column=1, value=title)
        cell.fill = fill("primary")
        cell.font = font(size=title_size, bold=True, color="text_on_dark")
        cell.alignment = Alignment(vertical="center")
        ws.row_dimensions[row].height = 22
        row += 1
        for key, desc in items:
            a = ws.cell(row=row, column=1, value=key)
            b = ws.cell(row=row, column=2, value=desc)
            a.font, b.font = font(bold=True), font()
            a.fill = fill("tint_secondary")
            for c in (a, b):
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.border = BORDER
            row += 1
        row += 1

    ws.merge_cells("A1:B1")
    title = ws.cell(row=1, column=1, value=spec.get("legend_title", f"Keterangan & Panduan Penggunaan - {spec['judul']}"))
    title.fill = fill("primary")
    title.font = font(size=12, bold=True, color="text_on_dark")
    ws.row_dimensions[1].height = 26
    row = 3
    section("KATEGORI MODULE", CATEGORY)
    section("STATUS PROGRESS", [(s, d) for s, d, _ in STATUS])
    section("DIFFICULTY", DIFFICULTY)
    section("MATERIAL SOURCE", SOURCE)
    for extra in spec.get("legend_extra", []):
        section(extra["title"].upper(), extra["rows"])
    if spec.get("alur_belajar"):
        section("ALUR BELAJAR", [(f"Step {i}", s) for i, s in enumerate(spec["alur_belajar"], start=1)])


def build_modul_sheet(spec: dict, output: Path) -> None:
    validate_modul_spec(spec)
    wb = Workbook()
    ws = wb.active
    ws.title = spec.get("sheet_name", "Training Modules")
    build_training_modules(ws, spec)
    build_legend(wb.create_sheet("Legend"), spec)
    save(wb, output)


# ---------- Demo (data sintetis) ----------

DEMO_TRACKER = {
    "sheets": [{
        "name": "Tracker",
        "headers": ["No", "Nama Peserta", "Track", "Modul", "Status", "Selesai", "Total", "Progress (%)"],
        "status_column": "Status",
        "rows": [[1, "Peserta A", "Data Engineering", "Modul 1", "Selesai", 8, 8, None],
                 [2, "Peserta B", "Data Science", "Modul 1", "Sedang Berjalan", 5, 8, None],
                 [3, "Peserta C", "Data Engineering", "Modul 2", "Belum Mulai", 0, 13, None]],
        "formula_columns": [{"header": "Progress (%)", "formula": "=ROUND(F{row}/G{row}*100,0)"}],
    }]
}

DEMO_MODUL = {
    "judul": "Contoh Program",
    "alur_belajar": ["Peserta belajar mandiri (materi internal atau external)",
                     "Peserta menghubungi mentor untuk tanya jawab dan review (on-demand)",
                     "Mini project dikerjakan mandiri, lalu Test Modul"],
    "legend_extra": [{"title": "Mode Belajar", "rows": [["Self-study", "Belajar mandiri dari materi yang tercantum"]]}],
    "modul": [
        {"nama": "Modul 1: Contoh Fondasi", "sub_modul": [
            {"sub_modul": "1.1 Konsep Dasar", "materi": "Intro: peran, ekosistem, istilah inti",
             "category": "Concept", "objectives": "Memahami peran dan ekosistem; membedakan istilah inti",
             "difficulty": "Beginner", "deliverable": "Ringkasan satu halaman", "source": "Internal",
             "ppt": "Contoh_1.1_Intro.pptx"},
            {"sub_modul": "1.2 Setup Environment", "materi": "Setup tool lokal",
             "category": "Setup", "objectives": ["Install tool", "Verifikasi instalasi"],
             "difficulty": "Beginner", "deliverable": "Environment siap", "source": "External",
             "external": "https://docs.python.org/3/tutorial/venv.html",
             "referensi": "Bagian 12.1 - 12.3"},
            {"sub_modul": "1.3 Mini Project - Fondasi", "materi": "Mini project end-to-end",
             "category": "Project", "objectives": "Menggabungkan 1.1 dan 1.2 dalam satu pipeline kecil",
             "difficulty": "Intermediate", "deliverable": "Repo dan README", "source": "Internal",
             "ppt": "Contoh_1.3_Mini_Project.pptx"},
            {"sub_modul": "Test Modul 1", "materi": "Quiz Konsep (1.1-1.2) + Rubrik Mini Project (1.3)",
             "category": "Test", "objectives": "Validasi pemahaman konsep Modul 1",
             "difficulty": "Intermediate", "source": "Internal", "ppt": "Contoh_Test_Modul1.pptx"},
        ]},
        {"nama": "Modul 2: Contoh Lanjutan", "sub_modul": [
            {"sub_modul": "2.1 Konsep Lanjutan", "materi": "Pola lanjutan", "category": "Concept",
             "objectives": "Memahami pola lanjutan", "difficulty": "Intermediate",
             "deliverable": "Diagram pola", "source": "Blended", "ppt": "Contoh_2.1.pptx",
             "external": "https://example.com/course", "status": "Sedang Berjalan"},
            {"sub_modul": "Test Modul 2", "materi": "Quiz Konsep (2.1)", "category": "Test",
             "objectives": "Validasi pemahaman Modul 2", "difficulty": "Intermediate",
             "source": "Internal", "ppt": "Contoh_Test_Modul2.pptx"},
        ]},
    ],
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
