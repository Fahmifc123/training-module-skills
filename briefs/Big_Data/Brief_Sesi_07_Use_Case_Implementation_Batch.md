# BRIEF SESI - Big Data

Sesi: 7 - Use Case Implementation: Batch
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta menjalankan batch pipeline end-to-end di atas 10 juta transaksi retail sebagai skrip Spark berparameter, memprosesnya per bulan secara inkremental menjadi tiga tabel laporan, lalu menangani late-arriving data dengan menjalankan ulang satu bulan saja.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch (sesi ini)
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk lima hal dari sesi sebelumnya: Sesi 1 (`stores.csv`, angka revenue per kota dan per tipe toko), Sesi 2 (revenue COMPLETED 10 juta baris, `32.737.599.110.000`), Sesi 3 (Parquet terpartisi per bulan), Sesi 4 (Spark membaca Parquet dan partition pruning), dan Sesi 6 (layer raw-cleaned-curated, idempotency, quarantine). Slide penutup menyebut Sesi 8 "Use Case Implementation: Real-Time" (versi stream dari pertanyaan yang sama) dan Sesi 9 "Cloud Approach for Big Data Solution" (tempat pipeline ini dijalankan terjadwal).

## Batasan cakupan
- Sesi ini membahas poin 8 outline: implementasi use case batch.
- Use case yang diimplementasikan (keputusan Fahmi): lanjutan laporan retail end-to-end. Sumber data 10 juta baris Parquet terpartisi per bulan dari Sesi 3 (keputusan Fahmi).
- Konsep dan keterampilan baru yang dibawakan (keputusan Fahmi): (1) proses inkremental per bulan, (2) pipeline sebagai skrip berparameter, (3) dimension join dan laporan multi-tabel.
- Tuning (jumlah shuffle partition, cache, membaca plan untuk mencari langkah mahal) tidak dibawakan. Hanya disebut sekilas bila ada pertanyaan.
- Layer, idempotency, dan quarantine sudah diajarkan di Sesi 6. Di sesi ini dipakai ulang tanpa penjelasan dari nol; cukup merujuk balik.
- Penjadwalan (cron, Airflow), monitoring, dan menjalankan pipeline di cloud hanya disebut sekilas sebagai jembatan ke Sesi 9. Tidak ada hands-on-nya.
- `spark-submit` hanya disebut sekilas. Skrip dijalankan dengan `python pipeline_s07.py` pada mode lokal.
- Tidak ada Kafka, Flink, Docker, platform cloud, Databricks, Delta Lake, dan Iceberg.
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.
- Versi stream dari pertanyaan yang sama ada di Sesi 8. Jangan mengajarkan streaming di sesi ini.

## Tujuan belajar (maksimal 4)
1. Menjelaskan perbedaan notebook eksplorasi dan pipeline yang dijalankan sebagai skrip berparameter.
2. Menjalankan batch pipeline inkremental per bulan di atas Parquet terpartisi, dan membuktikan hasil gabungan 12 bulan sama dengan hasil keseluruhan.
3. Membangun beberapa tabel laporan (curated) dari satu layer cleaned, termasuk join dengan dimension table.
4. Menangani late-arriving data dengan menjalankan ulang hanya bulan yang terdampak, dan membuktikan bulan lain tidak tersentuh.

