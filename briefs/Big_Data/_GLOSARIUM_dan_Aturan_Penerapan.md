# GLOSARIUM dan ATURAN PENERAPAN (berlaku untuk seluruh paket Big Data, Sesi 1-10)

File ini dibaca bersama setiap Brief. Bila bertentangan dengan kalimat di Brief, file ini yang berlaku.

## Bagian A - Aturan bahasa istilah

1. Kalimat berbahasa Indonesia. Istilah teknis yang lazim dipakai praktisi tetap bahasa Inggris, di judul slide, label tabel, anchor notebook, Modul Praktikum, Catatan Trainer, dan Answer Key. Jangan diterjemahkan.
2. Padanan Indonesia hanya boleh muncul sebagai penjelasan singkat dalam kurung pada kemunculan pertama istilah di satu dokumen, misalnya "late data (data yang datang setelah window-nya ditutup)". Sesudah itu hanya istilah Inggris.
3. Kata umum non-teknis tetap Indonesia: baris, kolom, tabel, hasil, toko, kota, bulan, jumlah, selisih, contoh, langkah.
4. Nama kolom, fungsi, berkas, perintah, dan pesan galat tidak pernah diterjemahkan.
5. Label yang dicetak notebook memakai istilah Inggris untuk konsep teknis, misalnya `nulls: 0`, `quarantine: 500`, `late data: 178`. Kata penghubung umum boleh Indonesia (`baris`, `total`, `lolos`).
6. Satu istilah satu bentuk di seluruh paket. Jangan memakai dua padanan untuk hal yang sama.

## Bagian B - Glosarium istilah (bentuk yang dipakai, dan bentuk yang tidak dipakai)

| Pakai | Penjelasan singkat untuk kemunculan pertama | Jangan dipakai sebagai istilah utama |
|---|---|---|
| batch processing, stream processing | pemrosesan data terkumpul vs data saat datang | pemrosesan batch, pemrosesan aliran |
| batch pipeline, stream pipeline | alur pemrosesan | pipeline batch, pipeline stream |
| layer (raw, cleaned, curated) | tingkat data dalam pipeline | lapisan |
| data quality | pemeriksaan kualitas data | kualitas data |
| quarantine | tempat baris yang gagal aturan | karantina |
| idempotent, idempotency | dijalankan ulang menghasilkan hasil sama | idempoten |
| late data | di stream: event datang setelah window ditutup | data terlambat |
| late-arriving data | di batch: data koreksi atau susulan untuk periode lama | data susulan |
| event time, processing time | waktu kejadian, waktu diproses | waktu kejadian (sebagai istilah utama) |
| window, tumbling window | potongan waktu tetap pada stream | jendela |
| watermark | batas kelengkapan data pada event time | batas air |
| stateless alert, stateful alert | alert yang cukup melihat satu event vs yang perlu mengingat hitungan | alert tanpa state, alert dengan state |
| alert rule | aturan pemicu alert | aturan alert |
| dimension table, dimension join | tabel atribut seperti `stores.csv`; join untuk menambah atribut | tabel dimensi, join dimensi |
| changelog | hasil stream berupa INSERT, UPDATE_BEFORE, UPDATE_AFTER | pembaruan, baris perubahan |
| bounded source | sumber yang berakhir sehingga semua window tertutup | sumber bounded (campuran) |
| sink | tujuan keluaran | tujuan keluaran |
| topic, partition, offset, consumer group, broker, replay | istilah Kafka | terjemahan apa pun |
| column pruning, partition pruning | hanya kolom atau folder yang dibutuhkan yang dibaca | pemangkasan kolom |
| columnar | data disimpan per kolom | berbasis kolom |
| bytes processed, bytes scanned | data yang dibaca query, dasar tagihan on-demand | data diproses, data dipindai |
| selected columns | kolom yang dipilih di query | kolom terpilih |
| serverless, managed cluster, self-managed | tingkat pengelolaan compute | cluster terkelola |
| service map, equivalent services | pemetaan komponen pipeline ke layanan cloud, dan layanan setara di tiap cloud | peta layanan, padanan layanan |
| cost model | cara cloud menagih | model biaya |
| daily quota, table expiration, free tier | batas versi gratis | kuota harian, kedaluwarsa tabel |
| feature table, feature engineering | tabel fitur plus target; pembuatan fitur | tabel fitur, rekayasa fitur |
| data leakage | fitur membawa informasi dari hari yang diprediksi | kebocoran data |
| time-based split, random split | pembagian data menurut waktu vs acak | split berdasarkan waktu, pembagian acak |
| training set, test set | data latih, data uji | data latih, data uji (sebagai istilah utama) |
| baseline, lag, rolling window, warm-up | istilah teknis time series | terjemahan apa pun |
| data preparation | persiapan data | persiapan data |
| nulls (missing values), duplicates, invalid values, missing days | pemeriksaan data | nilai kosong, nilai tidak valid, hari tanpa data |
| dataframe, vectorized operation, chunked, checkpoint, hands-on, Starter Kit, Answer Key | sudah baku | terjemahan apa pun |
| structured, semi-structured, unstructured data | data berstruktur tetap, bertingkat seperti JSON, dan bebas seperti teks atau gambar | terstruktur, semi-terstruktur, tidak terstruktur (sebagai istilah utama) |
| data lake, data warehouse, lakehouse | tiga pendekatan penyimpanan | danau data, gudang data |
| partition | selalu sebut konteks: folder `parts/` (Sesi 2), folder `month=` (Sesi 3, 6, 7), Spark partition (Sesi 4), Kafka partition (Sesi 5, 8), `partitionBy` pada window (Sesi 10), partisi tabel (Sesi 9) | partition tanpa konteks |

