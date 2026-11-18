# BRIEF SESI - Big Data

Sesi: 5 - Real-Time Processing Framework (Kafka/Flink)
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta memutar ulang transaksi retail sebagai stream ke Kafka, membaca dengan consumer group, lalu menghitung revenue per kota per window dengan Flink dan membuktikan hasilnya sama dengan cara batch, sambil melihat efek late data lewat watermark.
Track: lintas-track (Big Data standalone)

Revisi final: 11 November 2026. Brief ini sudah memuat (1) aturan istilah: istilah teknis Inggris dipertahankan (lihat `_GLOSARIUM_dan_Aturan_Penerapan.md`), (2) bagian baru "Penerapan teori di PPT" (Contoh kerja dan Tebak dulu), dan (3) bagian "Hasil build dan uji" dari paket yang sudah dibangun dan dijalankan oleh Claude Code.

## Peta 10 sesi (untuk slide "peta modul" dan penutup)
1. Intro Classical Data Processing
2. Common vs Big Data
3. Big Data Storage
4. Batch Processing Framework (Spark)
5. Real-Time Processing Framework (Kafka/Flink) (sesi ini)
6. Architecture Best Practice & Pipeline Design
7. Use Case Implementation: Batch
8. Use Case Implementation: Real-Time
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk dua hal dari sesi sebelumnya: Sesi 2 menyebut velocity (data datang terus-menerus) dan batch vs streaming secara sekilas, dan Sesi 4 menutup dengan batch processing. Slide penutup menyebut Sesi 6 "Architecture Best Practice & Pipeline Design" dan Sesi 8 "Use Case Implementation: Real-Time".

## Batasan cakupan
- Sesi ini membahas poin 6 outline: real-time processing dengan Kafka dan Flink. Target untuk peserta adalah memahami cara memakai tools, bukan membangun sistem streaming dari nol.
- Konsep inti yang dibawakan: arsitektur Kafka (topic, partition, producer, consumer, consumer group, offset), stream vs batch dan window, serta event time, processing time, dan watermark.
- Delivery semantics (at-least-once, exactly-once) dan state/checkpoint Flink hanya disebut sekilas di slide, tanpa hands-on.
- Tidak ada Spark Structured Streaming, Kafka Connect, Kafka Streams, schema registry, atau cluster Kafka multi-broker. Satu broker lokal.
- Tidak ada Docker, platform cloud, dan Databricks. Platform cloud di Sesi 9. Use case real-time penuh di Sesi 8, arsitektur end-to-end di Sesi 6.
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.
- Peserta tidak diasumsikan pernah memakai Kafka atau Flink.

## Tujuan belajar (maksimal 4)
1. Menjelaskan peran Kafka dalam pemrosesan real-time: topic, partition, producer, consumer group, offset.
2. Membedakan pemrosesan stream dan batch, dan menjelaskan tumbling window.
3. Menjelaskan event time, processing time, dan watermark, serta kompromi antara kelengkapan hasil dan kecepatan hasil.
4. Menjalankan pipeline Kafka ke Flink di satu laptop dan membuktikan hasil stream sama dengan hasil batch.

## Konsep inti (urutan penyampaian)
1. Kenapa streaming: data datang terus-menerus (velocity), hasil dibutuhkan saat data masih baru. Rujuk Sesi 2.
2. Arsitektur Kafka: topic, partition (sebagai pembagi beban dan urutan), producer, consumer, consumer group, offset. Kaitkan dengan partition di Sesi 2-4.
3. Stream vs batch: stream tidak punya akhir, jadi hasil dihitung per window. Tumbling window sebagai contoh. Batch dan stream menghasilkan angka yang sama untuk data yang sama; yang berbeda adalah kapan hasil keluar.
4. Event time vs processing time: waktu kejadian vs waktu bytes processed. Data bisa datang terlambat atau tidak berurutan.
5. Watermark: Flink menandai sampai kapan data dianggap sudah lengkap. Watermark kecil membuat hasil cepat tetapi late data terbuang; watermark besar membuat hasil lengkap tetapi lambat.
6. Sekilas: delivery semantics dan state Flink (hanya slide).

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1. Pertanyaan bisnis tetap revenue transaksi COMPLETED per kota, tetapi sekarang dihitung per hari dari stream. Pesan utamanya: angka stream harus sama dengan angka batch.

