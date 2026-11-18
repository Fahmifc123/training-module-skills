# BRIEF SESI - Big Data

Sesi: 1 - Intro Classical Data Processing
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta menjalankan alur pemrosesan data klasik (extract, clean, transform, aggregate, load) dengan Python dataframe untuk data tabular dan non-tabular (JSON bertingkat, teks bebas, gambar) di satu mesin, lalu melihat di titik mana pendekatan ini mulai kewalahan.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing (sesi ini)
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide penutup menyebut Sesi 2 sebagai "Common vs Big Data".

## Batasan cakupan
- Sesi ini membahas poin 1 dan 2 outline Mas Lindo yang digabung menjadi satu sesi penuh (bukan pembahasan ringkas), dengan porsi setara:
  1. Data Processing w/ Python (common data, dataframe) untuk data tabular.
  2. Data Processing w/ Python (common data, dataframe) untuk data non-tabular.
- Data non-tabular yang dipakai: JSON bertingkat (semi-terstruktur), teks bebas (tidak terstruktur), dan gambar (tidak terstruktur, file biner). Semuanya diolah sampai menjadi dataframe.
- Sentimen di langkah 10 memakai kamus kata sederhana, bukan NLP atau model machine learning. Sebut eksplisit di slide dan notebook.
- Tidak membahas 5V, scale up vs scale out, dan distributed processing. Itu wilayah Sesi 2.
- Struktur data (terstruktur, semi-terstruktur, tidak terstruktur) diperkenalkan di sesi ini tanpa memakai label "variety". Label itu dan 5V dibahas di Sesi 2, yang merujuk balik ke contoh Sesi 1.
- Tidak membahas format file kolumnar (Parquet) dan perbandingannya dengan CSV. Itu wilayah Sesi 3.
- Tidak ada Spark, PySpark, atau platform cloud di sesi ini.
- Pilot "Introduction_to_Big_Data" (22 slide, Pandas vs PySpark, platform Databricks) tumpang tindih dengan Sesi 2. Jangan dipakai sebagai dasar sesi ini. Dataset retail-nya boleh dipakai ulang.

## Tujuan belajar (maksimal 4)
1. Menjelaskan alur pemrosesan data klasik: extract, clean, transform, aggregate, load.
2. Menjalankan alur tersebut dengan Python dataframe (pandas) pada satu mesin, untuk data tabular (CSV) dan non-tabular (JSON bertingkat, teks bebas, gambar).
3. Membandingkan cara dataframe dan SQL di database relasional untuk operasi yang sama.
4. Mengenali tanda-tanda pendekatan klasik mulai kewalahan (memori, waktu proses, satu mesin, banyaknya file) sebagai jembatan ke Sesi 2.

## Konsep inti (urutan penyampaian)
1. Alur batch klasik: data dari file atau database transaksi, diproses script terjadwal, hasilnya menjadi laporan. Lima tahap: extract, clean, transform, aggregate, load.
2. Dataframe: baris, kolom, tipe data; operasi per kolom (vectorized) dibanding loop per baris.
3. SQL vs dataframe: operasi yang sama (filter, group by, join) ditulis dua cara, hasil harus sama.
4. Tabular vs non-tabular: terstruktur (tabel), semi-terstruktur (JSON bertingkat), tidak terstruktur (teks, gambar). Lima tahap tetap sama; yang berbeda adalah tahap extract, yaitu cara mengubah data menjadi baris dan kolom.
5. Batas satu mesin: seluruh data dimuat ke memori satu komputer, satu proses utama, waktu naik seiring ukuran data.

## Use case dan dataset sintetis
Use case: laporan penjualan retail. Pertanyaan bisnis tabular: berapa revenue dari transaksi yang selesai, per kota dan per bulan, dan per tipe toko? Pertanyaan bisnis non-tabular: (a) apakah order dari aplikasi cocok dengan data transaksi, dan berapa revenue per channel dan tier pelanggan; (b) bagaimana sentimen ulasan pelanggan per kota; (c) seperti apa karakteristik gambar produk per kategori.

