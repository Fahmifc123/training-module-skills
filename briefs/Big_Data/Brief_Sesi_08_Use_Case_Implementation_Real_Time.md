# BRIEF SESI - Big Data

Sesi: 8 - Use Case Implementation: Real-Time
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta membangun stream pipeline dari Kafka ke Flink yang menghitung laporan penjualan per kota dan per tipe toko serta memicu dua alert rule, membuktikan hasilnya sama dengan hasil batch, lalu melihat pipeline yang sama berjalan live dalam demo trainer.
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
8. Use Case Implementation: Real-Time (sesi ini)
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk empat hal dari sesi sebelumnya: Sesi 5 (Kafka, Flink, window, watermark), Sesi 6 (layer, data quality, latihan desain kasus "deteksi transaksi mencurigakan" yang dijawab stream), Sesi 7 (batch pipeline dengan pertanyaan yang sama), dan Sesi 1 (`stores.csv`). Slide penutup menyebut Sesi 9 "Cloud Approach for Big Data Solution" (tempat batch pipeline dan stream dijalankan sebagai layanan) dan Sesi 10 "Big Data Preparation for Robust AI/ML Use Case".

## Batasan cakupan
- Sesi ini membahas poin 9 outline: implementasi use case real-time.
- Use case (keputusan Fahmi): gabungan stream report dan alert. Laporan: revenue COMPLETED per kota dan per tipe toko. Alert: dua aturan sederhana (lihat bagian dataset).
- Mode eksekusi (keputusan Fahmi): hasil dan checkpoint dari replay bounded; demo live oleh trainer sebagai tambahan tanpa checkpoint angka.
- Konsep dari Sesi 5 (arsitektur Kafka, window, event time, watermark) dipakai ulang tanpa penjelasan dari nol; cukup merujuk balik. Konsep baru di sesi ini: aturan stateless alert dan stateful alert, dimension join pada stream, hasil stream berupa changelog, dan sink ke topic Kafka.
- Tidak ada Spark Structured Streaming, Kafka Connect, Kafka Streams, schema registry, dan cluster Kafka multi-broker. Satu broker lokal, sama dengan Sesi 5.
- Tidak ada Docker, platform cloud, dan Databricks. Platform cloud di Sesi 9.
- Delivery semantics (exactly-once), state dan checkpoint Flink hanya disebut sekilas, tidak ada hands-on.
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.
- Pipeline batch dengan pertanyaan yang sama ada di Sesi 7. Jangan mengajarkan ulang batch.

## Tujuan belajar (maksimal 4)
1. Menyusun stream pipeline end-to-end: sumber Kafka, pemrosesan Flink, sink ke topic Kafka.
2. Menjalankan stream report (per kota, per tipe toko dengan dimension join) dan membuktikan hasilnya sama dengan hasil batch pada data yang sama.
3. Membedakan aturan stateless alert (filter per event) dan stateful alert (window per toko), dan menjalankan keduanya.
4. Membaca hasil stream yang berupa changelog dan menjelaskan kapan hasil stream dianggap final.

## Konsep inti (urutan penyampaian)
1. Dari batch pipeline ke stream pipeline: pertanyaan bisnis yang sama (Sesi 7), pola yang sama (sumber, bersihkan, hitung, simpan), tetapi data datang terus dan hasil keluar per window.
2. Bentuk stream pipeline yang dibangun: topic `retail_events` ke Flink, lalu laporan dan alert, dan alert ditulis ke topic `retail_alerts`.
3. Aturan alert: stateless alert (satu transaksi bernilai besar, cukup melihat satu event) dan stateful alert (lonjakan transaksi per toko dalam window, Flink harus mengingat hitungan selama window).
4. Join dimensi pada stream: tipe toko dari `stores.csv`. Di Flink, window ditutup dulu per toko, baru digabung dengan dimensi, lalu dijumlah per tipe toko. Hasil gabungan seperti ini berupa changelog, bukan baris tambahan saja.
5. Kapan hasil stream final: window ditutup oleh watermark. Sumber dibuat bounded agar semua window tertutup (Sesi 5).
6. Sekilas: stream di cloud dan layanan terkelola (Sesi 9), data quality pada stream.

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1-7. Pertanyaan bisnis laporan: revenue transaksi COMPLETED per kota per hari dan per tipe toko per hari, dihitung dari stream. Pertanyaan bisnis alert: transaksi mana yang bernilai sangat besar, dan toko mana yang mendadak ramai.

