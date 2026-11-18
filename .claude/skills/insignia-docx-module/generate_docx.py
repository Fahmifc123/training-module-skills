"""Generator dokumen .docx Insignia dengan dua struktur.

Pemakaian:
    python .claude/skills/insignia-docx-module/generate_docx.py modul-praktikum <spec.json> <output.docx>
    python .claude/skills/insignia-docx-module/generate_docx.py panduan-bagian <spec.json> <output.docx>
    python .claude/skills/insignia-docx-module/generate_docx.py demo <output_dir>

Format spec.json dijelaskan di SKILL.md. Warna dan font dibaca dari <kit root>/brand/colors.json (lihat aturan bersama bagian 0).
"""
import argparse
import json
import os
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor



def find_kit_root() -> Path:
    """Kit root: TRAINING_KIT_HOME, atau tiga tingkat di atas folder skill (junction/symlink di-resolve)."""
    candidates = []
    if os.environ.get("TRAINING_KIT_HOME"):
        candidates.append(Path(os.environ["TRAINING_KIT_HOME"]))
    candidates.append(Path(os.path.realpath(__file__)).parents[3])
    for root in candidates:
        if (root / "brand" / "colors.json").exists():
            return root
    raise SystemExit("Kit root tidak ditemukan. Set TRAINING_KIT_HOME ke folder repo training-module-skills.")


REPO_ROOT = find_kit_root()
COLORS = json.loads((REPO_ROOT / "brand" / "colors.json").read_text(encoding="utf-8"))
FONT = COLORS.get("font_body", "Arial")
FONT_CODE = COLORS.get("font_code", "Courier New")


def rgb(name: str) -> RGBColor:
    return RGBColor.from_string(COLORS[name].replace("#", ""))


def run_font(run, size=11, bold=False, italic=False, color="text_primary", font=None):
    run.font.name = font or FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)


def shade(paragraph, color_name: str) -> None:
    ppr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), COLORS[color_name].replace("#", ""))
    ppr.append(shd)


def title_block(doc, kicker, title, subtitle):
    logo = REPO_ROOT / "brand" / "logo-light-bg.png"
    if logo.exists():
        doc.add_picture(str(logo), width=Pt(110))
    run_font(doc.add_paragraph().add_run(kicker.upper()), size=10, bold=True, color="accent")
    run_font(doc.add_paragraph().add_run(title), size=24, bold=True, color="primary")
    run_font(doc.add_paragraph().add_run(subtitle), size=12, italic=True, color="text_secondary")
    doc.add_paragraph()


def heading1(doc, number, text):
    run_font(doc.add_heading(level=1).add_run(f"{number}. {text}"), size=16, bold=True, color="primary")


def heading2(doc, text):
    run_font(doc.add_heading(level=2).add_run(text), size=13, bold=True, color="primary")


def paragraph(doc, text):
    run_font(doc.add_paragraph().add_run(text), size=11)


def bullets(doc, items):
    for item in items:
        run_font(doc.add_paragraph(style="List Bullet").add_run(item), size=11)


def code_block(doc, code: str):
    for line in code.rstrip("\n").split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Pt(18)
        shade(p, "surface")
        run_font(p.add_run(line if line else " "), size=9.5, font=FONT_CODE)
    doc.add_paragraph()


def steps(doc, step_list):
    """Setiap langkah: title, substeps (list teks), code (opsional), checkpoint."""
    for n, step in enumerate(step_list, start=1):
        heading2(doc, f"Langkah {n} - {step['title']}")
        for i, text in enumerate(step["substeps"], start=1):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(18)
            run_font(p.add_run(f"{n}.{i}  "), bold=True, color="accent")
            run_font(p.add_run(text))
        if step.get("code"):
            code_block(doc, step["code"])
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Pt(18)
        p.paragraph_format.space_after = Pt(10)
        run_font(p.add_run("CHECKPOINT - "), bold=True, color="accent")
        run_font(p.add_run(step["checkpoint"]), italic=True, color="text_secondary")


