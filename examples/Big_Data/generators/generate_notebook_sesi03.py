"""Generate notebook hands-on Sesi 3 Big Data (lengkap, tanpa bagian kosong)."""
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "output" / "Big_Data" / "Sesi_03_Big_Data_Storage" / "3_Starter_Kit_Peserta" / "Notebook_Big_Data_Storage.ipynb")

CELLS = [
    ("md", "# Sesi 3 - Big Data Storage\nSatu dataset 10 juta transaksi, empat percobaan penyimpanan: CSV vs Parquet, column pruning, partitioning, terlalu banyak partition."),
    ("md", "## Langkah 0 - Verifikasi environment dan data\nCek versi library, file data, dan path hasil. Sel ini cepat dan tidak memuat data, jadi setelah Restart Kernel cukup jalankan sel ini lalu lanjut ke langkah mana pun."),
    ("code", """import shutil, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

print("Python  :", sys.version.split()[0])
print("pandas  :", pd.__version__)
print("pyarrow :", pa.__version__)
print("numpy   :", np.__version__)

FILE_10M = Path("retail_transactions_10m.csv")
FILE_1M = Path("retail_transactions.csv")
if not FILE_10M.exists():
    raise FileNotFoundError(
        "retail_transactions_10m.csv belum ada di folder notebook. "
        "Salin dari Starter Kit Sesi 2, atau jalankan "
        "python make_data_s02.py --tanpa-parts di folder ini. "
        "Lihat README_Setup.md.")
if not FILE_1M.exists():
    raise FileNotFoundError(
        "retail_transactions.csv (Sesi 1) belum ada di folder notebook. "
        "Lihat README_Setup.md.")

OUT = Path("hasil_s03")
OUT.mkdir(exist_ok=True)
CSV_FILE = OUT / "retail_10m.csv"
PQ_FILE = OUT / "retail_10m.parquet"
DIR_MONTH = OUT / "retail_10m_by_month"
ONE_FILE = OUT / "sample_100k.parquet"
DIR_PRODUCT = OUT / "sample_by_product"


def size_mb(path):
    if path.is_file():
        return path.stat().st_size / 1e6
    files = [f for f in path.rglob("*") if f.is_file()]
    return sum(f.stat().st_size for f in files) / 1e6


print(f"File 10m: {size_mb(FILE_10M):,.0f} MB")"""),
    ("md", "## Langkah 1 - Simpan sebagai CSV dan Parquet\nData dibaca per chunk 1 juta baris (seperti Sesi 2), lalu tiap chunk ditulis ke dua format. Memori tetap kecil walau datanya 10 juta baris."),
    ("code", """csv_write_s = pq_write_s = 0.0
n_rows, writer = 0, None
chunks = pd.read_csv(FILE_10M, chunksize=1_000_000,
                     parse_dates=["transaction_ts"])
for i, chunk in enumerate(chunks):
    t = time.perf_counter()
    chunk.to_csv(CSV_FILE, mode="w" if i == 0 else "a", header=(i == 0),
                 index=False, lineterminator="\\n")
    csv_write_s += time.perf_counter() - t

    t = time.perf_counter()
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(PQ_FILE, table.schema)
    writer.write_table(table)
    pq_write_s += time.perf_counter() - t
    n_rows += len(chunk)
writer.close()

csv_mb, pq_mb = size_mb(CSV_FILE), size_mb(PQ_FILE)
print(f"Jumlah baris: {n_rows:,}")
print(f"CSV     : {csv_mb:,.0f} MB, tulis {csv_write_s:.1f} detik")
print(f"Parquet : {pq_mb:,.0f} MB, tulis {pq_write_s:.1f} detik")
print(f"Parquet {csv_mb / pq_mb:.1f}x lebih kecil")"""),
    ("md", "## Langkah 2 - Column pruning\nBaca hanya `quantity` dan `unit_price`. Total dihitung untuk semua status, bukan hanya COMPLETED."),
    ("code", """COLS = ["quantity", "unit_price"]

t = time.perf_counter()
from_csv = pd.read_csv(CSV_FILE, usecols=COLS)
csv_read_s = time.perf_counter() - t

t = time.perf_counter()
from_pq = pd.read_parquet(PQ_FILE, columns=COLS)
pq_read_s = time.perf_counter() - t

total_csv = int((from_csv["quantity"] * from_csv["unit_price"]).sum())
total_pq = int((from_pq["quantity"] * from_pq["unit_price"]).sum())
print(f"Total quantity x unit_price, CSV     : {total_csv:,}")
print(f"Total quantity x unit_price, Parquet : {total_pq:,}")
print("Sama:", total_csv == total_pq)
print(f"Baca 2 kolom, CSV     : {csv_read_s:.1f} detik")
print(f"Baca 2 kolom, Parquet : {pq_read_s:.2f} detik")

t = time.perf_counter()
full = pd.read_parquet(PQ_FILE)
full_read_s = time.perf_counter() - t
print(f"Baca seluruh Parquet (10 kolom): {full_read_s:.2f} detik")
del from_csv, from_pq, full"""),
    ("md", "## Langkah 3a - Partitioning per bulan\nBaca Parquet langkah 1 per batch 1 juta baris, tambah kolom `month`, tulis satu folder per bulan. Folder lama dihapus dulu supaya sel aman dijalankan ulang."),
    ("code", """shutil.rmtree(DIR_MONTH, ignore_errors=True)

t = time.perf_counter()
batches = pq.ParquetFile(PQ_FILE).iter_batches(batch_size=1_000_000)
for i, batch in enumerate(batches):
    part = batch.to_pandas()
    part["month"] = part["transaction_ts"].dt.to_period("M").astype(str)
    part.to_parquet(DIR_MONTH, partition_cols=["month"], index=False,
                    basename_template=f"batch{i:02d}-{{i}}.parquet")
print(f"Tulis terpartisi: {time.perf_counter() - t:.1f} detik")

folders = sorted(p.name for p in DIR_MONTH.iterdir())
print("Jumlah folder:", len(folders))
print(folders[0], "...", folders[-1])
print(f"Ukuran total: {size_mb(DIR_MONTH):,.0f} MB")"""),
    ("md", "## Langkah 3b - Baca satu bulan\nPartition pruning dengan `filters`: hanya folder Maret yang dibaca. Pembanding: tanpa partisi, kolom `transaction_ts` dari semua bulan harus dibaca dulu untuk menemukan Maret."),
    ("code", """t = time.perf_counter()
maret = pd.read_parquet(DIR_MONTH, filters=[("month", "==", "2025-03")])
pruned_s = time.perf_counter() - t

t = time.perf_counter()
ts = pd.read_parquet(PQ_FILE, columns=["transaction_ts"])
maret_ts = ts[(ts["transaction_ts"] >= "2025-03-01")
              & (ts["transaction_ts"] < "2025-04-01")]
full_s = time.perf_counter() - t

print(f"Dengan filters       : baca {len(maret):,} baris, {pruned_s:.2f} detik")
print(f"1 kolom, semua bulan : baca {len(ts):,} baris, {full_s:.2f} detik")
print(f"Maret dari pembanding: {len(maret_ts):,} baris")
print("Jumlah baris sama:", len(maret) == len(maret_ts))
del maret, ts, maret_ts"""),
    ("md", "## Langkah 4 - Terlalu banyak partition\n100.000 baris, partisi per `product_id` (sekitar 5.000 nilai unik). Sel ini wajar lama. Jangan buka folder hasilnya di file explorer."),
    ("code", """sample = pd.read_csv(FILE_1M, nrows=100_000)
print("Nilai unik product_id:", sample["product_id"].nunique())

sample.to_parquet(ONE_FILE, index=False)
shutil.rmtree(DIR_PRODUCT, ignore_errors=True)
t = time.perf_counter()
sample.to_parquet(DIR_PRODUCT, partition_cols=["product_id"], index=False,
                  max_partitions=10_000)  # batas bawaan pyarrow 1024
print(f"Tulis terpartisi: {time.perf_counter() - t:.1f} detik")

n_files = sum(1 for f in DIR_PRODUCT.rglob("*") if f.is_file())
many_mb, one_mb = size_mb(DIR_PRODUCT), size_mb(ONE_FILE)
print(f"Satu file Parquet       : {one_mb:.1f} MB")
print(f"Partisi per product_id  : {n_files:,} file, {many_mb:,.0f} MB")
print(f"Rata-rata per file      : {many_mb * 1000 / n_files:.1f} KB")
print(f"Membengkak {many_mb / one_mb:.0f}x")"""),
    ("md", "## Langkah 5 - Tabel keputusan\nFormat dan partisi untuk tiga kasus."),
    ("code", """pd.set_option("display.max_colwidth", None)
decision = pd.DataFrame([
    ["Rekap 500 baris dikirim ke tim finance untuk dibuka di Excel",
     "CSV", "Tanpa partisi", "Data kecil, perlu dibaca manusia"],
    ["10 juta transaksi, laporan dibaca berulang dan difilter per bulan",
     "Parquet", "month", "Column pruning dan partition pruning per bulan"],
    ["100.000 baris yang sering difilter per product_id",
     "Parquet", "Tanpa partisi",
     "product_id terlalu banyak nilai unik (small files)"],
], columns=["kasus", "format", "partisi", "alasan"])
decision"""),
    ("md", "## Pembersihan\nHapus folder `hasil_s03` setelah sesi (belasan ribu file, bisa butuh beberapa menit di Windows)."),
    ("code", """shutil.rmtree(OUT, ignore_errors=True)
print("hasil_s03 ada:", OUT.exists())"""),
]


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src) for kind, src in CELLS]
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, OUT)
    print("->", OUT)


if __name__ == "__main__":
    main()
