# BRIEF SESI - Big Data

Sesi: 9 - Cloud Approach for Big Data Solution
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta memetakan pipeline Sesi 7 dan 8 ke layanan cloud, lalu menjalankan pertanyaan bisnis yang sama di dua platform gratis (BigQuery sandbox dan Databricks Free Edition) untuk membandingkan model serverless, cost model, dan cara operasionalnya.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution (sesi ini)
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk empat hal dari sesi sebelumnya: Sesi 3 (Parquet, columnar, partition folder), Sesi 4 (Spark dan lazy evaluation), Sesi 7 dan Sesi 8 (batch pipeline dan stream yang kini dipetakan ke cloud). Slide penutup menyebut Sesi 10 "Big Data Preparation for Robust AI/ML Use Case".

## Batasan cakupan
- Sesi ini membahas poin 10 outline: cloud approach untuk solusi big data.
- Konsep yang diajarkan (keputusan Fahmi): service map cloud untuk big data; cost model cloud; serverless vs managed cluster vs self-managed. Keamanan dan tata kelola (IAM, region, enkripsi) tidak menjadi konsep inti; cukup disebut satu slide sebagai hal yang harus diurus sebelum produksi, tanpa hands-on.
- Hands-on (keputusan Fahmi): dua bagian terpisah, BigQuery sandbox (Google Cloud) dan Databricks Free Edition, dijalankan sendiri oleh setiap peserta. Pertanyaan bisnis sama dengan Sesi 7: revenue transaksi COMPLETED per kota per bulan.
- Platform bukan asumsi untuk seluruh modul. Sesi 9 memakai dua platform ini karena diputuskan di sesi ini. Sesi 1-8 tetap lokal.
- Tidak ada pipeline yang dirangkai antar kedua platform (Databricks Free Edition tidak bisa terhubung ke storage cloud lain; lihat risiko). Data diunggah terpisah ke masing-masing.
- Tidak ada stream di cloud secara hands-on. Padanan layanan streaming (Sesi 5 dan 8) hanya dibahas di service map.
- Tidak ada hands-on AWS, Azure, atau Huawei Cloud. Keempatnya muncul di service map dan perbandingan konsep. Jalur sertifikasi (misalnya Huawei HCCDP) tidak dibahas.
- Tidak ada Terraform, Kubernetes, Docker, VPC dan jaringan, tuning biaya tingkat lanjut, dan migrasi on-premise ke cloud.
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.

## Tujuan belajar (maksimal 4)
1. Memetakan komponen pipeline (storage, compute batch, query serverless, streaming, warehouse) ke layanan di AWS, Google Cloud, Azure, dan Huawei Cloud.
2. Membedakan serverless, managed cluster, dan self-managed, dan menyebut kapan masing-masing dipilih.
3. Menjalankan pertanyaan yang sama di BigQuery dan Databricks, dan menunjukkan hasilnya sama dengan hasil lokal.
4. Menjelaskan cost model (bayar per bytes scanned, per waktu compute, per storage) dan memperkirakan biaya satu pertanyaan bisnis.

## Konsep inti (urutan penyampaian)
1. Dari mesin sendiri ke cloud: masalah yang diselesaikan (kapasitas, perawatan, biaya di muka) dan harga yang dibayar (biaya berulang, ketergantungan vendor, tata kelola).
2. Peta layanan: object storage, compute batch terkelola, query serverless, streaming, data warehouse. Setiap komponen pipeline Sesi 7 dan 8 diberi padanan cloud.
3. Tiga tingkat pengelolaan: self-managed (VM, kita urus semuanya), managed cluster (kita atur ukuran dan nyalakan), serverless (platform yang mengatur). Trade-off kontrol, kerja operasional, dan biaya saat idle.
4. Model biaya: bayar per byte dipindai (BigQuery on-demand), bayar per waktu compute (Databricks, cluster), storage dan egress. Dampak ke desain: columnar dan kolom yang dipilih menurunkan bytes scanned (Sesi 3).
5. Hands-on gratis dan batasannya: kuota, expiration tabel, daily quota. Cloud gratis bagus untuk belajar, bukan tolok ukur produksi.
6. Sekilas: keamanan dan tata kelola sebelum produksi (satu slide).

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1-8. Pertanyaan bisnis: revenue transaksi COMPLETED per kota per bulan (revenue = quantity x unit_price), sama dengan tabel `revenue_by_city_month` di Sesi 7.