Dataset tabular: `retail_transactions.csv`, sintetis (bukan data internal Insignia atau klien), 1.000.000 baris, seed 42, periode Januari - Desember 2025, 8 kota, 40 toko. Kolom: transaction_id, transaction_ts, store_id, city, category, product_id, quantity, unit_price, payment_method, status. Nilai status: COMPLETED, CANCELLED, REFUNDED. Tidak ada nulls dan tidak ada duplikat transaction_id. Ukuran file sekitar 93 MB.

Tabel dimensi `stores.csv` (40 baris): store_id, store_type (Mall, Ruko, Supermarket), opened_year. Dibuat oleh skrip pembangkit data dengan seed 7 agar hasil join selalu sama. Starter Kit harus menyertakan file ini, dan peserta tidak membuatnya sendiri.

Dataset non-tabular, dibuat oleh `generate_dataset_sesi01_nontabular.py` (seed 11) dari transaksi COMPLETED di `retail_transactions.csv`. Starter Kit menyertakan file jadi; peserta tidak membuatnya sendiri.
- `orders_app.json` (sekitar 1,3 MB): 2.000 event order dari aplikasi. Field: order_id, created_at, channel (android, ios, web), customer {customer_id, tier, city}, payment {method, installment_months}, items [{transaction_id, product_id, category, quantity, unit_price}]. Setiap order membungkus 1-4 transaksi COMPLETED dari toko, metode bayar, dan tanggal yang sama (sehingga `customer.city`, `payment.method`, dan `created_at` konsisten dengan semua item-nya), total 4.704 item.
- `reviews.csv` (sekitar 136 KB): 3.000 ulasan berbahasa Indonesia, kolom transaction_id dan review_text. Kalimat dibangkitkan dari template, termasuk dua kalimat bernegasi ("Tidak bagus, ...", "Lumayan, tidak buruk ...") yang sengaja menjadi jebakan bagi kamus sederhana.
- `product_images/` (180 file PNG, sekitar 4 MB): 30 gambar sintetis per kategori, nama file `<slug_kategori>_NNN.png` (misalnya `electronics_001.png`, `home_living_001.png`). Ukuran 64x64 atau 128x128, mode RGB, warna dasar berbeda per kategori.

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing. Python 3.12 ke atas (pandas 3.0.5 dan numpy 2.5.4 tidak terpasang di Python 3.10 dan 3.11), pandas, numpy, pyarrow, Pillow, modul `json` dan `sqlite3` bawaan Python. Tidak ada platform cloud dan tidak ada Docker.
- `requirements.txt` memuat `pyarrow==26.0.1` dan `Pillow==12.3.0`. Sel verifikasi mencetak versi Python, pandas, pyarrow, dan Pillow, lalu memeriksa keberadaan `retail_transactions.csv`, `stores.csv`, `orders_app.json`, `reviews.csv`, dan folder `product_images/`.
- Angka memori (155 MB, 136 MB, estimasi 100x sekitar 14 GB) hanya muncul dengan pandas 3.x dan pyarrow terpasang. Tanpa pyarrow atau dengan pandas 2.2, hasilnya sekitar 483 MB, 423 MB, dan 42 GB. Angka revenue, jumlah baris, dan `same_as_pandas` tidak terpengaruh.
- Angka checkpoint diverifikasi di sandbox pengujian (Python 3.13, pandas 3.0.5, numpy 2.5.4, pyarrow 26.0.1, Pillow 12.3.0) dan lewat eksekusi notebook pada build Claude Code (11 November 2026), dengan hasil sama. Bila versi di `requirements.txt` diubah, jalankan ulang dan perbarui checkpoint.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan: tujuan sesi, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 13.58 | Alur pemrosesan data klasik, dataframe dan SQL | Konsep | 18 mnt |
| 13.58 - 14.08 | Data tabular vs non-tabular | Konsep | 10 mnt |
| 14.08 - 14.48 | Hands-on A: mini pipeline tabular (langkah 1-8) | Hands-on | 40 mnt |
| 14.48 - 15.13 | Hands-on B: JSON, teks, gambar (langkah 9-11) | Hands-on | 25 mnt |
| 15.13 - 15.25 | Batas pendekatan klasik dan jembatan ke Sesi 2 | Konsep | 12 mnt |
| 15.25 - 15.30 | Recap dan tanya jawab | Penutup | 5 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 karena penambahan slide penjelasan mekanisme (dataframe dan vectorized operation, batas satu mesin): Konsep +5 menit (Alur 15 menjadi 18, Batas 10 menjadi 12), Hands-on B -5 menit (30 menjadi 25), total tetap 120 menit.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, dua bagian. Bagian A: pipeline tabular dari CSV sampai hasil agregasi (langkah 1-8). Bagian B: tiga data non-tabular diubah menjadi dataframe lalu diolah dengan lima tahap yang sama (langkah 9-11). Hasil acuan di bawah dari eksekusi nyata. Durasi eksekusi bergantung spesifikasi laptop, jadi jangan dijadikan angka tetap di slide.