Dataset: 100.000 baris pertama `retail_transactions.csv` dari Sesi 1 (sintetis, bukan data internal Insignia atau klien; seed 42; urut `transaction_ts`, 1 Januari 2025 00:00:12 sampai 6 Februari 2025 08:32:32), diputar ulang ke Kafka sebagai event JSON dengan key = `store_id`, sama dengan Sesi 5. Dimensi: `stores.csv` dari Sesi 1 (40 toko, 3 tipe). Starter Kit menyertakan skrip `replay_s08.py` (variasi `replay_s05.py` dengan opsi kecepatan; lihat catatan teknis).

Aturan alert (keputusan Fahmi):
1. Alert nilai besar (stateless): satu transaksi COMPLETED dengan revenue (quantity x unit_price) >= 30.000.000.
2. Alert lonjakan toko (stateful): satu toko mencatat >= 5 transaksi COMPLETED dalam satu tumbling window 10 menit (event time).

Acuan batch (pandas) dari 100.000 baris itu, semuanya cocok dengan hasil Flink: 90.041 baris COMPLETED, total revenue 327.506.381.000 (327,5 miliar), 296 kombinasi kota dan hari, 111 kombinasi tipe toko dan hari (3 tipe x 37 hari).

## Platform dan tools peserta
Sama dengan Sesi 5 (keputusan Fahmi untuk Sesi 5, dipakai ulang di sini), jadi peserta tidak memasang apa pun yang baru.
- Environment khusus Python 3.12 (`requirements_s05.txt`): `apache-flink==2.3.0`, yang pada instalasi yang diuji memasang pandas 2.2.3, numpy 2.1.3, pyarrow 16.1.0. Jangan memakai environment Sesi 1-4 dan jangan memakai pin pandas 3.0.5.
- Java 17 atau lebih baru (Kafka 4.x mensyaratkan 17+; Flink diuji dengan Java 21). Kafka 4.3.2 mode KRaft, satu broker, tanpa Docker. Connector Kafka untuk Flink berupa file JAR yang disertakan di Starter Kit (versi mengikuti keputusan Sesi 5).
- Peserta Windows menjalankan seluruh hands-on di WSL2, karena wheel PyFlink hanya untuk Linux dan macOS.
- Sesi 8 memakai environment Sesi 5 (Python 3.12, Kafka 4.3.2 KRaft, PyFlink 2.3.0, connector `flink-sql-connector-kafka-5.0.0-2.2.jar`) yang sudah terbukti pada build Sesi 5 dan 8.
- Angka checkpoint dari eksekusi notebook dengan Kafka 4.3.2 sungguhan di WSL Ubuntu (Python 3.12.16, PyFlink 2.3.0, Java 21), dijalankan dua kali dengan hasil identik, dan sama dengan acuan pandas dan uji dengan sumber file CSV.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 5 dan Sesi 7, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.10 | Dari batch ke stream; bentuk pipeline; alert rule; dimension join; hasil sebagai changelog; slide penjelasan mekanisme | Konsep | 30 mnt |
| 14.10 - 15.15 | Hands-on: stream pipeline (55 mnt) dan demo live trainer (10 mnt) | Hands-on | 65 mnt |
| 15.15 - 15.30 | Recap, jembatan ke Sesi 9 dan Sesi 10 | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan menit per langkah: Bagian A berjumlah 54 menit, masih di dalam hands-on 55 menit, jadi tabel tidak diubah.