Dataset: 1.000.000 baris `retail_transactions.csv` dari Sesi 1 (sintetis, bukan data internal Insignia atau klien; seed 42; 1 Januari 2025 sampai 31 Desember 2025), disimpan sebagai Parquet agar kecil dan tipenya tegas: `retail_1m.parquet` (Parquet zstd 9.597.101 byte, sekitar 9,6 MB; versi CSV 93 MB). Kolom: `transaction_id`, `transaction_ts` (timestamp mikrodetik), `store_id`, `city`, `category`, `product_id`, `quantity` (int64), `unit_price` (int64), `payment_method`, `status`. Starter Kit menyertakan `retail_1m.parquet` yang sudah jadi, dan skrip pembuatnya (pandas, pyarrow) untuk pengajar. Peserta tidak perlu Python di laptop.

Acuan batch (pandas, lokal) dari data itu, jadi nilai yang harus sama di kedua platform:
- 1.000.000 baris; status COMPLETED 900.347, CANCELLED 69.741, REFUNDED 29.912.
- Revenue COMPLETED total 3273759911000 (3,27 triliun).
- Hasil per kota per bulan: 96 baris (8 kota x 12 bulan).
- Jakarta 2025-01: 77701988000 (77,7 miliar); Jakarta 2025-02: 70887080000 (70,9 miliar).
- Total per kota: Jakarta 918117634000, Surabaya 528045460000, Bandung 457990352000, Medan 326257053000, Semarang 293900284000, Makassar 263788374000, Yogyakarta 259412024000, Denpasar 226248730000.
- Transaksi COMPLETED terbanyak: Jakarta 252.079, Surabaya 144.642, Bandung 126.235.
- Estimasi data logis (perhitungan sendiri, bukan hasil dari BigQuery): seluruh tabel sekitar 94,5 MB, lima kolom yang dipakai query sekitar 44,4 MB. Hanya perbandingan arah (selected columns lebih kecil dari seluruh tabel) yang boleh dijadikan checkpoint sampai diverifikasi di BigQuery.

## Platform dan tools peserta
Seluruh hands-on di browser. Tidak ada instalasi lokal, Docker, Java, atau WSL2.
- Google Cloud: BigQuery sandbox. Sandbox tidak meminta kartu kredit atau billing account. Dokumentasi Google yang dicek 11 November 2026 menyebut batas 10 GB storage aktif dan 1 TB data query diproses per bulan, tabel expire otomatis setelah 60 hari, dan fitur yang tidak didukung: streaming, pernyataan DML, dan BigQuery Data Transfer Service. Dokumen itu tidak menyebut Cloud Storage atau load job, jadi tidak boleh diandalkan.
- Databricks Free Edition (bukan Community Edition: Community Edition dipensiunkan 1 Januari 2026 menurut pengumuman Databricks). Gratis tanpa batas waktu dengan daily quota. Hanya serverless (tidak ada cluster kustom), satu SQL warehouse ukuran 2X-Small, Python dan SQL didukung, R dan Scala tidak. Akses internet keluar dibatasi ke domain tertentu dan lokasi storage kustom tidak didukung. Login lewat email OTP, Google, atau Microsoft. Tanpa SLA dan tanpa dukungan; tidak boleh dipakai komersial (lihat risiko dan keputusan terbuka).
- Peserta memakai akun Google untuk BigQuery (2-Step Verification wajib aktif) dan akun Databricks Free Edition; buat keduanya sebelum sesi. Ketersediaan Free Edition untuk peserta di Indonesia dan dari jaringan kantor Insignia belum diuji.
- Semua batas dan nama layanan di atas diperiksa dari dokumentasi pada 11 November 2026 dan bisa berubah; periksa ulang menjelang sesi.
- Tidak ada langkah hands-on di Brief ini yang diverifikasi di akun cloud sungguhan (sandbox pengujian tidak punya akses akun). Yang diverifikasi hanya angka acuan dengan pandas. Claude Code atau pengajar wajib menjalankan seluruh langkah di akun sungguhan dan mengunci checkpoint.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 7 dan 8, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.05 | Dari mesin sendiri ke cloud; service map; serverless vs cluster vs self-managed; cost model | Konsep | 25 mnt |
| 14.05 - 15.15 | Hands-on: BigQuery sandbox, Databricks Free Edition, perbandingan dan estimasi biaya | Hands-on | 70 mnt |
| 15.15 - 15.30 | Recap, keamanan dan tata kelola sekilas, jembatan ke Sesi 10 | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook (untuk bagian Databricks) dan satu lembar langkah (untuk bagian BigQuery, karena dikerjakan di console). Angka waktu dan tampilan antarmuka bervariasi dan tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

