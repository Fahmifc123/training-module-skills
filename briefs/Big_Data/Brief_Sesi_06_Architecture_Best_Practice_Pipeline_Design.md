# BRIEF SESI - Big Data

Sesi: 6 - Architecture Best Practice & Pipeline Design
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta membangun mini pipeline berlapis (raw, cleaned, curated) dengan PySpark, membuktikan pipeline aman dijalankan ulang dan menahan data cacat di quarantine, lalu memakai pola yang sama untuk memilih desain pada tiga kasus.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design (sesi ini)
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk tiga hal dari sesi sebelumnya: Sesi 1 (lima tahap extract, clean, transform, aggregate, load), Sesi 3 (Parquet dan partition berupa folder), dan Sesi 4-5 (batch dengan Spark, streaming dengan Kafka dan Flink). Slide penutup menyebut Sesi 7 "Use Case Implementation: Batch" dan Sesi 8 "Use Case Implementation: Real-Time", yang memakai pola dari sesi ini.

## Batasan cakupan
- Sesi ini membahas poin 7 outline: best practice arsitektur dan desain pipeline.
- Konsep inti yang dibawakan (keputusan Fahmi): layer data raw-cleaned-curated (pola medallion: bronze, silver, gold), idempotency dan rerun aman, serta data quality dan baris gagal (quarantine).
- Pola batch, streaming, atau gabungan keduanya (lambda dan kappa) hanya satu slide sekilas yang merujuk Sesi 4-5, sebagai dasar latihan desain. Tidak diajarkan mendalam.
- Orkestrasi (penjadwalan), monitoring (observability), dan schema yang berubah hanya slide sekilas, tanpa hands-on.
- Hands-on memakai PySpark lokal (keputusan Fahmi), dengan environment yang sama dengan Sesi 4. Tidak ada Kafka dan Flink di hands-on sesi ini (Sesi 5 dan Sesi 8), tidak ada Airflow atau alat orkestrasi, tidak ada Delta Lake atau Iceberg.
- Tidak ada Docker, platform cloud, dan Databricks. Platform cloud di Sesi 9.
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.
- Pipeline penuh untuk use case ada di Sesi 7 dan 8. Sesi ini memberi pola dan kebiasaan desain, bukan use case lengkap.

## Tujuan belajar (maksimal 4)
1. Menjelaskan tugas tiap layer data (raw, cleaned, curated) dan kenapa dipisah.
2. Menjelaskan idempotency dan membuktikan pipeline aman dijalankan ulang tanpa menggandakan hasil.
3. Memasang aturan data quality dan memisahkan baris gagal ke quarantine beserta alasannya, tanpa merusak hasil.
4. Memilih desain pipeline (batch, stream, atau keduanya, dan letak layer serta pengecekan kualitas) untuk sebuah kasus.

## Konsep inti (urutan penyampaian)
1. Kenapa pipeline gagal di produksi: data kotor, dijalankan dua kali, perubahan di tengah jalan. Rujuk lima tahap Sesi 1.
2. Layer data: raw (disimpan apa adanya, tidak diubah), cleaned (tipe benar dan lolos aturan), curated (agregat siap pakai). Tiap layer bisa dibangun ulang dari layer sebelumnya.
3. Idempotency: menjalankan pipeline dua kali menghasilkan hasil yang sama. Dua cara menulis hasil: menambah (append) menggandakan data; menimpa per partisi (overwrite) aman.
4. Data quality: aturan yang diperiksa, baris yang gagal masuk quarantine dengan alasan, dan jumlah lolos ditambah quarantine harus sama dengan jumlah masuk.
5. Sekilas: pola batch, stream, atau keduanya; orkestrasi, monitoring, schema yang berubah.

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1. Pertanyaan bisnis: revenue transaksi COMPLETED per kota per bulan, tetapi sekarang dibangun sebagai pipeline berlapis yang bisa dijalankan ulang dan tahan data cacat.

