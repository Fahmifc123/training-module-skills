# BRIEF SESI - Big Data

Sesi: 2 - Common vs Big Data
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta belajar membedakan data biasa dan big data lewat 5V dan angka nyata, lalu menaiki tangga solusi di satu laptop (optimasi di mesin yang sama: tipe data hemat dan chunked processing; lalu ide scale out: partition paralel) untuk memahami ide dasar distributed processing sebelum Spark di Sesi 4.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data (sesi ini)
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Slide pembuka merujuk Sesi 1 (batas satu mesin). Slide penutup menyebut Sesi 3 "Big Data Storage".

## Batasan cakupan
- Sesi ini membahas poin 3 outline: perbedaan data biasa dan big data.
- Tidak ada Spark, PySpark, Dask, Kafka, atau Flink di sesi ini. Spark di Sesi 4, Kafka/Flink di Sesi 5.
- Tidak membahas format file kolumnar (Parquet) dan arsitektur lake/warehouse/lakehouse. Itu wilayah Sesi 3.
- Tidak ada platform cloud dan tidak ada Databricks. Platform cloud dibahas di Sesi 9.
- Paket pilot "Introduction_to_Big_Data" hanya bahan acuan untuk konsep 5V dan scale up vs scale out. Jangan menyalin struktur, hands-on (Pandas vs PySpark), dan asumsi platform-nya.
- Peserta tidak diasumsikan sudah paham Spark atau Databricks.
- Variety (V ketiga di 5V) sudah diperkenalkan lewat contoh Sesi 1 (data terstruktur, semi-terstruktur, tidak terstruktur: CSV, JSON bertingkat, teks, gambar). Di sesi ini cukup merujuk balik ke contoh itu, jangan mengajarkannya ulang dari nol.

## Tujuan belajar (maksimal 4)
1. Membedakan data biasa dan big data dengan 5V (volume, velocity, variety, veracity, value) dan angka nyata, bukan hanya istilah.
2. Menjelaskan scale up vs scale out dan kapan masing-masing dipilih.
3. Menjelaskan ide dasar distributed processing: bagi data (partition), proses paralel, gabungkan hasil.
4. Menilai apakah sebuah kasus perlu tools big data atau cukup pendekatan klasik.

## Konsep inti (urutan penyampaian)
1. 5V, dan kenapa ukuran data saja tidak cukup untuk menyebut sesuatu big data.
2. Titik patah: tanda kasus melewati batas satu mesin (memori penuh, waktu proses tidak masuk akal, data datang terus-menerus).
3. Tiga arah solusi: optimasi di mesin yang sama (tipe data hemat, kolom seperlunya, chunked), scale up (mesin lebih besar; hanya dijelaskan, tidak di-hands-on), dan scale out (banyak mesin bekerja bersama; langkah 5 memperlihatkan idenya dengan banyak proses di satu laptop). Tipe hemat dan chunked bukan scale up.
4. Ide distributed: partition, proses paralel per partition, gabungkan hasil parsial.
5. Batch vs streaming secara sekilas, sebagai jembatan ke Sesi 4 dan 5.

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1. Pertanyaan bisnis tetap sama (revenue transaksi COMPLETED per kota), tetapi datanya diperbesar 10 kali.

Dataset: `retail_transactions_10m.csv`, sintetis (bukan data internal Insignia atau klien), 10.000.000 baris, dibuat dengan menggandakan `retail_transactions.csv` Sesi 1 sebanyak 10 kali (seed 42) dan menambahkan akhiran `-0` sampai `-9` pada `transaction_id` agar tetap unik. Ukuran file 945-955 MB (955 MB di Windows karena akhir baris CRLF, 945 MB di macOS/Linux). Kolom sama dengan Sesi 1. Karena hasil penggandaan, semua angka revenue tepat 10 kali angka Sesi 1.