## Konsep inti (urutan penyampaian)
1. Dari notebook ke pipeline: notebook cocok untuk menjelajah, pipeline dijalankan berulang tanpa orang. Logika dipindah ke skrip dengan parameter (di sini bulan, sumber, folder hasil), supaya bisa dijalankan dari terminal atau penjadwal.
2. Proses inkremental: hanya memproses partisi yang berubah, bukan seluruh 10 juta baris. Syaratnya data terpartisi per bulan (Sesi 3), pembacaan hanya partisi yang dibutuhkan (partition pruning, Sesi 4), dan penulisan menimpa hanya partisi itu (overwrite dinamis per partisi, Sesi 6).
3. Satu layer cleaned, banyak konsumen: tiga tabel curated untuk kebutuhan laporan berbeda (revenue per kota per bulan, per tipe toko per bulan, 10 produk teratas per bulan). Tabel per tipe toko memakai join dengan dimensi `stores.csv` (Sesi 1).
4. Late-arriving data (late-arriving data): file koreksi untuk bulan yang sudah diproses datang belakangan. Cukup jalankan ulang bulan itu dengan late-arriving data; baris cacat masuk quarantine. Jalankan ulang tanpa late-arriving data mengembalikan hasil awal.
5. Sekilas: penjadwalan dan monitoring pipeline, dan pipeline di cloud (Sesi 9).

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1-6. Pertanyaan bisnis: laporan bulanan revenue transaksi COMPLETED per kota, per tipe toko, dan 10 produk teratas, yang dihasilkan oleh batch pipeline yang bisa dijalankan per bulan.

Dataset sumber: folder Parquet terpartisi per bulan hasil Sesi 3 (sintetis, bukan data internal Insignia atau klien): 10.000.000 baris, 12 folder `month=2025-01` sampai `month=2025-12`, kolom `transaction_id`, `transaction_ts`, `store_id`, `city`, `category`, `product_id`, `quantity`, `unit_price`, `payment_method`, `status`, `month`. Nama folder mengikuti paket Sesi 3. Peserta yang belum punya folder ini menjalankan skrip fallback yang sama dengan Sesi 4; notebook memeriksa keberadaannya dan memberi pesan jelas jika tidak ada.

Dimensi: `stores.csv` dari Sesi 1 (40 baris: `store_id`, `store_type`, `opened_year`). Seluruh 40 toko punya pasangan.

Late-arriving data: `susulan_2025-03.csv` (sintetis, sekitar 0,1 MB, 1.000 baris) dibuat oleh `make_susulan_s07.py` (disimpan di Instructor Only; Starter Kit menyertakan file jadi). Isinya 1.000 baris Maret 2025 pertama dari `retail_transactions.csv` Sesi 1 dengan `transaction_id` berawalan `S7-`, dengan cacat sengaja: 10 baris pertama `quantity` negatif, 10 baris berikutnya `status` = `UNKNOWN`. Sisa 980 baris bersih, 896 di antaranya COMPLETED dengan revenue `3499398000` (3,5 miliar).

Acuan hasil keseluruhan 12 bulan (semua turunan Sesi 1 dikali 10): 9.003.470 transaksi COMPLETED, total revenue `32737599110000` (32,7 triliun).

## Platform dan tools peserta
Lokal: Jupyter Notebook dan VS Code di laptop masing-masing, PySpark mode lokal. Environment sama dengan Sesi 4 dan Sesi 6 (keputusan Fahmi), jadi peserta tidak memasang apa pun yang baru.
- Python 3.12 ke atas, Java 17 atau lebih baru dengan `JAVA_HOME` terpasang (diuji dengan Java 21), `pyspark==4.3.0`, `pandas==3.0.5`, `numpy==2.5.4`, `pyarrow==26.0.1`, sama dengan Sesi 4. Pandas 3 menimbulkan `FutureWarning` dari PySpark; normal dan tidak memengaruhi hasil.
- Jangan memakai environment Sesi 5 (Python 3.12 dengan pandas 2.2.3).
- Sesi 7 mewarisi hal yang di Sesi 4 masih terbuka: cara pasang Java di Windows dan pengujian Windows belum dilakukan.
- Ruang disk: folder Parquet Sesi 3 sekitar 225 MB, folder hasil sekitar 171 MB setelah semua langkah. Sediakan minimal 1 GB kosong.
- Angka checkpoint dari eksekusi notebook di WSL Ubuntu (Python 3.12.16 dan 3.13.18, Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1); notebook menjalankan skrip pipeline sebagai proses terpisah. Semua angka sama pada kedua versi Python.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 6, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.00 | Dari notebook ke pipeline; skrip berparameter; proses inkremental | Konsep | 20 mnt |
| 14.00 - 14.15 | Satu layer cleaned untuk banyak laporan; dimension join; late-arriving data | Konsep | 15 mnt |
| 14.15 - 15.15 | Hands-on: batch pipeline inkremental | Hands-on | 60 mnt |
| 15.15 - 15.30 | Recap, jembatan ke Sesi 8 dan Sesi 9 | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

