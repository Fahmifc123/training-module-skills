"""Generate notebook hands-on Sesi 2 Big Data (lengkap, tanpa bagian kosong)."""
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "output" / "Big_Data" / "Sesi_02_Common_vs_Big_Data" / "3_Starter_Kit_Peserta" / "Notebook_Tangga_Solusi.ipynb")

CELLS = [
    ("md", "# Sesi 2 - Common vs Big Data\nTangga solusi: satu pertanyaan bisnis (revenue COMPLETED per kota), lima cara menjawabnya.\n\n- Langkah 2-4: **optimasi di mesin yang sama** (baseline, tipe hemat, chunked).\n- Langkah 5: **ide scale out**, data dibagi menjadi partition lalu diproses paralel.\n- Scale up (mesin lebih besar) dibahas di slide, tidak di-hands-on.\n\nLangkah 2-3 butuh memori kosong sekitar 4 GB. Jika RAM di bawah 12 GB, lewati langkah 2-3; langkah 4-6 tetap jalan."),
    ("md", "## Langkah 0 - Verifikasi environment dan data\nCek versi library, RAM, jumlah core, dan file hasil `make_data_s02.py`."),
    ("code", """import gc, glob, os, sys, time
from multiprocessing import Pool
from pathlib import Path
import pandas as pd
import workers
pd.set_option("display.width", 120)  # tabel langkah 6 tidak terpotong

print("Python :", sys.version.split()[0])
print("pandas :", pd.__version__)
ram = workers.total_ram_gb()
print(f"RAM    : {ram:.1f} GB")
print("Core   :", os.cpu_count())
print("File 10m ada  :", Path("retail_transactions_10m.csv").exists())
print("File parts/   :", len(glob.glob("parts/part_*.csv")))
if ram < 12:
    print("Saran  : RAM < 12 GB -> lewati langkah 2-3,")
    print("         lanjut dari langkah 4 (lihat demo trainer)")"""),
    ("md", "## Langkah 1 - Kenali data dan siapkan acuan\nUkuran file, jumlah baris, dan acuan hasil: data Sesi 1 (1 juta baris) dikali 10. Semua cara dibandingkan dengan acuan ini, jadi langkah 2-3 boleh dilewati."),
    ("code", """FILE = "retail_transactions_10m.csv"
print(f"Ukuran file: {os.path.getsize(FILE) / 1e6:,.0f} MB")
with open(FILE) as f:
    n_rows = sum(1 for _ in f) - 1  # dikurangi baris header
print(f"Jumlah baris: {n_rows:,}")
print("Jumlah core:", os.cpu_count())

# Acuan: data 10m = data Sesi 1 digandakan 10 kali
sesi1 = pd.read_csv("retail_transactions.csv", usecols=workers.USECOLS)
expected = workers.revenue_by_city(sesi1) * 10
del sesi1
print(f"Total revenue acuan: {expected.sum():,}")
summary = {}  # catatan tiap cara untuk tabel di langkah 6"""),
    ("md", "## Langkah 2 - Baseline: semua kolom ke memori\nCara Sesi 1, tetapi datanya 10 kali lebih besar. Butuh memori kosong sekitar 4 GB. Jika RAM di bawah 12 GB, lewati langkah 2-3 dan lanjut ke langkah 4."),
    ("code", """start = time.perf_counter()
df = pd.read_csv(FILE)
read_s = time.perf_counter() - start
mem_mb = df.memory_usage(deep=True).sum() / 1e6
print(f"Waktu baca: {read_s:.1f} detik")
print(f"Memori: {mem_mb:,.0f} MB")

start = time.perf_counter()
baseline = workers.revenue_by_city(df)
agg_s = time.perf_counter() - start
print(f"Waktu agregasi: {agg_s:.1f} detik")
print(f"Total revenue: {baseline.sum():,}")
print("equal:", baseline.sort_index().equals(expected.sort_index()))
summary["1. Baseline"] = [mem_mb, read_s + agg_s, "baca + agregasi",
                          baseline.sum()]
baseline.sort_values(ascending=False)"""),
    ("md", "## Langkah 3 - Optimasi: tipe hemat dan kolom seperlunya\nMasih di mesin yang sama. Kolom teks berulang jadi `category`, angka jadi `int32`, lalu kolom yang tidak dipakai dibuang."),
    ("code", """for col in ["store_id", "city", "category", "product_id",
            "payment_method", "status"]:
    df[col] = df[col].astype("category")
for col in ["quantity", "unit_price"]:
    df[col] = df[col].astype("int32")

mem_all = df.memory_usage(deep=True).sum() / 1e6
slim = df.drop(columns=["transaction_id", "transaction_ts"])
mem_slim = slim.memory_usage(deep=True).sum() / 1e6
print(f"Memori semua kolom: {mem_all:,.0f} MB")
print(f"Memori tanpa id dan timestamp: {mem_slim:,.0f} MB")

start = time.perf_counter()
scaled = workers.revenue_by_city(slim)
agg_s = time.perf_counter() - start
print(f"Waktu agregasi: {agg_s:.1f} detik")
print("equal:", scaled.sort_index().equals(expected.sort_index()))
summary["2. Optimasi: tipe + kolom"] = [mem_slim, agg_s, "agregasi saja",
                                      scaled.sum()]
del df, slim  # lepas memori sebelum langkah berikutnya
_ = gc.collect()"""),
    ("md", "## Langkah 4 - Optimasi: chunked processing\nBaca satu file per potongan 1 juta baris, agregasi per chunk, lalu gabungkan hasil."),
    ("code", """start = time.perf_counter()
partials, chunk_mb = [], 0
for chunk in pd.read_csv(FILE, chunksize=1_000_000,
                         usecols=workers.USECOLS):
    mb = chunk.memory_usage(deep=True).sum() / 1e6
    chunk_mb = max(chunk_mb, mb)
    partials.append(workers.revenue_by_city(chunk))
chunked = pd.concat(partials).groupby(level=0).sum()
chunk_s = time.perf_counter() - start

print(f"Jumlah chunk: {len(partials)}")
print(f"Memori satu chunk: {chunk_mb:,.0f} MB")
print(f"Waktu baca + agregasi: {chunk_s:.1f} detik")
print("equal:", chunked.sort_index().equals(expected.sort_index()))
summary["3. Optimasi: chunked"] = [chunk_mb, chunk_s, "baca + agregasi",
                                 chunked.sum()]"""),
    ("md", "## Langkah 5a - Partition tanpa paralel\nBaca file di `parts/` satu per satu, satu proses."),
    ("code", """files = sorted(glob.glob("parts/part_*.csv"))
start = time.perf_counter()
partials = [workers.revenue_by_city_from_file(f) for f in files]
serial = pd.concat(partials).groupby(level=0).sum()
serial_s = time.perf_counter() - start

print(f"Jumlah partition: {len(files)}")
print(f"Waktu: {serial_s:.1f} detik")
print("equal:", serial.sort_index().equals(expected.sort_index()))
one_part = pd.read_csv(files[0], usecols=workers.USECOLS)
part_mb = one_part.memory_usage(deep=True).sum() / 1e6
print(f"Memori satu partition: {part_mb:,.0f} MB")
summary["4. Partition"] = [part_mb, serial_s, "baca + agregasi",
                          serial.sum()]"""),
    ("md", "## Langkah 5b - Partition dan proses paralel (ide scale out)\nSatu worker per partition, lalu gabungkan hasil parsial. Di sistem big data, worker-nya berada di banyak mesin."),
    ("code", """start = time.perf_counter()
with Pool(processes=len(files)) as pool:
    partials = pool.map(workers.revenue_by_city_from_file, files)
parallel = pd.concat(partials).groupby(level=0).sum()
parallel_s = time.perf_counter() - start

print(f"Jumlah worker: {len(files)}")
print(f"Waktu: {parallel_s:.1f} detik")
print(f"Lebih cepat dari partition tanpa paralel: "
      f"{serial_s / parallel_s:.1f}x")
print("equal:", parallel.sort_index().equals(expected.sort_index()))
summary["5. Scale out: paralel"] = [part_mb * len(files), parallel_s,
                                  "baca + agregasi", parallel.sum()]"""),
    ("md", "## Langkah 6 - Bandingkan lima cara\nNilai hasil harus sama. Memori dan waktu berbeda di setiap laptop.\n\n`mem_data_mb` adalah memori dataframe, bukan memori proses di Task Manager. Proses Python sendiri butuh lebih banyak, dan di cara 5 setiap worker memuat Python dan pandas sendiri (biaya koordinasi)."),
    ("code", """CARA = ["1. Baseline", "2. Optimasi: tipe + kolom",
        "3. Optimasi: chunked", "4. Partition", "5. Scale out: paralel"]
skipped = [None, None, "dilewati", None]
rows = [[c] + summary.get(c, skipped) for c in CARA]
table = pd.DataFrame(rows, columns=["cara", "mem_data_mb", "detik",
                                   "waktu_untuk", "total_revenue"])
table["total_revenue"] = table["total_revenue"].astype("Int64")
table["sama"] = table["total_revenue"] == expected.sum()
print("Semua hasil sama:", table["sama"].dropna().all())
table.round({"mem_data_mb": 0, "detik": 1})"""),
    ("md", "Checklist keputusan:\n1. Apakah data muat di memori satu mesin?\n2. Apakah waktu proses masih masuk akal untuk kebutuhan bisnis?\n3. Apakah data datang terus-menerus dan harus segera diproses?\n\nPertanyaan penutup: kalau datanya 1 miliar baris dan satu laptop tidak cukup, apa yang kamu butuhkan dari sebuah sistem?"),
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