Starter Kit harus menyertakan skrip pembangkit (`make_data_s02.py`) yang menghasilkan dua hal sebelum sesi: file 10 juta baris dan folder `parts/` berisi file CSV yang sudah dibagi menjadi N partition (N sama dengan jumlah core CPU laptop). Peserta menjalankan skrip ini sebelum hari sesi, bukan di kelas, karena pembagian file memakan waktu lama.

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing. Python 3.12 ke atas (pandas 3.0.5 dan numpy 2.5.4 tidak terpasang di Python 3.10 dan 3.11), pandas, numpy, pyarrow, dan modul `multiprocessing` bawaan Python. Tidak ada cloud, Docker, atau Spark.
- `requirements.txt` memuat `pyarrow==26.0.1`. Angka memori di hands-on (sekitar 1.575 MB, 620 MB, dan 150 MB) hanya muncul dengan pandas 3.x dan pyarrow terpasang; tanpa itu kolom teks jauh lebih boros dan angkanya lebih besar.
- Minimum RAM laptop 8 GB. Starter Kit menyertakan langkah verifikasi environment dan pengecekan RAM serta jumlah core (`os.cpu_count()`). Langkah 2-3 butuh memori kosong sekitar 4 GB (puncak memori proses terukur 3,8 GB). Jika RAM di bawah 12 GB, Langkah 0 mencetak saran untuk melewati langkah 2-3; langkah 4-6 tetap berjalan.
- Fungsi worker untuk multiprocessing harus ditaruh di file modul terpisah (`workers.py`), bukan didefinisikan di dalam notebook, supaya jalan di Windows dan macOS.
- Angka checkpoint diverifikasi di sandbox pengujian (Python 3.13, pandas 3.0.5, pyarrow 26.0.1, mesin 2 core, RAM 7 GB) dan lewat eksekusi notebook pada build Claude Code (11 November 2026), dengan hasil sama. Bila versi pustaka diubah, jalankan ulang notebook dan perbarui checkpoint.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 1, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.05 | 5V dan titik patah data biasa vs big data | Konsep | 25 mnt |
| 14.05 - 14.25 | Scale up vs scale out, ide distributed | Konsep | 20 mnt |
| 14.25 - 15.10 | Hands-on: tangga solusi | Hands-on | 45 mnt |
| 15.10 - 15.20 | Batch vs streaming sekilas, jembatan ke Sesi 3 | Konsep | 10 mnt |
| 15.20 - 15.30 | Recap dan tanya jawab | Penutup | 10 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 karena penambahan slide penjelasan mekanisme (Konsep +5 menit, hands-on -5 menit, total tetap 120 menit).

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, satu pertanyaan bisnis (revenue COMPLETED per kota), lima cara menjawabnya. Nilai hasil harus identik di semua cara. Angka waktu di bawah dari mesin 2 core dan bervariasi antar laptop, jadi tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 1. Kenali data dan siapkan acuan: ukuran file, jumlah baris, jumlah core, acuan revenue per kota = data Sesi 1 dikali 10 | 5 | 10.000.000 baris; file 945-955 MB; total revenue acuan 32.737.599.110.000 |
| 2. Baseline: muat semua kolom ke memori, hitung revenue per kota untuk COMPLETED (boleh dilewati bila RAM di bawah 12 GB) | 5 | memori dataframe sekitar 1.575 MB; total revenue 32.737.599.110.000; `equal` True terhadap acuan; waktu agregasi sekitar 2-3 detik, tidak termasuk waktu baca |
| 3. Optimasi: ubah kolom teks berulang jadi `category`, `quantity` dan `unit_price` jadi `int32`, lalu buang kolom yang tidak dipakai (boleh dilewati bila RAM di bawah 12 GB) | 10 | memori tanpa kolom `transaction_id` dan `transaction_ts` sekitar 150 MB; dengan semua kolom sekitar 620 MB; hasil agregasi tidak berubah |
| 4. Optimasi: chunked processing, `read_csv` dengan `chunksize` 1 juta baris dan `usecols`, agregasi per chunk lalu gabung | 10 | total revenue sama dengan acuan (`equal` True); waktu mendekati baseline (sekitar 11 detik vs 12 detik baca plus agregasi), tetapi memori jauh lebih kecil karena hanya satu chunk di memori |
| 5. Partition dan paralel (ide scale out): `multiprocessing.Pool` dengan satu worker per partition di `parts/`, gabungkan hasil parsial | 10 | total revenue sama (`equal` True); pada 2 core, waktu sekitar 6 detik vs sekitar 12 detik baseline (sekitar 2 kali lebih cepat); percepatan mengikuti jumlah core |
| 6. Bandingkan lima cara dalam satu tabel (`mem_data_mb` = memori dataframe, bukan memori proses; waktu; hasil sama), lalu isi checklist keputusan | 5 | tabel perbandingan terisi; cara yang dilewati tertulis `dilewati`; peserta bisa menyebut cara mana yang cocok untuk kasus apa |

Pesan yang harus muncul dari langkah 5: membagi file menjadi partition di tengah query itu mahal (di mesin acuan sekitar 84 detik untuk 10 juta baris). Partition harus sudah ada sebelumnya. Inilah alasan sistem big data menyimpan data dalam bentuk terpartisi, dan menjadi jembatan ke Sesi 3.

