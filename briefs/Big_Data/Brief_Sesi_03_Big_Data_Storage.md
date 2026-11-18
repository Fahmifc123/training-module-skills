# BRIEF SESI - Big Data

Sesi: 3 - Big Data Storage
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta membandingkan format row-based (CSV) dan kolumnar (Parquet), mencoba partitioning pada data 10 juta baris, lalu memahami posisi data lake, data warehouse, dan lakehouse sebagai tempat data disimpan di skala besar.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage (sesi ini)
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Slide pembuka merujuk dua hal dari sesi sebelumnya: Sesi 1 menunda perbandingan CSV vs Parquet ke sesi ini, dan Sesi 2 menutup dengan pesan "partition harus sudah ada sebelum query". Slide penutup menyebut Sesi 4 "Batch Processing Framework (Spark)", yang akan membaca data Parquet terpartisi.

## Batasan cakupan
- Sesi ini membahas poin 4 outline: penyimpanan untuk big data.
- Tidak ada Spark, PySpark, Dask, dan DuckDB. Hands-on hanya memakai pandas dan pyarrow.
- Tidak ada platform cloud dan tidak ada Databricks. Object storage dan layanan cloud spesifik hanya disebut sekilas sebagai jembatan ke Sesi 9.
- Data lake, data warehouse, dan lakehouse dibahas sebagai konsep dengan slide, tanpa hands-on.
- Table format (misalnya Delta Lake dan Iceberg) hanya disebut sekilas di bagian lakehouse, tanpa kode.
- Paket pilot "Introduction_to_Big_Data" hanya bahan acuan untuk konsep lake, warehouse, lakehouse. Jangan menyalin struktur, hands-on, atau asumsi platform-nya.

## Tujuan belajar (maksimal 4)
1. Menjelaskan perbedaan format row-based (CSV) dan kolumnar (Parquet), dan kapan masing-masing cocok.
2. Menjelaskan partitioning dan manfaatnya: hanya membaca bagian data yang diperlukan.
3. Membedakan data lake, data warehouse, dan lakehouse dari sisi tujuan dan trade-off.
4. Memilih format dan cara menyimpan data untuk sebuah kasus.

## Konsep inti (urutan penyampaian)
1. Masalah penyimpanan di skala besar: ukuran data, biaya membaca, banyak pembaca.
2. Row-based vs kolumnar: cara data tersusun di disk, column pruning, kompresi.
3. Partitioning: satu folder per nilai kolom, partition pruning, dan jebakan terlalu banyak partition (small files).
4. Data lake, data warehouse, lakehouse: tujuan, jenis data, kapan dipakai.
5. Object storage dan file system terdistribusi, sekilas.

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1 dan 2. Pertanyaan bisnis: bagaimana menyimpan 10 juta transaksi supaya kueri tertentu (hanya beberapa kolom, atau hanya satu bulan) tidak perlu membaca semuanya.

Dataset: `retail_transactions_10m.csv` dari Sesi 2 (sintetis, bukan data internal Insignia atau klien; 10.000.000 baris, hasil penggandaan `retail_transactions.csv` seed 42 sebanyak 10 kali dengan akhiran `-0` sampai `-9` pada `transaction_id`). Dibuat oleh `make_data_s02.py` dari Starter Kit Sesi 2. Peserta yang belum punya file ini menjalankan skrip itu sebelum sesi. Notebook Sesi 3 harus memeriksa keberadaan file dan memberi pesan jelas jika belum ada.

Untuk langkah 4 hands-on dipakai 100.000 baris pertama dari `retail_transactions.csv` (Sesi 1). Kolom `product_id` memiliki 5.000 nilai unik, dipakai sebagai contoh kolom dengan kardinalitas terlalu tinggi.

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing. Python 3.12 ke atas, pandas 3.x, pyarrow, dan numpy. Versi Python minimum mengikuti Sesi 1 dan 2 (pandas 3.0.5 dan numpy 2.5.4 tidak terpasang di Python 3.10 dan 3.11). Tidak ada cloud, Docker, Spark, atau DuckDB.
- `requirements.txt` harus memuat pyarrow dengan versi yang dipin, dan Starter Kit memuat sel verifikasi versi.
- Angka checkpoint diverifikasi di sandbox pengujian (Python 3.13, pandas 3.0.5, pyarrow 26.0.1, mesin 2 core, RAM 7 GB) dan lewat eksekusi notebook pada build Claude Code (11 November 2026), dengan hasil sama. Bila versi pustaka diubah, jalankan ulang notebook dan perbarui checkpoint.
- Ruang disk kosong minimal 3 GB (CSV 945 MB, Parquet sekitar 166 MB, versi terpartisi sekitar 216 MB, ditambah file kerja).

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 2, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.08 | Row-based vs kolumnar | Konsep | 28 mnt |
| 14.08 - 14.25 | Partitioning | Konsep | 17 mnt |
| 14.25 - 15.05 | Hands-on: simpan, baca, partisi | Hands-on | 40 mnt |
| 15.05 - 15.20 | Data lake, warehouse, lakehouse, object storage sekilas | Konsep | 15 mnt |
| 15.20 - 15.30 | Recap dan jembatan ke Sesi 4 | Penutup | 10 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 (Konsep +5 menit, hands-on -5 menit, total tetap 120) karena penambahan tiga slide penjelasan mekanisme (struktur Parquet, alasan ukuran Parquet kecil, small files); perkiraan menit per langkah hands-on di bawah dipadatkan ke 40 menit.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah oleh CK/TD; perubahan +5 menit hanya untuk slide penjelasan mekanisme (lihat catatan di atas).