Catatan: agenda diubah 12 November 2026 (Konsep +5 menit, hands-on -5 menit, total tetap 120) karena penambahan slide penjelasan mekanisme (alur proses inkremental dan late-arriving data).

## Rancangan hands-on
Satu notebook, satu skrip pipeline. Skrip `pipeline_s07.py` sudah lengkap di Starter Kit; peserta membacanya, menjalankannya dari notebook dengan parameter berbeda, dan memeriksa hasilnya. Hasil acuan di bawah dari eksekusi nyata. Angka waktu dan ukuran file bervariasi antar laptop, jadi tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

Rancangan skrip (supaya hasilnya identik dengan acuan):
- Parameter: `--month` (misal `2025-03`, atau `all`), `--source` (folder Parquet), `--stores` (`stores.csv`), `--lake` (folder hasil), `--susulan` (opsional, CSV late-arriving data). Untuk `all`, bulan diambil dari nama folder `month=` di sumber dan diproses berurutan dalam satu proses.
- Baca satu bulan dengan filter `month` (partition pruning). Jika ada late-arriving data, baca CSV-nya dengan konversi tipe aman (`try_cast`, `try_to_timestamp`), hitung kolom `month` dari `transaction_ts`, ambil hanya baris bulan itu, lalu gabungkan dengan data sumber.
- Aturan kualitas sama dengan Sesi 6, diperiksa berurutan dan alasan pertama yang gagal dicatat: `id_kosong`, `ts_tidak_valid`, `city_kosong`, `quantity_tidak_valid`, `price_tidak_valid`, `status_tidak_dikenal`; lalu `transaction_id` ganda dalam satu bulan (kemunculan pertama dipertahankan, sisanya `id_ganda`).
- Tulis layer `cleaned` (partisi `month`) dan `quarantine` (partisi `month`, kolom `reason`). Hapus dulu folder `quarantine/month=<bulan>` sebelum menulis, lalu tulis quarantine hanya jika ada baris gagal.
- Dari baris COMPLETED di cleaned (revenue = quantity x unit_price), tulis tiga tabel curated, masing-masing dipartisi `month` dan memakai overwrite dinamis (`spark.sql.sources.partitionOverwriteMode` = `dynamic`):
  1. `curated/revenue_by_city_month`: kolom `city`, `month`, `revenue`, `n_trx`.
  2. `curated/revenue_by_store_type_month`: join kiri dengan `stores.csv` lewat `store_id`; kolom `store_type`, `month`, `revenue`, `n_trx`.
  3. `curated/top_products_month`: 10 produk teratas per bulan; kolom `product_id`, `month`, `revenue`, `rank`. Urutan: `revenue` menurun lalu `product_id` menaik (supaya hasil deterministik).
- Skrip mencetak satu baris ringkasan per bulan yang diawali `HASIL`: `bulan`, `masuk`, `lolos`, `quarantine`, `completed`, `revenue`.

| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: versi Python dan PySpark, Java, folder Parquet Sesi 3 (12 folder `month=`), `stores.csv`, `susulan_2025-03.csv`, `pipeline_s07.py` ada (di kelas tidak mengulang instalasi) | dikerjakan sebelum sesi | versi tercetak; berhenti dengan galat jelas bila ada yang kurang |
| 1. Baca skrip `pipeline_s07.py` bagian demi bagian: parameter, baca satu bulan, aturan kualitas, tiga tabel curated | 10 | peserta bisa menyebut tempat parameter bulan dipakai dan di mana partition pruning terjadi |
| 2. Jalankan satu bulan: `--month 2025-03` | 10 | masuk 844330 (844.330, sama dengan Sesi 3 dan 4), lolos 844330, quarantine 0, completed 760280, revenue `2754082270000` (2,75 triliun) |
| 3. Jalankan semua bulan: `--month all` | 10 | 12 baris `HASIL`; jumlah `masuk` seluruh bulan 10.000.000; bulan terbesar Januari (853460 baris), terkecil Februari (768900 baris); Januari revenue `2787832110000`, Desember `2800729300000` |
| 4. Verifikasi tabel curated: baca tiga tabel, jumlahkan, bandingkan dengan acuan Sesi 1 dikali 10 | 10 | `revenue_by_city_month` 96 baris, total `32737599110000` (32,7 triliun), 9003470 transaksi; `revenue_by_store_type_month` 36 baris, total sama, Supermarket `13945417270000`, Ruko `10825024740000`, Mall `7967157100000`; `top_products_month` 120 baris (12 bulan x 10), rank tertinggi 10; revenue per bulan sama dengan Sesi 1 dikali 10 (`equal` True) |
| 5. Late-arriving data Maret: `--month 2025-03 --susulan susulan_2025-03.csv`; periksa quarantine; bandingkan total sebelum dan sesudah; bulan lain tidak tersentuh | 12 | masuk 845330, lolos 845310, quarantine 20 (`quantity_tidak_valid` 10, `status_tidak_dikenal` 10), completed 761176, revenue Maret `2757581668000`; total keseluruhan `32741098508000` (selisih `3499398000`, tambah 896 transaksi, total 9004366); revenue bulan lain tidak berubah; waktu modifikasi file curated bulan lain (misal Februari dan April) tidak berubah (True) |
| 6. Rerun aman: jalankan lagi dengan late-arriving data, lalu jalankan Maret tanpa late-arriving data | 5 | rerun dengan susulan: total tetap `32741098508000`, 9004366 transaksi; tanpa susulan: total kembali `32737599110000`, quarantine Maret hilang |
| 7. Laporan: tampilkan isi tabel curated untuk Maret | 3 | top 3 kota: Jakarta `771622420000` (213620 transaksi), Surabaya `433977550000` (122450), Bandung `385776730000` (106190); per tipe toko: Supermarket `1168013060000`, Ruko `903888630000`, Mall `682180580000`; 3 produk teratas: P02348 `2178040000`, P01355 `2017380000`, P04485 `1875820000` |

Menit per langkah diselaraskan dengan hands-on 60 menit (12 November 2026): Langkah 6 dari 8 menjadi 5 (cadangan: demo trainer), Langkah 7 dari 5 menjadi 3.

Pertanyaan penutup hands-on: "Kalau besok ada koreksi untuk bulan Juli, apa yang kamu jalankan dan apa yang tidak perlu disentuh?" Jawaban diarahkan ke menjalankan ulang satu bulan dengan late-arriving data, partisi bulan lain tidak berubah, dan idempotency, bukan ke tools.