### Bagian A - Tabular (40 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 1. Extract: baca CSV dengan `pd.read_csv`, cek shape dan pemakaian memori | 5 | shape (1000000, 10); memori sekitar 155 MB; waktu baca sekitar 3 detik (bervariasi) |
| 2. Inspect: tipe data, nulls, duplikat, sebaran status | 4 | nulls 0; duplikat transaction_id 0; COMPLETED 900.347, CANCELLED 69.741, REFUNDED 29.912 |
| 3. Clean: ubah `transaction_ts` ke datetime, ambil hanya COMPLETED | 5 | 900.347 baris tersisa |
| 4. Transform: kolom `revenue` = quantity x unit_price, kolom `month` | 5 | total revenue 3.273.759.911.000 |
| 5. Aggregate: revenue per kota dan per bulan | 6 | 8 kota; top 3: Jakarta 918.117.634.000, Surabaya 528.045.460.000, Bandung 457.990.352.000; 12 bulan; bulan tertinggi 2025-12 (280.072.930.000) |
| 6. Join: gabungkan dengan `stores.csv`, revenue per store_type | 5 | 40 toko; 0 baris tanpa pasangan; Supermarket 1.394.541.727.000, Ruko 1.082.502.474.000, Mall 796.715.710.000 |
| 7. SQL: muat ke SQLite, jalankan query revenue per kota, bandingkan dengan hasil pandas | 6 | hasil sama persis dengan langkah 5 (`same_as_pandas` True); load ke SQLite beberapa detik, query di bawah 1 detik (bervariasi) |
| 8. Load dan batas: simpan hasil ke `revenue_by_city.csv`, hitung memori per 1 juta baris, estimasi 100x | 4 | file hasil kecil (8 baris); memori setelah tipe dirapikan sekitar 136 MB; estimasi 100x sekitar 14 GB |

Langkah 0 (verifikasi environment) tetap ada sebelum langkah 1. Instalasi (.venv dan pip install) dikerjakan sebelum sesi lewat README Setup; di kelas, Langkah 0 hanya mengaktifkan environment, membuka notebook, dan memverifikasi versi serta file.

### Bagian B - Non-tabular (25 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 9. JSON bertingkat: baca `orders_app.json` dengan modul `json`, ratakan dengan `pd.json_normalize(record_path="items", meta=[...])`, hitung revenue, cocokkan dengan `retail_transactions.csv` lewat transaction_id | 10 | 2.000 order; 4.704 baris item, 10 kolom; 4.704 item cocok dengan CSV dan revenue sama (True); total revenue 17.362.020.000; order per channel: android 620, ios 694, web 686 |
| 10. Teks bebas: baca `reviews.csv`, hitung kata positif dan negatif dari kamus kecil di notebook, beri label positif/negatif/netral, join ke kota lewat transaction_id | 8 | 3.000 ulasan; positif 1.653, negatif 684, netral 663; kota dengan proporsi negatif tertinggi Medan (sekitar 0,28); tabel ulasan berkata "tidak": "Kualitas buruk, tidak sesuai foto." (128) negatif, benar; "Lumayan, tidak buruk untuk harga segini." (78) terbaca negatif, salah (maksudnya positif); "Tidak bagus, warnanya pudar." (67) terbaca netral, salah (maksudnya negatif) |
| 11. Gambar: baca setiap file di `product_images/` dengan Pillow, ambil metadata (lebar, tinggi, mode, ukuran file) dan rata-rata piksel (R, G, B, brightness) dengan numpy menjadi dataframe, lalu agregasi per kategori | 7 | 180 gambar; 88 berukuran 64x64 dan 92 berukuran 128x128; semua mode RGB; ukuran file 8.2-32.4 KB, total 3699 KB; brightness terendah electronics (sekitar 92,5), tertinggi beauty (sekitar 195,9) |

