"""Generate notebook starter (peserta) dan solusi (instructor) untuk modul Introduction to Big Data.

Kedua notebook dibangun dari sumber yang sama: cell solusi berisi kode lengkap persis seperti di
Modul Praktikum, cell starter berisi kode yang sama dengan bagian kunci diganti ___ (TODO).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "output" / "Introduction_to_Big_Data"
STARTER = BASE / "3_Starter_Kit_Peserta" / "Notebook_Pandas_vs_PySpark.ipynb"
SOLUTION = BASE / "4_Instructor_Only" / "Notebook_Pandas_vs_PySpark_SOLUTION.ipynb"

SETUP = '''# Setup - ganti path di bawah kalau workspace kamu memakai catalog/schema lain
DATA_PATH = "/Volumes/workspace/default/bigdata_intro/retail_transactions.csv"
OUTPUT_DIR = "/Volumes/workspace/default/bigdata_intro"
TABLE_NAME = "workspace.default.summary_spark"
print("DATA_PATH :", DATA_PATH)'''

PANDAS_SOLUTION = '''# TODO 1 - versi Pandas (eager, single-machine)
import time
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
print(f"Pandas selesai dalam {pandas_seconds:.2f} detik")'''
PANDAS_STARTER = PANDAS_SOLUTION.replace(
    'df[df["status"] == "COMPLETED"]', 'df[df["status"] == ___]'
).replace(
    'completed["quantity"] * completed["unit_price"]', '___  # quantity x unit_price'
).replace(
    'completed.groupby(["city", "category"], as_index=False)', 'completed.groupby(___, as_index=False)'
)

SPARK_TRANSFORM_SOLUTION = '''# TODO 2 - versi PySpark: transformasi (lazy)
from pyspark.sql import functions as F

df_sp = spark.read.csv(DATA_PATH, header=True, inferSchema=True)
summary_sp = (df_sp.filter(F.col("status") == "COMPLETED")
              .withColumn("revenue", F.col("quantity") * F.col("unit_price"))
              .groupBy("city", "category")
              .agg(F.sum("revenue").alias("total_revenue"),
                   F.count("transaction_id").alias("n_trx"))
              .orderBy(F.desc("total_revenue")))
print("Plan tersusun - belum ada data yang diproses")'''
SPARK_TRANSFORM_STARTER = SPARK_TRANSFORM_SOLUTION.replace(
    'df_sp.filter(F.col("status") == "COMPLETED")', 'df_sp.filter(___)'
).replace(
    'F.col("quantity") * F.col("unit_price")', '___'
).replace(
    '.groupBy("city", "category")', '.groupBy(___)'
)

SPARK_ACTION_SOLUTION = '''# TODO 3 - action (eksekusi nyata)
t0 = time.perf_counter()
summary_sp.write.mode("overwrite").format("delta").saveAsTable(TABLE_NAME)
spark_seconds = time.perf_counter() - t0

n_summary = spark.table(TABLE_NAME).count()
print(f"Jumlah baris raw     : {df_sp.count():,}")
print(f"Jumlah baris summary : {n_summary}")
print(f"PySpark selesai dalam {spark_seconds:.2f} detik")'''
SPARK_ACTION_STARTER = SPARK_ACTION_SOLUTION.replace(
    'summary_sp.write.mode("overwrite").format("delta").saveAsTable(TABLE_NAME)',
    'summary_sp.write.mode(___).format(___).saveAsTable(TABLE_NAME)',
)

COMPARE = '''# TODO 4 - bandingkan hasil Pandas vs PySpark
keys = ["city", "category"]
left = summary_pd.sort_values(keys).reset_index(drop=True)
right = (spark.table(TABLE_NAME).toPandas()
         .sort_values(keys).reset_index(drop=True))

pd.testing.assert_frame_equal(left, right, check_dtype=False)
print("Hasil Pandas dan PySpark IDENTIK")
print(f"Total revenue  : {left['total_revenue'].sum():,}")
print(f"Total transaksi: {left['n_trx'].sum():,}")
print(f"Pandas {pandas_seconds:.2f} s vs PySpark {spark_seconds:.2f} s")'''

REFLECTION = '''## Refleksi

| Pertanyaan | Jawaban kamu |
|---|---|
| Waktu Pandas (detik) | |
| Waktu PySpark (detik) | |
| Mana yang lebih cepat di dataset ini, dan kenapa? | |
| Kapan PySpark akan mulai lebih unggul? | |'''


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.splitlines(keepends=True)}


def build(solution: bool):
    title = "# Introduction to Big Data - Pandas vs PySpark" + (" (SOLUSI - Instructor Only)" if solution else "")
    cells = [
        md(title + "\n\nTransformasi yang sama (filter COMPLETED -> revenue -> groupBy city, category) "
                   "dijalankan dua kali pada `retail_transactions.csv` (1.000.000 baris). "
                   "Ikuti Modul Praktikum, isi setiap `___` di cell TODO."),
        md("## Setup\nJalankan cell ini dulu (Modul Praktikum Langkah 2)."),
        code(SETUP),
        md("## Bagian A - Pandas (single-machine, eager)\nModul Praktikum Langkah 3."),
        code(PANDAS_SOLUTION if solution else PANDAS_STARTER),
        code("summary_pd.head(5)"),
        md("## Bagian B - PySpark (distributed, lazy)\nModul Praktikum Langkah 4. "
           "Perhatikan: cell TODO 2 selesai hampir seketika karena belum ada data yang diproses."),
        code(SPARK_TRANSFORM_SOLUTION if solution else SPARK_TRANSFORM_STARTER),
        code(SPARK_ACTION_SOLUTION if solution else SPARK_ACTION_STARTER),
        code("display(spark.table(TABLE_NAME))"),
        md("## Bagian C - Bandingkan hasil\nModul Praktikum Langkah 5."),
        code(COMPARE),
        md(REFLECTION),
    ]
    return {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5,
    }


def write(path: Path, nb):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Notebook tersimpan di: {path}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["starter", "solution"]
    if "starter" in targets:
        write(STARTER, build(solution=False))
    if "solution" in targets:
        write(SOLUTION, build(solution=True))
