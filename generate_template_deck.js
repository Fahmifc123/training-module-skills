// Contoh pemakaian semua komponen insignia_deck_lib.js.
// Hasil: brand/slide-templates/Template_Training_Insignia.pptx
// Jalankan: node generate_template_deck.js
const path = require("path");
const L = require("./insignia_deck_lib.js");

async function main() {
  const pptx = L.newDeck("Template Deck Training Insignia");

  L.addCoverSlide(pptx, {
    eyebrow: "Internal Training",
    title: "Big Data",
    subtitle: "Sesi 4 - Batch Processing Framework (Spark)",
    description: "Memproses data skala besar secara terdistribusi dengan Apache Spark.",
    meta: [
      { label: "Hari", value: "Rabu, 2 Desember 2026" },
      { label: "Slot siang", value: "13.30 - 15.30 WIB" },
      { label: "Slot sore", value: "15.30 - 17.30 WIB" },
      { label: "Lokasi", value: "Kantor Insignia / online" },
    ],
    notes: "Komponen: addCoverSlide. Nama program, judul sesi (merah), satu kalimat deskripsi, maksimal 4 meta-info.",
  });

  L.addAgendaSlide(pptx, {
    title: "Rencana Sesi 2 Jam",
    items: [
      { time: "13.30 - 13.40", text: "Pembukaan dan recap sesi sebelumnya", tag: "Pembukaan", duration: "10 mnt" },
      { time: "13.40 - 14.05", text: "Konsep: driver, executor, partition", tag: "Konsep", duration: "25 mnt" },
      { time: "14.05 - 14.20", text: "Lazy evaluation dan DAG", tag: "Konsep", duration: "15 mnt" },
      { time: "14.20 - 15.00", text: "Hands-on 1: agregasi batch di Spark", tag: "Hands-on", duration: "40 mnt" },
      { time: "15.00 - 15.20", text: "Hands-on 2: partition dan join", tag: "Hands-on", duration: "20 mnt" },
      { time: "15.20 - 15.30", text: "Recap dan tanya jawab", tag: "Penutup", duration: "10 mnt" },
    ],
    note: "Slot sore (15.30 - 17.30) memakai susunan yang sama.",
    notes: "Komponen: addAgendaSlide. Tag berisi kata 'hands-on' otomatis merah dan tebal, 'konsep' abu biru, lainnya abu.",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Tujuan Pembelajaran",
    title: "Setelah Sesi Ini, Kamu Mampu",
    cards: [
      { heading: "Menjelaskan", body: "peran driver, executor, dan partition saat Spark memproses data." },
      { heading: "Menjalankan", body: "transformasi batch di DataFrame Spark dari file CSV." },
      { heading: "Membaca", body: "DAG dan stage di Spark UI untuk menemukan shuffle." },
      { heading: "Mengoptimasi", body: "jumlah partition dan strategi join sederhana." },
    ],
    footerNote: "Target akhir sesi: setiap peserta menghasilkan ringkasan revenue per kota dan kategori dari 1 juta baris data.",
    notes: "Komponen: addCardGridSlide. 2-4 kartu. footerNote dengan pola 'Label: isi' tampil sebagai bar navy dengan label merah.",
  });

  L.addSectionSlide(pptx, {
    number: 1,
    title: "Konsep Inti Spark",
    subtitle: "Kenapa satu mesin tidak cukup, dan bagaimana Spark membagi pekerjaan.",
    items: ["Batas satu mesin", "Driver, executor, partition", "Lazy evaluation dan DAG", "Narrow vs wide transformation"],
    notes: "Komponen: addSectionSlide. Nomor bagian, judul, subjudul, panel 'Di bagian ini' (0-4 topik).",
  });

  L.addNumberedListSlide(pptx, {
    eyebrow: "Masalah",
    title: "Kenapa Pandas Mentok di Data Besar",
    items: [
      { heading: "Batas memori satu mesin", body: "Seluruh DataFrame harus muat di RAM. Data melebihi RAM berarti proses gagal." },
      { heading: "Hanya satu core bekerja", body: "Sebagian besar operasi Pandas berjalan di satu thread, core lain menganggur." },
      { heading: "Tidak tahan kegagalan", body: "Jika proses mati di tengah jalan, pekerjaan diulang dari awal." },
    ],
    quote: "Masalahnya bukan di kode, tapi di batas satu mesin.",
    note: "Spark menjawab ketiganya dengan membagi data ke banyak executor dan mengulang task yang gagal.",
    notes: "Komponen: addNumberedListSlide. 2-4 item, kutipan opsional di kanan, kalimat penutup di bawah.",
  });

  L.addStatSlide(pptx, {
    eyebrow: "Skala Data",
    title: "Data yang Dipakai di Hands-on",
    stats: [
      { value: "1 juta", label: "baris transaksi", body: "Dataset sintetis retail_transactions.csv" },
      { value: "93,5 MB", label: "ukuran file CSV", body: "Cukup untuk melihat perbedaan Pandas dan Spark" },
      { value: "200", label: "shuffle partitions default", body: "Nilai bawaan spark.sql.shuffle.partitions", highlight: true },
    ],
    conclusion: "Kesimpulan: data ini masih muat di laptop, jadi perbandingan Pandas dan Spark tetap adil.",
    source: "Sumber: generator dataset sintetis modul Big Data (seed 42) dan dokumentasi konfigurasi Spark SQL.",
    notes: "Komponen: addStatSlide. 2-4 angka, highlight: true untuk kartu navy. Selalu cantumkan sumber angka.",
  });

  L.addComparisonTableSlide(pptx, {
    eyebrow: "Perbandingan",
    title: "Pandas vs Spark",
    headers: ["Aspek", "Pandas", "Spark"],
    rows: [
      ["Model eksekusi", "Eager, langsung dijalankan", "Lazy, dijalankan saat ada action"],
      ["Skala", "Terbatas RAM satu mesin", "Total memori seluruh cluster"],
      ["Paralelisme", "Umumnya satu core", "Banyak task di banyak executor"],
      ["Saat gagal", "Ulang dari awal", "Task yang gagal diulang otomatis"],
      ["Cocok untuk", "Eksplorasi data kecil-menengah", "Data besar dan pipeline produksi"],
    ],
    note: "Spark tidak selalu lebih cepat. Untuk data kecil, overhead distribusinya membuat Pandas sering lebih cepat.",
    notes: "Komponen: addComparisonTableSlide. Maksimal 6 baris data.",
  });

  L.addTwoPanelSlide(pptx, {
    eyebrow: "Jenis Transformasi",
    title: "Narrow vs Wide Transformation",
    panels: [
      { label: "Narrow", title: "Tanpa shuffle", body: "Setiap partition output hanya butuh satu partition input. Bisa dijalankan dalam satu stage.", items: ["filter()", "select()", "withColumn()"], code: true },
      { label: "Wide", title: "Butuh shuffle", body: "Data dari banyak partition harus dipindah antar executor. Memecah job menjadi stage baru.", items: ["groupBy().agg()", "join()", "orderBy()"], code: true },
    ],
    note: "Shuffle adalah operasi paling mahal di Spark. Kurangi wide transformation yang tidak perlu.",
    notes: "Komponen: addTwoPanelSlide. Panel kedua navy untuk opsi yang ditekankan. code: true memakai Courier New untuk daftar.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Alur Eksekusi",
    title: "Dari Kode ke Hasil di Spark",
    steps: [
      { label: "Action dipanggil", description: "show(), count(), atau write() memicu eksekusi." },
      { label: "DAG dibentuk", description: "Driver menyusun rencana dari semua transformasi." },
      { label: "Dibagi jadi stage", description: "Setiap shuffle memisahkan stage baru." },
      { label: "Task per partition", description: "Executor menjalankan satu task per partition." },
      { label: "Hasil dikumpulkan", description: "Output ditulis ke storage atau dikirim ke driver." },
    ],
    note: "Transformasi tanpa action tidak menjalankan apa pun. Inilah lazy evaluation.",
    notes: "Komponen: addTimelineSlide. 3-5 langkah, langkah terakhir merah.",
  });

  L.addLabelRowsSlide(pptx, {
    eyebrow: "Istilah Kunci",
    title: "Lima Istilah yang Muncul di Spark UI",
    rows: [
      { term: "Driver", body: "Proses utama yang menyusun rencana eksekusi dan membagi task." },
      { term: "Executor", body: "Proses di worker yang menjalankan task dan menyimpan data sementara." },
      { term: "Partition", body: "Potongan data. Satu partition diproses oleh satu task." },
      { term: "Stage", body: "Kumpulan task yang bisa jalan tanpa memindahkan data antar executor." },
      { term: "Shuffle", body: "Pemindahan data antar executor. Paling mahal dari sisi waktu dan jaringan.", highlight: true },
    ],
    note: "Buka Spark UI di tab Jobs dan Stages untuk melihat kelima istilah ini secara langsung.",
    notes: "Komponen: addLabelRowsSlide. 3-5 baris, highlight: true memberi kotak merah.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on 1",
    title: "Agregasi Batch dengan DataFrame",
    language: "PySpark",
    code: [
      "from pyspark.sql import SparkSession, functions as F",
      "",
      "spark = SparkSession.builder.appName(\"bigdata_s04\").getOrCreate()",
      "",
      "df = spark.read.csv(\"retail_transactions.csv\", header=True, inferSchema=True)",
      "",
      "summary = (",
      "    df.withColumn(\"revenue\", F.col(\"quantity\") * F.col(\"unit_price\"))",
      "      .groupBy(\"city\", \"category\")",
      "      .agg(F.sum(\"revenue\").alias(\"total_revenue\"),",
      "           F.count(\"transaction_id\").alias(\"n_trx\"))",
      "      .orderBy(F.desc(\"total_revenue\"))",
      ")",
      "",
      "summary.show(10)",
    ].join("\n"),
    caption: "Semua transformasi di atas baru dieksekusi saat action show() dipanggil.",
    notes: "Komponen: addCodeSlide. Maksimal 18 baris, kode lengkap dan runnable.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on 1",
    title: "Langkah dan Checkpoint",
    steps: [
      { heading: "Load data", body: "Baca retail_transactions.csv ke DataFrame Spark." },
      { heading: "Tambah kolom", body: "Hitung revenue = quantity x unit_price." },
      { heading: "Agregasi", body: "Kelompokkan per city dan category." },
      { heading: "Simpan hasil", body: "Tulis summary ke format Parquet." },
    ],
    checkpoint: { title: "Expected output", items: ["48 baris (8 kota x 6 kategori)", "Kolom: city, category, total_revenue, n_trx", "Jumlah n_trx = 1.000.000"] },
    note: "Tertinggal? buka notebook SOLUTION dan lanjut dari langkah terakhir yang berhasil.",
    notes: "Komponen: addStepsCheckpointSlide. Setiap checkpoint harus punya jawaban di Answer Key.",
  });

  L.addChecklistSlide(pptx, {
    title: "Sebelum Sesi Selesai",
    items: [
      "Spark session berjalan tanpa error", "Data berhasil di-load (1.000.000 baris)",
      "Kolom revenue sudah terbentuk", "Summary berisi 48 baris",
      "Hasil tersimpan sebagai Parquet", "Stage dengan shuffle ditemukan di Spark UI",
    ],
    footerNote: "Detail langkah dan expected output ada di Modul Praktikum.",
    notes: "Komponen: addChecklistSlide. Maksimal 8 item.",
  });

  L.addClosingSlide(pptx, {
    title: "Ringkasan Sesi 4",
    points: [
      "Spark membagi data ke banyak executor lewat partition",
      "Transformasi bersifat lazy dan baru jalan saat ada action",
      "Wide transformation memicu shuffle, operasi paling mahal",
    ],
    nextStep: "Sesi 5 - Real-Time Processing Framework (Kafka/Flink), Kamis 3 Desember 2026",
    notes: "Komponen: addClosingSlide. Ringkasan 3-5 poin dan informasi sesi berikutnya.",
  });

  L.addThankYouSlide(pptx, {
    lines: ["Sesi berikutnya: Sesi 5 - Real-Time Processing Framework (Kafka/Flink)", "Kamis, 3 Desember 2026"],
    contact: "Kontak: Fahmi, Mentor Data & AI",
    notes: "Komponen: addThankYouSlide. Penutup Q&A.",
  });

  const out = await L.save(pptx, path.join(__dirname, "brand", "slide-templates", "Template_Training_Insignia.pptx"));
  console.log("written", out);
}

main();