Pertanyaan penutup hands-on: "Kalau datanya 100 kali lebih besar, apa yang terjadi di laptopmu?" Untuk bagian B tambahkan: "Kalau gambarnya 1 juta file dan ulasannya 100 juta baris, tahap mana yang paling lambat?" Jawaban diarahkan ke memori, waktu, dan banyaknya file, bukan ke tools tertentu.

Pesan yang harus muncul dari bagian B: lima tahap tetap sama untuk data apa pun. Pekerjaan terbesar data non-tabular ada di tahap extract, yaitu mengubahnya menjadi baris dan kolom. Setelah menjadi dataframe, operasinya sama dengan bagian A (join, group by).

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Langkah 6 dan 7 harus memakai `stores.csv` dari Starter Kit, bukan membangkitkannya di notebook.
- Langkah 9-11 harus memakai `orders_app.json`, `reviews.csv`, dan `product_images/` dari Starter Kit, bukan membangkitkannya di notebook. Skrip pembangkit disimpan di Instructor Only: `generate_dataset_sesi01.py` (data tabular dan `stores.csv`) dan `generate_dataset_sesi01_nontabular.py` (data non-tabular).
- Memori di langkah 1 (sekitar 155 MB) berbeda dari langkah 8 (sekitar 136 MB) karena tipe timestamp sudah diubah. Jelaskan perbedaan ini di Catatan Trainer agar tidak membingungkan.
- Kamus sentimen langkah 10 ditulis langsung di notebook (sekitar 7 kata positif dan 8 kata negatif) dan dicocokkan per kata utuh (`\b`), supaya peserta bisa membacanya. Jangan memakai library NLP.
- Langkah 11 membuka gambar dengan `with Image.open(...)` supaya file tertutup. Kategori diambil dari nama file dengan aturan slug: huruf kecil, tanda "&" dihapus, spasi menjadi garis bawah (Home & Living menjadi `home_living`). Notebook memetakan slug kembali ke nama kategori di CSV (Beauty, Electronics, Fashion, Groceries, Home & Living, Sports) dengan dictionary, sehingga tabel hasil memakai nama yang sama dengan bagian A. Jika file gambar yang sudah ada memakai nama lain, samakan lewat skrip pembangkit, bukan lewat penggantian nama manual, lalu laporkan perubahannya.
- Sel langkah 10 di generator notebook harus ditulis sebagai raw string (`r"""..."""`). Di string Python biasa, `\b` pada regex berubah menjadi karakter backspace dan semua 3.000 ulasan terbaca netral tanpa error. Cocokkan hasil eksekusi dengan angka checkpoint, jangan hanya memastikan sel tidak error.
- Jika Pillow belum terpasang, galatnya `ModuleNotFoundError: No module named 'PIL'` (nama impor berbeda dari nama paket). Sebut di README Setup dan Catatan Trainer.
- Langkah 0 berhenti dengan `FileNotFoundError` yang jelas bila salah satu file data tidak ada, termasuk `orders_app.json`, `reviews.csv`, dan `product_images/`.
- Starter Kit tidak boleh berisi file hasil notebook (`retail.db`, `revenue_by_city.csv`) atau notebook yang sudah berisi output.
- Notebook dan Modul Praktikum memberi penanda **Bagian A (langkah 1-8)** dan **Bagian B (langkah 9-11)**, sama dengan agenda dan slide.
- Bagian B harus bisa dijalankan hanya dengan Langkah 0 (tanpa bagian A, atau setelah Restart Kernel). Langkah 9 membaca ulang kolom acuan dari `retail_transactions.csv` (variabel `ref`), dan langkah 10 memakai `ref` yang sama.
- Gambaran Alur di modul memuat pertanyaan bisnis bagian A dan bagian B (a, b, c).
- Slide klasifikasi struktur data menjelaskan di slide (bukan hanya speaker notes) kenapa `reviews.csv` tergolong tidak terstruktur walau formatnya CSV.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `1,575 MB`, `900347`, `0.28`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(1.575 MB)", "(3,27 triliun)", "(28%)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.
- Jangan menambahkan Parquet, Spark, atau Dask ke notebook.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live.

