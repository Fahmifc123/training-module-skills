# BRIEF SESI - Big Data

Sesi: 4 - Batch Processing Framework (Spark)
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta melihat bagaimana Spark mengerjakan otomatis hal yang di Sesi 2 ditulis manual (bagi data, proses paralel, gabungkan hasil), lalu menjalankan query yang sama dengan DataFrame API dan Spark SQL pada Parquet terpartisi dari Sesi 3 dan membaca plan-nya.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark) (sesi ini)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk tiga sesi sebelumnya: Sesi 1 (dataframe dan SQL), Sesi 2 (bagi, paralel, gabung yang ditulis manual dengan `multiprocessing`), dan Sesi 3 (Parquet terpartisi per bulan). Slide penutup menyebut Sesi 5 sebagai "Real-Time Processing Framework (Kafka/Flink)".

## Batasan cakupan
- Sesi ini membahas poin 5 outline: batch processing framework dengan Spark.
- Konsep inti yang dibawakan: arsitektur (driver, executor, partition), lazy evaluation (transformation vs action, plan), serta DataFrame API dan Spark SQL berdampingan. Keputusan ini diambil bersama Fahmi (5 November 2026).
- Shuffle, join, dan skew hanya disebut satu kalimat sebagai penyebab utama job lambat. Tanpa hands-on.
- Spark UI hanya disebut sekilas (alamat lokalnya), tanpa langkah hands-on.
- Spark dijalankan dalam mode lokal. Executor berjalan di satu laptop, jadi ini bukan cluster sungguhan. Sebut ini jujur di slide dan di kelas.
- Tidak ada Databricks, platform cloud, Docker, Kafka, atau Flink. Platform cloud di Sesi 9, streaming di Sesi 5.
- Tidak ada Structured Streaming, MLlib, dan pandas API on Spark. Jangan memakai `toPandas()` di notebook (lihat bagian Risiko).
- Paket pilot "Introduction_to_Big_Data" hanya bahan acuan konsep. Jangan menyalin struktur, hands-on (Pandas vs PySpark), dan asumsi platform-nya.
- Peserta tidak diasumsikan pernah memakai Spark atau Databricks.

## Tujuan belajar (maksimal 4)
1. Menjelaskan arsitektur Spark: driver, executor, partition.
2. Membedakan transformation dan action, dan membaca plan lewat `explain()`.
3. Menulis query yang sama dengan DataFrame API dan Spark SQL, dengan hasil yang sama.
4. Menjelaskan bagaimana Spark membaca Parquet terpartisi dan kapan partition pruning terjadi.

## Konsep inti (urutan penyampaian)
1. Dari manual ke Spark: bagi data, proses paralel, gabungkan hasil (Sesi 2) dikerjakan Spark secara otomatis.
2. Arsitektur: driver (menyusun dan mengoordinasi), executor (mengerjakan), partition (potongan data yang dikerjakan satu task). Mode lokal: executor di laptop yang sama.
3. Lazy evaluation: transformation hanya menyusun plan, action memicu eksekusi. Plan dibaca dengan `explain()`.
4. DataFrame API dan Spark SQL: dua cara menulis query yang sama, satu mesin eksekusi (seperti pandas dan SQL di Sesi 1, tetapi di sini hasilnya tidak hanya sama, rencananya pun sama).
5. Membaca Parquet terpartisi: partition pruning pada kolom partisi (`month`), menyambung ke Sesi 3.

## Use case dan dataset
Use case: lanjutan laporan penjualan retail Sesi 1-3. Pertanyaan bisnis tetap sama (revenue transaksi COMPLETED per kota) pada data 10 juta baris, supaya hasilnya bisa dicocokkan dengan angka acuan Sesi 2 dan 3.

Dataset: folder Parquet terpartisi per bulan hasil Sesi 3 (langkah 3a): 10.000.000 baris, 12 folder `month=2025-01` sampai `month=2025-12`, sintetis (bukan data internal Insignia atau klien), turunan `retail_transactions.csv` seed 42 digandakan 10 kali. Nama folder mengikuti notebook Sesi 3 (Claude Code mengambil nama dari paket Sesi 3, jangan menebak). Kolom `month` ada di path folder, bukan di isi file, dan terbaca sebagai kolom oleh Spark.