Pesan yang harus muncul dari langkah 3 dan 5: pipeline yang sama dijalankan per bulan atau sekaligus menghasilkan angka yang sama, dan koreksi satu bulan tidak memaksa memproses ulang seluruh data. Dari langkah 6: menjalankan ulang tanpa late-arriving data mengembalikan hasil awal, jadi pipeline bisa diulang dengan aman.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Notebook menjalankan skrip dengan `subprocess.run([sys.executable, "pipeline_s07.py", ...])` supaya memakai Python yang sama dengan kernel, dan hanya mencetak baris yang diawali `HASIL`. Jika kode keluar tidak nol, cetak `stderr`. Pola ini diuji dari skrip uji, belum dari kernel Jupyter; wajib diuji sebagai notebook (path interpreter, Windows).
- Setiap pemanggilan skrip memulai SparkSession dan JVM baru. Itu sebabnya `--month all` memproses 12 bulan dalam satu proses. Sebut ini di Catatan Trainer.
- Hapus folder quarantine bulan itu secara eksplisit sebelum menulis quarantine. Spark tidak menulis file apa pun untuk DataFrame kosong dan tidak menimpa partisi yang sudah ada dengan data kosong. Terbukti pada uji: setelah Maret dijalankan dengan late-arriving data lalu tanpa late-arriving data, tanpa penghapusan eksplisit folder `quarantine/month=2025-03` tetap berisi 20 baris lama, jadi skrip menghapusnya. Hitung `lolos` dan `quarantine` dari DataFrame sebelum menulis, jangan membaca balik folder quarantine (galat `UNABLE_TO_INFER_SCHEMA` pada folder kosong, dari Sesi 6).
- Pengaturan `spark.sql.sources.partitionOverwriteMode` = `dynamic` wajib. Tanpa itu, `overwrite` menimpa seluruh folder tabel, bukan hanya partisi bulan (perilaku bawaan Spark).
- Bukti "bulan lain tidak tersentuh" memakai waktu modifikasi file Parquet di folder partisi curated bulan lain (misal Februari dan April) sebelum dan sesudah menjalankan Maret. Diuji dan hasilnya sama.
- Layer cleaned memuat salinan hampir identik dengan sumber, karena data Sesi 3 sudah bersih, dan berukuran sekitar 164 MB dari total sekitar 171 MB. Layer ini dipertahankan untuk menjaga pola Sesi 6. Jelaskan di Catatan Trainer bahwa pada sumber yang sudah bersih layer ini boleh diringkas, tetapi pola tetap dipakai agar late-arriving data dan quarantine punya tempat.
- Hasil acuan waktu pada mesin 2 core: satu bulan sekitar 30-56 detik (pemanggilan pertama paling lama), semua bulan sekitar 155 detik, bulan dengan late-arriving data sekitar 36-38 detik. Puncak memori proses (Python ditambah JVM, disampel tiap 0,5 detik) sepanjang uji sekitar 1,7 GB. Waktu bukan checkpoint. Claude Code mengukur ulang puncak memori proses dan melaporkan; RAM 8 GB diperkirakan cukup.
- Selama `--month all` berjalan (sekitar 2-3 menit), trainer menjelaskan konsep; jangan menambah langkah di waktu tunggu.
- Uji notebook lewat eksekusi sebagai notebook, bukan hanya sebagai skrip. Laporkan hasil uji ini.
- Notebook menghapus folder hasil lama di awal supaya sel bisa dijalankan berulang, dan menyediakan sel pembersihan di akhir.
- Jangan menambahkan Kafka, Flink, Airflow, Delta Lake, Iceberg, atau tuning.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `32737599110000`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(32,7 triliun)").
- Kode di code slide harus sama persis dengan baris di `pipeline_s07.py` atau sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Skrip `pipeline_s07.py` juga lengkap. Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S7-CK1 | Skrip berparameter | Satu perintah satu bulan: `python pipeline_s07.py --month 2025-03` mencetak `HASIL bulan=2025-03 masuk=844330 lolos=844330 quarantine=0 completed=760280 revenue=2754082270000` | Langkah 2 | `addCodeSlide` (perintah dan output) |
| S7-CK2 | Incremental processing | Maret saja: 844.330 dari 10.000.000 baris dibaca (8,4%), 11 bulan lain tidak disentuh. Semua bulan satu per satu: total masuk 10.000.000, gabungan revenue 32.737.599.110.000, bulan terbesar 2025-01 (853.460 baris) dan terkecil 2025-02 (768.900) | Langkah 2 dan 3 | `addStatSlide` |
| S7-CK3 | Late-arriving data | Koreksi Maret sebelum dan sesudah: revenue 2.754.082.270.000 (760.280 transaksi) menjadi 2.757.581.668.000 (761.176); selisih 3.499.398.000 = 896 transaksi COMPLETED bersih. Dari 1.000 baris late-arriving: 20 masuk quarantine (`quantity_tidak_valid` 10, `status_tidak_dikenal` 10), 980 lolos; bulan lain tidak berubah | Langkah 5 | `addBeforeAfterSlide` |
| S7-TD1 | Incremental processing | Tebak: besok ada koreksi untuk bulan Juli, apa yang dijalankan dan bulan mana yang tersentuh? Jawaban: `python pipeline_s07.py --month 2025-07 --susulan <file koreksi>`; hanya Juli, 11 bulan lain tidak disentuh | Pertanyaan penutup, Langkah 6 | `addTwoPanelSlide`, `addBeforeAfterSlide` |
| S7-TD2 | Idempotent rerun | Tebak: Maret dijalankan dengan late-arriving data lalu tanpa, total kembali ke berapa? Jawaban: 32.737.599.110.000 dan 9.003.470 transaksi; quarantine Maret lama sudah hilang | Langkah 6 | `addTwoPanelSlide`, `addStatSlide` |
| S7-TD3 | Data quality | Tebak: dari 1.000 baris late-arriving, berapa masuk quarantine? Jawaban: 20 baris | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 7 ditandai)
- Dari notebook ke pipeline: `addSectionSlide`, `addBeforeAfterSlide` (notebook dijalankan manual vs skrip berparameter dijalankan penjadwal), `addTwoPanelSlide` (perintah `python pipeline_s07.py --month 2025-03` dan arti tiap parameter)
- Proses inkremental: `addSectionSlide`, `addTimelineSlide` (12 partisi bulan, satu bulan diproses, sebelas bulan tidak disentuh), `addLabelRowsSlide` (tiga syarat inkremental: partisi per bulan, partition pruning, overwrite dinamis per partisi; masing-masing merujuk sesi asalnya)
- Banyak laporan dari satu layer: `addSectionSlide`, `addComparisonTableSlide` (tiga tabel curated: pertanyaan, kolom, jumlah baris), `addStatSlide` (angka: 96, 36, dan 120 baris; total revenue 32.737.599.110.000 sama dengan Sesi 2; sumber: hasil hands-on dataset sintetis)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, Java, folder Sesi 3, file late-arriving data), `addStepsCheckpointSlide` (langkah 1-4 lalu langkah 5-7), `addCodeSlide` (maks 18 baris: pembacaan satu bulan dengan filter `month` dan penulisan overwrite dinamis per partisi), `addBeforeAfterSlide` (total sebelum dan sesudah late-arriving data: 32.737.599.110.000 menjadi 32.741.098.508.000, selisih 3.499.398.000)
- Penutup: `addNumberedListSlide` (tiga pertanyaan sebelum menjalankan pipeline di produksi: bulan mana yang berubah, aman diulang atau tidak, baris gagal ke mana), `addClosingSlide` (ringkasan, Sesi 8 Use Case Implementation: Real-Time, Sesi 9 Cloud Approach for Big Data Solution), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Pipeline adalah skrip yang bisa dijalankan tanpa orang. Parameter membuat skrip yang sama dipakai untuk satu bulan atau semua bulan.
- Proses inkremental menghemat waktu dan biaya: hanya bulan yang berubah yang diproses ulang.
- Hasil per bulan dan hasil keseluruhan harus sama. Itu cara membuktikan pipeline benar.
- Late-arriving data adalah hal biasa. Pipeline yang idempotent membuat koreksi aman.
- Satu layer cleaned bisa melayani banyak laporan. Tambah laporan baru tanpa membaca ulang sumber.
- Versi stream dari pertanyaan yang sama ada di Sesi 8. Pola desainnya sama.