Dataset utama: `retail_transactions.csv` dari Sesi 1 (sintetis, bukan data internal Insignia atau klien; 1.000.000 baris, seed 42). Dipakai penuh supaya hasil curated bisa dicocokkan dengan angka Sesi 1 (total revenue 3.273.759.911.000, 900.347 transaksi COMPLETED). Peserta yang belum punya file ini memakai file Sesi 1; notebook memeriksa keberadaannya dan memberi pesan jelas jika tidak ada.

Dataset tambahan: `retail_transactions_batch2.csv` (sintetis, sekitar 0,5 MB, 5.500 baris), batch kedua berisi data cacat yang sengaja dibuat. Dibuat oleh `make_batch2_s06.py` (disimpan di Instructor Only; Starter Kit menyertakan file jadi) dari baris-baris pertama `retail_transactions.csv`:
- 5.000 baris bersih dengan `transaction_id` berawalan `B2-` (4.524 di antaranya COMPLETED; revenue COMPLETED 16.765.871.000)
- 100 baris `city` kosong, 100 baris `quantity` negatif, 100 baris `status` = `UNKNOWN`, 100 baris `transaction_ts` tidak valid (`2025-13-45 99:99:99`), dan 100 baris `transaction_id` ganda (salinan 100 baris bersih di atas)
- Total 500 baris cacat. Semua baris batch 2 jatuh pada Januari 2025.

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing, PySpark mode lokal. Environment sama dengan Sesi 4 (keputusan Fahmi), jadi peserta tidak memasang apa pun yang baru.
- Python 3.12 ke atas, Java 17 atau lebih baru dengan `JAVA_HOME` terpasang (diuji dengan Java 21), `pyspark==4.3.0`, `pandas==3.0.5`, `numpy==2.5.4`, `pyarrow==26.0.1`, sama dengan Sesi 4. Pandas 3 menimbulkan `FutureWarning` dari PySpark; itu normal dan tidak memengaruhi hasil. Jelaskan di Catatan Trainer.
- Jangan memakai environment Sesi 5 (Python 3.12 dengan pandas 2.2.3) untuk sesi ini.
- Sesi 6 mewarisi hal yang di Sesi 4 masih terbuka: cara pasang Java di Windows dan pengujian Windows belum dilakukan.
- Ruang disk: layer hasil sekitar 34 MB dan demo `append` (folder `lake_naive`) sekitar 79 MB, ditambah CSV Sesi 1 sekitar 93 MB. Sediakan minimal 500 MB kosong.
- Angka checkpoint dari eksekusi notebook di WSL Ubuntu (Python 3.12.16 dan 3.13.18, Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1); semua angka sama pada kedua versi Python.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 5, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.10 | Kenapa pipeline gagal; layer raw-cleaned-curated; idempotency; data quality | Konsep | 30 mnt |
| 14.10 - 14.20 | Batch, stream, atau keduanya; orkestrasi, monitoring, schema berubah (sekilas) | Konsep | 10 mnt |
| 14.20 - 15.15 | Hands-on: mini pipeline (40 mnt), latihan desain (15 mnt) | Hands-on | 55 mnt |
| 15.15 - 15.30 | Recap, jembatan ke Sesi 7 dan Sesi 8 | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 (Konsep +5 menit, hands-on -5 menit, total tetap 120) karena penambahan slide penjelasan mekanisme idempotency dan data quality.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, dua bagian. Bagian A: mini pipeline berlapis dengan PySpark (langkah 1-5). Bagian B: latihan desain (langkah 6). Hasil acuan di bawah dari eksekusi nyata. Angka waktu dan ukuran file bervariasi antar laptop, jadi tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