Dataset: 100.000 baris pertama `retail_transactions.csv` dari Sesi 1 (sintetis, bukan data internal Insignia atau klien; seed 42; urut berdasarkan `transaction_ts`, rentang 1 Januari 2025 00:00:12 sampai 6 Februari 2025 08:32:32). Pola 100.000 baris sama dengan langkah 4 Sesi 3. Peserta yang belum punya file ini memakai file Sesi 1; notebook memeriksa keberadaannya dan memberi pesan jelas jika tidak ada.

Starter Kit menyertakan skrip `replay_s05.py` yang mengirim baris CSV ke Kafka sebagai event JSON (field: transaction_ts, store_id, city, quantity, unit_price, status; key = store_id). Hanya baris COMPLETED yang dihitung di Flink; baris CANCELLED dan REFUNDED tetap dikirim agar peserta melihat filter di sisi stream.

Acuan batch (pandas) dari 100.000 baris itu: 90.041 baris COMPLETED, total revenue 327.506.381.000 (327,5 miliar), 296 kombinasi kota dan hari. Top 3 kota: Jakarta 91.454.097.000, Surabaya 53.244.187.000, Bandung 45.502.057.000.

## Platform dan tools peserta
Lokal, tanpa Docker dan tanpa cloud. Jupyter Notebook dan VS Code di laptop masing-masing, ditambah terminal untuk broker Kafka.
- **Environment khusus Sesi 5 (keputusan Fahmi).** Sesi 1-4 tidak diubah. Sesi 5 memakai venv Python 3.12 sendiri dengan `requirements_s05.txt` terpisah. Alasan: PyFlink (`apache-flink==2.3.0`) hanya mendukung Python 3.9 sampai 3.12 dan tidak mencantumkan 3.13, serta mensyaratkan pyarrow di bawah 21. Pada instalasi yang diuji, pip memasang pandas 2.2.3, numpy 2.1.3, pyarrow 16.1.0, apache-flink-libraries 2.3.0. Jangan memakai pin pandas 3.0.5, numpy 2.5.4, dan pyarrow 26.0.1 dari Sesi 1-4 di environment ini. Angka memori Sesi 1-2 tidak dipakai di sesi ini.
- **Windows.** Wheel PyFlink hanya tersedia untuk Linux dan macOS. Peserta Windows menjalankan seluruh hands-on Sesi 5 di WSL2 (keputusan Fahmi). Starter Kit memuat panduan pasang WSL2, Java, dan Python 3.12 di dalam WSL2, dikerjakan sebelum sesi.
- **Java 17 atau lebih baru.** Kafka 4.x mensyaratkan Java 17+. Flink diuji dengan Java 21.
- **Kafka 4.3.2** (`kafka_2.13-4.3.2.tgz`), mode KRaft, satu broker, tanpa ZooKeeper dan tanpa Docker. Unduhan dibagikan lewat folder bersama atau diunduh sebelum sesi, jangan bergantung pada internet di kelas.
- **Connector Kafka untuk Flink** berupa file JAR terpisah yang tidak ikut terpasang lewat pip (folder `pyflink/opt` hanya berisi connector bawaan). Starter Kit menyertakan JAR yang cocok dengan Flink 2.3.0. Versinya belum ditentukan, lihat Keputusan terbuka.
- **Klien Kafka Python.** Claude Code memilih satu library (misalnya `confluent-kafka` atau `kafka-python-ng`), memverifikasi kecocokannya dengan Kafka 4.3.2 dan Python 3.12, mengunci versinya di `requirements_s05.txt`, dan melaporkan pilihannya.
- Minimum RAM 8 GB. Puncak memori gabungan terukur sekitar 1,5 GB (broker 497 MB, Flink 761 MB, kernel Python 329 MB); dengan memori dibatasi 4 GB tanpa swap, notebook selesai dengan puncak 1.803 MB termasuk page cache. Starter Kit menyertakan langkah verifikasi environment: Java, Python, versi library, RAM, port 9092 bebas.
- Angka checkpoint dari eksekusi notebook dengan Kafka 4.3.2 sungguhan (KRaft, satu broker), Python 3.12, apache-flink 2.3.0, Java 21 (lihat Hasil build dan uji). Bila versi diubah, jalankan ulang notebook dan pastikan nilai hasil (bukan waktu) sama dengan tabel checkpoint.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 4, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.03 | Kenapa streaming, arsitektur Kafka | Konsep | 23 mnt |
| 14.03 - 14.25 | Stream vs batch, window, event time, watermark | Konsep | 22 mnt |
| 14.25 - 15.15 | Hands-on: Kafka (20 mnt), Flink (30 mnt) | Hands-on | 50 mnt |
| 15.15 - 15.30 | Recap, jembatan ke Sesi 6 dan Sesi 8 | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 (keputusan Fahmi) karena penambahan 3 slide penjelasan mekanisme (alur Kafka, consumer group dan offset, watermark langkah demi langkah): Konsep +5 menit (45 menjadi 50), hands-on -5 menit (55 menjadi 50), total tetap 120.

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook, satu pertanyaan bisnis (revenue COMPLETED per kota per hari), dua bagian: Kafka lalu Flink. Angka waktu bervariasi antar laptop dan tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