## Rancangan hands-on
Satu notebook, satu dataset, empat percobaan penyimpanan. Angka waktu di bawah dari mesin 2 core dan bervariasi antar laptop dan disk, jadi tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key. Ukuran file dan jumlah baris relatif stabil, tetapi tetap dilaporkan sebagai "sekitar".

| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: versi library, file data ada, path hasil didefinisikan. Tidak memuat data (cepat, aman diulang setelah Restart Kernel) | 2 | versi library; File 10m 945-955 MB (tergantung OS) |
| 1. Baca `retail_transactions_10m.csv` per chunk 1 juta baris (pola Sesi 2), tulis tiap chunk ke CSV dan Parquet (`pyarrow.parquet.ParquetWriter`), bandingkan ukuran file | 10 | 10.000.000 baris; CSV sekitar 945 MB; Parquet sekitar 166 MB (sekitar 5,7 kali lebih kecil); tulis CSV sekitar 30 detik vs Parquet sekitar 6 detik (bervariasi) |
| 2. Column pruning: baca hanya `quantity` dan `unit_price` dari CSV dan Parquet, hitung total quantity x unit_price | 8 | total 36.364.051.240.000 (semua status) di kedua cara; baca 2 kolom dari CSV sekitar 4 detik vs Parquet sekitar 0,1 detik; baca seluruh Parquet sekitar 1 detik (bervariasi) |
| 3a. Partitioning per bulan: baca Parquet per batch 1 juta baris (`iter_batches`), tambah kolom `month`, tulis tiap batch dengan `partition_cols=["month"]`. 3b. Baca hanya Maret 2025 dengan `filters`; pembanding: file tanpa partisi, baca kolom `transaction_ts` saja dari 10 juta baris lalu filter | 12 | 12 folder `month=2025-01` sampai `month=2025-12`; ukuran total sekitar 216 MB; dengan filters membaca 844.330 baris, pembanding membaca 10.000.000 baris; Maret 844.330 baris di kedua cara. Tekankan jumlah baris yang dibaca, bukan detik (selisihnya kecil, sekitar 0,07 vs 0,2 detik) |
| 4. Terlalu banyak partition: simpan 100.000 baris dengan `partition_cols=["product_id"]` | 5 | belasan ribu file (acuan sekitar 14.000) dan ukuran total sekitar 93 MB, dibanding sekitar 1,9 MB untuk satu file Parquet berisi data yang sama; rata-rata sekitar 7 KB per file |
| 5. Tabel keputusan: format dan partisi mana untuk kasus apa | 3 | tabel terisi, peserta bisa memilih untuk 3 kasus yang diberikan |

Menit per langkah diselaraskan dengan hands-on 40 menit (12 November 2026): Langkah 0 dari 5 menjadi 2, Langkah 4 dari 7 menjadi 5.

