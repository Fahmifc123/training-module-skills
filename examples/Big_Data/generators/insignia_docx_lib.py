
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