Peserta yang belum punya folder ini menjalankan `make_data_s02.py --tanpa-parts` (Sesi 2) lalu sel pembuat partisi per bulan dari Sesi 3 langkah 3a. Starter Kit Sesi 4 harus menyertakan skrip fallback yang melakukan keduanya dan README Setup menjelaskannya. Langkah 0 notebook harus memeriksa keberadaan folder dan memberi pesan jelas jika belum ada.

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing, PySpark mode lokal. Keputusan ini diambil bersama Fahmi (5 November 2026) dan konsisten dengan Sesi 1-3.
- Python 3.12 ke atas, Java 17 atau lebih baru dengan `JAVA_HOME` terpasang (diuji dengan Java 21), pandas, numpy, pyarrow, dan PySpark.
- `requirements.txt` memuat versi yang dipin: `pyspark==4.3.0` ditambah `pandas==3.0.5`, `numpy==2.5.4`, `pyarrow==26.0.1`. Periksa ulang versi PySpark yang masih terbaru sebelum paket dibuat dan laporkan jika ada versi stabil yang lebih baru.
- Instalasi PySpark besar (sekitar 456 MB diunduh, sekitar 482 MB setelah terpasang). Peserta memasangnya sebelum hari sesi, bukan di kelas. Sebutkan ukuran dan ruang disk di README Setup.
- Java bukan bagian dari `pip`. README Setup harus memuat cara memasang dan memeriksa Java (`java -version`) dan `JAVA_HOME` untuk Windows, macOS, dan Linux. Halaman instalasi resmi Spark tidak memberi instruksi khusus Windows, jadi bagian Windows harus diuji (lihat Risiko).
- Angka checkpoint diverifikasi di sandbox pengujian (Python 3.13, Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1, mesin 2 core, RAM 7 GB) dan lewat eksekusi notebook pada build Claude Code (11 November 2026), dengan hasil sama.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 3, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.03 | Arsitektur Spark | Konsep | 23 mnt |
| 14.03 - 14.20 | Lazy evaluation, transformation vs action, plan | Konsep | 17 mnt |
| 14.20 - 14.30 | DataFrame API dan Spark SQL | Konsep | 10 mnt |
| 14.30 - 15.10 | Hands-on: Spark pada Parquet terpartisi | Hands-on | 40 mnt |
| 15.10 - 15.20 | Kapan Spark, kapan tidak; jembatan ke Sesi 5 | Konsep | 10 mnt |
| 15.20 - 15.30 | Recap dan tanya jawab | Penutup | 10 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 (keputusan Fahmi) karena penambahan slide penjelasan mekanisme: Konsep +5 menit (Arsitektur 20 -> 23, Lazy evaluation 15 -> 17), hands-on 45 -> 40 menit, total tetap 120 menit.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, satu pertanyaan bisnis (revenue COMPLETED per kota), dijawab dengan Spark. Langkah 0 (verifikasi Java, PySpark, folder data) dikerjakan sebelum sesi. Angka waktu di bawah dari mesin 2 core dan bervariasi antar laptop, jadi tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key. Tulis angka checkpoint persis seperti output notebook.

| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 1. Mulai `SparkSession` mode lokal (`local[*]`), cek versi dan jumlah core yang dipakai | 4 | versi Spark 4.3.0; core terpakai sesuai laptop (acuan: 2) |
| 2. Baca folder Parquet terpartisi: `printSchema`, daftar kolom, jumlah partition Spark, jumlah baris | 6 | kolom 11 termasuk `month`; jumlah baris 10000000 (10.000.000); jumlah partition Spark 3 pada acuan (bergantung ukuran file dan core, bukan 12) |
| 3. Lazy: susun filter COMPLETED dan kolom `revenue`, ukur waktunya, lalu picu dengan `count()` | 6 | menyusun transformation sekitar 0,1 detik (belum ada data dibaca); action `count` menghasilkan 9003470 (9.003.470) |
| 4. DataFrame API: revenue per kota dengan `groupBy` dan `agg` | 6 | 8 kota; kota teratas Jakarta 9181176340000 (9.181.176.340.000); total 32737599110000 (32.737.599.110.000), `equal` True terhadap acuan Sesi 2 dan 3 |
| 5. Spark SQL: `createOrReplaceTempView`, query yang sama | 5 | hasil sama dengan langkah 4 (`equal` True) |
| 6. Partition pruning: filter `month == "2025-03"`, baca `explain()`, hitung baris | 8 | plan memuat `PartitionFilters` dengan `month = 2025-03` (nomor kolom seperti `#10` bisa berbeda); 844330 (844.330) baris; pembanding: filter memakai rentang `transaction_ts` tetap menghasilkan 844330 baris tetapi plan tidak punya `PartitionFilters`, hanya `PushedFilters` |
| 7. Pembanding pandas: baca Parquet yang sama dengan pandas, hitung total yang sama | 3 | total pandas 32737599110000, sama dengan Spark; Spark tidak lebih cepat di data sekecil ini (acuan: pandas sekitar 1,5 detik, Spark pertama sekitar 3,7 detik) |
| 8. Tabel keputusan: kapan Spark, kapan pandas, kapan sistem lain | 2 | tabel terisi, peserta bisa memilih untuk 3 kasus yang diberikan |

