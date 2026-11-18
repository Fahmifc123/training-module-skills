from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from insignia_docx_lib import (
    COLOR_PRIMARY, add_bullets, add_checkpoint, add_heading1, add_heading2,
    add_substep, add_title_block, set_run_font,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "Introduction_to_Big_Data" / "2_Modul_Praktikum" / "Modul_Praktikum_Introduction_to_Big_Data.docx"


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
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_PRIMARY
        if i < len(lines) - 1:
            r.add_break()


def add_para(doc, text):
    p = doc.add_paragraph()
    set_run_font(p.add_run(text), size=11)


MODULE_TITLE = "Introduction to Big Data"
MODULE_SUBTITLE = "Hands-on: Pandas vs PySpark pada dataset yang sama (retail_transactions.csv) di Databricks"

LEARNING_OBJECTIVES = [
    "Peserta mampu menyiapkan data di Unity Catalog Volume dan menjalankan notebook di Databricks",
    "Peserta mampu menjalankan transformasi dasar (read, filter, groupBy, write) dengan Pandas",
    "Peserta mampu menjalankan transformasi yang sama dengan PySpark DataFrame API",
    "Peserta memahami perbedaan eager vs lazy evaluation lewat pengamatan langsung",
    "Peserta mampu memverifikasi bahwa hasil Pandas dan PySpark identik, lalu membandingkan waktu eksekusinya",
]

OVERVIEW_TEXT = (
    "Alur hands-on: retail_transactions.csv (1.000.000 baris, 93,5 MB) di-upload ke Volume "
    "/Volumes/workspace/default/bigdata_intro -> dibaca dua kali, sekali dengan Pandas dan sekali dengan PySpark -> "
    "kedua versi menjalankan logika yang sama persis: ambil transaksi dengan status COMPLETED, hitung "
    "revenue = quantity x unit_price, lalu agregasi total_revenue dan n_trx per city dan category -> "
    "Pandas menulis summary_pandas.parquet ke Volume, PySpark menulis tabel Delta workspace.default.summary_spark -> "
    "hasil keduanya dibandingkan."
)
OVERVIEW_NOTE = (
    "Catatan penting: di dataset sebesar ini, Pandas kemungkinan besar lebih cepat daripada PySpark. Itu disengaja. "
    "Spark punya overhead (menyusun plan, menjadwalkan task ke executor) yang baru terbayar ketika data tidak lagi "
    "muat di memori satu mesin. Tujuan hands-on ini adalah merasakan perbedaan model eksekusinya, bukan membuktikan "
    "Spark selalu lebih cepat."
)

PREP_CHECKLIST = [
    "Akun Databricks aktif: workspace Insignia (utama) atau Databricks Free Edition (alternatif, daftar di databricks.com/learn/free-edition). "
    "Databricks Community Edition sudah tidak tersedia.",
    "Sudah login dan bisa membuka menu Catalog dan Workspace di sidebar kiri.",
    "File dari folder 3_Starter_Kit_Peserta sudah di-download ke laptop: retail_transactions.csv dan Notebook_Pandas_vs_PySpark.ipynb.",
    "Sudah membaca README_Setup.md di folder yang sama.",
    "Python 3.10+ hanya diperlukan kalau ingin mencoba versi Pandas di laptop sendiri (opsional, di luar sesi).",
]

STEPS = [
    {
        "title": "Langkah 1 - Siapkan Volume dan Upload Dataset",
        "substeps": [
            ("1.1", "Di sidebar kiri Databricks, klik Catalog."),
            ("1.2", "Expand catalog workspace, lalu klik schema default."),
            ("1.3", "Klik tombol Create di kanan atas, pilih Volume."),
            ("1.4", "Isi Volume name dengan bigdata_intro, biarkan Volume type = Managed volume, lalu klik Create."),
            ("1.5", "Di halaman volume bigdata_intro, klik Upload to this volume."),
            ("1.6", "Pilih file retail_transactions.csv dari laptop, klik Upload, tunggu sampai selesai (93,5 MB)."),
            ("1.7", "Workspace Insignia memakai nama catalog lain? Catat path volume yang tampil di bagian atas halaman; "
                    "di Langkah 2 kamu cukup mengganti DATA_PATH, OUTPUT_DIR, dan TABLE_NAME di cell Setup."),
        ],
        "checkpoint": "Volume bigdata_intro menampilkan file retail_transactions.csv dengan ukuran sekitar 93,5 MB, "
                      "dan path-nya adalah /Volumes/workspace/default/bigdata_intro/retail_transactions.csv.",
    },
    {
        "title": "Langkah 2 - Import Notebook dan Hubungkan ke Compute",
        "substeps": [
            ("2.1", "Di sidebar kiri, klik Workspace, lalu buka folder Home (folder dengan nama email kamu)."),
            ("2.2", "Klik tombol kebab (tiga titik) di kanan atas, atau klik kanan di area kosong, lalu pilih Import."),
            ("2.3", "Pilih File, drag file Notebook_Pandas_vs_PySpark.ipynb, lalu klik Import."),
            ("2.4", "Buka notebook yang baru ter-import."),
            ("2.5", "Klik dropdown Connect di kanan atas, pilih Serverless. Di workspace Insignia, pilih cluster yang "
                    "ditentukan trainer kalau Serverless tidak tersedia."),
            ("2.6", "Jalankan cell Setup (cell pertama) dengan Shift+Enter."),
        ],
        "code": 'DATA_PATH = "/Volumes/workspace/default/bigdata_intro/retail_transactions.csv"\n'
                'OUTPUT_DIR = "/Volumes/workspace/default/bigdata_intro"\n'
                'TABLE_NAME = "workspace.default.summary_spark"\n'
                'print("DATA_PATH :", DATA_PATH)',
        "checkpoint": "Indikator compute di kanan atas berwarna hijau (Connected), dan cell Setup selesai tanpa error "
                      "serta mencetak path DATA_PATH.",
    },
    {
        "title": "Langkah 3 - Versi Pandas (Single-Machine)",
        "substeps": [
            ("3.1", "Di cell TODO 1, lengkapi kode Pandas berikut. Perhatikan setiap baris langsung dieksekusi (eager)."),
            ("3.2", "Jalankan cell dengan Shift+Enter, lalu catat waktu yang tercetak di baris Pandas selesai dalam ... detik."),
            ("3.3", "Jalankan cell berikutnya, summary_pd.head(5), untuk melihat 5 baris teratas."),
        ],
        "code": '''import time
import pandas as pd

t0 = time.perf_counter()
df = pd.read_csv(DATA_PATH)
completed = df[df["status"] == "COMPLETED"].copy()
completed["revenue"] = completed["quantity"] * completed["unit_price"]
summary_pd = (completed.groupby(["city", "category"], as_index=False)
              .agg(total_revenue=("revenue", "sum"),
                   n_trx=("transaction_id", "count"))
              .sort_values("total_revenue", ascending=False))
summary_pd.to_parquet(f"{OUTPUT_DIR}/summary_pandas.parquet", index=False)
pandas_seconds = time.perf_counter() - t0

print(f"Jumlah baris raw       : {len(df):,}")
print(f"Jumlah baris COMPLETED : {len(completed):,}")
print(f"Jumlah baris summary   : {len(summary_pd)}")
print(f"Pandas selesai dalam {pandas_seconds:.2f} detik")''',
        "checkpoint": "Output menunjukkan Jumlah baris raw = 1,000,000, Jumlah baris COMPLETED = 900,347, dan "
                      "Jumlah baris summary = 48. Baris teratas summary_pd adalah Jakarta / Electronics dengan "
                      "total_revenue = 438029827000 dan n_trx = 30254. File summary_pandas.parquet muncul di Volume bigdata_intro.",
    },
    {
        "title": "Langkah 4 - Versi PySpark (Distributed) dan Lazy Evaluation",
        "substeps": [
            ("4.1", "Di cell TODO 2, lengkapi kode PySpark berikut. Cell ini HANYA menyusun rencana transformasi."),
            ("4.2", "Jalankan cell tersebut dan amati: cell selesai hampir seketika karena belum ada data yang diproses "
                    "(lazy evaluation). spark.read dengan inferSchema=True tetap memicu satu job kecil untuk membaca schema."),
            ("4.3", "Di cell TODO 3, jalankan action write. Di sinilah Spark benar-benar memproses data."),
            ("4.4", "Klik teks Spark Jobs di bawah output cell untuk melihat job dan stage yang dijalankan (lihat stage yang melibatkan shuffle karena groupBy)."),
            ("4.5", "Catat waktu yang tercetak di baris PySpark selesai dalam ... detik."),
        ],
        "code": '''# TODO 2 - versi PySpark: transformasi (lazy)
from pyspark.sql import functions as F

df_sp = spark.read.csv(DATA_PATH, header=True, inferSchema=True)
summary_sp = (df_sp.filter(F.col("status") == "COMPLETED")
              .withColumn("revenue", F.col("quantity") * F.col("unit_price"))
              .groupBy("city", "category")
              .agg(F.sum("revenue").alias("total_revenue"),
                   F.count("transaction_id").alias("n_trx"))
              .orderBy(F.desc("total_revenue")))
print("Plan tersusun - belum ada data yang diproses")

# TODO 3 - action (eksekusi nyata)
t0 = time.perf_counter()
summary_sp.write.mode("overwrite").format("delta").saveAsTable(TABLE_NAME)
spark_seconds = time.perf_counter() - t0

n_summary = spark.table(TABLE_NAME).count()
print(f"Jumlah baris raw     : {df_sp.count():,}")
print(f"Jumlah baris summary : {n_summary}")
print(f"PySpark selesai dalam {spark_seconds:.2f} detik")''',
        "checkpoint": "Output menunjukkan Jumlah baris raw = 1,000,000 dan Jumlah baris summary = 48. Di Catalog -> "
                      "workspace -> default muncul tabel summary_spark. Cell display(spark.table(TABLE_NAME)) "
                      "menampilkan baris teratas Jakarta / Electronics, total_revenue = 438029827000, n_trx = 30254.",
    },
    {
        "title": "Langkah 5 - Bandingkan Hasil dan Waktu Eksekusi",
        "substeps": [
            ("5.1", "Di cell TODO 4, jalankan kode berikut untuk membandingkan hasil Pandas dan PySpark baris per baris."),
            ("5.2", "Isi tabel refleksi di cell markdown terakhir notebook: waktu Pandas, waktu PySpark, dan satu kalimat "
                    "penjelasan kenapa hasilnya begitu."),
            ("5.3", "Diskusikan dengan trainer: pada ukuran data berapa PySpark mulai lebih unggul, dan kenapa."),
        ],
        "code": '''keys = ["city", "category"]
left = summary_pd.sort_values(keys).reset_index(drop=True)
right = (spark.table(TABLE_NAME).toPandas()
         .sort_values(keys).reset_index(drop=True))

pd.testing.assert_frame_equal(left, right, check_dtype=False)
print("Hasil Pandas dan PySpark IDENTIK")
print(f"Total revenue  : {left['total_revenue'].sum():,}")
print(f"Total transaksi: {left['n_trx'].sum():,}")
print(f"Pandas {pandas_seconds:.2f} s vs PySpark {spark_seconds:.2f} s")''',
        "checkpoint": "Output mencetak Hasil Pandas dan PySpark IDENTIK, Total revenue = 3,273,759,911,000, dan "
                      "Total transaksi = 900,347. Waktu eksekusi boleh berbeda antar peserta; yang wajib sama adalah angkanya.",
    },
]

SELF_PRACTICE = [
    "Tambahkan filter hanya untuk payment_method == \"E-Wallet\" di kedua versi, lalu pastikan hasil Pandas dan PySpark tetap identik.",
    "Ganti agregasi menjadi revenue per bulan (ambil bulan dari kolom transaction_ts) di kedua versi.",
    "Hapus parameter inferSchema=True dan definisikan schema secara eksplisit dengan StructType. Bandingkan waktu spark.read sebelum dan sesudah.",
    "Simulasikan data 5x lebih besar dengan menggabungkan 5 salinan df_sp memakai union (dan 5 salinan df memakai pd.concat untuk Pandas), lalu bandingkan lagi waktu Pandas vs PySpark. Amati kapan Pandas mulai berat.",
    "Jalankan DESCRIBE HISTORY workspace.default.summary_spark di cell SQL, lalu catat apa yang tercatat (pengantar untuk modul Delta Lake & Lakehouse Ops).",
]


def build_modul(output_path: Path) -> None:
    doc = Document()
    add_title_block(doc, kicker="Modul Praktikum", title=MODULE_TITLE, subtitle=MODULE_SUBTITLE)

    add_heading1(doc, 1, "Tujuan Pembelajaran")
    add_bullets(doc, LEARNING_OBJECTIVES)

    add_heading1(doc, 2, "Gambaran Alur")
    add_para(doc, OVERVIEW_TEXT)
    add_para(doc, OVERVIEW_NOTE)

    add_heading1(doc, 3, "Persiapan Sebelum Mulai")
    add_bullets(doc, PREP_CHECKLIST)

    add_heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    for step in STEPS:
        add_heading2(doc, step["title"])
        for label, text in step["substeps"]:
            add_substep(doc, label, text)
        if step.get("code"):
            add_code(doc, step["code"])
        add_checkpoint(doc, step["checkpoint"])

    add_heading1(doc, 5, "Latihan Mandiri")
    add_bullets(doc, SELF_PRACTICE)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"Modul praktikum tersimpan di: {output_path}")


if __name__ == "__main__":
    build_modul(OUT)
