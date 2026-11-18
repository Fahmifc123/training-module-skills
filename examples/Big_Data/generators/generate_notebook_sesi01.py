"""Generate notebook hands-on Sesi 1 Big Data (lengkap, tanpa bagian kosong)."""
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "output" / "Big_Data" / "Sesi_01_Intro_Classical_Data_Processing" / "3_Starter_Kit_Peserta" / "Notebook_Mini_Pipeline_Retail.ipynb")

CELLS = [
    ("md", "# Sesi 1 - Intro Classical Data Processing\nMini pipeline penjualan retail: extract, clean, transform, aggregate, load.\n\n"
           "- **Bagian A (langkah 1-8):** data tabular, `retail_transactions.csv` dan `stores.csv`.\n"
           "- **Bagian B (langkah 9-11):** data non-tabular, `orders_app.json`, `reviews.csv`, dan `product_images/`.\n\n"
           "Langkah 0 wajib dijalankan dulu. Bagian B bisa dijalankan tanpa bagian A."),
    ("md", "## Langkah 0 - Verifikasi environment\nCek versi library dan file dataset sebelum mulai."),
    ("code", """import json, sys, time, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow
import PIL
from PIL import Image

print("Python  :", sys.version.split()[0])
print("pandas  :", pd.__version__)
print("pyarrow :", pyarrow.__version__)
print("Pillow  :", PIL.__version__)
missing = []
for f in ["retail_transactions.csv", "stores.csv", "orders_app.json",
          "reviews.csv", "product_images"]:
    print(f, "ada" if Path(f).exists() else "TIDAK ADA")
    if not Path(f).exists():
        missing.append(f)
if missing:
    raise FileNotFoundError(
        f"{', '.join(missing)} tidak ditemukan. Buka notebook dari folder "
        "Starter Kit yang berisi semua file data. Lihat README_Setup.md.")"""),
    ("md", "# Bagian A - Data tabular (langkah 1-8)"),
    ("md", "## Langkah 1 - Extract\nBaca CSV, cek shape dan pemakaian memori."),
    ("code", """start = time.perf_counter()
df = pd.read_csv("retail_transactions.csv")
print(f"Waktu baca: {time.perf_counter() - start:.1f} detik")
print("Shape:", df.shape)
print(f"Memori: {df.memory_usage(deep=True).sum() / 1e6:.0f} MB")
df.head()"""),
    ("md", "## Langkah 2 - Inspect\nTipe data, nilai kosong, duplikat, sebaran status."),
    ("code", """print(df.dtypes)
print("Nilai kosong:", df.isna().sum().sum())
dup = df["transaction_id"].duplicated().sum()
print("Duplikat transaction_id:", dup)
df["status"].value_counts()"""),
    ("md", "## Langkah 3 - Clean\nUbah `transaction_ts` ke datetime, ambil hanya transaksi COMPLETED."),
    ("code", """df["transaction_ts"] = pd.to_datetime(df["transaction_ts"])
completed = df[df["status"] == "COMPLETED"].copy()
print("Baris tersisa:", len(completed))"""),
    ("md", "## Langkah 4 - Transform\nrevenue = quantity x unit_price, dan kolom month."),
    ("code", """completed["revenue"] = completed["quantity"] * completed["unit_price"]
completed["month"] = completed["transaction_ts"].dt.strftime("%Y-%m")
print(f"Total revenue: {completed['revenue'].sum():,}")"""),
    ("md", "## Langkah 5 - Aggregate\nRevenue per kota dan per bulan."),
    ("code", """revenue_by_city = (
    completed.groupby("city", as_index=False)["revenue"].sum()
    .sort_values("revenue", ascending=False, ignore_index=True)
)
print("Jumlah kota:", len(revenue_by_city))
revenue_by_city"""),
    ("code", """revenue_by_month = (
    completed.groupby("month", as_index=False)["revenue"].sum()
)
top_month = revenue_by_month.loc[revenue_by_month["revenue"].idxmax()]
print("Jumlah bulan:", len(revenue_by_month))
print("Bulan tertinggi:", top_month["month"])
print(f"Revenue bulan tertinggi: {top_month['revenue']:,}")
revenue_by_month"""),
    ("md", "## Langkah 6 - Join\nGabungkan dengan `stores.csv`, revenue per store_type."),
    ("code", """stores = pd.read_csv("stores.csv")
print("Jumlah toko:", len(stores))
joined = completed.merge(stores, on="store_id", how="left",
                         indicator=True)
print("Baris tanpa pasangan:", (joined["_merge"] != "both").sum())
revenue_by_type = (
    joined.groupby("store_type", as_index=False)["revenue"].sum()
    .sort_values("revenue", ascending=False, ignore_index=True)
)
revenue_by_type"""),
    ("md", "## Langkah 7 - SQL\nMuat ke SQLite, query revenue per kota, bandingkan dengan hasil pandas."),
    ("code", """conn = sqlite3.connect("retail.db")
start = time.perf_counter()
df.to_sql("transactions", conn, if_exists="replace", index=False)
print(f"Waktu load ke SQLite: {time.perf_counter() - start:.1f} detik")

query = \"\"\"
SELECT city, SUM(quantity * unit_price) AS revenue
FROM transactions
WHERE status = 'COMPLETED'
GROUP BY city
ORDER BY revenue DESC
\"\"\"
start = time.perf_counter()
sql_result = pd.read_sql_query(query, conn)
print(f"Waktu query: {time.perf_counter() - start:.2f} detik")
print("same_as_pandas:", sql_result.equals(revenue_by_city))
sql_result"""),
    ("md", "## Langkah 8 - Load dan batas satu mesin\nSimpan hasil, hitung memori, estimasi kalau data 100x lebih besar."),
    ("code", """revenue_by_city.to_csv("revenue_by_city.csv", index=False)
saved = pd.read_csv("revenue_by_city.csv")
print("Baris di revenue_by_city.csv:", len(saved))

mem_mb = df.memory_usage(deep=True).sum() / 1e6
mem_per_million = mem_mb / (len(df) / 1_000_000)
print(f"Memori setelah tipe dirapikan: {mem_mb:.0f} MB")
print(f"Memori per 1 juta baris: {mem_per_million:.0f} MB")
estimate_gb = mem_per_million * 100 / 1000
print(f"Estimasi 100x (100 juta baris): {estimate_gb:.1f} GB")
conn.close()"""),
    ("md", "**Titik berhenti bagian A.** Cocokkan checkpoint langkah 1-8. Pertanyaan: kalau datanya 100 kali lebih besar, apa yang terjadi di laptopmu?"),
    ("md", "# Bagian B - Data non-tabular (langkah 9-11)\nBagian ini hanya butuh Langkah 0. Kolom acuan dibaca ulang dari CSV di langkah 9, jadi tetap jalan setelah Restart Kernel."),
    ("md", "## Langkah 9 - JSON bertingkat\nRatakan `items` di `orders_app.json` menjadi dataframe, cocokkan dengan transaksi COMPLETED di CSV."),
    ("code", """ref = pd.read_csv("retail_transactions.csv",
                  usecols=["transaction_id", "city", "quantity",
                           "unit_price", "status"])
ref = ref[ref["status"] == "COMPLETED"].copy()
ref["revenue"] = ref["quantity"] * ref["unit_price"]

orders = json.loads(Path("orders_app.json").read_text(encoding="utf-8"))
print("Jumlah order:", len(orders))
items = pd.json_normalize(
    orders, record_path="items",
    meta=["order_id", "channel", ["customer", "tier"],
          ["customer", "city"], ["payment", "method"]])
print("Shape items:", items.shape)
items["revenue"] = items["quantity"] * items["unit_price"]

check = items.merge(ref[["transaction_id", "revenue"]],
                    on="transaction_id", suffixes=("", "_csv"))
print("Item cocok dengan CSV:", len(check))
print("Revenue sama:", (check["revenue"] == check["revenue_csv"]).all())
print(f"Total revenue: {items['revenue'].sum():,}")
items.groupby("channel")["order_id"].nunique()"""),
    ("md", "## Langkah 10 - Teks bebas\nSentimen dari kamus kata sederhana (bukan NLP), lalu join ke kota."),
    ("code", r"""reviews = pd.read_csv("reviews.csv")
POSITIF = ["bagus", "cepat", "puas", "mantap", "recommended", "murah",
           "ramah"]
NEGATIF = ["rusak", "kecewa", "lambat", "jelek", "buruk", "salah", "palsu",
           "pudar"]
text = reviews["review_text"].str.lower()
pos = sum(text.str.count(rf"\b{w}\b") for w in POSITIF)
neg = sum(text.str.count(rf"\b{w}\b") for w in NEGATIF)
reviews["score"] = pos - neg
reviews["sentiment"] = np.select(
    [reviews["score"] > 0, reviews["score"] < 0],
    ["positif", "negatif"], "netral")
print(reviews["sentiment"].value_counts())

by_city = reviews.merge(ref[["transaction_id", "city"]],
                        on="transaction_id")
is_negative = by_city["sentiment"] == "negatif"
negative_share = is_negative.groupby(by_city["city"]).mean()
print("Proporsi negatif tertinggi:", negative_share.idxmax(),
      round(negative_share.max(), 2))
tidak = reviews[reviews["review_text"].str.contains("tidak", case=False)]
tidak.groupby(["review_text", "sentiment"]).size()"""),
    ("md", "## Langkah 11 - Gambar\nMetadata dan rata-rata piksel tiap gambar produk menjadi dataframe, lalu agregasi per kategori."),
    ("code", """SLUG_TO_CATEGORY = {"beauty": "Beauty", "electronics": "Electronics",
                    "fashion": "Fashion", "groceries": "Groceries",
                    "home_living": "Home & Living", "sports": "Sports"}
rows = []
for f in sorted(Path("product_images").glob("*.png")):
    with Image.open(f) as img:
        px = np.asarray(img.convert("RGB"))
        slug = f.stem.rsplit("_", 1)[0]
        rows.append({"category": SLUG_TO_CATEGORY[slug], "mode": img.mode,
                     "width": img.width, "height": img.height,
                     "kb": f.stat().st_size / 1000, "brightness": px.mean(),
                     "mean_r": px[..., 0].mean(), "mean_g": px[..., 1].mean(),
                     "mean_b": px[..., 2].mean()})
images = pd.DataFrame(rows)
print("Jumlah gambar:", len(images))
print(images.groupby(["width", "height", "mode"]).size())
print(f"Ukuran file: {images['kb'].min():.1f}-{images['kb'].max():.1f} KB,",
      f"total {images['kb'].sum():.0f} KB")
cols = ["mean_r", "mean_g", "mean_b", "brightness"]
images.groupby("category")[cols].mean().round(1).sort_values("brightness")"""),
    ("md", "Pertanyaan penutup: kalau gambarnya 1 juta file dan ulasannya 100 juta baris, tahap mana yang paling lambat?"),
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
