"""Generate dataset sintetis Sesi 1 Big Data: retail_transactions.csv (1.000.000 baris, seed 42) dan stores.csv (40 toko, seed 7)."""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "Big_Data" / "Sesi_01_Intro_Classical_Data_Processing" / "3_Starter_Kit_Peserta"

N_ROWS = 1_000_000
SEED = 42
STORES_SEED = 7

CITIES = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar", "Yogyakarta", "Denpasar"]
CITY_WEIGHTS = [0.28, 0.16, 0.14, 0.10, 0.09, 0.08, 0.08, 0.07]
CATEGORIES = {  # kategori: (rentang harga satuan dalam Rupiah)
    "Electronics": (250_000, 5_000_000),
    "Fashion": (50_000, 750_000),
    "Groceries": (5_000, 150_000),
    "Home & Living": (40_000, 1_500_000),
    "Beauty": (20_000, 400_000),
    "Sports": (60_000, 2_000_000),
}
PAYMENTS = ["E-Wallet", "Credit Card", "Debit Card", "Bank Transfer", "Cash"]
STATUSES = ["COMPLETED", "CANCELLED", "REFUNDED"]
STORE_TYPES = ["Mall", "Ruko", "Supermarket"]


def make_transactions() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    cat_names = list(CATEGORIES)
    category = rng.choice(cat_names, size=N_ROWS, p=[0.12, 0.22, 0.30, 0.14, 0.12, 0.10])
    lo = np.array([CATEGORIES[c][0] for c in cat_names])
    hi = np.array([CATEGORIES[c][1] for c in cat_names])
    idx = pd.Categorical(category, categories=cat_names).codes
    unit_price = (rng.uniform(lo[idx], hi[idx]) // 1000 * 1000).astype(np.int64)

    city = rng.choice(CITIES, size=N_ROWS, p=CITY_WEIGHTS)
    store_no = rng.integers(1, 6, size=N_ROWS)
    store_id = [f"{c[:3].upper()}-{n:02d}" for c, n in zip(city, store_no)]

    start = np.datetime64("2025-01-01T00:00:00")
    seconds = rng.integers(0, 365 * 24 * 3600, size=N_ROWS)
    ts = np.sort(start + seconds.astype("timedelta64[s]"))

    return pd.DataFrame({
        "transaction_id": [f"TRX{i:07d}" for i in range(1, N_ROWS + 1)],
        "transaction_ts": pd.to_datetime(ts).strftime("%Y-%m-%d %H:%M:%S"),
        "store_id": store_id,
        "city": city,
        "category": category,
        "product_id": [f"P{n:05d}" for n in rng.integers(1, 5001, size=N_ROWS)],
        "quantity": rng.integers(1, 11, size=N_ROWS),
        "unit_price": unit_price,
        "payment_method": rng.choice(PAYMENTS, size=N_ROWS, p=[0.35, 0.20, 0.20, 0.15, 0.10]),
        "status": rng.choice(STATUSES, size=N_ROWS, p=[0.90, 0.07, 0.03]),
    })


def make_stores() -> pd.DataFrame:
    rng = np.random.default_rng(STORES_SEED)
    store_ids = sorted(f"{c[:3].upper()}-{n:02d}" for c in CITIES for n in range(1, 6))
    return pd.DataFrame({
        "store_id": store_ids,
        "store_type": rng.choice(STORE_TYPES, size=len(store_ids)),
        "opened_year": rng.integers(2005, 2025, size=len(store_ids)),
    })


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, df in [("retail_transactions.csv", make_transactions()), ("stores.csv", make_stores())]:
        out = OUT_DIR / name
        df.to_csv(out, index=False)
        print(f"{len(df):,} baris -> {out.name} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