## Latihan Bertingkat
Tidak. Sesi ini cukup satu notebook dengan dua bagian.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S1-CK1 | Lima tahap | Lima tahap pada 8 transaksi nyata (TRX0000001 sampai TRX0000008): extract 8 baris; clean membuang TRX0000003 (REFUNDED) sehingga tersisa 7 baris; transform revenue = quantity x unit_price (TRX0000001: 10 x 1.060.000 = 10.600.000); aggregate per kota; load 4 baris hasil | Jakarta 23.002.000 (empat transaksi: 6.076.000, 4.520.000, 11.350.000, 1.056.000), Makassar 10.600.000, Semarang 3.180.000, Denpasar 71.000. Sumber: 8 baris pertama `retail_transactions.csv` | `addLabelRowsSlide` |
| S1-CK2 | Clean dan transform | Clean pada skala penuh: 1.000.000 baris menjadi 900.347. Yang dibuang: 69.741 CANCELLED dan 29.912 REFUNDED (99.653 baris, 9,97%) | Langkah 2 dan 3 | `addBeforeAfterSlide` |
| S1-CK3 | Non-tabular: nested JSON | Satu order bertingkat menjadi beberapa baris: APP000003 punya 4 item, `json_normalize` menghasilkan 4 baris, atribut order dan customer (order_id, created_at, channel, customer.tier, customer.city) diulang di tiap baris | `orders_app.json`: 2.000 order, 1 sampai 4 item per order. Sumber: Langkah 9 | `addComparisonTableSlide` |
| S1-TD1 | Lima tahap | Tebak: dari 1.000.000 transaksi, berapa yang tersisa setelah clean (hanya COMPLETED)? Pilihan: sekitar 500 ribu, 900 ribu, 990 ribu. Jawaban: 900.347 | Langkah 3 | `addTwoPanelSlide` (pertanyaan), `addStatSlide` (jawaban) |
| S1-TD2 | Aggregate | Tebak: dari 8 kota, kota mana yang revenue-nya terbesar dan kira-kira berapa? Jawaban: Jakarta 918.117.634.000 (918,1 miliar), disusul Surabaya 528,0 miliar dan Bandung 458,0 miliar | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |
| S1-TD3 | Batas satu mesin | Tebak: 1 juta baris memakai sekitar 136 MB; kalau data 100 kali lebih besar, berapa memorinya dan muat di laptop RAM 8 GB? Jawaban: sekitar 13,6 GB (14 GB), tidak muat | Langkah 8 | `addTwoPanelSlide`, `addStatSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 1 ditandai)
- Alur pemrosesan data klasik, dataframe dan SQL (dipadatkan): `addSectionSlide`, `addTimelineSlide` (lima tahap), `addBeforeAfterSlide` (data mentah vs data bersih), `addTwoPanelSlide` (pandas vs SQL untuk query revenue per kota). `addLabelRowsSlide` dan `addComparisonTableSlide` lama boleh dihapus atau dipindah ke speaker notes untuk menghemat waktu.
- Tabular vs non-tabular: `addSectionSlide`, `addComparisonTableSlide` (terstruktur, semi-terstruktur, tidak terstruktur: contoh retail, bentuk file, cara extract di pandas), `addLabelRowsSlide` (JSON bertingkat, teks bebas, gambar: dari bentuk asli ke dataframe)
- Hands-on A: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, termasuk Pillow dan file non-tabular), `addStepsCheckpointSlide` (langkah 1-4, lalu langkah 5-8), `addCodeSlide` (langkah 3 dan langkah 7, kode sama persis dengan sel notebook)
- Hands-on B: `addSectionSlide`, `addStepsCheckpointSlide` (langkah 9-11), `addCodeSlide` (langkah 9 json_normalize dan langkah 11 Pillow, kode sama persis dengan sel notebook), `addBeforeAfterSlide` (kamus sentimen: yang terbaca benar vs jebakan negasi)
- Batas pendekatan klasik: `addSectionSlide`, `addStatSlide` (angka dari langkah 1 dan langkah 8: 1 juta baris, sekitar 155 MB, estimasi 100x sekitar 14 GB; sumber: hasil hands-on dataset sintetis), `addNumberedListSlide` (empat tanda kewalahan: memori, waktu, satu mesin, banyaknya file)
- Penutup: `addClosingSlide` (ringkasan dan Sesi 2 Common vs Big Data), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Pendekatan klasik tidak salah. Untuk data yang muat di satu mesin, pandas dan SQL adalah pilihan yang tepat.
- Alur lima tahap tetap sama di sesi-sesi berikutnya dan untuk data apa pun; yang berubah adalah tempat dan cara menjalankannya.
- Data non-tabular harus diubah menjadi baris dan kolom dulu. Setelah itu, operasinya sama dengan data tabular.
- Kewalahan dilihat dari angka (memori, waktu, jumlah file), bukan dari perasaan "datanya besar".
- Sebelum menjalankan langkah 10, sampaikan bahwa ulasan "Lumayan, tidak buruk untuk harga segini." yang terbaca negatif memang disengaja untuk memperlihatkan batas kamus sederhana, bukan bug.

Pertanyaan yang kemungkinan muncul:
- "Kenapa pakai SQLite, bukan database yang kita pakai di kantor?" Jawab: SQLite cukup untuk memperlihatkan cara kerja SQL di database relasional tanpa instalasi server.
- "Apakah pandas bisa dipercepat?" Jawab singkat: bisa sampai batas tertentu (tipe data lebih hemat, baca per bagian), tetapi batas satu mesin tetap ada. Detail ke Sesi 2.
- "Kenapa baris CANCELLED dan REFUNDED dibuang?" Karena pertanyaan bisnisnya revenue dari transaksi yang selesai. Aturan ini harus disebut eksplisit.
- "Apakah sentimen ini akurat?" Tidak. Kamus kata gagal membaca negasi ("tidak buruk" terbaca negatif). Ini contoh batas aturan sederhana; metode yang lebih baik (model NLP) di luar sesi ini dan relevan dengan Sesi 10.
- "Kenapa total revenue JSON (17.362.020.000) jauh lebih kecil dari CSV?" Karena JSON hanya memuat 4.704 transaksi COMPLETED, bukan seluruh 900.347 transaksi. Yang dicocokkan adalah revenue per transaction_id.
- "Gambar kan bukan tabel, kenapa jadi dataframe?" Yang masuk dataframe adalah fitur yang diambil dari gambar (metadata dan rata-rata piksel), bukan gambarnya.

## Risiko teknis dan hal yang dicek sebelum sesi
- Laptop peserta dengan RAM 8 GB atau kurang: baca 1 juta baris butuh sekitar 155 MB sehingga aman, tetapi muat ke SQLite beberapa detik. Cek dan sampaikan agar peserta tidak mengira notebook macet.
- Beda versi pandas antara laptop peserta dan acuan (3.0.5): beberapa dtype dan format tampilan bisa berbeda. Pin versi di `requirements.txt` dan sertakan sel verifikasi versi.
- Pillow adalah library baru di Sesi 1. Peserta yang sudah memasang environment dari paket lama harus menjalankan ulang `pip install -r requirements.txt`. Sebut di README Setup.
- File CSV sekitar 93 MB dan `retail.db` yang terbentuk sekitar 98 MB, ditambah data non-tabular sekitar 5,5 MB: kirim dataset lewat folder bersama, bukan email. Sebutkan ruang disk yang dibutuhkan.
- Folder `product_images/` harus tersalin utuh (180 file). Jika peserta menyalin sebagian, checkpoint langkah 11 tidak cocok.
- Instalasi Python dan Jupyter di laptop peserta: Starter Kit memuat langkah verifikasi 5 menit, dan trainer menjalankan uji ini sebelum sesi.
- Hands-on A dipadatkan dari 55 menjadi 40 menit (sekitar 5 menit per langkah). Trainer menjalankan langkah 1-8 lebih cepat dan memakai checkpoint slide sebagai pegangan; penjelasan panjang pindah ke speaker notes. Cadangan bila waktu mepet: langkah 7 (SQL) dibawakan trainer sebagai demo, lalu langkah 11 (gambar) sebagai demo.
- Hands-on berjalan 65 menit berturut-turut (14.08 - 15.13). Beri satu titik berhenti singkat di akhir bagian A (cek checkpoint, tanya jawab) tanpa menambah waktu agenda.
- Angka waktu (baca, load SQLite) bervariasi antar mesin. Jangan menulis angka waktu sebagai fakta tetap di slide atau Answer Key.

## Istilah yang harus konsisten di semua file
- classical data processing, batch processing, pipeline
- extract, clean, transform, aggregate, load (lima tahap, urutan tetap)
- dataframe, vectorized operation
- tabular data, non-tabular data; structured, semi-structured, unstructured
- common data: data yang masih muat dan nyaman diproses di satu mesin; pasangan istilah ini dipakai di Sesi 2
- nested JSON, `json_normalize`, free text, sentiment lexicon (kamus sentimen; bukan "AI" atau "NLP"), image metadata, pixel
- transaksi COMPLETED (bukan "transaksi sukses")
- revenue = quantity x unit_price
- batas satu mesin (bukan "keterbatasan hardware")
- Nama dataset: `retail_transactions.csv`; dimension table: `stores.csv`; hasil: `revenue_by_city.csv`; non-tabular: `orders_app.json`, `reviews.csv`, `product_images/`; slug kategori gambar: `electronics`, `beauty`, `fashion`, `groceries`, `home_living`, `sports`
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 1 dibangun dan notebook dijalankan dengan pandas 3.0.5, numpy 2.5.4, pyarrow 26.0.1, Pillow 12.3.0. Seluruh angka checkpoint sama dengan Brief.
- Memori turun dari sekitar 155 MB ke sekitar 136 MB karena `transaction_ts` diubah dari teks ke datetime. Tanpa pyarrow atau dengan pandas 2.2, memori sekitar 483 MB dan 423 MB; revenue, jumlah baris, dan `same_as_pandas` tidak berubah.
- Sebagian laptop Windows memblokir `pyarrow` (galat "An Application Control policy has blocked this file", Smart App Control). Jalur cadangan: WSL Ubuntu sesuai `README_Setup.md` bagian 6. Smart App Control tidak boleh dimatikan.
- Dua skrip pembangkit data dibuat untuk pengajar: `generate_dataset_sesi01.py` dan `generate_dataset_sesi01_nontabular.py`.
- Belum diuji: `README_Setup.md` pada laptop Windows bersih.

## Keputusan terbuka
1. Teks asli poin 1-2 outline Mas Lindo belum saya terima. Judul poin sudah dikutip (Data Processing w/ Python, common data, dataframe; tabular dan non-tabular). Sesuaikan bila teks aslinya berbeda.
2. Modul self-study untuk detail pemrosesan data klasik: ditunda, diputuskan belakangan. Tidak memengaruhi paket Sesi 1.
3. Hands-on A 40 menit untuk 8 langkah: dicek saat gladi. Cadangan: langkah 7 dan langkah 11 dibawakan sebagai demo.
4. Jalur WSL Ubuntu untuk peserta yang diblokir Smart App Control (README bagian 6) belum diuji di laptop Windows bersih; uji saat gladi.
5. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