### Bagian A - BigQuery sandbox (sekitar 33 menit, termasuk Langkah 4b)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Persiapan sebelum sesi: akun Google masuk ke BigQuery sandbox, `retail_1m.parquet` terunduh | sebelum sesi | konsol BigQuery terbuka tanpa meminta billing account |
| 1. Buat dataset `retail_s09` | 4 | dataset terlihat di panel |
| 2. Muat `retail_1m.parquet` ke tabel `transactions` lewat antarmuka (upload file lokal, format Parquet) | 6 | tabel berisi 1.000.000 baris; `transaction_ts` bertipe TIMESTAMP |
| 3. Query revenue COMPLETED per kota per bulan (SELECT, GROUP BY) | 7 | 96 baris; total `3273759911000`; Jakarta 2025-01 `77701988000`; sama dengan acuan pandas |
| 4. Bandingkan bytes processed: `SELECT *` vs query dengan selected columns (lihat estimasi bytes processed sebelum dijalankan) | 6 | estimasi bytes processed selected columns lebih kecil dari `SELECT *`; angka dicatat peserta |
| 4b. Big data bekerja: jalankan query pada tabel publik ratusan juta baris (`query_big_data_s09.sql`); baca estimasi sebelum Run | 10 | Q1 `true 52225197`, `false 228966780` (281.191.977 baris), estimasi 2,36 GB; Q2 estimasi sekitar 2,43 TB (tidak dijalankan); Q3a ditolak karena tanpa filter partisi; Q3b estimasi 1 hari 53,23 MB, 1 bulan 2,95 GB, 1 tahun 87,59 GB |

### Bagian B - Databricks Free Edition (sekitar 22 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Persiapan sebelum sesi: akun Free Edition aktif, workspace terbuka | sebelum sesi | workspace terbuka; compute serverless tersedia |
| 5. Unggah `retail_1m.parquet` ke volume Unity Catalog dan baca sebagai DataFrame | 7 | 1.000.000 baris; skema sesuai |
| 6. Query yang sama dengan Spark SQL dan PySpark; bandingkan hasil kedua cara | 10 | 96 baris; total `3273759911000`; Jakarta 2025-01 `77701988000`; kedua cara sama |
| 7. Amati serverless: tidak ada pengaturan cluster; lihat profil atau riwayat query | 5 | peserta bisa menyebut apa yang tidak perlu diatur |

### Bagian C - Perbandingan dan estimasi biaya (sekitar 15 menit, di dalam 70 menit hands-on)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 8. Tabel perbandingan: unit biaya, siapa mengatur compute, batas versi gratis, yang terasa lebih mudah | 7 | tabel terisi dari pengalaman langkah 1-7 |
| 9. Estimasi biaya: dari bytes processed di langkah 4 dan halaman harga resmi, hitung biaya satu query dan 30 query per bulan | 8 | peserta mencantumkan sumber harga dan tanggal cek; angka harga tidak ditulis dari ingatan |

Tidak ada waktu cadangan di 70 menit ini: Langkah 4b memakai 10 menit yang semula cadangan. Bila waktu mepet, Bagian C dibawakan trainer sebagai diskusi. Setup akun harus selesai sebelum sesi; jangan membuat akun di kelas.