### Bagian A - Kafka (20 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: Java 17+, Python 3.12, versi library, port 9092, file `retail_transactions.csv` (di kelas tidak mengulang instalasi) | dikerjakan sebelum sesi | versi tercetak; berhenti dengan galat jelas bila ada yang kurang |
| 1. Jalankan broker KRaft, buat topic `retail_events` dengan 3 partition | 3 | topic terdaftar dengan 3 partition |
| 2. Producer: putar ulang 100.000 baris sebagai event JSON, key = `store_id` | 7 | 100.000 pesan terkirim; jumlah offset akhir ketiga partition = 100.000. Pembagian per partition tidak dijadikan checkpoint |
| 3. Consumer group: satu consumer membaca ketiga partition; tambah consumer kedua di group yang sama dan amati pembagian partition | 10 | total pesan terbaca di semua consumer = 100.000; tiap partition dimiliki satu consumer dalam satu group |

### Bagian B - Flink (30 menit)
| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 4. Flink membaca topic `retail_events`, filter COMPLETED, hitung revenue per kota dengan tumbling window 1 hari (event time, watermark 5 detik) | 15 | 296 window (kombinasi kota dan hari); 90.041 baris; total revenue 327506381000 (327,5 miliar); `equal` True terhadap hasil pandas; top 3: Jakarta 91454097000, Surabaya 53244187000, Bandung 45502057000. Diverifikasi dengan sumber file; sumber Kafka belum |
| 5. Late data: kirim ulang data dengan 200 event pertama dipindah ke akhir urutan, bandingkan watermark 5 detik dengan watermark 60 hari | 15 | watermark 5 detik: 178 baris COMPLETED terbuang, revenue hilang 655.536.000, total 326850845000 (89.863 baris); watermark 60 hari: 0 baris terbuang, total 327506381000. Diverifikasi dengan Kafka sungguhan (paralelisme 1 dan 4 sama) |
| 6. Tabel keputusan: batch atau streaming untuk kasus apa, dan watermark sebesar apa | 5 (cadangan; sejak 12 November 2026 kemungkinan besar dibawakan trainer sebagai diskusi) | tabel terisi, peserta bisa memilih untuk 3 kasus yang diberikan |

Pesan yang harus muncul dari langkah 4: hasil stream sama persis dengan hasil batch; yang berbeda adalah kapan hasil keluar. Pesan dari langkah 5: watermark adalah kompromi antara kelengkapan hasil dan kecepatan hasil, dan data yang datang setelah window ditutup dibuang tanpa galat.