Pertanyaan yang kemungkinan muncul:
- "Kenapa tidak semua bulan diproses ulang saja setiap kali?" Jawab: untuk 10 juta baris masih bisa, tetapi biaya bertambah seiring data. Inkremental menjaga biaya tetap sebanding dengan data yang berubah.
- "Kenapa skripnya terpisah dari notebook?" Jawab: notebook untuk menjelajah dan mengajar; skrip bisa dijalankan terjadwal dan diuji ulang tanpa membuka notebook.
- "Kenapa satu bulan butuh waktu hampir sama lamanya dengan beberapa bulan?" Jawab: sebagian besar waktu satu pemanggilan adalah memulai Spark dan membaca; itu sebabnya semua bulan dijalankan dalam satu proses.
- "Bagaimana kalau duplikat datang di bulan berbeda atau susulan berisi ID yang sudah ada?" Jawab: aturan duplikat hanya memeriksa dalam satu bulan (data sumber dan susulan digabung); duplikat lintas bulan butuh aturan tambahan dan dibahas sebagai batas.
- "Kenapa ada FutureWarning pandas?" Jawab: PySpark 4.3.0 belum sepenuhnya mendukung pandas 3; hasil tidak terpengaruh.
- "Bagaimana dijadwalkan?" Jawab: skrip ini bisa dipanggil oleh penjadwal; contohnya dibahas sekilas dan konteks cloud-nya di Sesi 9.
- "Apa bedanya late-arriving data di batch dan late data di stream (Sesi 5)?" Jawab: di batch, kita menjalankan ulang bulan yang terdampak; di stream, watermark menentukan apakah data yang datang terlambat masih dihitung.