### Bagian A - Pipeline (40 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: versi Python dan PySpark, Java, file `retail_transactions.csv` dan `retail_transactions_batch2.csv` ada (di kelas tidak mengulang instalasi), buat SparkSession dengan `partitionOverwriteMode` = `dynamic` | dikerjakan sebelum sesi | versi tercetak; berhenti dengan galat jelas bila file atau Java tidak ada |
| 1. Raw: baca CSV apa adanya (semua kolom teks) dan simpan ke layer raw sebagai Parquet, partisi `batch_id=b1` | 8 | 1.000.000 baris masuk; ukuran layer raw sekitar 16,6 MB |
| 2. Cleaned: pasang tipe data dan aturan kualitas; baris gagal masuk quarantine dengan kolom `reason`; periksa lolos + quarantine = masuk | 10 | lolos 1.000.000, quarantine 0 (data Sesi 1 bersih); lolos + quarantine = 1.000.000 |
| 3. Curated: revenue COMPLETED per kota per bulan dari layer cleaned, tulis partisi per `month` | 8 | 96 baris (8 kota x 12 bulan); total revenue `3273759911000` (3,27 triliun) sama dengan acuan Sesi 1; 900347 transaksi |
| 4. Rerun: jalankan batch 1 lagi. Bandingkan versi `overwrite` per partisi dengan versi `append` yang dijalankan dua kali | 7 | versi overwrite: total tetap `3273759911000`, 900347 transaksi; versi append dua kali: total `6547519822000` (6,55 triliun) dan 1800694 transaksi, tepat dua kali lipat |
| 5. Batch kotor: jalankan batch 2 (`retail_transactions_batch2.csv`), lihat isi quarantine, bangun ulang curated, lalu jalankan batch 2 sekali lagi | 7 | 5.500 masuk, 5.000 lolos, 500 quarantine: `ts_tidak_valid` 100, `city_kosong` 100, `quantity_tidak_valid` 100, `status_tidak_dikenal` 100, `id_ganda` 100; curated tetap 96 baris, total `3290525782000` (3,29 triliun), 904871 transaksi; selisih dari batch 1 = 16.765.871.000 (4.524 transaksi COMPLETED batch 2); jalankan ulang batch 2: angka tidak berubah |

### Bagian B - Latihan desain (15 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 6. Tiga kasus fiktif generik: (a) laporan penjualan bulanan untuk manajemen, (b) deteksi transaksi mencurigakan yang harus diketahui dalam hitungan detik, (c) dashboard penjualan yang harus segar tiap menit tetapi juga akurat saat tutup bulan. Untuk tiap kasus peserta menentukan batch, stream, atau keduanya, letak layer, dan di layer mana pengecekan kualitas dipasang | 15 | tabel keputusan terisi untuk 3 kasus. Acuan diskusi: (a) batch, (b) stream, (c) keduanya. Ini bahan diskusi, bukan satu jawaban benar |

Pertanyaan penutup hands-on: "Kalau batch kemarin ternyata salah dan harus diulang, bagian mana dari pipeline-mu yang aman diulang dan bagian mana yang tidak?" Jawaban diarahkan ke idempotency dan layer yang bisa dibangun ulang, bukan ke tools.

