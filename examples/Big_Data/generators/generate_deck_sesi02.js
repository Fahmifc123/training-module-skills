// Deck Big Data Sesi 2 - Common vs Big Data.
// Jalankan: node generate_deck_sesi02.js
const path = require("path");
const L = require("./insignia_deck_lib.js");

const OUT = path.join(__dirname, "output", "Big_Data", "Sesi_02_Common_vs_Big_Data", "1_PPT", "Common_vs_Big_Data.pptx");
const SRC = "Sumber: hasil hands-on dataset sintetis retail_transactions.csv dan retail_transactions_10m.csv (pandas 3.0.5).";

async function main() {
  const pptx = L.newDeck("Big Data - Sesi 2");

  // ---------- Pembuka ----------
  L.addCoverSlide(pptx, {
    eyebrow: "Internal Training",
    title: "Big Data",
    subtitle: "Sesi 2 - Common vs Big Data",
    description: "Membedakan data biasa dan big data lewat 5V dan angka nyata, lalu menaiki tangga solusi di satu laptop.",
    meta: [
      { label: "Hari", value: "Kamis, 12 Nov 2026" },
      { label: "Slot siang", value: "13.30 - 15.30 WIB" },
      { label: "Slot sore", value: "15.30 - 17.30 WIB" },
      { label: "Platform", value: "Jupyter / VS Code lokal" },
    ],
    notes: "Buka dengan recap Sesi 1: pipeline lima tahap berjalan baik untuk 1 juta baris transaksi dan untuk data non-tabular (JSON order, ulasan, gambar produk), dan estimasi 100x menunjukkan batas satu mesin. Hari ini datanya kita besarkan 10 kali.",
  });

  L.addAgendaSlide(pptx, {
    title: "Rencana Sesi 2 Jam",
    items: [
      { time: "13.30 - 13.40", text: "Pembukaan, recap Sesi 1, peta 10 sesi", tag: "Pembukaan", duration: "10 mnt" },
      { time: "13.40 - 14.05", text: "5V dan titik patah data biasa vs big data", tag: "Konsep", duration: "25 mnt" },
      { time: "14.05 - 14.20", text: "Scale up vs scale out, ide distributed", tag: "Konsep", duration: "15 mnt" },
      { time: "14.20 - 15.10", text: "Hands-on: tangga solusi", tag: "Hands-on", duration: "50 mnt" },
      { time: "15.10 - 15.20", text: "Batch vs streaming sekilas, jembatan ke Sesi 3", tag: "Konsep", duration: "10 mnt" },
      { time: "15.20 - 15.30", text: "Recap dan tanya jawab", tag: "Penutup", duration: "10 mnt" },
    ],
    note: "Slot sore (15.30 - 17.30) memakai susunan yang sama.",
    notes: "Total 120 menit. Hands-on 50 menit, jaga agar bagian konsep tidak melebihi waktu.",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Tujuan Pembelajaran",
    title: "Setelah Sesi Ini, Kamu Mampu",
    cards: [
      { heading: "Membedakan", body: "data biasa dan big data dengan 5V dan angka nyata, bukan hanya istilah." },
      { heading: "Menjelaskan", body: "scale up vs scale out dan kapan masing-masing dipilih." },
      { heading: "Memahami", body: "ide distributed processing: bagi data, proses paralel, gabungkan hasil." },
      { heading: "Menilai", body: "apakah sebuah kasus perlu tools big data atau cukup pendekatan klasik." },
    ],
    footerNote: "Target akhir sesi: revenue COMPLETED per kota dari 10 juta baris dengan lima cara, hasilnya sama.",
    notes: "Tujuan keempat dipakai lagi di slide tiga pertanyaan penilaian di akhir sesi.",
  });

  L.addTimelineSlide(pptx, {
    eyebrow: "Peta Modul",
    title: "10 Sesi Big Data: Sesi 1 - 5",
    steps: [
      { label: "Sesi 1", description: "Intro Classical Data Processing" },
      { label: "Sesi 2", description: "Common vs Big Data (sesi ini)" },
      { label: "Sesi 3", description: "Big Data Storage" },
      { label: "Sesi 4", description: "Batch Processing Framework (Spark)" },
      { label: "Sesi 5", description: "Real-Time Processing Framework (Kafka/Flink)" },
    ],
    highlightIndex: 1,
    note: "Recap Sesi 1: pandas dan SQL cukup untuk 1 juta baris, tetapi ada batas satu mesin.",
    notes: "Ingatkan angka Sesi 1: sekitar 136 MB per 1 juta baris setelah tipe dirapikan, estimasi 100x sekitar 14 GB.",
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
    note: "Sesi 2 menjawab pertanyaan dasar: kapan sebuah kasus disebut big data, dan apa ide di balik solusinya.",
    notes: "Cukup sebut arah besarnya.",
  });

  // ---------- Bagian 1 ----------
  L.addSectionSlide(pptx, {
    number: 1,
    title: "5V dan Titik Patah",
    subtitle: "Ukuran data saja tidak cukup untuk menyebut sesuatu big data.",
    items: ["Lima V", "Data biasa vs big data", "Angka dari Sesi 1 dan Sesi 2", "Tanda titik patah"],
    notes: "25 menit. Big data bukan soal angka tertentu, tetapi saat cara klasik tidak lagi cukup.",
  });

  L.addLabelRowsSlide(pptx, {
    eyebrow: "5V",
    title: "Lima Sudut Pandang Big Data",
    rows: [
      { term: "Volume", body: "Seberapa besar data: jumlah baris, ukuran file, kebutuhan memori." },
      { term: "Velocity", body: "Seberapa cepat data datang dan seberapa cepat harus diproses." },
      { term: "Variety", body: "Seberapa beragam bentuk data: tabel, log, teks, gambar." },
      { term: "Veracity", body: "Seberapa bisa dipercaya data: duplikat, kosong, tidak konsisten." },
      { term: "Value", body: "Nilai bisnis yang didapat. Tanpa value, data besar hanya biaya.", highlight: true },
    ],
    note: "Satu V saja yang besar belum tentu big data. Lihat apakah cara klasik masih cukup.",
    notes: "Pakai contoh retail: volume 10 juta baris, velocity transaksi harian, veracity bersih (sintetis). Variety: rujuk balik ke Sesi 1, yang sudah memakai empat bentuk data (CSV transaksi, JSON order bertingkat, teks ulasan, gambar produk), semuanya masih bisa diolah di satu laptop. Jadi variety tinggi saja belum menjadikan kasus big data.",
  });

  L.addBeforeAfterSlide(pptx, {
    eyebrow: "Data Biasa vs Big Data",
    title: "Bagaimana Tiap V Berubah",
    before: { label: "Data biasa", items: [
      "Volume: muat di memori satu laptop",
      "Velocity: diproses batch harian",
      "Variety: CSV, JSON, teks, gambar (Sesi 1)",
      "Veracity: dicek manual masih sanggup",
      "Value: laporan dari satu sumber",
    ] },
    after: { label: "Big data", items: [
      "Volume: melebihi memori satu mesin",
      "Velocity: data datang terus-menerus",
      "Variety: banyak sumber, terus bertambah",
      "Veracity: perlu aturan otomatis",
      "Value: gabungan banyak sumber",
    ] },
    note: "Kesimpulan: big data muncul ketika cara klasik tidak lagi cukup dalam memori, waktu, atau kecepatan data.",
    notes: "Tanda silang dan centang di sini bukan berarti salah dan benar, hanya kondisi kiri dan kanan. Contoh variety data biasa: CSV, JSON, teks, dan gambar di Sesi 1.",
  });

  L.addStatSlide(pptx, {
    eyebrow: "Angka Nyata",
    title: "Data yang Sama, 10 Kali Lebih Besar",
    stats: [
      { value: "155 MB", label: "1 juta baris", body: "Sesi 1, semua kolom di memori" },
      { value: "1.575 MB", label: "10 juta baris", body: "Sesi 2, semua kolom di memori", highlight: true },
      { value: "150 MB", label: "10 juta baris, dioptimasi", body: "Tipe hemat (620 MB) lalu kolom seperlunya (150 MB), mesin yang sama" },
    ],
    conclusion: "Kesimpulan: memori naik sebanding jumlah baris, tetapi tipe data dan kolom yang dipilih bisa memangkasnya.",
    source: SRC,
    notes: "Angka 1.575 MB dari langkah 2 hands-on. Langkah 3: tipe hemat saja 620 MB, setelah dua kolom unik dibuang 150 MB. Ini memori dataframe; memori proses Python di Task Manager lebih besar (puncak terukur 3,8 GB di langkah 2). Angka memori bisa berbeda jika versi pandas berbeda.",
  });

  L.addCardGridSlide(pptx, {
    eyebrow: "Titik Patah",
    title: "Tanda Kasus Melewati Batas Satu Mesin",
    cards: [
      { heading: "Memori penuh", body: "Data tidak muat lagi di RAM, proses gagal atau laptop melambat drastis." },
      { heading: "Waktu tidak masuk akal", body: "Proses melewati jadwal: laporan pagi baru selesai siang." },
      { heading: "Data terus datang", body: "Data harus diproses saat tiba, bukan menunggu batch malam." },
    ],
    footerNote: "Titik patah: saat salah satu tanda ini muncul dan cara murah sudah dicoba.",
    notes: "Titik patah = batas satu mesin dari Sesi 1. Kaitkan dengan empat tanda kewalahan di akhir Sesi 1 (memori, waktu, satu mesin, banyak file): memori dan waktu muncul di sini, satu mesin dijawab scale out di bagian 2, dan banyak file dibahas lagi di Sesi 3 (small files).",
  });

  // ---------- Bagian 2 ----------
  L.addSectionSlide(pptx, {
    number: 2,
    title: "Scale Up vs Scale Out",
    subtitle: "Sebelum keduanya: optimasi di mesin yang sama. Lalu mesin lebih besar, atau banyak mesin bekerja bersama.",
    items: ["Optimasi di mesin yang sama", "Scale up vs scale out", "Ide distributed processing", "Bagi, proses paralel, gabungkan"],
    notes: "15 menit.",
  });

  L.addComparisonTableSlide(pptx, {
    eyebrow: "Tiga Arah Solusi",
    title: "Optimasi, Scale Up, Scale Out",
    headers: ["Aspek", "Optimasi", "Scale up", "Scale out"],
    rows: [
      ["Cara", "Mesin sama: tipe hemat, kolom seperlunya, chunked", "Mesin lebih besar (RAM, CPU)", "Banyak mesin bekerja bersama"],
      ["Batas", "RAM dan CPU mesin yang ada", "Mesin terbesar yang tersedia", "Data harus bisa dibagi, ada biaya koordinasi"],
      ["Biaya", "Hampir nol, hanya kode", "Naik tajam di ukuran mesin besar", "Bertambah bertahap per mesin"],
      ["Kegagalan", "Satu mesin mati, semua berhenti", "Satu mesin mati, semua berhenti", "Satu mesin mati, yang lain lanjut"],
      ["Contoh hari ini", "Langkah 3 - 4", "Hanya dijelaskan, tidak di-hands-on", "Langkah 5: ide-nya, di satu laptop"],
    ],
    note: "Urutan: optimasi dulu (paling murah), lalu scale up, lalu scale out saat satu mesin sudah tidak cukup.",
    notes: "Banyak masalah besar selesai dengan optimasi sebelum perlu mesin besar atau sistem terdistribusi. Tipe hemat dan chunked BUKAN scale up: mesinnya sama. Langkah 5 memakai banyak proses di satu laptop untuk memperlihatkan ide scale out; di sistem big data, worker-nya berada di banyak mesin.",
  });

  L.addTwoPanelSlide(pptx, {
    eyebrow: "Distributed Processing",
    title: "Ide Dasar: Bagi, Proses Paralel, Gabungkan",
    panels: [
      { label: "Bagi dan proses", title: "Partition diproses paralel", body: "Data dibagi menjadi partition. Tiap worker menghitung hasil parsial dari partition-nya.", listLabel: "Di hands-on", items: [
        "parts/part_00.csv ... part_NN.csv",
        "1 worker = 1 partition",
        "hasil parsial per kota",
      ], code: true },
      { label: "Gabungkan", title: "Hasil parsial digabung", body: "Hasil parsial dari semua worker dijumlahkan menjadi hasil akhir.", listLabel: "Di hands-on", items: [
        "pd.concat(partials)",
        ".groupby(level=0).sum()",
        "hasil sama dengan baseline",
      ], code: true },
    ],
    note: "Scale out bekerja karena data bisa dibagi. Partition yang sudah ada adalah syarat percepatan.",
    notes: "Ini ide yang nanti diotomatiskan Spark di Sesi 4.",
  });

  // ---------- Bagian 3 ----------
  L.addSectionSlide(pptx, {
    number: 3,
    title: "Hands-on: Tangga Solusi",
    subtitle: "Satu pertanyaan bisnis, lima cara menjawabnya. Hasilnya harus sama.",
    items: ["Verifikasi environment dan data", "Langkah 1 - 3: acuan, baseline, optimasi", "Langkah 4 - 6: chunk, partition, paralel", "Bandingkan lima cara"],
    notes: "50 menit. Notebook: Notebook_Tangga_Solusi.ipynb. Ingatkan: langkah 2-3 butuh memori kosong sekitar 4 GB (puncak terukur 3,8 GB). RAM di bawah 12 GB: lewati langkah 2-3, lihat demo trainer, lalu lanjut dari langkah 4.",
  });

  L.addChecklistSlide(pptx, {
    eyebrow: "Sebelum Mulai",
    title: "Verifikasi Environment dan Data",
    items: [
      "Python 3.12 ke atas dan library dari requirements.txt",
      "RAM minimal 8 GB; di bawah 12 GB lewati langkah 2-3",
      "make_data_s02.py sudah dijalankan sebelum sesi",
      "retail_transactions_10m.csv ada (10.000.000 baris)",
      "Folder parts/ berisi file sebanyak jumlah core",
      "workers.py ada di folder yang sama dengan notebook",
    ],
    footerNote: "Catatan: make_data_s02.py butuh beberapa menit dan ruang disk sekitar 2 GB, jangan dijalankan di kelas.",
    notes: "Sel Langkah 0 mencetak RAM, jumlah core, dan jumlah file di parts/, plus baris Saran bila RAM di bawah 12 GB. Jumlah file harus sama dengan jumlah core saat make_data_s02.py dijalankan.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Langkah 1 - 3",
    title: "Kenali Data, Baseline, Optimasi",
    steps: [
      { heading: "1. Kenali data", body: "Ukuran file, jumlah baris, acuan = Sesi 1 x 10." },
      { heading: "2. Baseline", body: "Muat semua kolom ke memori, hitung revenue per kota." },
      { heading: "3. Optimasi", body: "category dan int32, lalu buang kolom yang tidak dipakai." },
    ],
    checkpoint: { title: "Expected output", items: [
      "Jumlah baris: 10,000,000; file 945-955 MB",
      "Memori: 1,575 MB (1.575 MB)",
      "Total revenue: 32,737,599,110,000 (32,7 triliun)",
      "620 MB semua kolom, 150 MB tanpa id dan timestamp; equal: True",
    ] },
    note: "Langkah 2-3 butuh memori kosong sekitar 4 GB. RAM di bawah 12 GB: lewati langkah 2-3, lanjut dari langkah 4.",
    notes: "Total revenue tepat 10 kali Sesi 1 (3.273.759.911.000) karena data digandakan 10 kali.",
  });

  L.addStepsCheckpointSlide(pptx, {
    eyebrow: "Hands-on Langkah 4 - 6",
    title: "Chunk, Partition, Paralel",
    steps: [
      { heading: "4. Chunked", body: "Baca per 1 juta baris, agregasi per chunk, gabungkan." },
      { heading: "5a. Partition tanpa paralel", body: "Proses file di parts/ satu per satu." },
      { heading: "5b. Partition + paralel", body: "Satu worker per partition (ide scale out)." },
      { heading: "6. Bandingkan", body: "Satu tabel: memori, waktu, hasil sama." },
    ],
    checkpoint: { title: "Expected output", items: [
      "Semua cara: total revenue 32,737,599,110,000",
      "equal True di langkah 4, 5a, 5b",
      "Semua hasil sama: True",
      "Waktu dan percepatan berbeda di setiap laptop",
    ] },
    note: "Percepatan bukan kriteria berhasil. Kriterianya: hasil sama di semua cara.",
    notes: "Percepatan paralel dibatasi jumlah core, kecepatan disk, dan biaya koordinasi proses. Kolom mem_data_mb di tabel langkah 6 adalah memori dataframe, bukan memori proses: di cara 5 tiap worker memuat Python dan pandas sendiri (terukur sekitar 2,2 GB untuk 12 worker). Cara yang dilewati tertulis dilewati.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 4",
    title: "Chunked Processing: Satu Potongan di Memori",
    language: "Python (pandas)",
    code: "start = time.perf_counter()\npartials, chunk_mb = [], 0\nfor chunk in pd.read_csv(FILE, chunksize=1_000_000,\n                         usecols=workers.USECOLS):\n    mb = chunk.memory_usage(deep=True).sum() / 1e6\n    chunk_mb = max(chunk_mb, mb)\n    partials.append(workers.revenue_by_city(chunk))\nchunked = pd.concat(partials).groupby(level=0).sum()\nchunk_s = time.perf_counter() - start\n\nprint(f\"Jumlah chunk: {len(partials)}\")\nprint(f\"Memori satu chunk: {chunk_mb:,.0f} MB\")\nprint(f\"Waktu baca + agregasi: {chunk_s:.1f} detik\")\nprint(\"equal:\", chunked.sort_index().equals(expected.sort_index()))\nsummary[\"3. Optimasi: chunked\"] = [chunk_mb, chunk_s, \"baca + agregasi\",\n                                 chunked.sum()]",  // sama persis dengan sel notebook langkah 4
    caption: "Expected output: Jumlah chunk: 10, Memori satu chunk: 48 MB, equal: True.",
    notes: "Chunk = potongan saat membaca satu file. Hanya satu chunk di memori pada satu waktu.",
  });

  L.addCodeSlide(pptx, {
    eyebrow: "Hands-on Langkah 5b",
    title: "Partition dan Proses Paralel (Ide Scale Out)",
    language: "Python (multiprocessing)",
    code: "start = time.perf_counter()\nwith Pool(processes=len(files)) as pool:\n    partials = pool.map(workers.revenue_by_city_from_file, files)\nparallel = pd.concat(partials).groupby(level=0).sum()\nparallel_s = time.perf_counter() - start\n\nprint(f\"Jumlah worker: {len(files)}\")\nprint(f\"Waktu: {parallel_s:.1f} detik\")\nprint(f\"Lebih cepat dari partition tanpa paralel: \"\n      f\"{serial_s / parallel_s:.1f}x\")\nprint(\"equal:\", parallel.sort_index().equals(expected.sort_index()))\nsummary[\"5. Scale out: paralel\"] = [part_mb * len(files), parallel_s,\n                                  \"baca + agregasi\", parallel.sum()]",  // sama persis dengan sel notebook langkah 5b
    caption: "Expected output: Jumlah worker sama dengan jumlah partition, equal: True. Waktu berbeda di setiap laptop.",
    notes: "Fungsi worker ada di workers.py, bukan di notebook, supaya multiprocessing jalan di Windows dan macOS. serial_s berasal dari langkah 5a. Di laptop semua worker ada di satu mesin; di sistem big data worker berada di banyak mesin, itulah scale out.",
  });

  L.addLabelRowsSlide(pptx, {
    eyebrow: "Pelajaran dari Langkah 5",
    title: "Partition Harus Sudah Ada Sebelumnya",
    rows: [
      { term: "Chunk", body: "Potongan saat membaca satu file. Dibaca berurutan oleh satu proses." },
      { term: "Partition", body: "Bagian data yang sudah terpisah di file sendiri. Bisa dibaca banyak proses sekaligus." },
      { term: "Biaya membagi", body: "Membagi 10 juta baris jadi partition butuh beberapa menit, lebih lama dari query-nya." },
      { term: "Konsekuensi", body: "Sistem big data menyimpan data dalam bentuk terpartisi sejak awal.", highlight: true },
    ],
    note: "Inilah jembatan ke Sesi 3 - Big Data Storage: bagaimana data disimpan agar bisa diproses paralel.",
    notes: "Itu sebabnya make_data_s02.py dijalankan sebelum sesi. Durasinya berbeda di setiap laptop.",
  });

  // ---------- Bagian 4 ----------
  L.addSectionSlide(pptx, {
    number: 4,
    title: "Batch vs Streaming Sekilas",
    subtitle: "Dua cara data diproses: dikumpulkan dulu, atau diproses saat tiba.",
    items: ["Batch processing", "Streaming", "Jembatan ke Sesi 3, 4, dan 5"],
    notes: "10 menit. Cukup gambaran, detail di Sesi 4 dan 5.",
  });

  L.addTwoPanelSlide(pptx, {
    eyebrow: "Velocity",
    title: "Batch vs Streaming",
    panels: [
      { label: "Batch", title: "Kumpulkan dulu, proses berkala", body: "Data dikumpulkan lalu diproses terjadwal, misal setiap malam. Hands-on hari ini adalah batch.", listLabel: "Dibahas di", items: [
        "Sesi 4 - Batch Processing Framework (Spark)",
        "Sesi 7 - Use Case Implementation: Batch",
      ] },
      { label: "Streaming", title: "Proses saat data tiba", body: "Setiap transaksi diproses beberapa detik setelah terjadi, misal untuk deteksi fraud.", listLabel: "Dibahas di", items: [
        "Sesi 5 - Real-Time Processing Framework",
        "Sesi 8 - Use Case Implementation: Real-Time",
      ] },
    ],
    note: "Sebelum itu, Sesi 3 - Big Data Storage membahas cara menyimpan data besar agar siap diproses.",
    notes: "Jangan masuk ke detail Kafka atau Flink.",
  });

  // ---------- Penutup ----------
  L.addNumberedListSlide(pptx, {
    eyebrow: "Menilai Kasus",
    title: "Tiga Pertanyaan: Perlu Big Data atau Tidak",
    items: [
      { heading: "Apakah data muat di memori satu mesin?", body: "Setelah tipe hemat, kolom seperlunya, atau chunked processing." },
      { heading: "Apakah waktu proses masih masuk akal?", body: "Bandingkan dengan kebutuhan bisnis, misal laporan siap jam 7 pagi." },
      { heading: "Apakah data datang terus-menerus?", body: "Jika harus diproses saat tiba, batch di satu mesin tidak cukup." },
    ],
    quote: "Big data bukan soal angka tertentu, tetapi saat cara klasik tidak lagi cukup.",
    note: "Jika ketiganya masih aman, pendekatan klasik adalah pilihan yang tepat.",
    notes: "Pertanyaan penutup hands-on: kalau datanya 1 miliar baris dan satu laptop tidak cukup, apa yang kamu butuhkan? Arahkan ke penyimpanan terdistribusi, banyak mesin, dan koordinasi.",
  });

  L.addClosingSlide(pptx, {
    title: "Ringkasan Sesi 2",
    points: [
      "5V dan titik patah menentukan big data, bukan satu angka ukuran",
      "Optimasi di mesin yang sama (tipe hemat, chunked) sering cukup dan paling murah",
      "Scale out: bagi data jadi partition, proses paralel, gabungkan hasil parsial",
      "Hasil harus sama di semua cara. Percepatan dibatasi core dan koordinasi",
    ],
    nextStep: "Sesi 3 - Big Data Storage",
    notes: "Recap 10 menit, sisakan waktu untuk tanya jawab.",
  });

  L.addThankYouSlide(pptx, {
    lines: ["Sesi berikutnya: Sesi 3 - Big Data Storage"],
    contact: "Kontak: Fahmi, Mentor Data & AI",
    notes: "Tanya jawab.",
  });

  const out = await L.save(pptx, OUT);
  console.log("written", out);
}

main();