## Risiko teknis dan hal yang dicek sebelum sesi
- Sesi 7 mewarisi risiko Sesi 4 dan Sesi 6: instalasi PySpark besar (sekitar 456 MB diunduh) dan Java di luar `pip`. Windows asli gagal menulis Parquet; peserta Windows memakai WSL2 dengan `.venv` dari Sesi 6.
- Peserta yang melewatkan Sesi 3 belum punya folder Parquet terpartisi. Siapkan skrip fallback dan instruksinya di README Setup, sama dengan Sesi 4.
- Setiap pemanggilan skrip memulai JVM baru. Pada laptop lambat, langkah 2, 5, dan 6 masing-masing bisa lebih dari satu menit, dan langkah 3 beberapa menit. Beri tahu peserta bahwa menunggu itu wajar, dan rencanakan penjelasan selama menunggu.
- Waktu hands-on 60 menit sangat padat dan sekitar 5-6 menit di antaranya menunggu Spark berjalan. Cadangan bila waktu mepet: langkah 6 (rerun aman) dibawakan trainer sebagai demo, atau langkah 7 (laporan) dipotong menjadi tampilan trainer. Dicek saat gladi.
- Notebook menjalankan skrip sebagai proses terpisah. Pada uji, notebook dieksekusi sebagai notebook di WSL Ubuntu dan semua angka sama; VS Code dan macOS belum diuji.
- Folder hasil membuat ratusan file kecil (sekitar 264 file). Pada Windows dengan antivirus aktif, penulisan dan penghapusan bisa lambat. Sediakan sel pembersihan dan peringatkan peserta agar tidak membuka folder itu di file explorer.
- Waktu modifikasi file sebagai bukti "tidak tersentuh" bergantung pada sistem file lokal. Pada folder yang disinkronkan layanan cloud (OneDrive dan sejenisnya) hasil bisa berbeda. Sebut di README Setup agar folder kerja tidak di folder sinkronisasi.
- Angka waktu dan ukuran file bervariasi antar mesin dan versi Spark. Hanya nilai hasil (jumlah baris, total revenue, jumlah quarantine) yang boleh dijadikan checkpoint.
- Late-arriving data sintetis dan cacatnya sengaja dibuat. Sebut ini di slide dan Modul Praktikum.
- Rujukan lintas sesi: partisi `month=` di sini berarti partition berupa folder, sama dengan Sesi 3 dan Sesi 6, bukan partition Spark (Sesi 4) atau partition Kafka (Sesi 5).