Menit per langkah diselaraskan dengan hands-on 40 menit (12 November 2026): Langkah 7 dari 5 menjadi 3, Langkah 8 dari 5 menjadi 2.

Angka waktu acuan lain (bervariasi): `count` 10 juta baris sekitar 1,6 detik; query SQL sekitar 2,3 detik; hitung Maret dengan pruning sekitar 0,15 detik vs filter `transaction_ts` sekitar 1,05 detik. Tekankan baris yang dibaca dan isi plan, bukan detik.

Pesan yang harus muncul dari langkah 3: transformation selesai dalam sekejap karena belum ada data yang dibaca. Biaya sebenarnya muncul saat action. Itu sebabnya `explain()` berguna sebelum menjalankan job besar.

Pesan yang harus muncul dari langkah 6: Spark hanya membaca folder bulan yang diminta karena `month` adalah kolom partisi. Pada filter `transaction_ts`, Spark masih harus membuka file lalu menyaring di dalamnya. Ini hasil langsung dari keputusan menyimpan data per bulan di Sesi 3.

Pesan yang harus muncul dari langkah 7: Spark bukan otomatis lebih cepat. Pada 10 juta baris di satu laptop, overhead start-up dan koordinasi membuatnya tidak lebih cepat dari pandas. Spark berguna saat data atau jumlah mesin membesar.