## Bagian C - Aturan penerapan teori di PPT

Tujuan: setiap konsep inti langsung diterapkan pada data atau skenario nyata dari sesi itu, sebelum hands-on. Dua bentuk wajib:

**Contoh kerja (CK)**: satu slide. Konsep dijalankan pada data mini atau angka nyata dari dataset sesi. Peserta melihat input, proses, dan hasil di satu layar.

**Tebak dulu (TD)**: dua slide. Slide pertama berisi pertanyaan atau skenario dengan 2-3 pilihan atau permintaan memperkirakan angka. Trainer berhenti 30-45 detik. Slide kedua berisi jawaban berupa angka dari hands-on atau Answer Key, ditambah satu kalimat alasan yang merujuk ke konsep.

Aturan:
1. Setiap Brief menetapkan daftar CK dan TD (bagian "Penerapan teori di PPT"). Tiap konsep inti punya minimal satu CK atau TD.
2. Angka di CK dan TD harus sama persis dengan checkpoint di Brief atau perhitungan yang tercantum di Brief. Skenario ilustrasi diberi label "Ilustrasi" di slide dan tidak boleh dikutip sebagai hasil.
3. Data mini di slide: maksimal 8 baris dan 5 kolom. Satu ide per slide.
4. CK dan TD tidak mengulang kode hands-on. Kode hanya di code slide (maks sekitar 24 baris, kode sama persis dengan sel notebook).
5. Jawaban TD harus bisa ditemukan peserta sendiri di langkah hands-on tertentu. Slide jawaban menyebut langkahnya.
6. Setiap CK dan TD punya speaker notes 2-3 kalimat untuk trainer, dan jawaban TD dicatat di Answer Key.
7. Anggaran waktu bagian Konsep tetap sama dengan agenda. Slide definisi dipadatkan (gabungkan slide yang mengulang definisi) sehingga: definisi sekitar 40%, penerapan sekitar 60% waktu Konsep. Angka 60% adalah target untuk keseluruhan bagian Konsep satu sesi, bukan wajib per bagian; bila daftar CK/TD Brief tidak cukup mengisinya, sisa waktu dipakai trainer untuk diskusi (keputusan Fahmi, 12 November 2026). Perkiraan: CK 2 menit, TD 3 menit.
8. Jumlah slide sesi boleh bertambah sampai 12 dari versi v2 (keputusan Fahmi, 12 November 2026; sebelumnya 8), termasuk slide penjelasan mekanisme untuk konsep inti yang sulit (diagram alur atau langkah demi langkah) sebelum Contoh kerja konsep itu. Waktu tambahan diambil dari hands-on (Konsep +5 menit, hands-on -5 menit), kecuali Sesi 9.
9. Footer sumber untuk slide berangka: "Sumber: hasil hands-on dataset sintetis" (dan versi software bila relevan).
10. Komponen slide dari `Template_Training_Insignia.pdf`. Pemetaan umum: CK memakai `addLabelRowsSlide`, `addBeforeAfterSlide`, `addComparisonTableSlide`, atau `addStepsCheckpointSlide`; TD pertanyaan memakai `addTwoPanelSlide`; TD jawaban memakai `addStatSlide` atau `addBeforeAfterSlide`. Brief menyebut komponen per item.
11. Modul Praktikum menyertakan jawaban CK dan TD di bagian "Cek pemahaman" (satu paragraf per item), tanpa menambah langkah hands-on.

## Bagian D - Status verifikasi

Seluruh paket sudah dibangun dan dijalankan oleh Claude Code pada 11 November 2026. Setiap Brief punya bagian "Hasil build dan uji" yang menggantikan kalimat lama "belum diverifikasi" bila bertentangan. Hal yang masih terbuka dicatat di "Keputusan terbuka" masing-masing Brief.