## Istilah yang harus konsisten di semua file
- batch pipeline, pipeline script, parameter, `--month`, `--susulan`
- incremental processing, rerun, idempotent
- late-arriving data (untuk batch; argumen skrip tetap bernama `--susulan`). Di Sesi 5 dan 8 padanannya late data (untuk stream); jangan dicampur
- layer raw, cleaned, curated, quarantine; sumber di sesi ini adalah folder Parquet Sesi 3
- curated tables: `revenue_by_city_month`, `revenue_by_store_type_month`, `top_products_month`
- dimension join, dimension table `stores.csv`, `store_type`
- partition: tetap berarti folder (Sesi 3) pada `month=`; jangan dicampur dengan Spark partition (Sesi 4) atau Kafka partition (Sesi 5)
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama berkas: `pipeline_s07.py`, `make_susulan_s07.py`, `susulan_2025-03.csv`, folder hasil `lake_s07/` dengan `cleaned/`, `quarantine/`, `curated/`
- Nama dataset: folder Parquet terpartisi per bulan dari Sesi 3 (nama mengikuti paket Sesi 3), `stores.csv` dan `retail_transactions.csv` (Sesi 1)
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 7 dibangun dan notebook dijalankan di WSL Ubuntu dengan Java 21, PySpark 4.3.0, pandas 3.0.5, pyarrow 26.0.1. Angka sama pada Python 3.12.16 dan 3.13.18, dan sama dengan Brief.
- Folder quarantine bulan lama: setelah Maret dijalankan dengan late-arriving data lalu tanpa, tanpa penghapusan eksplisit folder `quarantine/month=2025-03` tetap berisi 20 baris lama (Spark tidak menimpa dengan DataFrame kosong). Skrip menghapusnya secara eksplisit.
- Pemasangan dari nol pada distro WSL baru termasuk skrip cadangan `make_data_s04.py` (12 folder bulan, `retail_by_month` 207 MB, CSV 10 juta baris 902 MB).
- Memori: puncak proses 2.410 MB (Python 3.12) dan 2.304 MB (Python 3.13) pada `--month all`; dengan memori dibatasi 4 GB tanpa swap puncak 2.751 MB termasuk page cache. Waktu: satu pemanggilan sekitar 27-28 detik dan notebook utuh sekitar 4,5 menit Spark pada laptop 12 core (acuan mesin 2 core sekitar dua kali lipat).
- Windows asli gagal menulis Parquet; peserta Windows memakai WSL2. `spark-submit` tidak diuji dan hanya disebut sekilas.
- Belum diuji: VS Code, macOS, laptop RAM 8 GB sungguhan.

## Keputusan terbuka
1. Teks asli poin 8 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi, urutan modul, dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Bentuk notebook peserta dan pilihan Latihan Bertingkat (tidak) memakai pola Sesi 1-6 dan belum Anda konfirmasi untuk sesi ini.
3. Hands-on 60 menit dengan 5-6 menit menunggu Spark dinilai padat. Dicek saat gladi. Cadangan: langkah 6 sebagai demo.
4. Skrip dijalankan dengan `python` (mode lokal), bukan `spark-submit`. `spark-submit` tidak diuji dan hanya disebut sekilas. Konfirmasi.
5. Layer cleaned pada sumber yang sudah bersih adalah salinan besar. Apakah tetap dipertahankan (usulan: ya, demi pola Sesi 6) atau diringkas.
6. VS Code, macOS, dan laptop RAM 8 GB sungguhan belum diuji.
7. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