Pertanyaan penutup hands-on: "Untuk laporan retail ini, mana yang kamu pilih untuk perusahaanmu: serverless, managed cluster, atau self-managed? Apa dasar pilihanmu: ukuran data, pola query, kebutuhan kontrol, atau biaya?"

Pesan yang harus muncul: pertanyaan yang sama memberi hasil yang sama di semua platform; yang berbeda adalah cara menagih, siapa mengatur compute, dan batasnya. Kolom yang dipilih mengurangi bytes processed (hubungan ke Sesi 3). Versi gratis cukup untuk belajar tetapi bukan gambaran biaya atau performa produksi.

Catatan teknis untuk Claude Code:
- Kode PySpark dan SQL lengkap dan runnable, tanpa TODO dan tanpa `___`. Gunakan hanya API yang didukung serverless di Free Edition (Spark Connect); uji di akun sungguhan dan catat API yang ditolak (misalnya RDD, cache, atau pengaturan konfigurasi Spark).
- BigQuery sandbox: hanya SELECT dan pemuatan data. Jangan memakai DML, streaming, atau Data Transfer Service. Jangan membuat `CREATE TABLE AS` atau tabel partisi di jalur utama tanpa diuji di sandbox.
- Unggah file lokal Parquet ke BigQuery sandbox terbukti jalan lewat Create table > Upload (format Parquet terdeteksi, skema dari file, sekitar 30 detik).
- Unggah ke volume Unity Catalog terbukti jalan lewat Catalog > volume > Upload to this volume; path `/Volumes/workspace/retail_s09/raw/retail_1m.parquet`.
- Tabel BigQuery sandbox expiration setelah 60 hari: tulis di Modul Praktikum bahwa tabel akan hilang dan peserta tidak boleh bergantung padanya.
- Kuota harian Databricks: jika terlampaui, compute mati sampai akhir hari. Susun notebook agar hemat (satu baca, query berulang tidak berlebihan) dan tulis penanganannya di Modul Praktikum.
- Padanan layanan di peta (lihat bagian slide): periksa ulang nama dan kategori layanan di dokumentasi resmi masing-masing cloud sebelum masuk slide, dan tulis tanggal cek. Jangan mencantumkan harga di slide kecuali dengan sumber dan tanggal cek.
- Untuk perbandingan biaya, gunakan halaman harga resmi dan kalkulator harga pada saat paket dibuat; beri tahu peserta bahwa harga berubah.
- Format angka checkpoint: tulis persis seperti output (misal `3273759911000`), lalu format Indonesia di dalam kurung bila angkanya besar (misal "(3,27 triliun)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Bagian BigQuery dan Databricks dikerjakan di antarmuka web; sertakan tangkapan layar hanya dari akun sungguhan, bukan buatan. Jangan memuat kredensial, email, atau ID proyek nyata di tangkapan layar.
- Tanpa emoji atau ikon di dokumen training formal.
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan) untuk bagian Databricks. Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live. Bagian BigQuery berupa lembar langkah singkat (Modul Praktikum) dengan query SQL siap salin.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S9-CK1 | Cost model | Estimasi bytes processed sebelum Run: query lima kolom 42,35 MB vs `SELECT *` 90,08 MB (selisih sekitar 53%). Rumus: biaya = bytes processed / 1 TB x harga on-demand per TB (harga dari halaman resmi, tanggal cek dicantumkan). 30 query per bulan x 42,35 MB = sekitar 1,24 GB. BigQuery menampilkan satuan biner berlabel MB | Langkah 4 | `addBeforeAfterSlide` |
| S9-CK2 | Big data bekerja | Q1 pada tabel publik: 281.191.977 baris, bytes processed 2,36 GB, durasi sekitar 1,3 detik, slot time 153.373 ms atau sekitar 115 slot paralel (153.373 ms / sekitar 1.300 ms; perkiraan kasar). Q2 menambah kolom `content`: estimasi sekitar 2,43 TB (tidak dijalankan, di atas kuota 1 TB) | Langkah 4b | `addStatSlide` |
| S9-CK3 | Serverless vs managed cluster vs self-managed | Tiga model pada satu pertanyaan: self-managed (mesin dan Spark dipasang dan dirawat sendiri), managed cluster (pilih ukuran, start dan stop), serverless (tanpa cluster). Konsekuensi serverless nyata: di Databricks serverless `df.rdd` ditolak (`RDD_NOT_SUPPORTED`) dan `spark.sparkContext` ditolak: kontrol berkurang demi kerja operasional lebih sedikit | Langkah 7 | `addComparisonTableSlide` |
| S9-TD1 | Cost model | Tebak: Q1 menambah satu kolom `content`, bytes processed dari 2,36 GB menjadi berapa? Jawaban: sekitar 2,43 TB (sekitar 1.000 kali) | Langkah 4b | `addTwoPanelSlide`, `addStatSlide` |
| S9-TD2 | Partition di cloud | Tebak: query pageviews Indonesia tanpa filter `datehour` diterima atau ditolak? Jawaban: ditolak (wajib filter partisi); dengan filter: 1 hari 53,23 MB, 1 bulan 2,95 GB, 1 tahun 87,59 GB | Langkah 4b | `addTwoPanelSlide`, `addComparisonTableSlide` |
| S9-TD3 | Memilih pengelolaan | Tebak: laporan retail 1 juta baris dengan query ad hoc, pilih serverless, managed cluster, atau self-managed? Jawaban acuan: serverless untuk ukuran ini; dasar: ukuran data, pola query, kebutuhan kontrol, biaya | Langkah 9 | `addTwoPanelSlide`, `addComparisonTableSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 9 ditandai)
- Dari mesin sendiri ke cloud: `addSectionSlide`, `addBeforeAfterSlide` (kelola sendiri vs layanan cloud: yang diurus, biaya, risiko)
- Peta layanan: `addSectionSlide`, `addComparisonTableSlide` (komponen pipeline vs padanan di AWS, Google Cloud, Azure, Huawei Cloud; tanggal cek dicantumkan), `addTwoPanelSlide` (pipeline Sesi 7 dan 8 dipetakan ke cloud)
- Tiga tingkat pengelolaan: `addSectionSlide`, `addLabelRowsSlide` (self-managed, managed cluster, serverless: siapa mengatur, kontrol, biaya idle), `addComparisonTableSlide` (kapan memilih yang mana)
- Model biaya: `addSectionSlide`, `addCardGridSlide` (tiga unit biaya: bytes scanned, waktu compute, storage dan egress), `addStatSlide` (satu angka dari hands-on langkah 4 setelah diverifikasi; sumber: hasil hands-on dataset sintetis)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (akun, file, batas versi gratis, kuota), `addStepsCheckpointSlide` (langkah 1-4 lalu langkah 5-9), `addCodeSlide` (maks 18 baris: query revenue per kota per bulan dalam SQL; dan versi PySpark)
- Penutup: `addNumberedListSlide` (empat pertimbangan memilih pendekatan cloud; satu poin keamanan dan tata kelola), `addClosingSlide` (ringkasan, Sesi 10 Big Data Preparation for Robust AI/ML Use Case), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Cloud memindahkan pekerjaan operasional ke penyedia, dan sebagai gantinya biayanya berulang dan terikat penyedia.
- Pertanyaan bisnis dan hasilnya sama di mana pun; pilihan platform adalah soal cara kerja dan biaya.
- Serverless menghemat kerja operasional tetapi mengurangi kontrol; self-managed memberi kontrol penuh dengan beban kerja terbesar.
- Biaya mengikuti desain data: Parquet, selected columns, dan partisi menurunkan bytes scanned.
- Versi gratis untuk belajar. Jangan menyimpulkan kinerja atau biaya produksi darinya.

Pertanyaan yang kemungkinan muncul:
- "Kenapa tidak lokal saja seperti Sesi 1-8?" Jawab: lokal cukup untuk belajar; sesi ini menunjukkan apa yang berubah saat compute dan storage dikelola penyedia: siapa mengatur, bagaimana ditagih, apa batasnya.
- "Bisa dihubungkan ke storage cloud kita?" Jawab: tidak di versi gratis ini; itu fitur akun berbayar dan di luar cakupan sesi.
- "Berapa biayanya di produksi?" Jawab: bergantung data dan pola query; hitung dengan kalkulator harga resmi, bukan dari hands-on gratis.
- "Kenapa tabel BigQuery saya hilang?" Jawab: tabel sandbox expiration setelah 60 hari.
- "Kenapa compute Databricks mati?" Jawab: daily quota Free Edition terlampaui; lanjut besok atau kurangi query.
- "Mana yang lebih baik, BigQuery atau Databricks?" Jawab: keduanya menjawab kebutuhan berbeda; bandingkan pada kontrol, cost model, dan ekosistem, bukan menyebut pemenang.
- "Bagaimana dengan AWS, Azure, dan Huawei Cloud?" Jawab: ada equivalent services di peta; hands-on memakai dua platform yang gratis tanpa kartu kredit.

## Risiko teknis dan hal yang dicek sebelum sesi
- Seluruh langkah cloud diuji di akun sungguhan pada 11 November 2026 (lihat Hasil build dan uji). Uji dari jaringan kantor Insignia dan akun Google Workspace belum dilakukan.
- Free Edition tidak boleh dipakai komersial dan hanya ditujukan untuk belajar. Training internal karyawan Insignia perlu dipastikan boleh atau tidak sebelum peserta diminta membuat akun. Jika tidak boleh, bagian Databricks diganti (lihat keputusan terbuka).
- Free Edition bisa berubah tanpa pemberitahuan (Community Edition sudah dipensiunkan). Cek ulang sebelum sesi.
- Ketersediaan Free Edition untuk peserta di Indonesia dan dari jaringan kantor Insignia belum diuji.
- Akun Google kantor mungkin diblokir untuk BigQuery sandbox oleh kebijakan organisasi; sediakan jalur memakai akun Google pribadi.
- Jaringan atau proxy kantor bisa memblokir domain BigQuery atau Databricks. Uji dari jaringan kantor Insignia.
- Sebagian peserta bisa kehabisan daily quota Databricks karena mengulang query. Sediakan cadangan: pengajar menunjukkan hasil dari layar.
- Unggahan file (sekitar 9,6 MB) dari rumah atau jaringan kantor yang lambat. Bagikan juga lewat folder bersama.
- Antarmuka cloud berubah sering sehingga tangkapan layar cepat usang. Instruksi menyebut nama menu, dan tangkapan layar diberi tanggal ambil.
- Hands-on 70 menit dengan dua platform padat. Cadangan bila waktu mepet: bagian C (perbandingan) dikerjakan sebagai diskusi trainer dengan tabel yang sudah terisi sebagian. Dicek saat gladi.
- Biaya dan harga cloud berubah. Jangan menulis harga dari ingatan; sertakan sumber dan tanggal cek.
- Rujukan lintas sesi: "partition" di Sesi 9 hanya muncul sebagai konsep partisi tabel, bukan partisi Kafka atau Spark; sebut konteksnya bila dipakai.

## Istilah yang harus konsisten di semua file
- cloud, cloud service, service map, equivalent services
- object storage, managed batch compute, serverless query, data warehouse
- self-managed, managed cluster, serverless
- cost model: on-demand (bytes processed), compute time, storage, egress
- BigQuery sandbox, Databricks Free Edition (bukan "Community Edition")
- daily quota, table expiration (60 hari), free tier limits
- Unity Catalog volume, SQL warehouse 2X-Small, Spark SQL, PySpark
- revenue = quantity x unit_price; transaksi COMPLETED; `revenue_by_city_month`
- Nama dataset: `retail_1m.parquet` (sumber `retail_transactions.csv` 1 juta baris Sesi 1; Parquet zstd), `query_bigquery_s09.sql`, `query_big_data_s09.sql`
- bytes processed, selected columns, columnar
- partition: di sesi ini hanya berarti partisi tabel, bukan Kafka partition atau Spark partition
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Semua langkah diuji di akun sungguhan pada 11 November 2026: BigQuery sandbox (project baru tanpa billing) dan Databricks Free Edition (compute Serverless). Seluruh angka checkpoint sama dengan acuan pandas.
- Parquet ditulis ulang dengan kompresi zstd level 19: 9.597.101 byte (sebelumnya snappy sekitar 17,7 MB). Isi identik. `transaction_ts` ditulis tanpa zona waktu: BigQuery memuat sebagai TIMESTAMP, Databricks membacanya sebagai `timestamp_ntz`; bulan yang dihasilkan sama.
- BigQuery sandbox: 2-Step Verification wajib aktif (sejak 6 Oktober 2026; tanpa itu muncul "Google Cloud access blocked"). Jebakan: banner dan iklan "Try Google Cloud for free" (Free Trial, $300) meminta kartu kredit; jalur sandbox tidak meminta kartu. `CREATE SCHEMA` (DDL) berjalan di sandbox. Unggah Parquet lewat Create table > Upload sekitar 30 detik. Tabel kedaluwarsa 60 hari (uji: 2027-01-10).
- Estimasi BigQuery: query lima kolom 42,35 MB, `SELECT *` 90,08 MB (satuan biner berlabel MB; sama dengan perhitungan 44,4 dan 94,5 juta byte).
- Langkah 4b ditambahkan pada build dan dibawa ke Brief ini: Q1 `github_repos.contents` 281.191.977 baris, estimasi 2,36 GB, durasi 1,3 detik; Q2 estimasi 2,43 TB (tidak dijalankan); Q3a `pageviews_2025` tanpa filter `datehour` ditolak; Q3b 1 hari 53,23 MB, 1 bulan 2,95 GB, 1 tahun 87,59 GB, dan Execution details memperlihatkan slot time 41 detik vs elapsed 2 detik. Pemakaian kuota per peserta sekitar 5,3 GB bila Q1 dan Q3b dijalankan. Langkah 4b memakai 10 menit yang semula cadangan.
- Databricks Free Edition: `CREATE SCHEMA` dan `CREATE VOLUME` lewat SQL Editor berjalan; unggah lewat Catalog > volume > Upload to this volume (dialog menyebut file di atas 5 GB memakai CLI); path `/Volumes/workspace/retail_s09/raw/retail_1m.parquet`. Serverless menolak `df.rdd` (`RDD_NOT_SUPPORTED`) dan `spark.sparkContext` (`JVM_ATTRIBUTE_NOT_SUPPORTED`); `df.cache()` dan `spark.conf.set('spark.sql.shuffle.partitions', ...)` berjalan.
- Istilah: Google Cloud menamai ulang Dataproc menjadi Managed Service for Apache Spark sejak 3 April 2026; bila peserta menyebut Dataproc, maksudnya sama.
- Belum diuji: Free Edition untuk peserta di Indonesia dan dari jaringan kantor Insignia; akun Google Workspace Insignia untuk BigQuery sandbox.

## Keputusan terbuka
1. Teks asli poin 10 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi dan keputusan Fahmi. Cocokkan sebelum finalisasi paket.
2. Izin pemakaian Databricks Free Edition untuk training internal karyawan. Dokumentasi Databricks menyebut Free Edition untuk tujuan non-komersial dan pendaftaran dengan email pribadi. Konfirmasi ke legal atau Databricks sebelum peserta diminta membuat akun; bila tidak boleh, bagian B menjadi demo trainer.
3. Ketersediaan Free Edition untuk peserta di Indonesia dan dari jaringan kantor Insignia belum diuji. Akun Google Workspace Insignia belum diuji untuk BigQuery sandbox.
4. Padanan layanan AWS, Azure, dan Huawei Cloud di service map perlu dicek ulang menjelang sesi (nama layanan berubah, contoh Dataproc menjadi Managed Service for Apache Spark pada 3 April 2026). Harga tidak ditulis dari ingatan.
5. Hands-on 70 menit dengan tiga bagian dan Langkah 4b dinilai padat. Cadangan: bagian C sebagai diskusi trainer. Dicek saat gladi.
6. Langkah 4b memakai tabel publik BigQuery (`bigquery-public-data`); pastikan tabel itu masih tersedia dan Q2 tidak dijalankan di akun berbayar.
7. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
