// Deck Big Data Sesi 1 - Intro Classical Data Processing (tabular dan non-tabular).
// Jalankan: node generate_deck_sesi01.js
const path = require("path");
const L = require("./insignia_deck_lib.js");

const OUT = path.join(__dirname, "output", "Big_Data", "Sesi_01_Intro_Classical_Data_Processing", "1_PPT", "Intro_Classical_Data_Processing.pptx");
const SRC = "Sumber: hasil hands-on dataset sintetis retail_transactions.csv (pandas 3.0.5, pyarrow 26.0.1).";

// Kode slide langkah 3, 7, 9, dan 11 sama persis dengan sel notebook (generate_notebook_sesi01.py).
const CODE_STEP3 = `df["transaction_ts"] = pd.to_datetime(df["transaction_ts"])
completed = df[df["status"] == "COMPLETED"].copy()
print("Baris tersisa:", len(completed))`;

const CODE_STEP7 = `conn = sqlite3.connect("retail.db")
start = time.perf_counter()
df.to_sql("transactions", conn, if_exists="replace", index=False)
print(f"Waktu load ke SQLite: {time.perf_counter() - start:.1f} detik")

query = """
SELECT city, SUM(quantity * unit_price) AS revenue
FROM transactions
WHERE status = 'COMPLETED'
GROUP BY city
ORDER BY revenue DESC
"""
start = time.perf_counter()
sql_result = pd.read_sql_query(query, conn)
print(f"Waktu query: {time.perf_counter() - start:.2f} detik")
print("same_as_pandas:", sql_result.equals(revenue_by_city))
sql_result`;

const CODE_STEP9 = `ref = pd.read_csv("retail_transactions.csv",
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
items.groupby("channel")["order_id"].nunique()`;

const CODE_STEP11 = `SLUG_TO_CATEGORY = {"beauty": "Beauty", "electronics": "Electronics",
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
images.groupby("category")[cols].mean().round(1).sort_values("brightness")`;

