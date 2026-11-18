const fs = require("fs");
const path = require("path");
const L = require("./insignia_deck_lib.js");

const MODULE_TITLE = "Introduction to Big Data";
const OUT_DIR = path.join(__dirname, "output", "Introduction_to_Big_Data", "1_PPT");

async function main() {
  const pptx = L.newDeck(MODULE_TITLE, "Introduction to Big Data | Insignia Data & AI Training");

  // 1. Title
  let s = L.addDividerSlide(pptx, {
    eyebrow: "Internal Training",
    title: MODULE_TITLE,
    subtitle: "Kenapa data besar butuh pendekatan berbeda: dari Pandas ke Spark",
    meta: [
      { label: "Peserta", value: "DE & DS" },
      { label: "Level", value: "Pemula-Menengah" },
      { label: "Tool", value: "Databricks" },
    ],
  });
  s.addNotes("Pembukaan. Modul ini fondasi sebelum Spark Performance Tuning, Delta Lake & Lakehouse Ops, dan Streaming at Scale.");

  // 2. Agenda
  L.addAgendaSlide(pptx, {
    eyebrow: "Agenda",
    title: "Rencana Sesi (120 Menit)",
    items: [
      { number: "01", text: "Pembukaan & tujuan pembelajaran", tag: "Pembukaan", time: "00:00-00:10" },
      { number: "02", text: "Apa itu Big Data: 5V & kapan data jadi besar", tag: "Konsep", time: "00:10-00:30" },
      { number: "03", text: "Single-machine vs distributed processing", tag: "Konsep", time: "00:30-00:50" },
      { number: "04", text: "Data lake vs data warehouse vs lakehouse", tag: "Konsep", time: "00:50-01:05" },
      { number: "05", text: "Batch vs streaming", tag: "Konsep", time: "01:05-01:15" },
      { number: "06", text: "Tools landscape: Spark, Databricks, Delta Lake", tag: "Konsep", time: "01:15-01:30" },
      { number: "07", text: "Hands-on: Pandas vs PySpark di dataset yang sama", tag: "Hands-on", time: "01:30-01:50" },
      { number: "08", text: "Q&A & penutup", tag: "Penutup", time: "01:50-02:00" },
    ],
  });

  // 3. Tujuan
  L.addCardGridSlide(pptx, {
    eyebrow: "Tujuan Pembelajaran",
    title: "Setelah Sesi Ini, Kamu Mampu",
    cards: [
      { number: 1, heading: "Menjelaskan", body: "apa itu Big Data lewat 5V, bukan sekadar ukuran file." },
      { number: 2, heading: "Membedakan", body: "single-machine vs distributed processing dan kapan masing-masing cocok." },
      { number: 3, heading: "Memetakan", body: "posisi lake, warehouse, lakehouse, serta batch vs streaming." },
      { number: 4, heading: "Menjalankan", body: "transformasi dasar yang sama di Pandas dan PySpark di Databricks." },
    ],
    footerNote: "Target akhir sesi: notebook Pandas vs PySpark jalan dan hasil keduanya identik.",
  });

  // ---- Section 1: 5V ----
  L.addDividerSlide(pptx, {
    eyebrow: "Bagian 1",
    title: "Apa Itu Big Data?",
    subtitle: "Kapan data \"jadi besar\" dan kenapa ukuran file saja tidak cukup",
  });

  s = L.addComparisonTableSlide(pptx, {
    eyebrow: "Konsep",
    title: "5V: Lima Dimensi Big Data",
    headers: ["Dimensi", "Artinya", "Contoh di industri"],
    rows: [
      ["Volume", "Jumlah data melebihi kapasitas satu mesin", "Log transaksi harian ratusan GB"],
      ["Velocity", "Data datang terus-menerus dan cepat", "Clickstream aplikasi, sensor IoT"],
      ["Variety", "Format beragam: tabel, JSON, teks, gambar", "CSV + API JSON + file PDF"],
      ["Veracity", "Kualitas & keandalan data tidak seragam", "Data duplikat, nilai kosong, typo"],
      ["Value", "Data harus menghasilkan insight bisnis", "Rekomendasi produk, deteksi fraud"],
    ],
  });
  s.addNotes("Tekankan: data 5 GB bisa 'big' kalau datang tiap detik (velocity) atau formatnya campur (variety). Sebaliknya 50 GB statis di warehouse belum tentu butuh Spark.");

  s = L.addComparisonTableSlide(pptx, {
    eyebrow: "Konsep",
    title: "Kapan Data \"Jadi Besar\"?",
    headers: ["Ukuran data", "Pendekatan yang masuk akal", "Catatan"],
    rows: [
      ["< 1 GB", "Pandas di laptop", "Spark justru lebih lambat (overhead)"],
      ["1 - 10 GB", "Pandas mulai berat, Spark mulai relevan", "Tergantung RAM mesin"],
      ["10 - 100 GB", "Distributed processing (Spark)", "Tidak muat di memori satu mesin"],
      ["> 100 GB / streaming", "Spark + lakehouse (Delta Lake)", "Butuh skala horizontal"],
    ],
  });
  s.addNotes("Angka ini rule of thumb, bukan batas mutlak. Patokan praktis: Pandas butuh RAM sekitar 5-10x ukuran file. Di hands-on nanti, dataset 1 juta baris kemungkinan lebih cepat di Pandas; itu disengaja.");

  // ---- Section 2: Arsitektur ----
  L.addDividerSlide(pptx, {
    eyebrow: "Bagian 2",
    title: "Single-Machine vs Distributed",
    subtitle: "Scale up vs scale out",
  });

  L.addBeforeAfterSlide(pptx, {
    eyebrow: "Arsitektur",
    title: "Scale Up vs Scale Out",
    before: {
      label: "Single-machine (Pandas)",
      items: [
        "Semua data harus muat di RAM satu mesin",
        "Diproses satu core secara default",
        "Scale up: beli mesin lebih besar, ada batasnya",
        "Mesin mati = job gagal",
      ],
    },
    after: {
      label: "Distributed (Spark)",
      items: [
        "Data dipecah jadi partisi di banyak node",
        "Partisi diproses paralel oleh executor",
        "Scale out: tambah node sesuai kebutuhan",
        "Task gagal diulang otomatis (fault tolerance)",
      ],
    },
  });

  s = L.addTimelineSlide(pptx, {
    eyebrow: "Arsitektur",
    title: "Cara Spark Memproses Data",
    steps: [
      { label: "Driver", description: "Menerima kode dan menyusun execution plan" },
      { label: "Partition", description: "Data dipecah jadi potongan kecil" },
      { label: "Executor", description: "Tiap partisi diproses paralel di node berbeda" },
      { label: "Shuffle", description: "Data dipertukarkan antar node saat groupBy/join" },
      { label: "Result", description: "Hasil digabung atau ditulis ke storage" },
    ],
  });
  s.addNotes("Cukup konsep. Detail shuffle & partition tuning ada di modul Spark Performance Tuning. Sebut juga lazy evaluation: transformasi baru dieksekusi saat ada action (show, count, write).");

  // ---- Section 3: Storage ----
  L.addDividerSlide(pptx, {
    eyebrow: "Bagian 3",
    title: "Lake, Warehouse, Lakehouse",
    subtitle: "Di mana Big Data disimpan",
  });

  s = L.addComparisonTableSlide(pptx, {
    eyebrow: "Storage",
    title: "Data Lake vs Data Warehouse vs Lakehouse",
    headers: ["Aspek", "Data Lake", "Data Warehouse", "Lakehouse"],
    rows: [
      ["Format data", "Semua format, raw", "Terstruktur", "Semua format, open table"],
      ["Schema", "Schema-on-read", "Schema-on-write", "Schema enforcement opsional"],
      ["Transaksi ACID", "Tidak", "Ya", "Ya (Delta Lake)"],
      ["Biaya storage", "Murah (object storage)", "Mahal", "Murah (object storage)"],
      ["Use case utama", "Data science, arsip raw", "BI & reporting", "BI + ML di satu tempat"],
    ],
  });
  s.addNotes("Peserta sudah kenal warehouse & lake. Fokus ke kenapa lakehouse muncul: menggabungkan biaya murah lake dengan keandalan warehouse. Detail di modul Delta Lake & Lakehouse Ops.");

  // ---- Section 4: Batch vs Streaming ----
  L.addDividerSlide(pptx, {
    eyebrow: "Bagian 4",
    title: "Batch vs Streaming",
    subtitle: "Kapan data diproses",
  });

  s = L.addComparisonTableSlide(pptx, {
    eyebrow: "Processing",
    title: "Batch vs Real-time / Streaming",
    headers: ["Aspek", "Batch", "Streaming"],
    rows: [
      ["Kapan diproses", "Terjadwal (per jam / harian)", "Terus-menerus saat data datang"],
      ["Latensi", "Menit sampai jam", "Detik sampai sub-detik"],
      ["Kompleksitas", "Lebih sederhana", "Lebih kompleks (state, late data)"],
      ["Contoh", "Laporan penjualan harian", "Deteksi fraud transaksi"],
      ["Di Spark", "spark.read / df.write", "spark.readStream / writeStream"],
    ],
  });
  s.addNotes("Konsep saja. Spark memakai API DataFrame yang mirip untuk batch dan streaming. Detail di modul Streaming at Scale. Hands-on hari ini batch.");

  // ---- Section 5: Tools ----
  L.addDividerSlide(pptx, {
    eyebrow: "Bagian 5",
    title: "Tools Landscape",
    subtitle: "Spark, Databricks, Delta Lake: siapa mengerjakan apa",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Tools",
    title: "Posisi Masing-Masing Tool",
    cards: [
      { number: 1, heading: "Apache Spark", body: "Engine open-source untuk distributed processing. Lapisan compute: yang menjalankan transformasi." },
      { number: 2, heading: "Delta Lake", body: "Format tabel open-source di atas Parquet. Lapisan storage: ACID, time travel, schema enforcement." },
      { number: 3, heading: "Databricks", body: "Platform managed yang menyatukan Spark, Delta Lake, notebook, dan governance (Unity Catalog)." },
    ],
    footerNote: "Analogi: Spark = mesin, Delta Lake = gudang yang rapi, Databricks = pabrik yang menyatukan keduanya.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Learning Path",
    title: "Setelah Modul Ini",
    steps: [
      { label: "Intro to Big Data", description: "Konsep dasar (modul ini)" },
      { label: "Spark Performance Tuning", description: "Partition, shuffle, caching, AQE" },
      { label: "Delta Lake & Lakehouse Ops", description: "ACID, MERGE, OPTIMIZE, time travel" },
      { label: "Streaming at Scale", description: "Structured Streaming end-to-end" },
    ],
  });

  // ---- Hands-on ----
  L.addDividerSlide(pptx, {
    eyebrow: "Hands-on",
    title: "Pandas vs PySpark",
    subtitle: "Transformasi yang sama di dataset yang sama: retail_transactions.csv",
    meta: [
      { label: "Durasi", value: "20 menit" },
      { label: "Dataset", value: "1.000.000 baris" },
      { label: "Platform", value: "Databricks" },
    ],
  });

  s = L.addCodeSlide(pptx, {
    eyebrow: "Hands-on 1",
    title: "Versi Pandas (Single-Machine)",
    language: "Python",
    code: [
      'import pandas as pd',
      '',
      'DATA_PATH = "/Volumes/workspace/default/bigdata_intro/retail_transactions.csv"',
      '',
      'df = pd.read_csv(DATA_PATH)',
      'completed = df[df["status"] == "COMPLETED"].copy()',
      'completed["revenue"] = completed["quantity"] * completed["unit_price"]',
      'summary_pd = (completed.groupby(["city", "category"], as_index=False)',
      '              .agg(total_revenue=("revenue", "sum"),',
      '                   n_trx=("transaction_id", "count"))',
      '              .sort_values("total_revenue", ascending=False))',
      'summary_pd.to_parquet(',
      '    "/Volumes/workspace/default/bigdata_intro/summary_pandas.parquet",',
      '    index=False)',
    ].join("\n"),
    caption: "Eksekusi langsung (eager): setiap baris langsung diproses di memori driver.",
  });

  s = L.addCodeSlide(pptx, {
    eyebrow: "Hands-on 2",
    title: "Versi PySpark (Distributed)",
    language: "PySpark",
    code: [
      'from pyspark.sql import functions as F',
      '',
      'DATA_PATH = "/Volumes/workspace/default/bigdata_intro/retail_transactions.csv"',
      '',
      'df_sp = spark.read.csv(DATA_PATH, header=True, inferSchema=True)',
      'summary_sp = (df_sp.filter(F.col("status") == "COMPLETED")',
      '              .withColumn("revenue", F.col("quantity") * F.col("unit_price"))',
      '              .groupBy("city", "category")',
      '              .agg(F.sum("revenue").alias("total_revenue"),',
      '                   F.count("transaction_id").alias("n_trx"))',
      '              .orderBy(F.desc("total_revenue")))',
      'summary_sp.write.mode("overwrite").format("delta") \\',
      '    .saveAsTable("workspace.default.summary_spark")',
    ].join("\n"),
    caption: "Lazy evaluation: tidak ada yang dieksekusi sampai action (write / show / count).",
  });

  s = L.addComparisonTableSlide(pptx, {
    eyebrow: "Refleksi",
    title: "Apa yang Kamu Amati?",
    headers: ["Aspek", "Pandas", "PySpark"],
    rows: [
      ["Model eksekusi", "Eager, satu mesin", "Lazy, terdistribusi"],
      ["Kecepatan di 1 juta baris", "Biasanya lebih cepat", "Ada overhead scheduling"],
      ["Batas skala", "RAM satu mesin", "Tambah node"],
      ["Output", "File Parquet", "Tabel Delta (ACID)"],
      ["Hasil agregasi", "Identik", "Identik"],
    ],
  });
  s.addNotes("Poin pembelajaran kunci: di data kecil Spark kalah cepat karena overhead. Spark menang saat data tidak muat di satu mesin. Big Data adalah soal memilih alat sesuai 5V, bukan selalu pakai Spark.");

  L.addChecklistSlide(pptx, {
    eyebrow: "Checklist",
    title: "Sebelum Sesi Selesai",
    items: [
      "Notebook terbuka dan terhubung ke compute",
      "Dataset ter-upload ke Volume bigdata_intro",
      "Versi Pandas jalan, summary_pandas.parquet tertulis",
      "Versi PySpark jalan, tabel summary_spark terbentuk",
      "Hasil Pandas dan PySpark sudah dibandingkan",
      "Waktu eksekusi keduanya sudah dicatat",
    ],
    footerNote: "Detail langkah dan checkpoint ada di Modul Praktikum.",
  });

  L.addClosingSlide(pptx, {
    title: "Ringkasan",
    points: [
      "Big Data didefinisikan oleh 5V, bukan ukuran file saja",
      "Distributed processing menang saat data melebihi satu mesin",
      "Lakehouse menggabungkan biaya lake dan keandalan warehouse",
      "Spark = compute, Delta Lake = storage, Databricks = platform",
    ],
    nextStep: "Spark Performance Tuning",
  });

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const outPath = path.join(OUT_DIR, "Introduction_to_Big_Data.pptx");
  await pptx.writeFile({ fileName: outPath });
  console.log(`Deck tersimpan di: ${outPath}`);
}

main();
