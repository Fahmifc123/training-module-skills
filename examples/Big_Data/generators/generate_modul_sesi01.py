"""Generate Modul Praktikum Big Data Sesi 1 - Intro Classical Data Processing.

Kode di setiap langkah diambil langsung dari generate_notebook_sesi01.CELLS
supaya isi modul selalu sama dengan notebook peserta.
"""
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from generate_notebook_sesi01 import CELLS
from insignia_docx_lib import (
    COLOR_PRIMARY, add_bullets, add_checkpoint, add_heading1, add_heading2,
    add_substep, add_title_block, set_run_font,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "Big_Data" / "Sesi_01_Intro_Classical_Data_Processing" / "2_Modul_Praktikum" / "Modul_Praktikum_Intro_Classical_Data_Processing.docx"

CODE = [src for kind, src in CELLS if kind == "code"]  # urutan: L0, L1, L2, L3, L4, L5a, L5b, L6, L7, L8, L9, L10, L11


def add_code(doc, code):
    """Blok kode Courier New dengan background abu (surface #F2F3F7)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "F2F3F7")
    pPr.append(shd)
    lines = code.strip("\n").split("\n")
    for i, line in enumerate(lines):
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_PRIMARY
        if i < len(lines) - 1:
            r.add_break()


def add_para(doc, text, italic=False):
    p = doc.add_paragraph()
    set_run_font(p.add_run(text), size=11, italic=italic)


MODULE_TITLE = "Intro Classical Data Processing"
MODULE_SUBTITLE = "Big Data - Sesi 1: mini pipeline retail dengan pandas dan SQLite untuk data tabular dan non-tabular di satu mesin"

LEARNING_OBJECTIVES = [
    "Peserta mampu menjelaskan alur pemrosesan data klasik: extract, clean, transform, aggregate, load.",
    "Peserta mampu menjalankan alur tersebut dengan dataframe pandas di satu mesin, untuk data tabular (CSV) dan non-tabular (JSON bertingkat, teks bebas, gambar).",
    "Peserta mampu membandingkan dataframe dan SQL di database relasional untuk operasi yang sama.",
    "Peserta mampu mengenali tanda pendekatan klasik mulai kewalahan (memori, waktu, satu mesin).",
]

OVERVIEW = [
    "Bagian A (langkah 1-8), data tabular. Pertanyaan bisnis: berapa revenue dari transaksi COMPLETED, per kota, per bulan, dan per tipe toko?",
    "Alur pipeline: retail_transactions.csv -> extract -> clean -> transform -> aggregate (plus join stores.csv) "
    "-> load ke revenue_by_city.csv. Langkah 7 menjalankan query yang sama di SQLite untuk membandingkan hasil "
    "dataframe dan SQL.",
    "Aturan bisnis: hanya transaksi COMPLETED yang dihitung. Transaksi CANCELLED dan REFUNDED dibuang. "
    "revenue = quantity x unit_price.",
    "Bagian B (langkah 9-11), data non-tabular. Pertanyaan bisnis: (a) apakah order dari aplikasi cocok dengan data transaksi, "
    "dan berapa order per channel; (b) bagaimana sentimen ulasan pelanggan per kota; (c) seperti apa karakteristik gambar produk per kategori.",
    "Bagian B memakai data non-tabular turunan transaksi yang sama, terhubung lewat transaction_id: "
    "orders_app.json (JSON bertingkat, 2.000 order aplikasi), reviews.csv (3.000 ulasan teks bebas), dan product_images/ "
    "(180 gambar produk). Bagian B hanya butuh Langkah 0, jadi bisa dijalankan tanpa bagian A atau setelah Restart Kernel. Lima tahap tetap sama; pekerjaan terbesarnya ada di tahap extract, yaitu mengubah data menjadi baris dan kolom.",
    "Dataset bersifat sintetis (bukan data internal Insignia atau klien): 1.000.000 baris, periode Januari - Desember 2025, "
    "8 kota, 40 toko. Angka waktu (baca CSV, load SQLite) berbeda di setiap laptop, jadi tidak dipakai sebagai checkpoint.",
]

PREP_CHECKLIST = [
    "Python 3.12 ke atas terpasang (pandas 3.0.5 dan numpy 2.5.4 tidak tersedia untuk Python 3.10 dan 3.11). Angka acuan diverifikasi dengan Python 3.13, pandas 3.0.5, pyarrow 26.0.1, dan Pillow 12.3.0.",
    "Jupyter Notebook atau VS Code (dengan extension Python dan Jupyter) terpasang.",
    "Folder 3_Starter_Kit_Peserta sudah disalin ke laptop dari folder bersama: Notebook_Mini_Pipeline_Retail.ipynb, "
    "retail_transactions.csv, stores.csv, orders_app.json, reviews.csv, folder product_images/ (180 file), requirements.txt, README_Setup.md.",
    "Ruang disk kosong minimal 500 MB (CSV sekitar 93 MB, data non-tabular sekitar 5,5 MB, retail.db yang terbentuk di langkah 7 sekitar 98 MB).",
    "Verifikasi environment di README_Setup.md sudah dijalankan sebelum sesi (sekitar 5 menit).",
]

STEPS = [
    {
        "title": "Langkah 0 - Buka Notebook dan Verifikasi Environment",
        "substeps": [
            ("0.1", "Instalasi (.venv dan pip install -r requirements.txt) sudah dikerjakan sebelum sesi lewat README_Setup.md, jadi tidak perlu diulang di kelas. Kalau belum, ikuti README_Setup.md dulu."),
            ("0.2", "Buka terminal di folder Starter Kit, lalu aktifkan environment. Windows: .venv\\Scripts\\activate. macOS/Linux: source .venv/bin/activate"),
            ("0.3", "Jupyter: jalankan jupyter notebook, lalu klik Notebook_Mini_Pipeline_Retail.ipynb. VS Code: File > Open Folder, pilih folder Starter Kit, buka notebook, klik Select Kernel > Python Environments > .venv."),
            ("0.4", "Klik sel Langkah 0, lalu tekan Shift+Enter untuk menjalankannya."),
        ],
        "code": CODE[0],
        "checkpoint": "Output mencetak pandas : 3.0.5, pyarrow : 26.0.1, Pillow : 12.3.0, dan lima baris ada (retail_transactions.csv, stores.csv, orders_app.json, reviews.csv, product_images). "
                      "Jika tertulis TIDAK ADA, sel berhenti dengan FileNotFoundError: buka notebook dari folder Starter Kit yang berisi semua file data, lalu jalankan ulang sel. "
                      "Galat No module named 'PIL' berarti Pillow belum terpasang: jalankan ulang pip install -r requirements.txt.",
    },
    {
        "title": "Langkah 1 - Extract: Baca CSV",
        "substeps": [
            ("1.1", "Jalankan sel Langkah 1 dengan Shift+Enter. Sel ini membaca retail_transactions.csv dengan pd.read_csv."),
            ("1.2", "Baca tiga baris output: waktu baca, shape, dan memori. Lihat juga 5 baris pertama tabel."),
        ],
        "code": CODE[1],
        "checkpoint": "Shape: (1000000, 10). Memori sekitar 155 MB. Waktu baca beberapa detik dan berbeda di setiap laptop.",
    },
    {
        "title": "Langkah 2 - Inspect: Tipe Data, Nilai Kosong, Duplikat",
        "substeps": [
            ("2.1", "Jalankan sel Langkah 2."),
            ("2.2", "Perhatikan kolom transaction_ts masih bertipe str (teks), belum datetime."),
            ("2.3", "Catat sebaran nilai kolom status."),
        ],
        "code": CODE[2],
        "checkpoint": "Nilai kosong: 0. Duplikat transaction_id: 0. COMPLETED 900347, CANCELLED 69741, REFUNDED 29912.",
    },
    {
        "title": "Langkah 3 - Clean: Ubah Tipe dan Filter COMPLETED",
        "substeps": [
            ("3.1", "Jalankan sel Langkah 3. Baris pertama mengubah transaction_ts menjadi datetime."),
            ("3.2", "Baris kedua mengambil hanya transaksi COMPLETED sesuai aturan bisnis. .copy() membuat dataframe baru agar penambahan kolom di langkah 4 tidak memunculkan peringatan."),
        ],
        "code": CODE[3],
        "checkpoint": "Baris tersisa: 900347.",
    },
    {
        "title": "Langkah 4 - Transform: Kolom revenue dan month",
        "substeps": [
            ("4.1", "Jalankan sel Langkah 4. revenue dihitung sebagai quantity x unit_price untuk semua baris sekaligus (vectorized operation), tanpa loop per baris."),
            ("4.2", "Kolom month dibentuk dari transaction_ts dengan format YYYY-MM."),
        ],
        "code": CODE[4],
        "checkpoint": "Total revenue: 3,273,759,911,000 (3.273.759.911.000).",
    },
    {
        "title": "Langkah 5 - Aggregate: Revenue per Kota dan per Bulan",
        "substeps": [
            ("5.1", "Jalankan sel pertama Langkah 5 (revenue per kota). Hasil disimpan di variabel revenue_by_city dan dipakai lagi di langkah 7 dan 8."),
            ("5.2", "Jalankan sel kedua Langkah 5 (revenue per bulan)."),
        ],
        "code": CODE[5] + "\n\n# --- sel berikutnya ---\n" + CODE[6],
        "checkpoint": "Jumlah kota: 8. Tiga teratas: Jakarta 918117634000, Surabaya 528045460000, Bandung 457990352000 (918,1 / 528,0 / 458,0 miliar). "
                      "Jumlah bulan: 12. Bulan tertinggi: 2025-12. Revenue bulan tertinggi: 280,072,930,000 (280,1 miliar).",
    },
    {
        "title": "Langkah 6 - Join: Gabungkan dengan stores.csv",
        "substeps": [
            ("6.1", "Jalankan sel Langkah 6. Sel ini membaca stores.csv dari Starter Kit (jangan dibuat ulang) lalu melakukan left join pada store_id."),
            ("6.2", "Periksa baris tanpa pasangan. Nilai 0 berarti setiap transaksi punya data toko."),
        ],
        "code": CODE[7],
        "checkpoint": "Jumlah toko: 40. Baris tanpa pasangan: 0. Supermarket 1394541727000, Ruko 1082502474000, Mall 796715710000 (1,39 / 1,08 / 0,80 triliun).",
    },
    {
        "title": "Langkah 7 - SQL: Query yang Sama di SQLite",
        "substeps": [
            ("7.1", "Jalankan sel Langkah 7. Sel ini membuat file retail.db, memuat 1.000.000 baris ke tabel transactions, lalu menjalankan query revenue per kota."),
            ("7.2", "Tunggu sampai sel selesai. Load ke SQLite butuh beberapa detik; selama tanda [*] masih muncul di samping sel, notebook sedang bekerja, bukan macet."),
            ("7.3", "Bandingkan tabel hasil SQL dengan hasil langkah 5."),
        ],
        "code": CODE[8],
        "checkpoint": "same_as_pandas: True. Tabel hasil SQL sama persis dengan revenue_by_city di langkah 5. Waktu load dan query berbeda di setiap laptop, jadi tidak dipakai sebagai patokan.",
    },
    {
        "title": "Langkah 8 - Load dan Batas Satu Mesin",
        "substeps": [
            ("8.1", "Jalankan sel Langkah 8. Hasil agregasi disimpan ke revenue_by_city.csv di folder yang sama."),
            ("8.2", "Bandingkan memori di langkah ini dengan langkah 1. Angkanya lebih kecil karena transaction_ts sudah berupa datetime, bukan teks."),
            ("8.3", "Baca estimasi 100x. Angka memori ini berlaku untuk pandas 3.x dengan pyarrow terpasang."),
            ("8.4", "Titik berhenti bagian A: cocokkan semua checkpoint langkah 1-8, lalu jawab pertanyaan di sel berikutnya: kalau datanya 100 kali lebih besar, apa yang terjadi di laptopmu?"),
        ],
        "code": CODE[9],
        "checkpoint": "Baris di revenue_by_city.csv: 8. Memori setelah tipe dirapikan sekitar 136 MB. Estimasi 100x sekitar 14 GB (tercetak 13.6 GB).",
    },
    {
        "title": "Langkah 9 - JSON Bertingkat: Order Aplikasi",
        "substeps": [
            ("9.1", "Jalankan sel Langkah 9. orders_app.json dibaca dengan modul json, lalu pd.json_normalize membuat satu baris per item (record_path=\"items\")."),
            ("9.2", "Perhatikan kolom customer.tier, customer.city, dan payment.method: field bertingkat ikut menjadi kolom lewat meta."),
            ("9.3", "Baris pertama sel membaca ulang kolom acuan dari retail_transactions.csv (variabel ref), lalu revenue tiap item dicocokkan dengan transaksi COMPLETED lewat transaction_id. Karena itu bagian B tidak bergantung pada variabel dari bagian A."),
            ("9.4", "Satu order berisi 1-4 item dari toko, metode bayar, dan tanggal yang sama, sehingga customer.city dan payment.method berlaku untuk semua item-nya."),
        ],
        "code": CODE[10],
        "checkpoint": "Jumlah order: 2000. Shape items: (4704, 10). Item cocok dengan CSV: 4704. Revenue sama: True. "
                      "Total revenue: 17,362,020,000 (17,4 miliar; lebih kecil dari CSV karena JSON hanya memuat 4.704 transaksi). Order per channel: android 620, ios 694, web 686.",
    },
    {
        "title": "Langkah 10 - Teks Bebas: Sentimen Ulasan",
        "substeps": [
            ("10.1", "Jalankan sel Langkah 10. Setiap ulasan dihitung kata positif dan negatifnya dari kamus kecil di sel (POSITIF dan NEGATIF), lalu diberi label positif, negatif, atau netral. Ini kamus kata sederhana, bukan NLP."),
            ("10.2", "Hasil sentimen di-join ke kota lewat transaction_id."),
            ("10.3", "Perhatikan tabel terakhir: ulasan yang mengandung kata tidak. Dari tiga kalimat, dua terbaca salah: \"Lumayan, tidak buruk untuk harga segini.\" (maksudnya positif, terbaca negatif) dan \"Tidak bagus, warnanya pudar.\" (maksudnya negatif, terbaca netral). \"Kualitas buruk, tidak sesuai foto.\" terbaca negatif, dan itu benar. Ini disengaja untuk memperlihatkan batas kamus sederhana, bukan bug."),
        ],
        "code": CODE[11],
        "checkpoint": "positif 1653, negatif 684, netral 663. Proporsi negatif tertinggi: Medan 0.28 (28%). "
                      "Tabel kata tidak: Kualitas buruk... negatif 128 (benar), Lumayan, tidak buruk... negatif 78 (salah), Tidak bagus, warnanya pudar. netral 67 (salah).",
    },
    {
        "title": "Langkah 11 - Gambar: Metadata dan Piksel",
        "substeps": [
            ("11.1", "Jalankan sel Langkah 11. Setiap file di product_images/ dibuka dengan Pillow; lebar, tinggi, mode, ukuran file, dan rata-rata piksel (R, G, B, brightness) disimpan sebagai satu baris."),
            ("11.2", "Kategori diambil dari nama file (misalnya home_living_001.png) lalu dipetakan ke nama kategori di CSV (Home & Living) dengan SLUG_TO_CATEGORY."),
            ("11.3", "Jawab pertanyaan penutup: kalau gambarnya 1 juta file dan ulasannya 100 juta baris, tahap mana yang paling lambat?"),
        ],
        "code": CODE[12],
        "checkpoint": "Jumlah gambar: 180. 88 gambar 64x64 dan 92 gambar 128x128, semua mode RGB. Ukuran file: 8.2-32.4 KB, total 3699 KB. "
                      "Brightness terendah Electronics 92.5, tertinggi Beauty 195.9.",
    },
]



def build() -> None:
    doc = Document()
    add_title_block(doc, kicker="Modul Praktikum", title=MODULE_TITLE, subtitle=MODULE_SUBTITLE)

    add_heading1(doc, 1, "Tujuan Pembelajaran")
    add_bullets(doc, LEARNING_OBJECTIVES)

    add_heading1(doc, 2, "Gambaran Alur Pipeline Tabular dan Non-Tabular")
    for text in OVERVIEW:
        add_para(doc, text)

    add_heading1(doc, 3, "Persiapan Sebelum Mulai")
    add_bullets(doc, PREP_CHECKLIST)

    add_heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    add_para(doc, "Semua sel di notebook sudah terisi lengkap. Jalankan sel secara berurutan dari atas. "
                  "Jika tertinggal atau ada error, pilih Run All (Jupyter: Run > Run All Cells; VS Code: tombol Run All).", italic=True)
    parts = {"Langkah 1 ": ("Bagian A - Data Tabular (Langkah 1-8)", "retail_transactions.csv dan stores.csv."),
             "Langkah 9 ": ("Bagian B - Data Non-Tabular (Langkah 9-11)",
                            "orders_app.json, reviews.csv, dan product_images/. Bagian ini hanya butuh Langkah 0, "
                            "jadi tetap jalan walau bagian A belum dijalankan atau kernel di-restart.")}
    for step in STEPS:
        for prefix, (part_title, part_desc) in parts.items():
            if step["title"].startswith(prefix):
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(14)
                set_run_font(p.add_run(part_title.upper()), size=12, bold=True, color=COLOR_PRIMARY)
                add_para(doc, part_desc, italic=True)
        add_heading2(doc, step["title"])
        for label, text in step["substeps"]:
            add_substep(doc, label, text)
        add_code(doc, step["code"])
        add_checkpoint(doc, step["checkpoint"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("->", OUT)


if __name__ == "__main__":
    build()
