// Deck Big Data Sesi 3 - Big Data Storage.
// Jalankan: node generate_deck_sesi03.js
const path = require("path");
const L = require("./insignia_deck_lib.js");

const OUT = path.join(__dirname, "output", "Big_Data", "Sesi_03_Big_Data_Storage", "1_PPT", "Big_Data_Storage.pptx");
const SRC = "Sumber: hasil hands-on dataset sintetis retail_transactions_10m.csv (pandas 3.0.5, pyarrow 26.0.1). Angka bervariasi antar mesin.";

// Kode slide langkah 1 dan 3a sama persis dengan sel notebook (generate_notebook_sesi03.py).
const CODE_STEP1 = "csv_write_s = pq_write_s = 0.0\nn_rows, writer = 0, None\nchunks = pd.read_csv(FILE_10M, chunksize=1_000_000,\n                     parse_dates=[\"transaction_ts\"])\nfor i, chunk in enumerate(chunks):\n    t = time.perf_counter()\n    chunk.to_csv(CSV_FILE, mode=\"w\" if i == 0 else \"a\", header=(i == 0),\n                 index=False, lineterminator=\"\\n\")\n    csv_write_s += time.perf_counter() - t\n\n    t = time.perf_counter()\n    table = pa.Table.from_pandas(chunk, preserve_index=False)\n    if writer is None:\n        writer = pq.ParquetWriter(PQ_FILE, table.schema)\n    writer.write_table(table)\n    pq_write_s += time.perf_counter() - t\n    n_rows += len(chunk)\nwriter.close()\n\ncsv_mb, pq_mb = size_mb(CSV_FILE), size_mb(PQ_FILE)\nprint(f\"Jumlah baris: {n_rows:,}\")\nprint(f\"CSV     : {csv_mb:,.0f} MB, tulis {csv_write_s:.1f} detik\")\nprint(f\"Parquet : {pq_mb:,.0f} MB, tulis {pq_write_s:.1f} detik\")\nprint(f\"Parquet {csv_mb / pq_mb:.1f}x lebih kecil\")";

const CODE_STEP3 = "shutil.rmtree(DIR_MONTH, ignore_errors=True)\n\nt = time.perf_counter()\nbatches = pq.ParquetFile(PQ_FILE).iter_batches(batch_size=1_000_000)\nfor i, batch in enumerate(batches):\n    part = batch.to_pandas()\n    part[\"month\"] = part[\"transaction_ts\"].dt.to_period(\"M\").astype(str)\n    part.to_parquet(DIR_MONTH, partition_cols=[\"month\"], index=False,\n                    basename_template=f\"batch{i:02d}-{{i}}.parquet\")\nprint(f\"Tulis terpartisi: {time.perf_counter() - t:.1f} detik\")\n\nfolders = sorted(p.name for p in DIR_MONTH.iterdir())\nprint(\"Jumlah folder:\", len(folders))\nprint(folders[0], \"...\", folders[-1])\nprint(f\"Ukuran total: {size_mb(DIR_MONTH):,.0f} MB\")";