Pertanyaan penutup hands-on: "Kalau pesanan datang dari 1.000 toko dan sebagian koneksinya sering terlambat, watermark seperti apa yang kamu pilih dan apa harganya?" Jawaban diarahkan ke kompromi kelengkapan vs kecepatan, bukan ke merek tools.

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Sumber Kafka di Flink harus bounded (misalnya `scan.bounded.mode` = `latest-offset`) supaya job berakhir dan semua window ditutup. Pada sumber Kafka yang tidak bounded, window terakhir tidak pernah ditutup sebelum ada data baru, sehingga hasil tidak sama dengan batch. Verifikasi dan jelaskan di Catatan Trainer.
- Partition yang kosong atau diam (idle) menahan watermark. Verifikasi apakah ini muncul dengan key = `store_id` dan 3 partition, dan tangani (misalnya idle timeout) bila perlu. Laporkan.
- Langkah 5 memakai topic terpisah dengan 1 partition dan paralelisme 1 agar jumlah baris terbuang deterministik. Jika angka hasil Kafka berbeda dari angka acuan di atas, pakai angka hasil eksekusi nyata, laporkan selisihnya, dan jelaskan penyebabnya. Jangan mengubah angka secara manual.
- Interval watermark 60 hari ditulis `INTERVAL '60' DAY`. Interval yang ditulis dalam detik dengan nilai sangat besar ditolak Flink dengan galat `exceeds precision of SECOND(2) field` (terjadi pada 36.288.000 detik). Sebut di Catatan Trainer.
- Folder log Kafka dibersihkan dan broker dihentikan di akhir notebook, supaya notebook bisa dijalankan ulang dan port tidak tertinggal terpakai.
- Waktu job (sekitar 2-6 detik pada mesin acuan, termasuk start JVM) bukan checkpoint.
- Ukur puncak memori proses (broker, Flink, klien) dan sediakan jalur aman untuk laptop RAM 8 GB, misalnya satu proses pada satu waktu.
- Uji notebook lewat eksekusi sebagai notebook, dan uji jalur WSL2 bila memungkinkan. Laporkan hasilnya.
- Jangan menambahkan Spark, Kafka Connect, Kafka Streams, atau Docker.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook (misal `327506381000`), lalu format Indonesia di dalam kurung bila angkanya besar atau bisa salah baca (misal "(327,5 miliar)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live. Perintah terminal untuk broker ditulis di notebook sebagai sel kode atau di README Setup, bukan di markdown panjang.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S5-CK1 | Tumbling window | Window 1 hari untuk Jakarta pada enam transaksi COMPLETED nyata di pergantian 1 ke 2 Januari 2025. Window 1 Januari: TRX0002801 23:56:01 (9.324.000), TRX0002802 23:56:52 (336.000), TRX0002805 23:59:59 (27.464.000). Window 2 Januari: TRX0002807 00:01:31 (243.000), TRX0002809 00:02:45 (1.930.000), TRX0002814 00:04:41 (513.000). Window 1 Januari Jakarta lengkap: 717 transaksi, 2.481.370.000 | Dihitung dari 100.000 baris pertama | `addLabelRowsSlide` |
| S5-CK2 | Arsitektur Kafka | Key menentukan partition: 100.000 event dengan key `store_id` ke 3 Kafka partition; event dengan key sama selalu di partition yang sama. Contoh satu uji: offset akhir [36.548, 35.002, 28.450]; satu consumer membaca partition [0, 1, 2]; dua consumer membagi 71.550 dan 28.450 pesan. Beri label "contoh satu uji, bukan checkpoint" | Langkah 2 dan 3 | `addTwoPanelSlide` |
| S5-CK3 | Watermark | Watermark 5 detik. Ilustrasi urutan kedatangan: event 2 Januari 00:00:10 tiba, watermark = 00:00:05, window 1 Januari (berakhir 00:00:00) ditutup dan dikeluarkan; lalu TRX0002805 (23:59:59, 27.464.000) tiba, window sudah tertutup, jadi late data dan dibuang. Beri label "Ilustrasi: transaksi nyata, urutan kedatangan skenario" | Konsep; hasil skala penuh di S5-TD1 | `addStepsCheckpointSlide` |
| S5-TD1 | Watermark | Tebak: pada skenario late data hands-on dengan watermark 5 detik, berapa baris terbuang? Jawaban: 178 baris, revenue hilang 655.536.000 (total 326.850.845.000 vs 327.506.381.000) | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |
| S5-TD2 | Event time | Tebak: dengan watermark 60 hari, berapa baris terbuang dan apakah total sama dengan batch? Jawaban: 0 baris, total 327.506.381.000 sama dengan batch (`equal` True) | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |
| S5-TD3 | Batch atau streaming | Tiga kasus: laporan bulanan; menandai transaksi mencurigakan dalam hitungan detik; revenue per toko per hari dengan sebagian toko sering terlambat. Jawaban per Answer Key: batch; streaming dengan watermark kecil; streaming dengan watermark besar atau batch | Langkah 6 | `addTwoPanelSlide`, `addComparisonTableSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 5 ditandai)
- Kenapa streaming dan arsitektur Kafka: `addSectionSlide`, `addBeforeAfterSlide` (batch: hasil setelah semua data terkumpul; stream: hasil saat data datang), `addTwoPanelSlide` (producer, topic dengan partition, consumer group, offset), `addLabelRowsSlide` (topic, partition, producer, consumer, consumer group, offset; satu baris per istilah)
- Stream vs batch, window, watermark: `addSectionSlide`, `addTimelineSlide` (tumbling window per hari pada garis waktu), `addComparisonTableSlide` (event time vs processing time), `addBeforeAfterSlide` (watermark kecil: cepat tetapi late data terbuang; watermark besar: lengkap tetapi lambat), `addNumberedListSlide` (delivery semantics dan state Flink, sekilas)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, Java, WSL2, port), `addStepsCheckpointSlide` (langkah 1-3 lalu langkah 4-6), `addCodeSlide` (maks 18 baris: langkah 2 producer dan langkah 4 window Flink), `addStatSlide` (angka: 296 window, 90.041 baris, total revenue 327.506.381.000 sama dengan batch; sumber: hasil hands-on dataset sintetis)
- Penutup: `addNumberedListSlide` (tiga pertanyaan untuk memilih batch atau streaming), `addClosingSlide` (ringkasan, Sesi 6 Architecture Best Practice & Pipeline Design, Sesi 8 Use Case Implementation: Real-Time), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Streaming bukan pengganti batch. Untuk data yang sama, keduanya menghasilkan angka yang sama; yang berbeda adalah kapan hasil keluar dan biaya menjalankannya.
- Kafka menyimpan dan membagi aliran data; Flink menghitung dari aliran itu. Keduanya punya peran berbeda.
- Partition di Kafka membagi beban dan menjaga urutan per key, mirip ide partition di Sesi 2-4 tetapi dengan arti berbeda.
- Watermark adalah kompromi antara kelengkapan dan kecepatan hasil. Data yang datang setelah window ditutup dibuang tanpa galat.
- Target sesi adalah memakai tools, bukan membangun sistem streaming dari nol. Arsitektur lengkap dibahas di Sesi 6 dan 8.

Pertanyaan yang kemungkinan muncul:
- "Kenapa tidak pakai Spark untuk streaming juga?" Jawab: Spark punya fitur streaming sendiri (Structured Streaming), tetapi tidak dibahas di sesi ini; perbandingan pilihan tools ada di Sesi 6.
- "Kenapa hasil stream baru keluar di akhir?" Jawab: window baru ditutup setelah watermark melewatinya; sumber di hands-on dibuat bounded supaya semua window ditutup.
- "Kenapa ada baris yang hilang di langkah 5?" Jawab: itu late data yang datang setelah window ditutup; bukan bug. Diperlihatkan sengaja.
- "Apa bedanya partition Kafka dengan partition Spark atau folder partition?" Jawab: lihat glosarium di bawah; empat arti dengan konteks berbeda.
- "Kenapa harus WSL2 di Windows?" Jawab: PyFlink tidak menyediakan paket untuk Windows.

## Risiko teknis dan hal yang dicek sebelum sesi
- Langkah 1-3 dan sumber Kafka di langkah 4-5 sudah dijalankan dengan Kafka sungguhan pada build (11 November 2026) dan angkanya sama dengan Brief.
- Jaringan kantor atau proxy bisa memblokir unduhan Kafka dan JAR connector (hal yang sama terjadi di sandbox pengujian). Bagikan Kafka dan JAR lewat folder bersama, jangan mengandalkan unduhan saat sesi.
- Peserta Windows butuh WSL2. Pemasangan WSL2 butuh hak administrator dan restart; kerjakan jauh sebelum hari sesi. README diuji pada distro WSL baru; `wsl --install` di laptop tanpa WSL beserta restart-nya belum teruji.
- Peserta dengan Python 3.13 sebagai default harus memasang Python 3.12 berdampingan. Environment Sesi 5 terpisah dari Sesi 1-4 dan memasang pandas 2.2.3 sehingga tidak boleh dicampur dengan environment lama.
- RAM 8 GB: broker Kafka, Flink (JVM), dan klien Python berjalan bersamaan. Puncak gabungan terukur sekitar 1,5 GB (1,8 GB bila memori dibatasi 4 GB). Belum diuji pada laptop 8 GB sungguhan dan macOS.
- Port 9092 terpakai atau folder log Kafka sisa dari percobaan sebelumnya membuat broker gagal start. Sediakan sel pembersihan dan langkah cek port.
- Watermark dan partition kosong: partition yang tidak menerima data menahan watermark, sehingga window tidak ditutup. Lihat catatan teknis.
- Angka waktu bervariasi antar mesin. Hanya nilai hasil (jumlah window, jumlah baris, total revenue) yang boleh dijadikan checkpoint.
- Rujukan lintas sesi: velocity dan batch vs streaming dikenalkan sekilas di Sesi 2. Konsep partition Kafka perlu dibedakan dari Sesi 2-4 (lihat glosarium).

## Istilah yang harus konsisten di semua file
- stream processing, real-time, batch, event (satu transaksi yang dikirim sebagai pesan)
- Kafka, broker, topic, partition (Kafka), producer, consumer, consumer group, offset
- Flink, PyFlink, window, tumbling window, event time, processing time, watermark
- late data (di stream: event datang setelah window-nya ditutup); berbeda dari late-arriving data di batch (Sesi 7); jangan dicampur
- partition punya empat arti, selalu sebut konteksnya: folder `parts/` (Sesi 2), folder `month=...` (Sesi 3), Spark partition (Sesi 4), Kafka partition (Sesi 5)
- chunk (Sesi 2) tetap berbeda dari partition
- hasil stream, hasil batch, `equal` True
- transaksi COMPLETED; revenue = quantity x unit_price
- Nama dataset: `retail_transactions.csv` (100.000 baris pertama), topic `retail_events`, skrip `replay_s05.py`, environment `requirements_s05.txt`, connector `flink-sql-connector-kafka-5.0.0-2.2.jar`
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 5 dibangun dan notebook dijalankan dengan Kafka 4.3.2 sungguhan (KRaft, satu broker), Python 3.12, apache-flink 2.3.0, confluent-kafka 2.16.1, Java 21. Seluruh angka checkpoint sama dengan Brief, termasuk 296 window, 90.041 baris, total 327.506.381.000, dan late data 178 baris pada watermark 5 detik.
- Connector: Maven belum punya rilis khusus Flink 2.3; `flink-sql-connector-kafka-5.0.0-2.2.jar` (dibuat untuk Flink 2.2) lolos uji dengan Flink 2.3.0.
- Partition kosong: topic dengan 4 partition dan satu partition kosong pada sumber bounded tetap menghasilkan 296 window dan 90.041 baris; idle timeout tidak diperlukan. Paralelisme notebook 1 (paralelisme 4 menghasilkan angka sama).
- Memori: puncak gabungan sekitar 1,5 GB (broker 497 MB, Flink 761 MB, kernel Python 329 MB); dengan memori dibatasi 4 GB tanpa swap, selesai dengan puncak 1.803 MB termasuk page cache.
- Pemasangan dari nol diuji pada distro WSL baru (Ubuntu 26.04, Python bawaan 3.14): Kafka dari URL README, Java dari `apt`, Python 3.12 lewat `uv`. Jupyter di WSL terbuka dari sisi Windows lewat `localhost`.
- Belum diuji: `wsl --install` di laptop tanpa WSL beserta restart-nya, laptop RAM 8 GB sungguhan, dan macOS. Kafka `kafka_2.13-4.3.2.tgz` disediakan lewat folder bersama karena jaringan kantor bisa memblokir unduhan.

## Keputusan terbuka
1. Teks asli poin 6 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi, catatan di file konteks (target memahami penggunaan tools), dan pembahasan kita. Cocokkan sebelum finalisasi paket.
2. Hands-on 50 menit (sejak 12 November 2026, sebelumnya 55) untuk dua sistem baru dinilai padat. Langkah 6 kemungkinan besar dibawakan trainer sebagai diskusi. Cadangan bila waktu mepet: langkah 5 (late data) dibawakan trainer sebagai demo. Dicek saat gladi.
3. `wsl --install` dan restart di laptop tanpa WSL, laptop RAM 8 GB sungguhan, dan macOS belum diuji.
4. Connector `flink-sql-connector-kafka-5.0.0-2.2.jar` lolos dengan Flink 2.3.0, tetapi Maven belum punya rilis khusus Flink 2.3. Periksa ulang menjelang sesi.
5. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