Catatan: agenda diubah 12 November 2026 (Konsep 25 menjadi 30 menit, hands-on 60 menjadi 55 menit) karena penambahan 3 slide penjelasan mekanisme (alur stream pipeline, dimension join dan changelog, bounded source); cadangan Langkah 7 sebagai demo trainer kemungkinan besar terpakai.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, dua bagian: stream pipeline bounded (langkah 1-7, hasil dan checkpoint) dan demo live (langkah 8, trainer). Langkah 9 menutup. Angka waktu bervariasi antar laptop dan tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

### Bagian A - Pipeline stream bounded (60 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: Java 17+, Python 3.12, versi library, JAR connector, port 9092, `retail_transactions.csv` dan `stores.csv` ada (di kelas tidak mengulang instalasi) | dikerjakan sebelum sesi | versi tercetak; berhenti dengan galat jelas bila ada yang kurang |
| 1. Jalankan broker KRaft, bersihkan folder log lama, buat topic `retail_events` (3 partition) dan `retail_alerts` (1 partition) | 5 | kedua topic terdaftar dengan jumlah partition yang benar |
| 2. Producer: putar ulang 100.000 baris ke `retail_events` (kecepatan maksimum, key = `store_id`) | 6 | 100.000 pesan terkirim; jumlah offset akhir ketiga partition = 100.000 |
| 3. Laporan stream 1: revenue COMPLETED per kota per hari (window 1 hari, event time, watermark 5 detik, sumber Kafka bounded) | 7 | 296 window; 90.041 baris; total revenue `327506381000` (327,5 miliar); `equal` True terhadap pandas. Diverifikasi dengan sumber file; sumber Kafka belum |
| 4. Laporan stream 2 dengan dimension join: window 1 hari per toko, gabung `stores.csv`, jumlahkan per tipe toko; materialisasi changelog | 13 | 111 baris (3 tipe x 37 hari); total `327506381000`; Supermarket `138904659000`, Ruko `107286512000`, Mall `81315210000`; `equal` True terhadap pandas. Diverifikasi dengan Kafka sungguhan |
| 5. Alert 1 (stateless): transaksi COMPLETED dengan revenue >= 30.000.000 | 7 | 1269 alert (1.269); total revenue alert `47072975000` (47,1 miliar); revenue terbesar `49930000`; per kota: Jakarta 353, Bandung 197, Surabaya 195; alert pertama 2025-01-01 00:57:57, terakhir 2025-02-06 06:51:03. Cocok dengan pandas |
| 6. Alert 2 (stateful): >= 5 transaksi COMPLETED per toko dalam window 10 menit; ubah ambang ke 6 dan bandingkan | 9 | ambang 5: 78 alert dari 10 toko berbeda (68 alert dengan 5 transaksi, 9 dengan 6, 1 dengan 7); terbesar JAK-05 pada 2025-01-05 22:50:00 dengan 7 transaksi; ambang 6: 10 alert. Cocok dengan pandas |
| 7. Sink: tulis kedua alert ke topic `retail_alerts` (kolom `rule` membedakan aturan), lalu baca dengan consumer Python | 7 | 1347 pesan di `retail_alerts` (1269 + 78); consumer menampilkan contoh alert dari kedua aturan |

### Bagian B - Demo live dan penutup (10 + 6 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 8. Demo live (trainer): stream pipeline berjalan terus, producer memutar ulang dengan kecepatan dipercepat, hasil dan alert muncul bertahap, lalu dihentikan manual | 10 | tidak ada checkpoint angka; yang diamati: alert muncul saat data masuk, bukan setelah semua data terkumpul |
| 9. Perbandingan batch (Sesi 7) dan stream (Sesi 8) untuk pertanyaan yang sama | 6 | tabel terisi: hasil sama pada data yang sama; beda pada kapan hasil keluar, kebutuhan sistem, dan biaya |

