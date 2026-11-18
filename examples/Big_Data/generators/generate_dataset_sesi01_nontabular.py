"""Generate data non-tabular Sesi 1 Big Data (sintetis, turunan retail_transactions.csv).

Hasil di folder tujuan (default: Starter Kit Sesi 1):
- orders_app.json      : 2.000 event order aplikasi (JSON bertingkat). Setiap order membungkus
                         1-4 transaksi COMPLETED (toko, metode bayar, tanggal sama) sebagai items[].
- reviews.csv          : 3.000 ulasan pelanggan berbahasa Indonesia (teks bebas) per transaction_id.
- product_images/      : 180 gambar produk sintetis (PNG), 30 per kategori, nama file <kategori>_NNN.png.

Jalankan: python generate_dataset_sesi01_nontabular.py [folder_tujuan]
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    ROOT / "output" / "Big_Data" / "Sesi_01_Intro_Classical_Data_Processing" / "3_Starter_Kit_Peserta")
SOURCE = OUT / "retail_transactions.csv"
SEED = 11
N_ORDERS = 2_000
N_REVIEWS = 3_000
IMAGES_PER_CATEGORY = 30

POSITIVE = ["Barangnya bagus dan sesuai deskripsi.", "Pengiriman cepat, puas sekali.", "Kualitas mantap, recommended.",
            "Harga murah dan kualitas bagus.", "Pelayanan ramah, puas belanja di sini."]
NEGATIVE = ["Barang rusak saat diterima, kecewa.", "Pengiriman lambat dan kemasan jelek.", "Kualitas buruk, tidak sesuai foto.",
            "Kecewa, ukuran salah dan pelayanan lambat.", "Barang palsu, sangat kecewa."]
NEUTRAL = ["Barang sudah diterima.", "Pesanan sampai hari ini.", "Sesuai pesanan.", "Belum dicoba, nanti diulas lagi."]
TRICKY = ["Tidak bagus, warnanya pudar.", "Lumayan, tidak buruk untuk harga segini."]  # negasi: jebakan untuk kamus sederhana

CATEGORY_COLORS = {  # warna dasar RGB per kategori
    "Beauty": (230, 140, 180), "Electronics": (40, 50, 70), "Fashion": (200, 60, 60),
    "Groceries": (90, 170, 80), "Home & Living": (200, 170, 120), "Sports": (60, 120, 210),
}


def make_orders(completed: pd.DataFrame, rng: np.random.Generator) -> list[dict]:
    """Satu order = 1-4 transaksi COMPLETED berurutan dari toko, metode bayar, dan tanggal yang sama,
    supaya customer.city, payment.method, dan created_at konsisten dengan semua item-nya."""
    sizes = rng.integers(1, 5, size=N_ORDERS)
    rows = completed.to_dict("records")
    queues: dict[tuple, list[int]] = {}
    for idx, r in enumerate(rows):
        queues.setdefault((r["store_id"], r["payment_method"], r["transaction_ts"][:10]), []).append(idx)
    used: set[int] = set()
    orders, cursor = [], 0
    for i, size in enumerate(sizes):
        while cursor in used:
            cursor += 1
        c = rows[cursor]
        queue = queues[(c["store_id"], c["payment_method"], c["transaction_ts"][:10])]
        chunk_idx = [k for k in queue if k not in used][:size]
        used.update(chunk_idx)
        chunk = [rows[k] for k in chunk_idx]
        first = chunk[0]
        orders.append({
            "order_id": f"APP{i + 1:06d}",
            "created_at": chunk[-1]["transaction_ts"],
            "channel": str(rng.choice(["android", "ios", "web"])),
            "customer": {"customer_id": f"C{int(rng.integers(1, 50_000)):05d}",
                         "tier": str(rng.choice(["regular", "silver", "gold"], p=[0.6, 0.3, 0.1])),
                         "city": first["city"]},
            "payment": {"method": first["payment_method"], "installment_months": int(rng.choice([0, 0, 0, 3, 6]))},
            "items": [{"transaction_id": r["transaction_id"], "product_id": r["product_id"],
                       "category": r["category"], "quantity": int(r["quantity"]), "unit_price": int(r["unit_price"])}
                      for r in chunk],
        })
    return orders


def make_reviews(completed: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    ids = completed["transaction_id"].sample(N_REVIEWS, random_state=SEED).to_numpy()
    pools = [POSITIVE, NEGATIVE, NEUTRAL, TRICKY]
    kind = rng.choice(len(pools), size=N_REVIEWS, p=[0.55, 0.2, 0.2, 0.05])
    texts = [str(rng.choice(pools[k])) for k in kind]
    return pd.DataFrame({"transaction_id": ids, "review_text": texts})


def make_images(folder: Path, rng: np.random.Generator) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.png"):
        old.unlink()
    for category, base in CATEGORY_COLORS.items():
        slug = category.lower().replace(" & ", "_")
        for k in range(1, IMAGES_PER_CATEGORY + 1):
            size = int(rng.choice([64, 128]))
            noise = rng.integers(-25, 26, size=(size, size, 3))
            pixels = np.clip(np.array(base) + noise, 0, 255).astype("uint8")
            img = Image.fromarray(pixels, "RGB")
            draw = ImageDraw.Draw(img)
            m = size // 4
            draw.ellipse([m, m, size - m, size - m], fill=(245, 245, 245))  # "produk" di tengah
            img.save(folder / f"{slug}_{k:03d}.png")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"{SOURCE} tidak ditemukan.")
    rng = np.random.default_rng(SEED)
    tx = pd.read_csv(SOURCE)
    completed = tx[tx["status"] == "COMPLETED"].reset_index(drop=True)

    orders = make_orders(completed, rng)
    (OUT / "orders_app.json").write_text(json.dumps(orders, ensure_ascii=False, indent=1), encoding="utf-8")
    make_reviews(completed, rng).to_csv(OUT / "reviews.csv", index=False)
    make_images(OUT / "product_images", rng)
    print(f"orders_app.json: {len(orders)} order, {sum(len(o['items']) for o in orders)} item")
    print(f"reviews.csv: {N_REVIEWS} ulasan")
    print(f"product_images/: {len(list((OUT / 'product_images').glob('*.png')))} gambar")


if __name__ == "__main__":
    main()