async function main() {
  const pptx = L.newDeck("Big Data - Sesi 3");

  // ---------- Pembuka ----------
  L.addCoverSlide(pptx, {
    eyebrow: "Internal Training",
    title: "Big Data",
    subtitle: "Sesi 3 - Big Data Storage",
    description: "Membandingkan CSV dan Parquet, mencoba partitioning pada 10 juta baris, lalu memetakan data lake, data warehouse, dan lakehouse.",
    meta: [
      { label: "Hari", value: "Rabu, 25 Nov 2026" },
      { label: "Slot siang", value: "13.30 - 15.30 WIB" },
      { label: "Slot sore", value: "15.30 - 17.30 WIB" },
      { label: "Platform", value: "Jupyter / VS Code lokal" },
    ],
    notes: "Jadwal 25 November masih menunggu persetujuan. Buka dengan dua janji dari sesi sebelumnya: Sesi 1 menunda perbandingan CSV vs Parquet ke sesi ini, dan Sesi 2 menutup dengan pesan partition harus sudah ada sebelum query.",
  });

  L.addAgendaSlide(pptx, {
    title: "Rencana Sesi 2 Jam",
    items: [
      { time: "13.30 - 13.40", text: "Pembukaan, recap Sesi 2, peta 10 sesi", tag: "Pembukaan", duration: "10 mnt" },
      { time: "13.40 - 14.05", text: "Row-based vs kolumnar", tag: "Konsep", duration: "25 mnt" },
      { time: "14.05 - 14.20", text: "Partitioning", tag: "Konsep", duration: "15 mnt" },
      { time: "14.20 - 15.05", text: "Hands-on: simpan, baca, partisi", tag: "Hands-on", duration: "45 mnt" },
      { time: "15.05 - 15.20", text: "Data lake, warehouse, lakehouse, object storage sekilas", tag: "Konsep", duration: "15 mnt" },
      { time: "15.20 - 15.30", text: "Recap dan jembatan ke Sesi 4", tag: "Penutup", duration: "10 mnt" },
    ],
    note: "Slot sore (15.30 - 17.30) memakai susunan yang sama.",
    notes: "Total 120 menit. Hands-on 45 menit, jaga agar dua bagian konsep di awal tidak melebihi 40 menit.",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Tujuan Pembelajaran",
    title: "Setelah Sesi Ini, Kamu Mampu",
    cards: [
      { heading: "Menjelaskan", body: "perbedaan format row-based (CSV) dan kolumnar (Parquet), dan kapan masing-masing cocok." },
      { heading: "Menjelaskan", body: "partitioning dan manfaatnya: hanya membaca bagian data yang diperlukan." },
      { heading: "Membedakan", body: "data lake, data warehouse, dan lakehouse dari sisi tujuan dan trade-off." },
      { heading: "Memilih", body: "format dan cara menyimpan data untuk sebuah kasus." },
    ],
    footerNote: "Target akhir sesi: 10 juta transaksi tersimpan sebagai Parquet terpartisi per bulan, dan satu bulan terbaca tanpa membaca semuanya.",
    notes: "Tujuan keempat dipakai di tabel keputusan langkah 5 hands-on.",
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
    highlightIndex: 2,
    note: "Janji sebelumnya: Sesi 1 menunda CSV vs Parquet. Sesi 2: partition harus ada sebelum query.",
    notes: "Sesi 1 menunda pertanyaan CSV vs Parquet. Sesi 2 membagi file 10 juta baris menjadi part_00.csv dan seterusnya untuk diproses paralel. Hari ini partition disimpan permanen dalam format yang tepat.",
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
    note: "Format dan partition dari sesi ini dipakai lagi di Sesi 4 (Spark) dan Sesi 9 (cloud).",
    notes: "Cukup sebut arah besarnya.",
  });

  // ---------- Bagian 1: Row-based vs kolumnar ----------
  L.addSectionSlide(pptx, {
    number: "01",
    title: "Row-based vs Kolumnar",
    subtitle: "Cara data tersusun di disk menentukan berapa banyak yang harus dibaca",
    items: ["Masalah penyimpanan di skala besar", "Susunan per baris vs per kolom", "Column pruning dan kompresi", "CSV vs Parquet"],
    notes: "25 menit untuk bagian ini termasuk diskusi.",
  });

  L.addNumberedListSlide(pptx, {
    eyebrow: "Masalah di Skala Besar",
    title: "Tiga Biaya yang Membesar Bersama Data",
    items: [
      { heading: "Ukuran data", body: "10 juta transaksi dalam CSV hampir 1 GB. Ruang disk dan waktu salin ikut membesar." },
      { heading: "Biaya membaca", body: "Kueri yang hanya butuh dua kolom atau satu bulan tetap membaca seluruh file bila formatnya tidak mendukung." },
      { heading: "Banyak pembaca", body: "Laporan, analis, dan model membaca data yang sama berulang kali. Setiap pembacaan yang boros dikalikan jumlah pembaca." },
    ],
    quote: "Pertanyaan bisnis: bagaimana menyimpan 10 juta transaksi supaya kueri tertentu tidak perlu membaca semuanya?",
    notes: "Konsep inti nomor 1. Hubungkan ke laporan penjualan retail Sesi 1 dan 2.",
  });

  L.addBeforeAfterSlide(pptx, {
    eyebrow: "Susunan di Disk",
    title: "Per Baris vs Per Kolom untuk Kueri Dua Kolom",
    before: {
      label: "Row-based (CSV)",
      items: [
        "Satu baris utuh disimpan berurutan: id, waktu, kota, ..., status",
        "Kueri quantity x unit_price tetap memindai semua 10 kolom",
        "Angka disimpan sebagai teks, harus di-parse ulang",
        "Nilai sejenis berjauhan, sulit dikompres",
      ],
    },
    after: {
      label: "Kolumnar (Parquet)",
      items: [
        "Nilai satu kolom disimpan berdekatan",
        "Column pruning: hanya quantity dan unit_price yang dibaca",
        "Tipe data disimpan apa adanya (int, datetime)",
        "Nilai sejenis berdekatan, mudah dikompres",
      ],
    },
    note: "Column pruning: membaca hanya kolom yang diminta kueri.",
    notes: "Gambarkan di papan: tabel 3 baris x 4 kolom, lalu tulis urutan byte versi baris dan versi kolom.",
  });

  L.addComparisonTableSlide(pptx, {
    eyebrow: "CSV vs Parquet",
    title: "Dua Format, Dua Tujuan",
    headers: ["Aspek", "CSV", "Parquet"],
    rows: [
      ["Susunan", "Row-based, teks", "Kolumnar, biner"],
      ["Ukuran", "Besar, tanpa kompresi", "Kecil, terkompresi per kolom"],
      ["Kecepatan baca", "Memindai seluruh file walau butuh 2 kolom", "Hanya membaca kolom yang diminta"],
      ["Dapat dibaca manusia", "Ya, buka di editor teks", "Tidak, perlu library"],
      ["Cocok untuk", "Data kecil, pertukaran sederhana", "Data besar, analitik berulang"],
    ],
    note: "Parquet bukan jawaban untuk semuanya. CSV tetap cocok untuk data kecil dan data yang perlu dibaca manusia.",
    notes: "Pesan kunci kedua. Pertanyaan yang sering muncul: apakah selalu pakai Parquet? Tidak, lihat tabel keputusan di akhir hands-on.",
  });

  L.addStatSlide(pptx, {
    eyebrow: "Hasil Hands-on",
    title: "10 Juta Transaksi, Dua Format",
    stats: [
      { value: "~945 MB", label: "CSV", body: "10 juta baris, 10 kolom, teks" },
      { value: "~177 MB", label: "Parquet", body: "data yang sama, kolumnar dan terkompresi", highlight: true },
      { value: "~5x", label: "Lebih kecil", body: "nilai sejenis berdekatan dan tipe data disimpan apa adanya" },
    ],
    conclusion: "Kesimpulan: format kolumnar menghemat ruang dan memungkinkan column pruning. Waktu tulis dan baca diukur sendiri di laptop masing-masing.",
    source: SRC,
    notes: "Ukuran file relatif stabil, tetapi tetap sebut sekitar. Jangan menjanjikan angka waktu, karena tergantung laptop, disk, dan antivirus. Kenapa Parquet lebih kecil: nilai sejenis berdekatan sehingga mudah dikompres, dan tipe data disimpan apa adanya. Kenapa tulis Parquet lebih cepat padahal ada kompresi: file yang ditulis jauh lebih kecil dan tidak ada konversi angka ke teks.",
  });

  // ---------- Bagian 2: Partitioning ----------
  L.addSectionSlide(pptx, {
    number: "02",
    title: "Partitioning",
    subtitle: "Satu folder per nilai kolom, supaya kueri bisa melewati folder yang tidak perlu",
    items: ["Struktur folder month=...", "Partition pruning", "Kardinalitas dan small files", "Memilih kolom partisi"],
    notes: "15 menit. Hubungkan ke Sesi 2: di sana partition dibuat sementara untuk diproses paralel, di sini partition disimpan permanen.",
  });

  L.addTwoPanelSlide(pptx, {
    eyebrow: "Struktur Partisi",
    title: "Satu Folder per Bulan",
    panels: [
      {
        label: "Di disk",
        title: "retail_10m_by_month/",
        body: "Nilai kolom partisi menjadi nama folder. Isi tiap folder adalah file Parquet biasa.",
        listLabel: "Isi folder",
        items: ["month=2025-01/", "month=2025-02/", "month=2025-03/", "... sampai month=2025-12/"],
      },
      {
        label: "Di kode",
        title: "partition_cols dan filters",
        body: "Tulis dengan partition_cols, baca dengan filters. Folder lain tidak dibuka.",
        listLabel: "Parameter",
        items: ['partition_cols=["month"]', 'filters=[("month", "==", "2025-03")]'],
        code: true,
      },
    ],
    note: "Chunk adalah potongan saat membaca satu file. Partition adalah bagian data yang disimpan terpisah.",
    notes: "Bedakan chunk (Sesi 2 langkah 4, chunksize; dipakai lagi di langkah 1 hari ini) dan partition (disimpan terpisah, dipilih saat baca).",
  });

  L.addLabelRowsSlide(pptx, {
    eyebrow: "Empat Hal tentang Partition",
    title: "Partition Menolong Bila Kolomnya Tepat",
    rows: [
      { term: "Partition pruning", body: "Kueri dengan filter pada kolom partisi hanya membuka folder yang cocok. Satu bulan = sekitar 1/12 data." },
      { term: "Kardinalitas", body: "Jumlah nilai unik kolom. month punya 12, product_id punya 5.000." },
      { term: "Small files", body: "Kardinalitas tinggi menghasilkan banyak file kecil. Metadata tiap file menjadi beban dan ukuran total membengkak.", highlight: true },
      { term: "Memilih kolom partisi", body: "Pilih kolom dengan nilai unik sedikit yang sering dipakai untuk filter, misalnya bulan." },
    ],
    note: "Terlalu banyak partition membuat penyimpanan lebih buruk, bukan lebih baik.",
    notes: "Langkah 4 hands-on membuktikan baris ketiga.",
  });

  // ---------- Bagian 3: Hands-on ----------
  L.addSectionSlide(pptx, {
    number: "03",
    title: "Hands-on: Simpan, Baca, Partisi",
    subtitle: "Satu notebook, satu dataset, empat percobaan penyimpanan",
    items: ["Langkah 0 - 1: verifikasi, CSV vs Parquet", "Langkah 2: column pruning", "Langkah 3: partitioning per bulan", "Langkah 4 - 5: terlalu banyak partition, tabel keputusan"],
    notes: "45 menit. Notebook lengkap, peserta menjalankan sel demi sel bersama trainer.",
  });

  L.addChecklistSlide(pptx, {
    eyebrow: "Sebelum Mulai",
    title: "Cek Environment dan File Data",
    items: [
      "Python 3.12 ke atas (acuan 3.13)",
      "pip install -r requirements.txt sudah dijalankan",
      "Sel versi menampilkan pandas 3.0.5, pyarrow 26.0.1, numpy 2.5.4",
      "retail_transactions_10m.csv ada di folder notebook (dari make_data_s02.py)",
      "retail_transactions.csv (Sesi 1) ada di folder notebook",
      "Ruang disk kosong minimal 3 GB",
      "Jangan buka folder hasil_s03 di file explorer selama sesi",
    ],
    footerNote: "Belum punya file 10 juta baris: salin dari Starter Kit Sesi 2, atau jalankan python make_data_s02.py --tanpa-parts sebelum sesi.",
    notes: "Langkah 0 notebook memeriksa keberadaan file dan memberi pesan jelas bila belum ada. Notebook membaca per chunk dan per batch, puncak memori sekitar 2,5 GB (langkah 2), jadi laptop RAM 8 GB aman bila aplikasi berat ditutup.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Bagian A",
    title: "Langkah 0 - 3",
    steps: [
      { heading: "0. Verifikasi", body: "Cek versi, file data, dan path hasil. Cepat, tidak memuat data." },
      { heading: "1. CSV vs Parquet", body: "Baca per chunk 1 juta baris, tulis ke dua format, bandingkan ukuran dan waktu." },
      { heading: "2. Column pruning", body: "Baca hanya quantity dan unit_price dari kedua file, hitung total quantity x unit_price." },
      { heading: "3. Partitioning", body: "Simpan per bulan dengan partition_cols, baca Maret 2025 dengan filters." },
    ],
    checkpoint: {
      title: "Checkpoint",
      items: ["Jumlah baris: 10,000,000", "CSV ~945 MB, Parquet ~177 MB", "Total: 36,364,051,240,000 (36,4 triliun, semua status)", "Jumlah folder: 12", "Maret 2025: 844,330 baris"],
    },
    note: "Waktu bervariasi antar laptop. Yang dicocokkan hanya jumlah baris, total, dan jumlah folder.",
    notes: "Langkah 2 sengaja menghitung semua status, bukan hanya COMPLETED. Sebut eksplisit agar tidak tertukar dengan revenue COMPLETED Sesi 1 dan 2. Pembanding langkah 3b: tanpa partisi, kolom transaction_ts dari semua bulan (10 juta baris) harus dibaca dulu untuk menemukan Maret. Tekankan jumlah baris yang dibaca (844.330 vs 10 juta), bukan selisih detik yang kecil.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Langkah 1",
    title: "Simpan sebagai CSV dan Parquet",
    language: "python",
    code: CODE_STEP1,
    caption: "Per chunk 1 juta baris: hanya satu chunk di memori. Jumlah baris: 10,000,000; CSV ~945 MB, Parquet ~177 MB.",
    notes: "Pola chunked yang sama dengan Sesi 2 langkah 4. lineterminator membuat ukuran CSV sama di Windows, macOS, dan Linux. Tulis CSV adalah bagian paling lama di langkah 1. Di Windows, baca Parquet pertama setelah file baru ditulis bisa lambat, kemungkinan karena antivirus memindai file baru. Jalankan ulang sel bila angkanya janggal.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Langkah 3",
    title: "Partisi per Bulan, per Batch",
    language: "python",
    code: CODE_STEP3,
    caption: "Expected output: Jumlah folder: 12, sekitar 225 MB. Langkah 3b membaca Maret dengan filters: 844,330 baris.",
    notes: "rmtree menghapus folder lama, jadi sel aman dijalankan ulang. Satu folder bulan bisa berisi beberapa file (satu per batch). Langkah 3b: dengan filters hanya folder Maret yang dibaca; pembanding membaca kolom transaction_ts dari 10 juta baris. Jumlah barisnya harus sama, 844.330.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Bagian B",
    title: "Langkah 4 - 5",
    steps: [
      { heading: "4. Terlalu banyak partition", body: "Ambil 100.000 baris pertama retail_transactions.csv, simpan dengan partition_cols=[\"product_id\"] dan max_partitions=10000." },
      { heading: "Bandingkan", body: "Hitung jumlah file dan ukuran total, bandingkan dengan satu file Parquet berisi data yang sama." },
      { heading: "5. Tabel keputusan", body: "Pilih format dan kolom partisi untuk 3 kasus yang diberikan." },
    ],
    checkpoint: {
      title: "Checkpoint",
      items: ["Belasan ribu file kecil", "Ukuran total sekitar 93 MB vs sekitar 1,9 MB satu file", "Rata-rata beberapa KB per file", "Tabel keputusan terisi untuk 3 kasus"],
    },
    note: "Sel langkah 4 wajar lama, apalagi dengan antivirus aktif. Jumlah file persis berbeda antar versi dan mesin.",
    notes: "Tanpa max_partitions, pyarrow menolak dengan ArrowInvalid: ... exceeds the maximum of 1024. Itu batas pengaman bawaan terhadap partisi berlebihan. Langkah 4 hanya memakai 100.000 baris; 1 juta baris menghasilkan ratusan ribu file.",
  });

  // ---------- Bagian 4: Lake, warehouse, lakehouse ----------
  L.addSectionSlide(pptx, {
    number: "04",
    title: "Data Lake, Data Warehouse, Lakehouse",
    subtitle: "Tiga pendekatan menyimpan data di skala besar, bukan tiga produk",
    items: ["Tujuan dan jenis data", "Kekuatan dan kelemahan", "Object storage dan file system terdistribusi", "Table format sekilas"],
    notes: "15 menit, konsep saja, tanpa hands-on.",
  });

  L.addComparisonTableSlide(pptx, {
    eyebrow: "Tiga Pendekatan",
    title: "Lake, Warehouse, Lakehouse",
    headers: ["Aspek", "Data lake", "Data warehouse", "Lakehouse"],
    rows: [
      ["Tujuan", "Tampung semua data mentah", "Laporan dan analitik terstruktur", "Analitik dan ML di atas satu salinan data"],
      ["Jenis data", "Terstruktur, semi, tidak terstruktur", "Terstruktur", "Semua jenis, dikelola sebagai tabel"],
      ["Struktur", "File (CSV, Parquet, JSON) di storage", "Tabel dengan skema ketat", "File Parquet + lapisan table format"],
      ["Kekuatan", "Murah, fleksibel, skala besar", "Konsisten, kueri SQL cepat", "Fleksibel seperti lake, terkelola seperti warehouse"],
      ["Kelemahan", "Mudah jadi tidak terkelola", "Mahal, kurang fleksibel", "Lebih banyak komponen untuk dipelajari"],
    ],
    note: "Hasil hands-on hari ini (Parquet terpartisi per bulan) adalah bentuk paling sederhana dari isi data lake.",
    notes: "Contoh isi lake dari sesi sebelumnya: orders_app.json, reviews.csv, dan product_images/ di Sesi 1 (semi dan tidak terstruktur) bisa disimpan berdampingan dengan Parquet hari ini. Apa bedanya lakehouse dengan lake: lakehouse menambahkan lapisan pengelolaan tabel (transaksi dan skema) di atas file di lake. Detail produk di luar sesi ini.",
  });

  L.addNumberedListSlide(pptx, {
    eyebrow: "Sekilas",
    title: "Di Mana File Itu Disimpan di Skala Besar",
    items: [
      { heading: "Object storage", body: "Penyimpanan file berbasis objek yang murah dan hampir tanpa batas. Folder month=... tetap dipakai sebagai awalan nama objek." },
      { heading: "File system terdistribusi", body: "File dipecah dan disimpan di banyak mesin, contohnya HDFS. Pembaca membaca bagian-bagian file secara paralel." },
      { heading: "Table format", body: "Lapisan metadata di atas file Parquet yang menambahkan transaksi dan skema, misalnya Delta Lake dan Iceberg." },
    ],
    quote: "Layanan cloud spesifik dibahas di Sesi 9 - Cloud Approach for Big Data Solution.",
    notes: "Sebut sekilas saja, tanpa kode. Jembatan ke Sesi 4 dan Sesi 9.",
  });

  // ---------- Penutup ----------
  L.addClosingSlide(pptx, {
    title: "Ringkasan Sesi 3",
    points: [
      "Cara menyimpan data menentukan cara memprosesnya",
      "Kolumnar dan partition membuat kueri hanya membaca yang perlu",
      "CSV tetap cocok untuk data kecil dan data yang dibaca manusia",
      "Partition pada kolom berkardinalitas tinggi menghasilkan small files",
      "Lake, warehouse, lakehouse adalah pendekatan, bukan produk",
    ],
    nextStep: "Sesi 4 - Batch Processing Framework (Spark), membaca data Parquet terpartisi",
    notes: "Recap 10 menit. Sesi 4 akan membaca folder Parquet terpartisi seperti yang dibuat hari ini.",
  });

  L.addThankYouSlide(pptx, {
    lines: ["Sesi berikutnya: Sesi 4 - Batch Processing Framework (Spark)"],
    contact: "Kontak: Fahmi, Mentor Data & AI",
    notes: "Tanya jawab. Ingatkan peserta menjalankan sel pembersihan di akhir notebook untuk menghapus folder hasil_s03.",
  });

  const out = await L.save(pptx, OUT);
  console.log("written", out);
}

if (require.main === module) main();
module.exports = { CODE_STEP1, CODE_STEP3 };