Pesan yang harus muncul dari langkah 4: partition pada kolom dengan kardinalitas tinggi menghasilkan banyak file kecil, ukuran total membengkak puluhan kali, dan metadata tiap file menjadi beban. Pilih kolom dengan nilai unik sedikit yang sering dipakai untuk filter (misalnya bulan).

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Langkah 4 wajib memakai `max_partitions` (misalnya 10000) pada `to_parquet`. Tanpa itu pyarrow menolak dengan `ArrowInvalid: Fragment would be written into 4996 partitions. This exceeds the maximum of 1024`. Sebut galat ini di Catatan Trainer sebagai pengaman bawaan dan jelaskan kenapa batasnya ada.
- Langkah 4 hanya boleh memakai 100.000 baris. Percobaan dengan 1 juta baris menghasilkan ratusan ribu file, ukuran sekitar 900 MB, dan waktu tulis lebih dari 6 menit, sedangkan 10 juta baris membuat proses kehabisan memori pada mesin 7 GB.
- Untuk perbandingan di langkah 3, jangan memfilter bulan dengan `strftime` pada 10 juta baris karena sangat lambat dan tidak adil sebagai pembanding. Bandingkan dengan membaca seluruh Parquet lalu memfilter memakai rentang `transaction_ts`.
- Langkah 3 dan 4 membuat banyak file. Notebook harus menghapus folder hasil lama sebelum menulis ulang agar sel bisa dijalankan berulang.
- Jangan menambahkan Spark, Dask, atau DuckDB.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S3-CK1 | Row-based vs columnar | Column pruning: total revenue hanya butuh 2 dari 10 kolom (`quantity`, `unit_price`). CSV: seluruh file 945 MB harus dibaca; Parquet: 2 kolom dari file 166 MB (sekitar 5,7 kali lebih kecil). Hasil sama: 36.364.051.240.000 (semua status) | Langkah 1 dan 2 | `addBeforeAfterSlide` |
| S3-CK2 | Partition pruning | Filter bulan Maret pada tabel yang dipartisi per bulan: 844.330 baris dibaca (8,4% dari 10.000.000); tanpa partisi 10.000.000 baris dibaca. Folder: 12 (`month=2025-01` sampai `month=2025-12`), total 216 MB | Langkah 3a dan 3b | `addBeforeAfterSlide` |
| S3-CK3 | Memilih kolom partisi | Kolom `month` (12 folder, sekitar 18 MB per folder) vs `product_id` (5.000 nilai unik pada 100.000 baris): belasan ribu file (acuan 14.230), rata-rata 6,5 KB per file, total 92,9 MB. Cardinality tinggi menghasilkan small files | Langkah 3a dan 4 | `addComparisonTableSlide` |
| S3-TD1 | Format file | Tebak: Parquet berapa kali lebih kecil dari CSV untuk data yang sama? Jawaban: sekitar 5,7 kali (945 MB vs 166 MB; 5,8 kali di Windows) | Langkah 1 | `addTwoPanelSlide`, `addStatSlide` |
| S3-TD2 | Partition pruning | Tebak: berapa baris yang dibaca untuk filter Maret pada tabel berpartisi? Jawaban: 844.330, bukan 10.000.000 | Langkah 3b | `addTwoPanelSlide`, `addStatSlide` |
| S3-TD3 | Kolom partisi | Tebak: bila 100.000 baris dipartisi per `product_id` (5.000 nilai unik), berapa file yang terbentuk? Jawaban: belasan ribu (acuan 14.230), rata-rata 6,5 KB | Langkah 4 | `addTwoPanelSlide`, `addStatSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 3 ditandai)
- Row-based vs kolumnar: `addSectionSlide`, `addBeforeAfterSlide` (data tersusun per baris vs per kolom, dan akibatnya pada kueri yang hanya butuh dua kolom), `addComparisonTableSlide` (CSV vs Parquet: susunan, ukuran, kecepatan baca, dapat dibaca manusia, cocok untuk), `addStatSlide` (angka hasil hands-on: sekitar 945 MB vs sekitar 166 MB; sumber: hasil hands-on dataset sintetis)
- Partitioning: `addSectionSlide`, `addTwoPanelSlide` (struktur folder `month=...` dan kode `partition_cols`), `addLabelRowsSlide` (partition pruning, kardinalitas, small files, memilih kolom partisi)
- Hands-on: `addSectionSlide`, `addStepsCheckpointSlide` (langkah 1-3 lalu langkah 4-5), `addCodeSlide` (maks 18 baris: langkah 1 menyimpan dan langkah 3 partisi), `addChecklistSlide` (verifikasi environment dan file data sebelum mulai)
- Lake, warehouse, lakehouse: `addSectionSlide`, `addComparisonTableSlide` (tiga pendekatan: tujuan, jenis data, struktur, kekuatan, kelemahan), `addNumberedListSlide` (object storage dan file system terdistribusi sekilas, serta table format sekilas)
- Penutup: `addClosingSlide` (ringkasan dan Sesi 4 Batch Processing Framework (Spark)), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Cara menyimpan data menentukan cara memprosesnya. Format kolumnar dan partition membuat kueri hanya membaca yang perlu.
- Parquet bukan jawaban untuk semuanya. CSV tetap cocok untuk data kecil, pertukaran sederhana, dan data yang perlu dibaca manusia.
- Partition menolong bila kolomnya dipilih dengan benar. Terlalu banyak partition membuat penyimpanan lebih buruk, bukan lebih baik.
- Data lake, warehouse, dan lakehouse bukan produk tertentu, melainkan pendekatan dengan tujuan berbeda.

Pertanyaan yang kemungkinan muncul:
- "Kenapa Parquet lebih kecil?" Jawab: data disusun per kolom sehingga nilai sejenis berdekatan dan lebih mudah dikompres, dan tipe data disimpan apa adanya.
- "Kenapa tulisnya Parquet lebih cepat padahal ada kompresi?" Jawab: file yang ditulis jauh lebih kecil dan tidak ada konversi angka ke teks.
- "Apakah selalu pakai Parquet?" Jawab: tidak, lihat tabel keputusan.
- "Apa bedanya lakehouse dengan lake?" Jawab: lakehouse menambahkan layer pengelolaan tabel (transaksi dan skema) di atas file di lake. Detail produknya di luar sesi ini.
- "Kenapa muncul galat tentang 1024 partitions?" Jawab: itu batas pengaman pyarrow terhadap partisi yang terlalu banyak. Itu sebabnya langkah 4 perlu `max_partitions`.

## Risiko teknis dan hal yang dicek sebelum sesi
- File dan folder yang dihasilkan banyak. Langkah 4 menghasilkan belasan ribu file kecil dan bisa lambat dihapus di Windows (sekitar 14.000 file). Sediakan sel pembersihan, dan peringatkan peserta agar tidak membuka folder itu di file explorer.
- Waktu tulis langkah 4 sekitar 17 detik pada mesin acuan dan bisa jauh lebih lama pada laptop dengan disk lambat atau antivirus aktif. Beri tahu peserta bahwa sel itu wajar lama.
- Perilaku partisi di pyarrow dapat berbeda antar versi (jumlah file yang dihasilkan). Jangan menjadikan jumlah file persis sebagai kriteria berhasil. Gunakan "belasan ribu".
- RAM 8 GB: langkah 1 per chunk dan langkah 3a per batch, jadi 10 juta baris tidak pernah dimuat sekaligus. Puncak memori proses terukur: langkah 0 0,1 GB; langkah 1 0,7 GB; langkah 2 2,5 GB (sengaja membaca seluruh Parquet sebagai pembanding); langkah 3a 1,3 GB; langkah 3b 1,4 GB. Hapus variabel yang tidak dipakai (`del`) antar langkah.
- Peserta yang melewatkan Sesi 2 belum punya `retail_transactions_10m.csv`. Siapkan `make_data_s02.py` dan instruksinya di README Setup, dengan opsi `--tanpa-parts` (tidak membuat folder `parts/` yang hanya dipakai Sesi 2).
- Angka waktu bervariasi antar mesin. Hanya nilai hasil (jumlah baris, total, jumlah folder) yang boleh dijadikan checkpoint.
- Rujukan lintas sesi: chunk diperkenalkan di Sesi 2 langkah 4 (bukan Sesi 1). Contoh isi data lake boleh memakai data non-tabular Sesi 1 (`orders_app.json`, `reviews.csv`, `product_images/`).
- Latihan Mandiri yang mempartisi 10 juta baris memakai pola per batch dari langkah 3a.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `1,575 MB`, `900347`, `0.28`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(1.575 MB)", "(3,27 triliun)", "(28%)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Istilah yang harus konsisten di semua file
- row-based, columnar
- Parquet, CSV
- column pruning, partition pruning
- partitioning, partition, `partition_cols`
- cardinality, small files
- data lake, data warehouse, lakehouse
- object storage, distributed file system, table format
- transaksi COMPLETED; revenue = quantity x unit_price (di langkah 2 total dihitung untuk semua status, sebut ini eksplisit)
- chunk (potongan saat membaca satu file) vs partition (bagian data yang disimpan terpisah)
- Nama dataset: `retail_transactions.csv` (Sesi 1), `retail_transactions_10m.csv` (Sesi 2 dan 3)
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 3 dibangun dan notebook dijalankan dengan pandas 3.0.5 dan pyarrow 26.0.1; angka checkpoint sama dengan Brief.
- Langkah 4 hanya memakai 100.000 baris: percobaan 1 juta baris menghasilkan ratusan ribu file, dan 10 juta baris membuat proses kehabisan memori pada mesin 7 GB. Galat `ArrowInvalid: Fragment would be written into 4996 partitions` muncul bila `max_partitions` terhapus dari sel.
- Ukuran CSV 945 MB di Linux dan macOS, 955 MB di Windows (akhir baris CRLF); rasio 5,7 dan 5,8 kali. Jumlah file langkah 4 bervariasi (acuan 14.230); kriteria "belasan ribu".
- Belum diuji: langkah 4 di laptop Windows (menulis dan menghapus sekitar 14.000 file bisa lambat).

## Keputusan terbuka
1. Teks asli poin 4 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi, janji dari Sesi 1 dan 2, dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Draf outline memakai usulan awal: hanya pandas dan pyarrow, lake/warehouse/lakehouse hanya konsep, table format sekilas. Belum ada jawaban eksplisit. Konfirmasi atau koreksi.
3. Langkah 4 (sekitar 14.000 file) di laptop Windows belum diuji.
4. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