Pesan yang harus muncul dari langkah 4: pipeline yang tidak idempotent menghasilkan angka yang salah tanpa galat. Dari langkah 5: data cacat tidak dibuang diam-diam; jumlah lolos ditambah quarantine selalu sama dengan jumlah masuk.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Pengaturan `spark.sql.sources.partitionOverwriteMode` = `dynamic` diperlukan agar `overwrite` hanya menimpa partisi `batch_id` yang ditulis. Tanpa itu, perilaku bawaan `overwrite` menimpa seluruh folder layer, yang menghapus batch lain.
- Konversi tipe dan tanggal memakai `try_cast` dan `try_to_timestamp` supaya invalid values menjadi NULL dan masuk quarantine, bukan menghentikan job. Spark 4 menjalankan mode ANSI secara bawaan, sehingga `cast` dan `to_timestamp` biasa bisa menghentikan job; verifikasi di notebook.
- Aturan kualitas diperiksa berurutan dan alasan pertama yang gagal dicatat: `id_kosong`, `ts_tidak_valid`, `city_kosong`, `quantity_tidak_valid`, `price_tidak_valid`, `status_tidak_dikenal`. Baris lolos yang `transaction_id`-nya ganda dalam satu batch: kemunculan pertama dipertahankan, sisanya ke quarantine dengan `id_ganda`. Salinan ganda identik, jadi salinan mana yang dipertahankan tidak memengaruhi angka.
- Jebakan nyata: Spark tidak menulis file apa pun untuk DataFrame kosong. Pada batch 1 quarantine kosong, sehingga membaca balik folder quarantine gagal dengan `UNABLE_TO_INFER_SCHEMA`. Hitung lolos dan quarantine dari DataFrame sebelum menulis, jangan membaca balik. Sebut galat ini di Catatan Trainer.
- Curated dibangun ulang penuh dari seluruh layer cleaned dan ditimpa setiap kali dijalankan (aman karena kecil).
- Cek duplikat hanya dalam satu batch. Duplikat lintas batch tidak dicek di hands-on ini; sebut sebagai batas dan bahan diskusi di Catatan Trainer.
- Demo `append` memakai folder terpisah (`lake_naive`) supaya tidak merusak layer utama. Notebook menghapus folder hasil lama di awal supaya sel bisa dijalankan berulang.
- Hasil acuan: waktu batch 1 sekitar 25 detik (termasuk start JVM) dan bangun curated sekitar 2 detik pada mesin 2 core; puncak memori proses (Python ditambah JVM, disampel tiap 0,5 detik) sekitar 1,7 GB. Waktu bukan checkpoint. RAM 8 GB cukup; Claude Code mengukur ulang puncak memori proses, bukan memori dataframe, dan melaporkan.
- Uji notebook lewat eksekusi sebagai notebook, bukan hanya sebagai skrip. Laporkan hasil uji ini.
- Jangan menambahkan Kafka, Flink, Airflow, Delta Lake, atau Iceberg.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `3273759911000`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(3,27 triliun)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live. Latihan desain (langkah 6) memakai tabel di Modul Praktikum dan slide, bukan sel kode.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S6-CK1 | Layer raw, cleaned, curated | Dua baris melewati tiga layer. B2-0000001 (normal): raw (string apa adanya), cleaned (lolos aturan, tipe diperbaiki), curated (ikut agregat). B2-0005001 (city kosong): raw, gagal aturan `city_kosong`, masuk quarantine dengan `reason`, tidak masuk curated | Batch 2, `retail_transactions_batch2.csv` | `addLabelRowsSlide` |
| S6-CK2 | Idempotency | Dijalankan dua kali: overwrite per partition tetap 96 baris, total 3.273.759.911.000, 900.347 transaksi; append menjadi total 6.547.519.822.000 dan 1.800.694 transaksi (kelipatan 2,0) | Langkah 4 | `addBeforeAfterSlide` |
| S6-CK3 | Data quality | Lima aturan, lima contoh baris batch 2 (100 baris per aturan): `city_kosong` (B2-0005001), `quantity_tidak_valid` (B2-0005101, quantity -8), `status_tidak_dikenal` (B2-0005201, UNKNOWN), `ts_tidak_valid` (B2-0005301, `2025-13-45 99:99:99`), `id_ganda` (B2-0000001 muncul dua kali). Masuk 5.500, lolos 5.000, quarantine 500 | Langkah 5 | `addComparisonTableSlide` |
| S6-TD1 | Data quality | Tebak: dari batch 2, berapa baris masuk quarantine dan berapa tambahan transaksi COMPLETED di curated? Jawaban: 500 baris; 4.524 transaksi dan revenue 16.765.871.000 | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |
| S6-TD2 | Idempotency | Tebak: batch 2 dijalankan dua kali, apakah revenue berubah? Jawaban: tidak, tetap 3.290.525.782.000; partisi cleaned `batch_id=b1` dan `batch_id=b2` | Langkah 5 | `addTwoPanelSlide`, `addBeforeAfterSlide` |
| S6-TD3 | Batch atau stream | Kasus (b) deteksi transaksi mencurigakan dalam hitungan detik: batch, stream, atau keduanya? Kasus (c) dashboard segar tiap menit dan akurat saat tutup bulan? Jawaban: stream; keduanya | Langkah 6 | `addTwoPanelSlide`, `addComparisonTableSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 6 ditandai)
- Kenapa pipeline gagal dan layer data: `addSectionSlide`, `addBeforeAfterSlide` (satu skrip langsung dari sumber ke laporan vs pipeline berlapis), `addTimelineSlide` (raw, cleaned, curated, dengan tugas tiap layer), `addLabelRowsSlide` (aturan tiap layer: apa yang boleh dan tidak boleh diubah)
- Idempotency dan data quality: `addSectionSlide`, `addBeforeAfterSlide` (append dijalankan dua kali menggandakan angka vs overwrite per partisi tetap sama), `addComparisonTableSlide` (aturan kualitas, contoh cacat, alasan di quarantine), `addStatSlide` (angka: 5.500 masuk, 5.000 lolos, 500 quarantine; sumber: hasil hands-on dataset sintetis)
- Sekilas: `addNumberedListSlide` (batch, stream, atau keduanya; orkestrasi, monitoring, schema berubah)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, Java, file data), `addStepsCheckpointSlide` (langkah 1-3 lalu langkah 4-6), `addCodeSlide` (maks 18 baris: aturan kualitas langkah 2 dan penulisan overwrite per partisi langkah 4)
- Penutup: `addNumberedListSlide` (tiga pertanyaan desain untuk pipeline baru), `addClosingSlide` (ringkasan, Sesi 7 Use Case Implementation: Batch, Sesi 8 Use Case Implementation: Real-Time), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Pipeline yang baik bukan yang tidak pernah gagal, tetapi yang aman diulang dan jelas apa yang gagal.
- Simpan data mentah apa adanya. Layer lain bisa dibangun ulang dari raw.
- Jangan menggandakan hasil saat dijalankan ulang (idempotency). Angka yang salah tanpa galat lebih berbahaya daripada galat.
- Baris cacat dipisah dan dihitung, bukan dibuang diam-diam. Lolos ditambah quarantine sama dengan masuk.
- Pola yang sama berlaku untuk batch dan stream. Tools boleh berbeda, kebiasaan desain sama.

Pertanyaan yang kemungkinan muncul:
- "Kenapa raw disimpan semua kolom sebagai teks?" Jawab: supaya tidak ada data yang hilang atau berubah saat masuk. Tipe baru dipasang di cleaned.
- "Kenapa tidak langsung dibuang saja baris yang salah?" Jawab: baris yang dibuang diam-diam membuat angka tidak bisa dipertanggungjawabkan. Quarantine memberi bukti dan bisa diperbaiki lalu dimasukkan lagi.
- "Apa bedanya ini dengan data lake, warehouse, lakehouse di Sesi 3?" Jawab: Sesi 3 membahas tempat menyimpan; sesi ini membahas cara menyusun alur data di atasnya. Layer medallion biasa dipakai di lakehouse.
- "Bagaimana kalau duplikat datang di batch berbeda?" Jawab: hands-on ini hanya memeriksa duplikat dalam satu batch; duplikat lintas batch butuh aturan tambahan dan dibahas sebagai batas.
- "Kenapa ada FutureWarning pandas?" Jawab: PySpark 4.3.0 belum sepenuhnya mendukung pandas 3; hasil tidak terpengaruh.

## Risiko teknis dan hal yang dicek sebelum sesi
- Sesi 6 mewarisi risiko Sesi 4: instalasi PySpark besar (sekitar 456 MB diunduh) dan Java di luar `pip`. Windows asli gagal menulis Parquet (`HADOOP_HOME and hadoop.home.dir are unset`); peserta Windows mengerjakan sesi ini di WSL2 dengan `.venv` baru (sekitar 934 MB). Peserta memasang environment sebelum hari sesi.
- Hands-on membuat banyak folder dan file Parquet (layer raw, cleaned, quarantine, curated, dan `lake_naive`). Notebook menghapus folder lama di awal. Sediakan sel pembersihan di akhir.
- Memori: puncak proses 1.773 MB (Python 3.12) dan 1.727 MB (Python 3.13); dengan memori dibatasi 4 GB tanpa swap puncak 2.030 MB termasuk page cache. RAM 8 GB cukup; belum diuji di laptop peserta.
- Hands-on 55 menit padat (PySpark ditambah latihan desain). Cadangan bila waktu mepet: langkah 5 (batch kotor) dibawakan trainer sebagai demo, atau latihan desain dipotong menjadi diskusi dua kasus.
- Angka waktu dan ukuran file bervariasi antar mesin dan versi Spark. Hanya nilai hasil (jumlah baris, total revenue, jumlah per alasan quarantine) yang boleh dijadikan checkpoint.
- Rujukan lintas sesi: partisi `batch_id=` dan `month=` adalah partition berupa folder, sama dengan arti di Sesi 3. Bukan arti baru.
- Data batch 2 sintetis dan cacatnya sengaja dibuat. Sebut ini di slide dan Modul Praktikum.

## Istilah yang harus konsisten di semua file
- pipeline, layer (raw, cleaned, curated); medallion (bronze, silver, gold) hanya disebut sebagai padanan istilah industri
- idempotency, idempotent, rerun, append, overwrite per partition
- data quality, quality rule, quarantine, `reason`
- batch 1, batch 2, `batch_id`
- partition: tetap berarti folder (Sesi 3) pada `batch_id=` dan `month=`; jangan dicampur dengan Spark partition (Sesi 4) atau Kafka partition (Sesi 5)
- batch, stream, lambda, kappa (hanya disebut sekilas)
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama dataset: `retail_transactions.csv` (Sesi 1), `retail_transactions_batch2.csv` (Sesi 6), folder `lake/` dengan `raw/`, `cleaned/`, `quarantine/`, `curated/`, dan `lake_naive/` untuk demo append
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 6 dibangun dan notebook dijalankan di WSL Ubuntu dengan Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1. Angka sama pada Python 3.12.16 dan 3.13.18, dan sama dengan Brief.
- Windows asli: PySpark gagal menulis Parquet (`HADOOP_HOME and hadoop.home.dir are unset`). Peserta Windows mengerjakan Sesi 6 (dan 7, 10) di WSL2; notebook berhenti dengan pesan jelas bila dibuka di Windows.
- Mode ANSI Spark 4: `cast` biasa menghentikan job; aturan data quality memakai `try_cast` dan `try_to_timestamp` sehingga nilai tidak valid menjadi NULL dan baris masuk quarantine. Data batch 1 bersih, quarantine 0 itu wajar.
- Spark tidak menulis file untuk DataFrame kosong, sehingga membaca balik folder quarantine batch 1 gagal (`UNABLE_TO_INFER_SCHEMA`); notebook menghitung dari DataFrame sebelum menulis.
- Memori: puncak proses 1.773 MB (Python 3.12) dan 1.727 MB (Python 3.13); dengan memori dibatasi 4 GB tanpa swap puncak 2.030 MB termasuk page cache. `.venv` di WSL sekitar 934 MB. Spark sekitar 1 menit dari 55 menit hands-on pada laptop 12 core; di laptop 2 core perkirakan dua sampai tiga kali lipat.
- Belum diuji: `wsl --install` dan restart di laptop peserta, laptop RAM 8 GB sungguhan, macOS.

## Keputusan terbuka
1. Teks asli poin 7 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi, urutan modul, dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Tiga kasus latihan desain (laporan bulanan, deteksi transaksi mencurigakan, dashboard segar dan akurat) adalah usulan saya dan belum Anda tinjau. Konfirmasi atau ganti.
3. Slide pola batch, stream, lambda, kappa hanya sekilas karena bukan konsep inti yang Anda pilih, tetapi latihan desain bergantung padanya. Konfirmasi kedalamannya.
4. Hands-on 55 menit untuk dua bagian dinilai padat. Dicek saat gladi. Cadangan: langkah 5 sebagai demo.
5. `wsl --install` dan restart di laptop peserta, laptop RAM 8 GB sungguhan, dan macOS belum diuji.
6. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