async function main() {
  const pptx = L.newDeck("Big Data - Sesi 1");

  // ---------- Pembuka ----------
  L.addCoverSlide(pptx, {
    eyebrow: "Internal Training",
    title: "Big Data",
    subtitle: "Sesi 1 - Intro Classical Data Processing",
    description: "Menjalankan alur pemrosesan data klasik dengan pandas untuk data tabular dan non-tabular di satu mesin, lalu melihat di mana batasnya.",
    meta: [
      { label: "Hari", value: "Rabu, 11 November 2026" },
      { label: "Slot siang", value: "13.30 - 15.30 WIB" },
      { label: "Slot sore", value: "15.30 - 17.30 WIB" },
      { label: "Platform", value: "Jupyter / VS Code lokal" },
    ],
    notes: "Jadwal 11 November masih menunggu persetujuan. Buka dengan pertanyaan: sebelum ada istilah big data, bagaimana laporan penjualan dibuat, dan bagaimana kalau datanya bukan tabel?",
  });

  L.addAgendaSlide(pptx, {
    title: "Rencana Sesi 2 Jam",
    items: [
      { time: "13.30 - 13.40", text: "Pembukaan: tujuan sesi, peta 10 sesi", tag: "Pembukaan", duration: "10 mnt" },
      { time: "13.40 - 13.55", text: "Alur pemrosesan data klasik, dataframe dan SQL", tag: "Konsep", duration: "15 mnt" },
      { time: "13.55 - 14.05", text: "Data tabular vs non-tabular", tag: "Konsep", duration: "10 mnt" },
      { time: "14.05 - 14.45", text: "Hands-on A: mini pipeline tabular (langkah 1-8)", tag: "Hands-on", duration: "40 mnt" },
      { time: "14.45 - 15.15", text: "Hands-on B: JSON, teks, gambar (langkah 9-11)", tag: "Hands-on", duration: "30 mnt" },
      { time: "15.15 - 15.25", text: "Batas pendekatan klasik dan jembatan ke Sesi 2", tag: "Konsep", duration: "10 mnt" },
      { time: "15.25 - 15.30", text: "Recap dan tanya jawab", tag: "Penutup", duration: "5 mnt" },
    ],
    note: "Slot sore (15.30 - 17.30) memakai susunan yang sama.",
    notes: "Total 120 menit. Hands-on 70 menit berturut-turut; beri satu titik berhenti singkat di akhir bagian A tanpa menambah waktu. Cadangan bila mepet: langkah 7 (SQL) lalu langkah 11 (gambar) dibawakan trainer sebagai demo.",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Tujuan Pembelajaran",
    title: "Setelah Sesi Ini, Kamu Mampu",
    cards: [
      { heading: "Menjelaskan", body: "alur pemrosesan data klasik: extract, clean, transform, aggregate, load." },
      { heading: "Menjalankan", body: "alur tersebut dengan pandas untuk data tabular (CSV) dan non-tabular (JSON, teks, gambar)." },
      { heading: "Membandingkan", body: "dataframe dan SQL di database relasional untuk operasi yang sama." },
      { heading: "Mengenali", body: "tanda pendekatan klasik mulai kewalahan: memori, waktu, satu mesin." },
    ],
    footerNote: "Target akhir sesi: revenue transaksi COMPLETED dari 1 juta baris, ditambah order aplikasi, ulasan, dan gambar produk yang diubah menjadi dataframe.",
    notes: "Tujuan kedua mencakup poin 1 dan 2 outline: data tabular dan non-tabular. Tujuan keempat adalah jembatan ke Sesi 2.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Peta Modul",
    title: "10 Sesi Big Data: Sesi 1 - 5",
    steps: [
      { label: "Sesi 1", description: "Intro Classical Data Processing" },
      { label: "Sesi 2", description: "Common vs Big Data" },
      { label: "Sesi 3", description: "Big Data Storage" },
      { label: "Sesi 4", description: "Batch Processing Framework (Spark)" },
      { label: "Sesi 5", description: "Real-Time Processing Framework (Kafka/Flink)" },
    ],
    highlightIndex: 0,
    note: "Sesi 1 menjadi titik awal: cara data biasa (common data) diproses di satu mesin.",
    notes: "Data biasa = data yang masih muat dan nyaman diproses di satu mesin. Pasangan istilah ini dipakai di Sesi 2 - Common vs Big Data.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Peta Modul",
    title: "10 Sesi Big Data: Sesi 6 - 10",
    steps: [
      { label: "Sesi 6", description: "Architecture Best Practice & Pipeline Design" },
      { label: "Sesi 7", description: "Use Case Implementation: Batch" },
      { label: "Sesi 8", description: "Use Case Implementation: Real-Time" },
      { label: "Sesi 9", description: "Cloud Approach for Big Data Solution" },
      { label: "Sesi 10", description: "Big Data Preparation for Robust AI/ML Use Case" },
    ],
    highlightIndex: -1,
    note: "Alur lima tahap tetap sama sampai Sesi 10. Yang berubah adalah tempat dan cara menjalankannya.",
    notes: "Tidak perlu membahas detail tiap sesi. Cukup sebut arah besarnya.",
  });

  // ---------- Bagian 1: alur klasik, dataframe dan SQL (15 menit) ----------
  L.addSectionSlide(pptx, {
    number: 1,
    title: "Alur Pemrosesan Data Klasik",
    subtitle: "Data dari file atau database transaksi, diproses script terjadwal, hasilnya menjadi laporan.",
    items: ["Batch processing, lima tahap", "Data mentah vs data bersih", "Dataframe dan SQL"],
    notes: "15 menit untuk seluruh bagian ini. Pemrosesan data klasik (classical data processing) di sini berarti batch processing di satu mesin.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Batch Processing",
    title: "Lima Tahap Pipeline Klasik",
    steps: [
      { label: "Extract", description: "Ambil data dari file atau database transaksi." },
      { label: "Clean", description: "Rapikan tipe data, buang baris yang tidak relevan." },
      { label: "Transform", description: "Bentuk kolom baru sesuai kebutuhan bisnis." },
      { label: "Aggregate", description: "Ringkas data per dimensi: kota, bulan, tipe toko." },
      { label: "Load", description: "Simpan hasil ke file atau tabel laporan." },
    ],
    note: "Pipeline ini biasanya dijalankan script terjadwal, misal setiap malam, lalu hasilnya dibaca tim bisnis.",
    notes: "Contoh pada data retail: extract = baca retail_transactions.csv (1.000.000 baris, 10 kolom); clean = transaction_ts ke datetime dan ambil COMPLETED; transform = revenue = quantity x unit_price dan kolom month; aggregate = revenue per kota, bulan, store_type; load = revenue_by_city.csv (8 baris).",
  });

  L.addBeforeAfterSlide(pptx, {
    eyebrow: "Clean dan Transform",
    title: "Data Mentah vs Data Siap Dianalisis",
    before: { label: "Data mentah", items: [
      "transaction_ts masih berupa teks",
      "Status campur: COMPLETED, CANCELLED, REFUNDED",
      "Belum ada kolom revenue",
      "Belum ada kolom month untuk agregasi bulanan",
      "1.000.000 baris transaksi",
    ] },
    after: { label: "Data bersih", items: [
      "transaction_ts bertipe datetime",
      "Hanya transaksi COMPLETED",
      "revenue = quantity x unit_price",
      "Kolom month berformat YYYY-MM",
      "900.347 baris siap diagregasi",
    ] },
    note: "Aturan bisnis: CANCELLED dan REFUNDED dibuang karena yang dihitung adalah revenue dari transaksi yang selesai.",
    notes: "Tekankan bahwa aturan filter harus disebut eksplisit, bukan asumsi diam-diam.",
  });

  L.addTwoPanelSlide(pptx, {
    eyebrow: "Revenue per Kota",
    title: "Satu Pertanyaan, Dua Cara Menulis",
    panels: [
      { label: "pandas", title: "Dataframe di memori", body: "Operasi per kolom (vectorized operation), dijalankan di proses Python.", listLabel: "Filter, hitung, kelompokkan", items: [
        'df.status == "COMPLETED"',
        "df.quantity * df.unit_price",
        '.groupby("city").sum()',
      ], code: true },
      { label: "SQL", title: "Query di database relasional", body: "Deklaratif: tulis hasil yang diinginkan, database yang mengeksekusi.", listLabel: "Filter, hitung, kelompokkan", items: [
        "WHERE status = 'COMPLETED'",
        "SUM(quantity * unit_price)",
        "GROUP BY city",
      ], code: true },
    ],
    note: "Di langkah 7, kedua hasil dibandingkan dan harus sama persis (same_as_pandas True).",
    notes: "Padanan lain: join = df.merge(stores, on='store_id') vs JOIN stores USING (store_id); urutkan = sort_values vs ORDER BY. Untuk data yang muat di satu mesin, keduanya pilihan tepat.",
  });

  // ---------- Bagian 2: tabular vs non-tabular (10 menit) ----------
  L.addSectionSlide(pptx, {
    number: 2,
    title: "Data Tabular vs Non-Tabular",
    subtitle: "Lima tahap tetap sama. Yang berbeda adalah tahap extract: cara mengubah data menjadi baris dan kolom.",
    items: ["Terstruktur, semi-terstruktur, tidak terstruktur", "JSON bertingkat", "Teks bebas", "Gambar"],
    notes: "10 menit. Jangan memakai label 'variety' atau 5V di sini; itu dibahas di Sesi 2, yang merujuk balik ke contoh hari ini.",
  });

  L.addComparisonTableSlide(pptx, {
    eyebrow: "Struktur Data",
    title: "Tiga Bentuk Data Retail",
    headers: ["Struktur", "Contoh retail", "Bentuk file", "Extract di pandas"],
    rows: [
      ["Terstruktur", "Transaksi penjualan", "retail_transactions.csv", "pd.read_csv"],
      ["Semi-terstruktur", "Order dari aplikasi", "orders_app.json", "json + pd.json_normalize"],
      ["Tidak terstruktur", "Ulasan pelanggan", "reviews.csv (isi kolom = kalimat bebas)", "operasi string, kamus kata"],
      ["Tidak terstruktur", "Gambar produk", "product_images/*.png", "Pillow + numpy per file"],
    ],
    note: "reviews.csv memang berformat CSV, tetapi isi kolom review_text adalah kalimat bebas: strukturnya ada di kalimat, bukan di kolom. Semua data terhubung lewat transaction_id.",
    notes: "Ulasan disimpan di CSV, tetapi isinya teks bebas: strukturnya ada di kalimat, bukan di kolom.",
  });

  L.addLabelRowsSlide(pptx, {
    eyebrow: "Dari Bentuk Asli ke Dataframe",
    title: "Apa yang Masuk ke Baris dan Kolom",
    rows: [
      { term: "JSON bertingkat", body: "Satu order berisi daftar items. json_normalize membuat satu baris per item, field customer dan payment ikut jadi kolom." },
      { term: "Teks bebas", body: "Kalimat ulasan dihitung kata positif dan negatifnya dari kamus kecil, hasilnya kolom score dan sentiment." },
      { term: "Gambar", body: "Yang masuk dataframe adalah fitur gambar: lebar, tinggi, mode, ukuran file, rata-rata piksel. Bukan gambarnya." },
      { term: "Setelah jadi dataframe", body: "Operasinya sama dengan data tabular: join lewat transaction_id, group by kota atau kategori.", highlight: true },
    ],
    note: "Pekerjaan terbesar data non-tabular ada di tahap extract.",
    notes: "Ini pesan utama bagian B hands-on.",
  });

  // ---------- Bagian 3: hands-on A (40 menit) ----------
  L.addSectionSlide(pptx, {
    number: 3,
    title: "Hands-on A: Mini Pipeline Tabular",
    subtitle: "Satu notebook, dari CSV sampai hasil agregasi.",
    items: ["Verifikasi environment", "Langkah 1 - 4: extract sampai transform", "Langkah 5 - 8: aggregate sampai load", "Titik berhenti: cek checkpoint"],
    notes: "40 menit, sekitar 5 menit per langkah. Notebook: Notebook_Mini_Pipeline_Retail.ipynb di Starter Kit. Semua sel sudah terisi, jalankan berurutan.",
  });

  L.addChecklistSlide(pptx, {
    eyebrow: "Sebelum Mulai",
    title: "Verifikasi Environment",
    items: [
      "Python 3.12 ke atas terpasang",
      "pip install -r requirements.txt sudah dijalankan",
      "Sel Langkah 0 mencetak pandas 3.0.5, pyarrow 26.0.1, Pillow 12.3.0",
      "retail_transactions.csv dan stores.csv ada di folder notebook",
      "orders_app.json, reviews.csv, product_images/ (180 file) ada",
      "Ruang disk kosong minimal 500 MB",
    ],
    footerNote: "Catatan: tanpa pyarrow atau dengan pandas 2.2, angka memori berbeda (sekitar 483 MB, bukan 155 MB).",
    notes: "Langkah 0 berhenti dengan FileNotFoundError bila ada file yang hilang. Galat No module named 'PIL' berarti Pillow belum terpasang.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Langkah 1 - 4",
    title: "Extract sampai Transform",
    steps: [
      { heading: "1. Extract", body: "Baca CSV dengan pd.read_csv, cek shape dan memori." },
      { heading: "2. Inspect", body: "Cek tipe data, nilai kosong, duplikat, sebaran status." },
      { heading: "3. Clean", body: "Ubah transaction_ts ke datetime, ambil transaksi COMPLETED." },
      { heading: "4. Transform", body: "Tambah kolom revenue dan kolom month." },
    ],
    checkpoint: { title: "Expected output", items: [
      "Shape (1000000, 10), memori sekitar 155 MB",
      "Nulls 0, duplikat transaction_id 0",
      "COMPLETED 900347, CANCELLED 69741, REFUNDED 29912",
      "Total revenue 3,273,759,911,000 (3,27 triliun)",
    ] },
    note: "Tertinggal? Jalankan ulang semua sel dari atas dengan Run All.",
    notes: "Waktu baca CSV bervariasi antar laptop, umumnya beberapa detik. Jangan jadikan patokan.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 3",
    title: "Clean: Tipe Data dan Filter Status",
    language: "Python (pandas)",
    code: CODE_STEP3,
    caption: "Expected output: Baris tersisa: 900347. df sudah dibaca di langkah 1.",
    notes: ".copy() mencegah peringatan saat menambah kolom di langkah 4. df berasal dari langkah 1, jadi sel ini harus dijalankan setelah langkah 1 dan 2.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Langkah 5 - 8",
    title: "Aggregate sampai Load",
    steps: [
      { heading: "5. Aggregate", body: "Revenue per kota dan per bulan." },
      { heading: "6. Join", body: "Gabungkan dengan stores.csv, revenue per store_type." },
      { heading: "7. SQL", body: "Muat ke SQLite, query revenue per kota, bandingkan." },
      { heading: "8. Load", body: "Simpan revenue_by_city.csv, hitung memori, estimasi 100x." },
    ],
    checkpoint: { title: "Expected output", items: [
      "8 kota, Jakarta teratas; 12 bulan, tertinggi 2025-12",
      "40 toko, 0 tanpa pasangan; Supermarket teratas",
      "same_as_pandas True",
      "8 baris; memori sekitar 136 MB; estimasi 100x sekitar 14 GB",
    ] },
    note: "Titik berhenti bagian A: cocokkan checkpoint, lalu tanya jawab singkat sebelum bagian B.",
    notes: "Angka lengkap (seperti output): Jakarta 918117634000; 2025-12 280,072,930,000; Supermarket 1394541727000, Ruko 1082502474000, Mall 796715710000. Load ke SQLite butuh beberapa detik, notebook tidak macet. Bila waktu mepet, langkah 7 dibawakan trainer sebagai demo.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 7",
    title: "SQL: Query yang Sama di SQLite",
    language: "Python (sqlite3)",
    code: CODE_STEP7,
    caption: "Expected output: same_as_pandas: True. 8 kota, Jakarta teratas 918117634000, sama dengan revenue_by_city langkah 5.",
    notes: "sqlite3 bawaan Python, tidak perlu instalasi server. retail.db yang terbentuk sekitar 98 MB.",
  });

  // ---------- Bagian 4: hands-on B (30 menit) ----------
  L.addSectionSlide(pptx, {
    number: 4,
    title: "Hands-on B: JSON, Teks, Gambar",
    subtitle: "Tiga data non-tabular diubah menjadi dataframe, lalu diolah dengan lima tahap yang sama.",
    items: ["Langkah 9: JSON bertingkat", "Langkah 10: teks bebas", "Langkah 11: gambar", "Cukup Langkah 0, tidak butuh bagian A"],
    notes: "30 menit, sekitar 10 menit per langkah. Eksekusinya cepat (beberapa detik); waktu dipakai untuk penjelasan.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Langkah 9 - 11",
    title: "Dari Non-Tabular ke Dataframe",
    steps: [
      { heading: "9. JSON bertingkat", body: "json_normalize items di orders_app.json, cocokkan revenue dengan CSV." },
      { heading: "10. Teks bebas", body: "Sentimen dari kamus kata (bukan NLP), join ke kota." },
      { heading: "11. Gambar", body: "Metadata dan rata-rata piksel dengan Pillow, agregasi per kategori." },
    ],
    checkpoint: { title: "Expected output", items: [
      "4704 item cocok, total 17,362,020,000 (17,4 miliar)",
      "positif 1653, negatif 684, netral 663",
      "180 gambar, semua RGB",
      "Electronics tergelap, Beauty paling terang",
    ] },
    note: "Total revenue JSON lebih kecil dari CSV karena JSON hanya memuat 4.704 transaksi. Bagian B tetap jalan setelah Restart Kernel.",
    notes: "Channel: android 620, ios 694, web 686. Proporsi negatif tertinggi Medan 0.28 (28%). Gambar: 88 berukuran 64x64, 92 berukuran 128x128. Brightness: Electronics 92.5, Beauty 195.9. Ukuran file 8.2-32.4 KB, total 3699 KB. Bila waktu mepet, langkah 11 dibawakan trainer sebagai demo.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 9",
    title: "JSON Bertingkat dengan json_normalize",
    language: "Python (pandas)",
    code: CODE_STEP9,
    caption: "Expected output: Shape items: (4704, 10), Item cocok dengan CSV: 4704, Revenue sama: True.",
    notes: "Baris ref membaca ulang kolom acuan dari CSV supaya bagian B tidak bergantung pada variabel bagian A. Satu order berisi item dari toko, metode bayar, dan tanggal yang sama. record_path='items' membuat satu baris per item. meta membawa field order ke setiap baris item; customer.tier dan customer.city menjadi nama kolom dengan titik.",
  });

  L.addBeforeAfterSlide(pptx, {
    eyebrow: "Langkah 10: Kamus Sentimen",
    title: "Yang Terbaca Benar vs Jebakan Negasi",
    before: { label: "Jebakan negasi", items: [
      "\"Lumayan, tidak buruk untuk harga segini.\" terbaca negatif (78 ulasan)",
      "\"Tidak bagus, warnanya pudar.\" terbaca netral (67 ulasan)",
      "Kamus menghitung kata, bukan makna kalimat",
    ] },
    after: { label: "Terbaca benar", items: [
      "\"Pengiriman cepat, puas sekali.\" positif",
      "\"Barang rusak saat diterima, kecewa.\" negatif",
      "\"Pesanan sampai hari ini.\" netral",
    ] },
    note: "Jebakan ini disengaja untuk memperlihatkan batas aturan sederhana, bukan bug.",
    notes: "Sampaikan sebelum menjalankan langkah 10. Metode yang lebih baik (model NLP) di luar sesi ini dan relevan dengan Sesi 10.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 11",
    title: "Gambar Menjadi Dataframe dengan Pillow",
    language: "Python (Pillow, numpy)",
    code: CODE_STEP11,
    caption: "Expected output: Jumlah gambar: 180. Electronics brightness terendah, Beauty tertinggi.",
    notes: "Slug nama file (home_living) dipetakan ke nama kategori di CSV (Home & Living) supaya sama dengan bagian A. with Image.open menutup file setelah dibaca.",
  });

  // ---------- Bagian 5: batas (10 menit) ----------
  L.addSectionSlide(pptx, {
    number: 5,
    title: "Batas Pendekatan Klasik",
    subtitle: "Kewalahan dilihat dari angka, bukan dari perasaan datanya besar.",
    items: ["Angka dari hands-on", "Estimasi kalau data 100x", "Tanda kewalahan", "Jembatan ke Sesi 2"],
    notes: "10 menit. Mulai dengan pertanyaan: kalau gambarnya 1 juta file dan ulasannya 100 juta baris, tahap mana yang paling lambat?",
  });

  L.addStatSlide(pptx, {
    eyebrow: "Angka dari Hands-on",
    title: "Seberapa Besar Data di Memori",
    stats: [
      { value: "1 juta", label: "baris transaksi", body: "retail_transactions.csv, sekitar 93 MB di disk" },
      { value: "155 MB", label: "memori awal", body: "Langkah 1, transaction_ts masih teks" },
      { value: "136 MB", label: "memori akhir", body: "Langkah 8, transaction_ts sudah datetime" },
      { value: "14 GB", label: "estimasi data 100x", body: "100 juta baris, belum termasuk salinan saat diproses", highlight: true },
    ],
    conclusion: "Kesimpulan: 1 juta baris aman di laptop, 100 juta baris mendekati atau melebihi RAM laptop pada umumnya.",
    source: SRC,
    notes: "Semua angka memori bersifat sekitar dan bergantung pyarrow: tanpa pyarrow atau dengan pandas 2.2, angkanya sekitar 483 MB, 423 MB, dan 42 GB. Estimasi 100x = 136 MB x 100.",
  });

  L.addNumberedListSlide(pptx, {
    eyebrow: "Tanda Kewalahan",
    title: "Empat Tanda Pendekatan Klasik Mulai Mentok",
    items: [
      { heading: "Memori", body: "Seluruh data harus dimuat ke RAM satu komputer." },
      { heading: "Waktu", body: "Waktu baca, load, dan proses naik seiring ukuran data." },
      { heading: "Satu mesin", body: "Satu proses utama. Menambah data tidak menambah tenaga." },
      { heading: "Banyak file", body: "Gambar dibaca satu per satu. 1 juta file berarti 1 juta kali buka file." },
    ],
    quote: "Pendekatan klasik tidak salah. Ia hanya punya batas satu mesin.",
    notes: "Arahkan jawaban ke memori, waktu, dan banyaknya file, bukan ke nama tools tertentu. Sesi 2 - Common vs Big Data membahas apa yang berubah setelah batas ini tercapai.",
  });

  // ---------- Penutup ----------
  L.addClosingSlide(pptx, {
    title: "Ringkasan Sesi 1",
    points: [
      "Pemrosesan data klasik mengikuti lima tahap: extract, clean, transform, aggregate, load",
      "pandas dan SQL memberi hasil yang sama untuk operasi yang sama",
      "Data non-tabular diubah dulu menjadi baris dan kolom, lalu diolah dengan cara yang sama",
      "Batas satu mesin terlihat dari angka memori, waktu, dan jumlah file",
    ],
    nextStep: "Sesi 2 - Common vs Big Data",
    notes: "Recap 5 menit.",
  });

  L.addThankYouSlide(pptx, {
    lines: ["Sesi berikutnya: Sesi 2 - Common vs Big Data"],
    contact: "Kontak: Fahmi, Mentor Data & AI",
    notes: "Tanya jawab.",
  });

  const out = await L.save(pptx, process.env.DECK_OUT || OUT);
  console.log("written", out);
}

if (require.main === module) main();
module.exports = { CODE_STEP9, CODE_STEP11 };