Pertanyaan penutup hands-on: "Kalau kamu harus memilih satu pertanyaan bisnis yang butuh stream dan satu yang cukup batch di perusahaanmu, apa dasar pilihanmu?" Jawaban diarahkan ke kebutuhan kecepatan hasil dan biaya, bukan ke merek tools.

Pesan yang harus muncul dari langkah 3 dan 4: pertanyaan yang sama dijawab stream dan batch dengan angka yang sama; perbedaannya adalah kapan hasil keluar. Dari langkah 5 dan 6: stateless alert hanya melihat satu event, sedangkan stateful alert harus mengingat hitungan per toko selama window. Dari langkah 4: hasil join pada stream berupa changelog, dan nilai final baru ada setelah window ditutup.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Sumber Kafka di Flink wajib bounded (misalnya `scan.bounded.mode` = `latest-offset`) agar job berakhir dan semua window ditutup, sama dengan Sesi 5. Demo live memakai sumber tidak bounded atau topic yang terus diisi, dan tidak punya checkpoint.
- Urutan di langkah 4: window per toko dulu, baru join dengan `stores.csv`, lalu jumlahkan per tipe toko. Urutan sebaliknya (join dulu, baru window) tidak dicoba di sesi pengujian; jangan menjadikannya jalur utama tanpa diuji. Join regular menghasilkan changelog, sehingga hasilnya berupa baris dengan jenis perubahan (insert, update sebelum, update sesudah, delete). Notebook memegang hasil terakhir per kunci (tipe toko, hari) dan membuang baris "update sebelum" dan "delete". Jenis perubahan dibaca lewat `row.get_row_kind()`. Pola ini diuji dan hasilnya sama dengan pandas.
- Alert 2 memakai `TUMBLE` 10 menit dengan `HAVING COUNT(*) >= 5`. Window Flink dan `pd.Grouper(freq="10min")` sejajar jam sehingga jumlahnya sama (78 dan 10). Alert 1 dan alert 2 bersifat hanya-tambah (append-only), jadi aman ditulis ke topic Kafka.
- Kedua alert ditulis ke topic `retail_alerts` dalam satu job, dengan kolom `rule` (`nilai_besar`, `lonjakan_toko`). Terbukti pada uji: 1.347 pesan, 1.269 `nilai_besar` dan 78 `lonjakan_toko`.
- `replay_s08.py` mempunyai opsi `--speed`: kecepatan percepatan waktu kejadian terhadap waktu nyata (tanpa opsi atau nol berarti kecepatan maksimum). Pada uji, `--speed 45000` mengirim 37 hari data dalam sekitar 70 detik dan `--speed 30000` sekitar 105 detik.
- Interval watermark memakai satuan yang cocok (`INTERVAL '5' SECOND`); interval besar dalam detik ditolak Flink dengan galat precision (dari Sesi 5).
- Partition yang diam (idle) menahan watermark; ikuti keputusan dan penanganan dari Sesi 5.
- Folder log Kafka dibersihkan dan broker dihentikan di akhir notebook, sama dengan Sesi 5. Topic dari Sesi 5 (`retail_events`) dihapus atau dibuat ulang di langkah 1 supaya jumlah pesan tepat 100.000.
- Waktu satu query (sekitar 2-9 detik pada mesin 2 core, termasuk start JVM) bukan checkpoint.
- Puncak memori terukur: broker sekitar 470 MB, JVM Flink sekitar 1,2 GB, proses Python sekitar 1,6 GB; RAM seluruh sistem WSL paling tinggi 2.583 MB, aman untuk laptop 8 GB. Belum diuji pada laptop 8 GB sungguhan.
- Uji notebook lewat eksekusi sebagai notebook, dan uji jalur WSL2 bila memungkinkan. Laporkan hasilnya.
- Jangan menambahkan Spark, Kafka Connect, Kafka Streams, atau Docker.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `327506381000`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(327,5 miliar)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live. Demo live (langkah 8) ada di sel atau skrip terpisah milik trainer dan tidak wajib dijalankan peserta. Perintah terminal untuk broker ditulis sebagai sel kode atau di README Setup.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S8-CK1 | Stateless alert | Satu transaksi cukup: TRX0059729 (JAK-04, 2025-01-22 16:15:41): 10 x 4.993.000 = 49.930.000, di atas ambang 30.000.000, alert keluar saat event masuk. Ini transaksi terbesar di 100.000 baris; total alert nilai besar 1.269 (1,4% dari 90.041 transaksi COMPLETED) | Langkah 5 | `addLabelRowsSlide` |
| S8-CK2 | Stateful alert | JAK-05, window 2025-01-05 22:50 sampai 23:00: tujuh transaksi COMPLETED (22:51:59 33.971.000; 22:52:08 637.000; 22:52:43 38.853.000; 22:53:08 12.150.000; 22:55:12 1.141.000; 22:55:29 111.000; 22:57:59 333.000). Jumlah 7, di atas ambang 5, alert lonjakan keluar setelah window ditutup. Dua dari tujuh (TRX0013803 dan TRX0013806) juga memicu alert nilai besar | Langkah 5 dan 6 | `addComparisonTableSlide` |
| S8-CK3 | Dimension join dan changelog | Empat tahap: window 1 hari per toko, join `stores.csv`, jumlah per `store_type`, changelog. Contoh satu uji: INSERT 111, UPDATE_BEFORE 1.369, UPDATE_AFTER 1.369 (jumlah changelog bukan checkpoint); hasil akhir 111 baris (3 tipe x 37 hari), total 327.506.381.000 (Supermarket 138.904.659.000; Ruko 107.286.512.000; Mall 81.315.210.000) | Langkah 4 | `addStepsCheckpointSlide` |
| S8-TD1 | Alert rule | Tebak: ambang alert nilai besar dinaikkan ke 40.000.000, berapa alert tersisa dari 1.269? Jawaban: 345 | Latihan Mandiri 1 | `addTwoPanelSlide`, `addStatSlide` |
| S8-TD2 | Stateful alert | Tebak: ambang lonjakan dinaikkan ke 6 transaksi per 10 menit, berapa alert dari 78? Jawaban: 10 | Langkah 6 | `addTwoPanelSlide`, `addStatSlide` |
| S8-TD3 | Watermark | Tebak: alert mana yang keluar lebih lambat, nilai besar atau lonjakan toko? Jawaban: lonjakan toko, karena menunggu watermark melewati akhir window 10 menit | Latihan Mandiri 2 | `addTwoPanelSlide`, `addBeforeAfterSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 8 ditandai)
- Dari batch ke stream: `addSectionSlide`, `addBeforeAfterSlide` (batch pipeline Sesi 7: hasil setelah semua bulan diproses; stream pipeline: hasil per window saat data masuk), `addTwoPanelSlide` (bentuk pipeline: `retail_events` ke Flink ke laporan dan `retail_alerts`)
- Aturan alert: `addSectionSlide`, `addComparisonTableSlide` (stateless alert vs stateful: aturan, yang harus diingat Flink, contoh, jumlah alert di hands-on), `addStatSlide` (angka: 1.269 alert nilai besar dan 78 alert lonjakan toko dari 100.000 transaksi; sumber: hasil hands-on dataset sintetis)
- Dimension join dan changelog: `addSectionSlide`, `addLabelRowsSlide` (window per toko, join stores, jumlah per tipe toko, hasil berupa changelog), `addBeforeAfterSlide` (baris hasil sementara vs hasil akhir setelah window ditutup)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, Java, WSL2, port, JAR), `addStepsCheckpointSlide` (langkah 1-4 lalu langkah 5-9), `addCodeSlide` (maks 18 baris: query alert 2 dengan window dan HAVING, dan penulisan sink ke `retail_alerts`)
- Penutup: `addNumberedListSlide` (tiga pertanyaan untuk memilih stream atau batch), `addClosingSlide` (ringkasan, Sesi 9 Cloud Approach for Big Data Solution, Sesi 10 Big Data Preparation for Robust AI/ML Use Case), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Stream dan batch menjawab pertanyaan yang sama dengan angka yang sama; yang berbeda adalah kapan hasil keluar dan biaya menjalankannya.
- Alert real-time bernilai karena muncul saat kejadian, bukan setelah semua data terkumpul.
- Stateless alert murah; stateful alert butuh Flink mengingat data selama window.
- Hasil stream bisa berupa changelog. Nilai final baru ada setelah window ditutup.
- Target sesi adalah memakai tools untuk use case, bukan membangun sistem produksi. Aspek produksi (cloud, layanan terkelola) di Sesi 9.

Pertanyaan yang kemungkinan muncul:
- "Kenapa hasil join berupa changelog, bukan satu baris?" Jawab: tipe toko dijumlahkan dari banyak window toko, dan jumlahnya naik setiap ada window toko baru yang ditutup; Flink mengirim koreksi atas hasil sebelumnya.
- "Kenapa alert 1 muncul 1.269 kali padahal hanya 100.000 transaksi?" Jawab: 1,4% transaksi COMPLETED bernilai >= 30.000.000. Ambang adalah pilihan bisnis; ubah ambang, jumlah alert berubah.
- "Kenapa ambang 5 transaksi per 10 menit?" Jawab: rata-rata toko hanya 1,3 transaksi per 10 menit, sehingga 5 jarang terjadi; ambang itu memilih kejadian yang tidak biasa.
- "Apakah alert bisa terlewat?" Jawab: alert window baru keluar setelah window ditutup oleh watermark, jadi ada jeda; late data bisa terbuang (Sesi 5).
- "Kenapa window 10 menit bukan sliding window?" Jawab: tumbling window cukup untuk pembelajaran; sliding window disebut sekilas bila ditanya.
- "Kenapa Flink, bukan Spark Structured Streaming?" Jawab: sesi ini memakai Flink sesuai Sesi 5; perbandingan tools di Sesi 6 dan bahasan lanjut di luar modul.

## Risiko teknis dan hal yang dicek sebelum sesi
- Sesi 8 mewarisi risiko Sesi 5: jaringan atau proxy kantor bisa memblokir unduhan Kafka dan JAR connector (bagikan lewat folder bersama), WSL2 di Windows butuh hak administrator dan restart, dan peserta dengan Python 3.13 sebagai default butuh Python 3.12 berdampingan.
- Demo live: penghentian proses sudah dipastikan, tetapi Ctrl+C di terminal interaktif belum diuji langsung. Siapkan rekaman layar sebagai cadangan.
- Hands-on 70 menit sangat padat (tujuh langkah ditambah demo live), dan setiap query Flink memulai JVM. Cadangan bila waktu mepet: langkah 7 (sink dan consumer) dibawakan trainer sebagai demo, atau langkah 3 (laporan per kota) dibawakan cepat karena sudah dibahas di Sesi 5. Dicek saat gladi.
- Demo live bergantung pada kecepatan replay dan beban laptop trainer. Siapkan rekaman layar sebagai cadangan bila demo gagal.
- Hasil join berupa changelog bisa membingungkan peserta. Siapkan penjelasan di Catatan Trainer dan jangan mencetak seluruh baris changelog.
- Port 9092 terpakai atau folder log Kafka sisa dari Sesi 5 membuat broker gagal start atau jumlah pesan tidak tepat 100.000. Sediakan sel pembersihan dan langkah cek port.
- Angka waktu bervariasi antar mesin. Hanya nilai hasil (jumlah window, baris, alert, total revenue) yang boleh dijadikan checkpoint.
- Alert 2 bergantung pada window yang sejajar jam. Jika Flink atau Kafka berbeda versi, jumlah alert harus dicocokkan ulang dengan pandas.
- Data sintetis dan ambang alert dipilih untuk pembelajaran, bukan aturan deteksi penipuan sungguhan. Sebut di slide dan Modul Praktikum.
- Rujukan lintas sesi: partition di Sesi 8 berarti partition Kafka (Sesi 5), bukan folder (Sesi 3, 6, 7) atau partition Spark (Sesi 4).

## Istilah yang harus konsisten di semua file
- stream pipeline, stream report, alert, alert rule, `rule`
- stateless alert, stateful alert
- topic `retail_events` (masukan), topic `retail_alerts` (keluaran), sink
- window, tumbling window, event time, watermark (sama dengan Sesi 5)
- dimension join, dimension table `stores.csv`, `store_type`
- changelog (INSERT, UPDATE_BEFORE, UPDATE_AFTER), final result, materialization
- bounded source (bounded replay), live demo
- late data (untuk stream, Sesi 5) berbeda dari late-arriving data (untuk batch, Sesi 7); jangan dicampur
- partition: di sesi ini berarti Kafka partition (Sesi 5); empat arti di modul (folder `parts/` Sesi 2, folder `month=` Sesi 3, 6, 7, Spark partition Sesi 4, Kafka partition Sesi 5 dan 8), selalu sebut konteksnya
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama dataset: `retail_transactions.csv` (100.000 baris pertama), `stores.csv`, skrip `replay_s08.py`, environment `requirements_s05.txt`
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 8 dibangun dan notebook dijalankan dua kali dari awal dengan Kafka 4.3.2 sungguhan di WSL Ubuntu (Python 3.12.16, PyFlink 2.3.0, confluent-kafka 2.16.1, pandas 2.2.3, pyarrow 16.1.0, Java 21). Hasil identik dan sama dengan acuan pandas dan uji sumber file.
- Changelog langkah 4: INSERT 111, UPDATE_BEFORE 1.369, UPDATE_AFTER 1.369; jumlahnya bergantung urutan window toko ditutup, jadi checkpoint adalah hasil akhir 111 baris dan `equal` True.
- Sink: `retail_alerts` berisi 1.347 pesan (1.269 `nilai_besar` dan 78 `lonjakan_toko`).
- Demo live: `--speed 45000` mengirim 37 hari data dalam sekitar 70 detik (alert pertama di detik 0, terakhir di detik 70, jumlah akhir sama dengan bounded); `--speed 30000` sekitar 105 detik. Ctrl+C di terminal interaktif belum diuji langsung; siapkan rekaman layar.
- Memori: broker sekitar 470 MB, JVM Flink sekitar 1,2 GB, proses Python sekitar 1,6 GB; RAM seluruh sistem WSL paling tinggi 2.583 MB. Seluruh notebook sekitar 60-75 detik.
- Belum diuji: pemasangan WSL2 baru khusus Sesi 8 (environment uji sudah berisi setup Sesi 5), laptop RAM 8 GB sungguhan.

## Keputusan terbuka
1. Teks asli poin 9 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi, Sesi 5-7, dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Hands-on 70 menit dengan delapan langkah ditambah demo live dinilai padat. Cadangan: langkah 7 (sink dan consumer) dibawakan trainer sebagai demo. Dicek saat gladi.
3. Ctrl+C di terminal interaktif untuk menghentikan demo live belum diuji langsung. Siapkan rekaman layar.
4. Pemasangan WSL2 baru khusus Sesi 8 dan laptop RAM 8 GB sungguhan belum diuji.
5. Urutan "join dulu baru window" belum dicoba; hanya "window dulu baru join" yang diverifikasi.
6. Ambang alert (nilai >= 30.000.000, >= 5 transaksi per 10 menit) mengikuti pilihan Fahmi; jumlah alert dihitung dari 100.000 baris pertama dan berubah bila data atau ambang berubah.
7. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