def footer(doc, text):
    p = doc.sections[0].footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_font(p.add_run(text), size=8, color="muted")


def build_modul_praktikum(spec: dict, output: Path) -> None:
    """Struktur Modul Praktikum (mode Live Session): 5 heading tetap."""
    doc = Document()
    title_block(doc, spec.get("kicker", "Modul Praktikum"), spec["title"], spec["subtitle"])
    heading1(doc, 1, "Tujuan Pembelajaran")
    bullets(doc, spec["objectives"])
    heading1(doc, 2, spec.get("overview_heading", "Gambaran Alur"))
    paragraph(doc, spec["overview"])
    heading1(doc, 3, "Persiapan Sebelum Mulai")
    bullets(doc, spec["prep"])
    heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    steps(doc, spec["steps"])
    heading1(doc, 5, "Latihan Mandiri")
    bullets(doc, spec["self_practice"])
    footer(doc, spec.get("footer", "Insignia - Data & AI Mentor Program"))
    save(doc, output)


def build_panduan_bagian(spec: dict, output: Path) -> None:
    """Struktur Panduan Bagian (mode Preparation): self-study, ada konsep singkat dan bukti selesai."""
    doc = Document()
    title_block(doc, spec.get("kicker", "Panduan Bagian"), spec["title"], spec["subtitle"])
    heading1(doc, 1, "Tujuan")
    bullets(doc, spec["objectives"])
    heading1(doc, 2, "Konsep Singkat")
    for item in spec["concepts"]:
        heading2(doc, item["heading"])
        paragraph(doc, item["body"])
    heading1(doc, 3, "Persiapan")
    bullets(doc, spec["prep"])
    heading1(doc, 4, "Langkah Mengerjakan")
    steps(doc, spec["steps"])
    heading1(doc, 5, "Bukti Selesai")
    bullets(doc, spec["evidence"])
    heading1(doc, 6, "Latihan Mandiri")
    bullets(doc, spec["self_practice"])
    footer(doc, spec.get("footer", "Insignia - Data & AI Mentor Program"))
    save(doc, output)


def save(doc, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(f"Tersimpan: {output}")


DEMO_STEPS = [{
    "title": "Jalankan contoh",
    "substeps": ["Buka terminal di folder Starter Kit.", "Jalankan perintah di bawah."],
    "code": "import statistics\nprint(statistics.mean([3, 5, 7]))",
    "checkpoint": "Terminal menampilkan angka 5.",
}]

DEMO_PRAKTIKUM = {
    "title": "Contoh Modul Praktikum", "subtitle": "Data sintetis untuk menguji struktur",
    "objectives": ["Peserta mampu menjalankan contoh end-to-end"],
    "overview": "Input, proses, output.", "prep": ["Python 3 terpasang"],
    "steps": DEMO_STEPS, "self_practice": ["Ganti angka input dan bandingkan hasilnya."],
}

DEMO_PANDUAN = {
    "title": "Contoh Panduan Bagian", "subtitle": "Data sintetis untuk menguji struktur",
    "objectives": ["Memahami konsep contoh"],
    "concepts": [{"heading": "Konsep A", "body": "Penjelasan singkat konsep A."}],
    "prep": ["Python 3 terpasang"], "steps": DEMO_STEPS,
    "evidence": ["Screenshot output terminal"], "self_practice": ["Coba variasi input."],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("struktur", choices=["modul-praktikum", "panduan-bagian", "demo"])
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    if args.struktur == "demo":
        out = Path(args.paths[0])
        build_modul_praktikum(DEMO_PRAKTIKUM, out / "demo_modul_praktikum.docx")
        build_panduan_bagian(DEMO_PANDUAN, out / "demo_panduan_bagian.docx")
        return
    if len(args.paths) != 2:
        parser.error("butuh <spec.json> <output.docx>")
    spec = json.loads(Path(args.paths[0]).read_text(encoding="utf-8"))
    builder = build_modul_praktikum if args.struktur == "modul-praktikum" else build_panduan_bagian
    builder(spec, Path(args.paths[1]))


if __name__ == "__main__":
    main()