Pertanyaan penutup hands-on: "Kalau datanya 1 miliar baris dan ada 50 mesin, bagian mana dari notebook ini yang berubah, dan bagian mana yang sama?" Jawaban diarahkan ke: query sama, tempat jalannya berbeda.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Jangan memakai `toPandas()` dan jangan memakai `pyspark.pandas`. PySpark 4.3.0 menampilkan `FutureWarning: PySpark does not yet fully support pandas >= 3.0.0` saat SparkSession dibuat. Notebook menyembunyikan peringatan ini di sel setup (`warnings.filterwarnings`) dan README Setup serta Catatan Trainer menjelaskan alasannya. Hasil langkah 4 diambil dengan `collect()`.
- Langkah 7 membaca Parquet dengan pandas hanya sebagai pembanding. Hapus variabel besar dengan `del` sesudahnya.
- Tangkap keluaran `explain()` dengan `contextlib.redirect_stdout` atau tampilkan langsung. Di slide dan modul, kutip hanya baris yang memuat `PartitionFilters`, bukan seluruh plan.
- Notebook menutup sesi dengan `spark.stop()` di sel terakhir, dan Langkah 0 aman dijalankan ulang setelah Restart Kernel.
- Jangan menetapkan konfigurasi memori Spark di notebook kecuali terbukti perlu. Jika perlu, jelaskan alasannya di Catatan Trainer.
- Uji notebook lewat eksekusi sebagai notebook (bukan hanya skrip), dan laporkan hasilnya.
- Jangan menambahkan Databricks, Docker, atau streaming.
- Slide 5V dan sejenisnya tidak dipakai di sesi ini. Rujukan balik: Sesi 2 (6 detik vs 12 detik, partisi manual dengan `multiprocessing`) dan Sesi 3 (12 folder bulan).
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `9003470`, `844330`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(9.003.470)", "(32,7 triliun)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S4-CK1 | Arsitektur Spark | Satu query dari folder ke task: 12 folder `month=` dibaca menjadi Spark partition (acuan 3 pada mesin 2 core, 12 pada laptop 12 core; bukan checkpoint), dijalankan sebagai task di executor lokal; driver menyusun plan dan mengumpulkan hasil: total revenue 32.737.599.110.000 | Langkah 2 dan 4 | `addLabelRowsSlide` |
| S4-CK2 | Lazy evaluation | Tiga baris dari sel Langkah 3: dua transformation (`filter`, `withColumn`) tidak membaca data; `count()` (action) memicu eksekusi dan mengembalikan 9.003.470 baris COMPLETED. Kutip kode dari notebook | Langkah 3 | `addCodeSlide` (maks 8 baris) |
| S4-CK3 | Membaca plan | Dua plan untuk hasil yang sama (844.330 baris Maret): filter pada kolom `month` memuat `PartitionFilters: [isnotnull(month), (month = 2025-03)]`; filter pada `transaction_ts` memuat `PartitionFilters: []` dan `PushedFilters` | Langkah 6 | `addComparisonTableSlide` |
| S4-TD1 | Lazy evaluation | Tebak: setelah baris `.filter(...)` dijalankan, berapa baris sudah dibaca? Jawaban: belum ada; angka 9.003.470 baru muncul setelah `count()` | Langkah 3 | `addTwoPanelSlide`, `addBeforeAfterSlide` |
| S4-TD2 | Partition pruning | Tebak: filter `month = '2025-03'` vs filter `transaction_ts` di bulan Maret: hasil dan plan sama atau beda? Jawaban: baris sama (844.330), plan beda | Langkah 6 | `addTwoPanelSlide`, `addComparisonTableSlide` |
| S4-TD3 | Spark atau pandas | Tiga kasus: laporan harian 2 juta baris yang muat di laptop; laporan harian 5 miliar baris di banyak mesin; dashboard yang diperbarui tiap detik. Jawaban per Answer Key: pandas, Spark, sistem streaming (Sesi 5) | Langkah 8 | `addTwoPanelSlide`, `addComparisonTableSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 4 ditandai)
- Arsitektur Spark: `addSectionSlide`, `addComparisonTableSlide` (yang ditulis manual di Sesi 2 vs yang dikerjakan Spark: bagi data, proses paralel, gabungkan hasil, koordinasi), `addTwoPanelSlide` (driver dan executor, dengan catatan mode lokal), `addLabelRowsSlide` (driver, executor, partition, task)
- Lazy evaluation: `addSectionSlide`, `addBeforeAfterSlide` (transformation vs action: apa yang berjalan dan kapan), `addCodeSlide` (maks 18 baris: langkah 3), `addStatSlide` (menyusun transformation sekitar 0,1 detik vs action; sumber: hasil hands-on)
- DataFrame API dan Spark SQL: `addTwoPanelSlide` (query yang sama dalam dua gaya, kode di panel), `addComparisonTableSlide` (filter, group by, agregasi: DataFrame API, Spark SQL, pandas)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi Java, PySpark, dan folder data sebelum mulai), `addStepsCheckpointSlide` (langkah 1-4, lalu langkah 5-8), `addCodeSlide` (maks 18 baris: langkah 6 partition pruning)
- Penutup: `addNumberedListSlide` (tiga pertanyaan untuk memilih Spark atau pandas), `addClosingSlide` (ringkasan dan Sesi 5 Real-Time Processing Framework (Kafka/Flink)), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Spark mengerjakan otomatis ide yang sudah dikenal dari Sesi 2: bagi data, proses paralel, gabungkan hasil.
- Spark itu lazy: transformation hanya menyusun rencana, action menjalankannya. Membaca plan adalah keterampilan inti.
- Query sama bisa ditulis dengan DataFrame API atau Spark SQL, dan menghasilkan plan yang sama.
- Partition pruning bekerja karena data disimpan per bulan di Sesi 3. Penyimpanan dan pemrosesan saling bergantung.
- Mode lokal mengajarkan cara kerja Spark, bukan kecepatan cluster.

Pertanyaan yang kemungkinan muncul:
- "Kenapa Spark lebih lambat dari pandas di sini?" Jawab: data 10 juta baris muat di satu laptop, jadi overhead start-up dan koordinasi lebih besar dari manfaatnya. Spark unggul saat data atau jumlah mesin membesar.
- "Kenapa jumlah partition 3 padahal ada 12 folder bulan?" Jawab: partition Spark adalah potongan kerja yang dibentuk Spark berdasarkan ukuran file dan core, berbeda dari folder partisi di disk. Lihat bagian istilah.
- "Kenapa menyusun transformation hanya sekejap?" Jawab: lazy evaluation, belum ada data yang dibaca.
- "Apa bedanya Spark SQL dengan SQLite di Sesi 1?" Jawab: SQLite berjalan di satu proses di satu mesin. Spark SQL memakai mesin eksekusi Spark yang bisa membagi pekerjaan ke banyak executor.
- "Kenapa harus Java?" Jawab: Spark berjalan di JVM, PySpark hanya antarmuka Python-nya.
- "Apakah Spark UI bisa dilihat?" Jawab: ya, di alamat lokal yang tercetak saat sesi dimulai. Hanya disebut sekilas di sesi ini.

## Risiko teknis dan hal yang dicek sebelum sesi
- Java: sumber masalah instalasi terbesar. Peserta tanpa Java 17+ atau tanpa `JAVA_HOME` melihat galat saat SparkSession dibuat. README Setup memuat langkah verifikasi `java -version` dan pesan galat yang umum. Trainer menguji ini sebelum sesi.
- Windows asli: membaca Parquet diperkirakan berjalan (Sesi 4 tidak terkena galat penulisan Parquet yang muncul di Sesi 6), tetapi bagian Windows di README belum diuji di laptop Windows peserta; uji saat gladi. Sebagian laptop Windows memblokir `pyarrow` (Smart App Control); peserta itu memakai WSL Ubuntu sesuai README Sesi 1.
- Ukuran unduhan: PySpark sekitar 456 MB. Bagikan lewat folder bersama atau pastikan peserta memasangnya sebelum hari sesi.
- Memori: puncak memori proses terbesar (JVM) terukur sekitar 2,0 GB pada mesin acuan (pengukuran sampling, bukan total). Cukup untuk laptop 8 GB. Jika kernel mati: Restart Kernel, jalankan Langkah 0, lanjut dari langkah 1. Jangan menetapkan konfigurasi memori Spark kecuali terbukti perlu.
- Peringatan `FutureWarning` PySpark terhadap pandas 3.x: hanya peringatan. Notebook menyembunyikannya, dan `toPandas()` tidak dipakai karena dukungan penuh pandas 3 belum dijamin PySpark.
- Peringatan Spark di konsol tentang hostname atau `NativeCodeLoader` tidak berbahaya. Jika SparkSession gagal terkait alamat, atur `SPARK_LOCAL_IP`. Catat di README Setup.
- Start-up pertama lebih lama (JVM dan SparkSession): beri tahu peserta bahwa sel pertama wajar lambat.
- Peserta yang melewatkan Sesi 3 belum punya folder Parquet terpartisi. Siapkan skrip fallback dan instruksinya di README Setup.
- Perilaku jumlah partition Spark dapat berbeda antar versi dan antar laptop. Jangan menjadikan angka 3 sebagai kriteria berhasil.
- Angka waktu bervariasi antar mesin. Hanya nilai hasil (jumlah baris, total, hasil sama) yang boleh dijadikan checkpoint.

## Istilah yang harus konsisten di semua file
- Spark, PySpark, local mode (bukan "cluster" untuk setup peserta)
- driver, executor, task
- partition, dengan tiga makna yang harus dibedakan eksplisit di slide dan Catatan Trainer:
  - folder partisi di disk (Sesi 3: `month=2025-03`) = "folder partisi"
  - potongan kerja Spark di memori (jumlah partition Spark) = "Spark partition"
  - bagian file yang diproses worker `multiprocessing` (Sesi 2: `parts/`) = "partition" di Sesi 2
- chunk (potongan saat membaca satu file di Sesi 2) tidak dipakai di Spark
- lazy evaluation, transformation, action, plan, `explain()`
- DataFrame API, Spark SQL, `createOrReplaceTempView`
- partition pruning, `PartitionFilters`, `PushedFilters`
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama dataset: folder Parquet terpartisi per bulan dari Sesi 3 (nama mengikuti paket Sesi 3), `retail_transactions.csv` (Sesi 1), `retail_transactions_10m.csv` (Sesi 2 dan 3)
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 4 dibangun dan notebook dijalankan dengan Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1; angka checkpoint sama dengan Brief.
- Jumlah Spark partition bervariasi (3 pada acuan 2 core, 12 pada laptop 12 core) dan bukan checkpoint. Notebook tidak menetapkan konfigurasi memori Spark karena tidak terbukti perlu.
- Windows asli tidak terkena galat penulisan Parquet yang muncul di Sesi 6 karena Sesi 4 hanya membaca Parquet; bagian Windows di README belum diuji di laptop Windows peserta. Peserta yang memakai WSL2 dari Sesi 5 dianjurkan memakainya juga di sini.
- Peserta yang diblokir Smart App Control memakai WSL Ubuntu dan memasang Java di dalamnya.

## Keputusan terbuka
1. Teks asli poin 5 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi dan keputusan bersama Fahmi. Cocokkan sebelum finalisasi paket.
2. Bagian Windows di README Setup belum diuji di laptop Windows peserta; hasilnya menentukan isi README.
3. Laptop RAM 8 GB sungguhan belum diuji.
4. Versi PySpark yang dipin perlu diperiksa ulang menjelang sesi.
5. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