Pertanyaan penutup hands-on: "Kalau datanya 1 miliar baris dan satu laptop tidak cukup, apa yang kamu butuhkan dari sebuah sistem?" Jawaban diarahkan ke penyimpanan terdistribusi, banyak mesin, dan koordinasi, bukan ke merek tools.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Hapus variabel besar dengan `del` setelah langkah 2 dan 3 supaya laptop 8 GB tidak kehabisan memori (langkah 3 membuat salinan).
- Langkah 1 menyiapkan acuan `expected` dari `retail_transactions.csv` Sesi 1 dikali 10. Semua cara dibandingkan dengan acuan ini, bukan dengan baseline, supaya langkah 2-3 boleh dilewati.
- Jika kernel mati: Restart Kernel, jalankan Langkah 0 dan 1, lalu lanjut dari langkah 4.
- Uji notebook lewat eksekusi sebagai notebook (bukan hanya sebagai skrip), karena multiprocessing di Jupyter punya perilaku berbeda. Laporkan hasil uji ini.
- Jangan menambahkan Parquet, Spark, atau Dask.
- Slide 5V merujuk balik ke contoh Sesi 1 untuk variety (CSV, JSON order, teks ulasan, gambar produk): keempatnya masih diolah di satu laptop, jadi variety tinggi saja belum big data. Jangan menulis "variety: satu tabel".
- Sesi 1 ditutup dengan empat tanda kewalahan (memori, waktu, satu mesin, banyak file). Sesi 2 merujuk keempatnya.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `1,575 MB`, `900347`, `0.28`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(1.575 MB)", "(3,27 triliun)", "(28%)").
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
| S2-CK1 | 5V | 5V pada dataset kita: volume 10.000.000 baris (file 945 MB); variety tiga bentuk data (tabular, nested JSON, gambar; Sesi 1); velocity sekitar 27.400 transaksi per hari (10.000.000 / 365); veracity 9,97% transaksi bukan COMPLETED (CANCELLED 69.741 dan REFUNDED 29.912 per 1.000.000 baris); value revenue COMPLETED 32,74 triliun | Dataset Sesi 1 dan 2 (10 juta baris = 10 salinan dataset Sesi 1, proporsi status sama) | `addLabelRowsSlide` |
| S2-CK2 | Titik patah dan tangga solusi | Tangga solusi dengan angka memori: 1.575 MB (baseline) menjadi 620 MB (tipe hemat), 150 MB (tanpa `transaction_id` dan `transaction_ts`), 48 MB (satu chunk) | Langkah 2 sampai 4 | `addStepsCheckpointSlide` |
| S2-CK3 | Distributed processing | Bagi, proses, gabungkan: file 10 juta baris dibagi 4 bagian 2,5 juta baris; partial result 8.186.818.584.000, 8.181.980.971.000, 8.186.818.584.000, 8.181.980.971.000; jumlahnya 32.737.599.110.000, sama dengan baseline. Beri label "Ilustrasi pembagian" | Dihitung dari `retail_transactions_10m.csv`, COMPLETED; jumlah bagian pada Langkah 5 bergantung core | `addLabelRowsSlide` |
| S2-TD1 | Scale up atau optimasi | Tebak: berapa memori dataframe 10 juta baris tanpa optimasi tipe data? Pilihan: 150 MB, 1,5 GB, 15 GB. Jawaban: 1.575 MB (sekitar 1,5 GB) | Langkah 2 | `addTwoPanelSlide`, `addStatSlide` |
| S2-TD2 | Optimasi | Tebak: dengan tipe data hemat berapa memorinya, dan bila dua kolom terbesar dibuang? Jawaban: 620 MB, lalu 150 MB | Langkah 3 | `addTwoPanelSlide`, `addBeforeAfterSlide` |
| S2-TD3 | Menilai kasus | Tiga kasus: laporan harian 2 juta baris di laptop; laporan harian 10 juta baris di laptop RAM 8 GB; laporan per jam dari 1 miliar baris. Pertanyaan: perlu big data atau tidak? Jawaban per Answer Key (baseline atau tipe hemat; chunked dengan kolom seperlunya; storage terdistribusi dan banyak mesin) | Langkah 6 | `addTwoPanelSlide`, `addComparisonTableSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 2 ditandai)
- 5V dan titik patah: `addSectionSlide`, `addCardGridSlide` (5V, satu kartu per V, maksimal 4 kartu per slide sehingga pecah menjadi dua slide atau pakai `addLabelRowsSlide`), `addBeforeAfterSlide` (data biasa vs big data: bagaimana tiap V berubah), `addStatSlide` (angka dari Sesi 1 dan Sesi 2: 1 juta baris sekitar 155 MB, 10 juta baris sekitar 1.575 MB; sumber: hasil hands-on dataset sintetis)
- Scale up vs scale out: `addSectionSlide`, `addComparisonTableSlide` (scale up vs scale out: cara, batas, biaya, contoh), `addTwoPanelSlide` (ide distributed: bagi, proses paralel, gabung)
- Hands-on: `addSectionSlide`, `addStepsCheckpointSlide` (langkah 1-3 lalu langkah 4-6), `addCodeSlide` (maks 18 baris: langkah 4 chunked dan langkah 5 paralel), `addChecklistSlide` (verifikasi environment dan data sebelum mulai)
- Penutup: `addNumberedListSlide` (tiga pertanyaan untuk menilai apakah kasus butuh big data), `addClosingSlide` (ringkasan dan Sesi 3 Big Data Storage), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Big data bukan soal angka tertentu. Sebuah kasus menjadi big data ketika cara klasik tidak lagi cukup dalam memori, waktu, atau kecepatan data.
- Banyak masalah "besar" selesai dengan optimasi di mesin yang sama (tipe data hemat, chunked) sebelum perlu scale up atau scale out.
- Scale out bekerja karena data bisa dibagi. Partition yang sudah ada adalah syarat percepatan.
- Percepatan paralel dibatasi jumlah core dan biaya koordinasi, jadi tidak selalu sebanding dengan jumlah worker.

Pertanyaan yang kemungkinan muncul:
- "Berapa ukuran data minimal untuk disebut big data?" Jawab: tidak ada angka tunggal. Gunakan titik patah dan 5V.
- "Kenapa tidak langsung pakai Spark?" Jawab: Spark muncul di Sesi 4. Dengan mengenali ide dasarnya dulu, peserta paham apa yang Spark otomatiskan.
- "Kenapa paralel di laptop saya tidak jadi dua kali lebih cepat?" Jawab: jumlah core, kecepatan disk, dan biaya koordinasi proses memengaruhi hasil.

## Risiko teknis dan hal yang dicek sebelum sesi
- RAM laptop 8 GB: dataframe langkah 2 berukuran sekitar 1,6 GB, tetapi puncak memori proses terukur 3,8 GB (langkah 3: 3,5 GB; langkah 5b dengan 12 worker: 2,6 GB). Langkah 2-3 butuh memori kosong sekitar 4 GB; RAM di bawah 12 GB disarankan melewatinya.
- Pembuatan data 10 juta baris dan partition memakan waktu beberapa menit sampai lebih dari satu menit, dan butuh sekitar 2 GB ruang disk (file 945-955 MB ditambah partition). `make_data_s02.py --tanpa-parts` membuat file 10 juta baris saja (dipakai Sesi 3). Peserta menjalankannya sebelum hari sesi.
- Multiprocessing di Jupyter pada Windows dan macOS: fungsi worker wajib di `workers.py`. Uji di kedua sistem operasi bila memungkinkan.
- Laptop dengan 2 core atau lebih sedikit tidak memperlihatkan percepatan yang jelas. Siapkan penjelasan, dan jangan menjadikan angka percepatan sebagai kriteria berhasil.
- Angka waktu bervariasi antar mesin. Hanya nilai hasil (total revenue, jumlah baris) yang boleh dijadikan checkpoint.

## Istilah yang harus konsisten di semua file
- big data, common data (bukan "small data")
- 5V: volume, velocity, variety, veracity, value
- titik patah (batas satu mesin)
- scale up, scale out
- partition, chunk (chunk = potongan saat membaca satu file; partition = bagian data yang sudah terpisah)
- parallel processing, distributed processing
- partial result, combine results
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama dataset: `retail_transactions.csv` (Sesi 1), `retail_transactions_10m.csv` (Sesi 2), folder `parts/`
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 2 dibangun dan notebook dijalankan dengan pandas 3.0.5 dan pyarrow 26.0.1; angka checkpoint sama dengan Brief.
- Langkah 2-3 butuh memori kosong sekitar 4 GB (puncak proses terukur 3,8 GB). Peserta dengan RAM di bawah 12 GB otomatis melewatinya (flag `RUN_HEAVY` di Langkah 0); yang tetap ingin mencoba mengubah `RUN_HEAVY` menjadi `True` dengan risiko kernel mati.
- Fungsi worker multiprocessing ada di `workers.py`. Pembuat data: `make_data_s02.py` (opsi `--tanpa-parts` untuk Sesi 3).
- Peserta yang diblokir Smart App Control memakai WSL Ubuntu seperti Sesi 1.
- Belum diuji: multiprocessing di Windows dan macOS, dan laptop RAM 8 GB sungguhan.

## Keputusan terbuka
1. Teks asli poin 3 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Status paket pilot terhadap Sesi 2: Brief ini memperlakukannya sebagai bahan acuan konsep, bukan dasar sesi. Konfirmasi.
3. Skala 10 juta baris diuji di mesin 2 core RAM 7 GB. Laptop RAM 8 GB sungguhan dan multiprocessing di Windows dan macOS belum diuji.
4. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
