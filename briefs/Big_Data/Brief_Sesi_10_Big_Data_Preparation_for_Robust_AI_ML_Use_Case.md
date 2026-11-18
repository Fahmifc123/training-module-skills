# BRIEF SESI - Big Data

Sesi: 10 - Big Data Preparation for Robust AI/ML Use Case
Tanggal mengajar: awal Desember 2026, tanggal pasti per sesi belum ditetapkan (slot siang 13.30 - 15.30 WIB; slot sore 15.30 - 17.30 WIB memakai materi yang sama). Seluruh paket 10 sesi diselesaikan sebelum sesi pertama.
Deskripsi satu kalimat: Peserta menyiapkan data retail untuk use case forecast revenue harian per toko: memeriksa data quality, membangun feature table dengan Spark, membagi data berdasarkan waktu, membandingkan model dengan baseline, dan melihat sendiri bagaimana data leakage (data leakage) membuat hasil tampak terlalu bagus.
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
9. Cloud Approach for Big Data Solution
10. Big Data Preparation for Robust AI/ML Use Case (sesi ini)

Gunakan judul persis seperti daftar ini di seluruh paket. Slide pembuka merujuk empat hal dari sesi sebelumnya: Sesi 4 (PySpark, DataFrame, lazy evaluation), Sesi 6 (layer raw-cleaned-curated dan data quality), Sesi 7 (laporan revenue per toko per hari dari batch pipeline), dan Sesi 1 (`retail_transactions.csv`, `stores.csv`). Slide penutup adalah penutup modul: ringkasan 10 sesi sebagai alur dari data mentah sampai data siap untuk AI/ML, tanpa sesi berikutnya.

## Batasan cakupan
- Sesi ini membahas poin 11 outline: data preparation besar untuk use case AI/ML yang andal.
- Use case (keputusan Fahmi): forecast revenue harian per toko. Data retail tidak punya `customer_id`, jadi use case berbasis pelanggan tidak dipakai.
- Konsep inti (keputusan Fahmi): feature engineering skala besar; split tanpa data leakage (leakage); data quality untuk ML. Reproducibility dan versi dataset, feature store, dan drift tidak menjadi konsep inti; disebut sekilas satu slide di penutup tanpa hands-on.
- Fokus sesi adalah data preparation, bukan membangun model terbaik. Model hanya dipakai untuk menguji data preparation. Tidak ada tuning hyperparameter, deep learning, MLOps, dan deployment model.
- Data sintetis tidak punya pola musiman atau pola hari dalam minggu (diperiksa), sehingga model tidak akan mengalahkan baseline sederhana. Itu bagian dari pelajaran dan harus dikatakan terus terang di slide dan Catatan Trainer, bukan disembunyikan.
- Tidak ada Kafka, Flink, atau cloud di sesi ini. Hanya lokal (lihat platform).
- Kasus internal Edelweiss tidak dipakai (keputusannya ditunda). Hanya dataset sintetis retail.
- Proyek ML nyata di perusahaan (termasuk migrasi model ke cloud) tidak dibahas.

## Tujuan belajar (maksimal 4)
1. Memeriksa data quality sebelum dipakai untuk ML: nilai hilang, duplikat, invalid values, pengaruh status transaksi, dan missing days.
2. Membangun feature table dari data transaksi dengan Spark (lag, rolling window, fitur kalender, atribut toko) tanpa memakai informasi masa depan.
3. Membagi data berdasarkan waktu dan menjelaskan mengapa random split bisa menyesatkan pada data berurutan.
4. Membandingkan model dengan baseline dan mengenali data leakage dari hasil yang terlalu bagus.

## Konsep inti (urutan penyampaian)
1. Dari pipeline data ke data untuk ML: pertanyaan berubah dari "berapa revenue" menjadi "berapa revenue besok", dan tabel keluaran berubah dari laporan menjadi feature table plus target.
2. Definisi target dan unit prediksi: revenue transaksi COMPLETED per toko per hari (satu baris = satu toko pada satu hari). Pilihan ini adalah keputusan data, bukan teknis.
3. Data quality untuk ML: nilai hilang, duplikat, invalid values, status transaksi, missing days, distribusi miring (skew), dan nulls di awal deret karena lag.
4. Rekayasa fitur skala besar: lag, rolling window, fitur kalender, atribut toko, dihitung dengan window function Spark; hasilnya dicocokkan dengan pandas.
5. Split berdasarkan waktu: latih pada masa lalu, uji pada masa depan; cegah kebocoran.
6. Data leakage (leakage): fitur yang diam-diam memuat informasi dari hari yang diprediksi. Cara mengenali: hasil jauh lebih bagus dari baseline dan dari akal sehat.
7. Baseline dulu: model hanya berguna jika mengalahkan baseline sederhana. Ukuran: MAE dan WAPE.
8. Sekilas: feature table yang sama untuk training dan inference, versi dataset, drift (satu slide).

## Use case dan dataset sintetis
Use case: lanjutan laporan penjualan retail Sesi 1-9. Pertanyaan: dari data transaksi, siapkan data untuk memprediksi revenue harian setiap toko, lalu uji kualitas persiapan dengan model sederhana.

Dataset: `retail_transactions.csv` dari Sesi 1 (1.000.000 baris; sintetis, bukan data internal Insignia atau klien; seed 42; 1 Januari 2025 sampai 31 Desember 2025) dan `stores.csv` (40 toko; 3 tipe: Supermarket 17, Ruko 13, Mall 10). Skrip dan notebook memakai CSV yang sama dengan Sesi 1, jadi tidak ada berkas data baru. Dataset 10 juta baris dari Sesi 3 dan 7 tidak dipakai di sesi ini (lihat keputusan terbuka).

Hasil pemeriksaan kualitas pada data itu (acuan pandas, dan hasil Spark sama):
- 1.000.000 baris, tidak ada nulls, tidak ada `transaction_id` ganda, tidak ada `quantity` atau `unit_price` yang nol atau negatif.
- Status: COMPLETED 900.347; CANCELLED 69.741; REFUNDED 29.912. Target hanya memakai COMPLETED (revenue = quantity x unit_price).
- Tabel harian per toko: 14.600 baris (40 toko x 365 hari); tidak ada missing days; jumlah transaksi per toko per hari antara 17 dan 186 (median 48).
- Revenue harian per toko miring ke kanan: median 184.465.500 (pandas; notebook mencetak `percentile_approx` Spark 184452000), maksimum 856.590.000, skewness 1,37.
- Pola: rata-rata revenue per hari dalam minggu dan per bulan hampir sama (sekitar 222 sampai 226 juta), jadi tidak ada musiman. Data sintetis dibuat seperti ini.

Feature table (hasil Spark, dicocokkan dengan pandas):
- Kolom: `store_id`, `date`, `revenue` (target), `n_tx`, `store_type`, `opened_year`, `lag_1`, `lag_7`, `roll7`, `roll28`, `cnt28`, `dow`, `month`, dan satu kolom contoh kebocoran `roll7_leak`.
- `lag_1` dan `lag_7` adalah revenue 1 dan 7 hari sebelumnya; `roll7` dan `roll28` adalah rata-rata revenue 7 dan 28 hari sebelumnya, tidak termasuk hari itu (window dari 7 atau 28 baris sebelum sampai 1 baris sebelum); `cnt28` adalah jumlah hari yang tersedia dalam window 28 hari.
- `roll7_leak` adalah rata-rata 7 hari yang termasuk hari itu sendiri (window dari 6 baris sebelum sampai baris itu), sehingga memuat target.
- Nilai kosong di awal deret per toko: `lag_1` 40, `lag_7` 280, `roll7` 40, `roll28` 40. Baris dengan `cnt28` kurang dari 28 dibuang sebagai warm-up, tersisa 13.480 baris (mulai 2025-01-29).
- Split berdasarkan waktu: latih untuk tanggal sebelum 2025-10-01 (9.800 baris); uji 2025-10-01 sampai 2025-12-31 (3.680 baris).

## Platform dan tools peserta
- Environment Sesi 4, 6, dan 7: Python 3.12+, PySpark 4.3.0, Java 17+ (diuji dengan Java 21), pandas 3.0.5, numpy 2.5.x, pyarrow 26.0.1, ditambah scikit-learn 1.9.1 (diuji bersama pandas 3.0.5). Jangan memakai environment Sesi 5.
- Pengujian dengan Python 3.13.18 di WSL Ubuntu sebagai kernel Jupyter (Java 21); notebook selesai sekitar 37 detik, puncak RAM seluruh sistem WSL sekitar 1,8 GB. Windows asli tidak didukung untuk sesi ini (peserta memakai WSL2); laptop RAM 8 GB sungguhan belum diuji.
- Spark mode lokal (`local[2]`). Hasil Spark dipindahkan ke pandas lewat `toPandas()`; hanya 14.600 baris. FutureWarning dari pandas 3.0.5 saat memakai PySpark normal.
- Hasil model bergantung pada versi scikit-learn (angka di bawah dari 1.9.1 dengan `random_state=42`). Jika versi berbeda, hasil boleh berbeda sedikit; kunci versi di requirements.
- Semua checkpoint di Brief ini dijalankan lewat eksekusi notebook dan cocok.

## Agenda dan rentang waktu (total 120 menit)
| Waktu | Bagian | Kategori | Durasi |
|---|---|---|---|
| 13.30 - 13.40 | Pembukaan, recap Sesi 7 dan 9, peta 10 sesi | Pembukaan | 10 mnt |
| 13.40 - 14.10 | Dari pipeline data ke data untuk ML; data quality; fitur; split waktu; kebocoran | Konsep | 30 mnt |
| 14.10 - 15.15 | Hands-on: data quality, feature table Spark, split waktu, baseline dan model, demo kebocoran | Hands-on | 65 mnt |
| 15.15 - 15.30 | Recap modul 10 sesi, penutup | Penutup | 15 mnt |

Slot sore memakai pola yang sama, digeser mulai 15.30.

Catatan: agenda diubah 12 November 2026 (Konsep 25 menjadi 30 menit, hands-on 70 menjadi 65 menit, total tetap 120) karena penambahan tiga slide penjelasan mekanisme (feature engineering di garis waktu, window Spark dan warm-up, time-based split vs random split).

Pembagian waktu di bagian Konsep: slide definisi sekitar 40% dan penerapan teori (Contoh kerja dan Tebak dulu, lihat bagian "Penerapan teori di PPT") sekitar 60%. Total menit Konsep tidak berubah.

## Rancangan hands-on
Satu notebook. Angka waktu bervariasi antar laptop dan tidak boleh ditulis sebagai fakta tetap di slide atau Answer Key.

| Langkah | Perkiraan menit | Output checkpoint |
|---|---|---|
| 0. Verifikasi: Java 17+, versi Python, PySpark 4.3.0, scikit-learn 1.9.1, `retail_transactions.csv` dan `stores.csv` ada | sebelum sesi | versi tercetak; berhenti dengan galat jelas bila ada yang kurang |
| 1. Baca CSV dengan Spark; periksa kualitas: jumlah baris, nulls, duplikat, invalid values, distribusi status | 7 | 1.000.000 baris; kosong 0; duplikat 0; tidak valid 0; COMPLETED 900.347, CANCELLED 69.741, REFUNDED 29.912 |
| 2. Bentuk target: revenue COMPLETED per toko per hari; periksa kelengkapan hari | 5 | 14.600 baris (40 toko x 365 hari); hari hilang 0; transaksi per toko per hari 17 sampai 186 |
| 3. Bangun fitur dengan window function Spark (`lag_1`, `lag_7`, `roll7`, `roll28`, `dow`, `month`, `store_type`) dan kolom `roll7_leak`; cocokkan dengan pandas | 10 | 14.600 baris; nulls `lag_1` 40, `lag_7` 280, `roll7` 40, `roll28` 40; seluruh kolom fitur sama dengan hasil pandas (`equal` True) |
| 4. Buang warm-up dan bagi data berdasarkan waktu | 7 | 13.480 baris setelah warm-up (mulai 2025-01-29); latih 9.800; uji 3.680 (2025-10-01 sampai 2025-12-31) |
| 5. Baseline dan model: rata-rata toko dari training set, `lag_7`, `lag_1`, `roll7`, `roll28`, Ridge, GradientBoostingRegressor; hitung MAE dan WAPE pada test set | 15 | lihat tabel hasil di bawah |
| 6. Kebocoran: tambahkan `roll7_leak` sebagai fitur, latih ulang, bandingkan | 10 | GradientBoosting dengan `roll7_leak`: MAE 30529554, WAPE 0,1363, jauh lebih baik dari tanpa kebocoran (MAE 45126581, WAPE 0,2014); peserta menjelaskan mengapa itu menipu |
| 7. Simpan feature table sebagai Parquet dan tuliskan definisi tiap kolom (satu sel markdown) | 5 | berkas Parquet terbaca ulang dengan 14.600 baris dan 14 kolom |
| 8. Daftar periksa data preparation untuk ML (peserta menyusun lima butir dari langkah 1 sampai 7) | 6 | daftar lima butir tersusun; cadangan waktu 1 menit |

Hasil langkah 5 (test set 3.680 baris; WAPE = jumlah selisih absolut dibagi jumlah revenue aktual; MAE dibulatkan ke rupiah):
| Model | MAE | WAPE |
|---|---|---|
| Rata-rata revenue toko dari training set (baseline) | 44681578 | 0,1994 |
| `lag_7` | 62201226 | 0,2776 |
| `lag_1` | 63701905 | 0,2843 |
| `roll7` | 47608866 | 0,2125 |
| `roll28` | 45078667 | 0,2012 |
| Ridge (6 fitur plus tipe toko) | 45092432 | 0,2013 |
| GradientBoostingRegressor (sama) | 45126581 | 0,2014 |

Pesan dari langkah 5: tidak ada model yang mengalahkan baseline rata-rata toko, karena data sintetis tidak punya pola yang bisa dipelajari selain level toko. Pada data nyata hasilnya bisa berbeda, tetapi urutan kerja sama: baseline dulu, lalu model.

Pesan dari langkah 6: kebocoran membuat WAPE turun dari 20,1% menjadi 13,6% pada data yang sama, tanpa ada pengetahuan baru. Hasil yang tiba-tiba jauh lebih bagus dari baseline harus dicurigai dulu, bukan dirayakan.

Catatan: pada percobaan, random split (80/20) pada data ini memberi WAPE 0,1962 untuk GradientBoosting, hampir sama dengan pembagian waktu, karena data sintetis stasioner. Karena itu, jangan memakai langkah ini sebagai bukti bahwa random split menyesatkan. Alasan memakai split waktu disampaikan sebagai konsep (data nyata punya tren dan musim; random split membuat fitur lag dari masa depan bisa bocor ke training set) dan bukan sebagai hasil di notebook.

Pertanyaan penutup hands-on: "Dari lima butir daftar periksa, mana yang paling sering terlewat di proyek ML di perusahaanmu, dan siapa yang seharusnya memeriksanya?"

Catatan teknis untuk Claude Code:
- Kode hands-on lengkap dan runnable, tanpa TODO dan tanpa `___`.
- Window Spark: `Window.partitionBy("store_id").orderBy("date")` dengan `rowsBetween(-7, -1)` untuk `roll7`, `rowsBetween(-28, -1)` untuk `roll28`, dan `rowsBetween(-6, 0)` untuk `roll7_leak`. Pengujian membuktikan hasilnya sama dengan pandas (`shift(1).rolling(7)`, `shift(1).rolling(28)`, `rolling(7)`); uji kesamaan itu masuk notebook sebagai checkpoint.
- `lag_1` dan `lag_7` memakai `lag` pada window yang sama. `dow` memakai `dayofweek` (Spark: 1 Minggu sampai 7 Sabtu); sebut ini di anchor markdown karena berbeda dari pandas (Senin 0).
- Warm-up dihitung dari `cnt28` (jumlah hari tersedia dalam window 28 hari); buang baris dengan `cnt28` di bawah 28.
- Model memakai `random_state=42`. One-hot `store_type` dengan `pandas.get_dummies` dan ubah ke integer. Jangan menambah tuning.
- Metrik: MAE dan WAPE dihitung sendiri dengan numpy (rumus di atas), bukan `mean_absolute_percentage_error`.
- Jangan menjadikan hasil model sebagai klaim bahwa fitur berguna. Hanya urutan baseline, fitur, dan kebocoran yang diajarkan.
- Nilai MAE bisa berbeda sedikit antar versi scikit-learn atau numpy; kunci versi di requirements dan perbarui checkpoint bila versi diubah.
- Uji notebook lewat eksekusi sebagai notebook (kernel Jupyter), bukan hanya skrip, dan uji di Windows asli bila memungkinkan. Ukur memori dan waktu untuk RAM 8 GB.
- Format angka checkpoint (modul, slide, Answer Key): tulis persis seperti output notebook, lalu format Indonesia di dalam kurung bila angkanya besar (misal `30529554` "(30,5 juta)").
- Kode di code slide harus sama persis dengan sel notebook. Library deck mendukung sampai sekitar 24 baris (font mengecil otomatis di atas 15, 18, dan 21 baris).
- Tanpa emoji atau ikon di dokumen training formal.
- Keputusan yang menjadi hak Fahmi (ruang lingkup, konsep, angka Brief, trade-off waktu) diputuskan lewat skill `grill-me`.

## Bentuk notebook peserta
Lengkap (semua sel sudah terisi dan bisa dijalankan). Markdown di notebook hanya anchor satu atau dua baris per langkah, karena pengajar merekam video sambil menjalankan notebook secara live.

## Latihan Bertingkat
Tidak.

## Penerapan teori di PPT
Aturan lengkap: `_GLOSARIUM_dan_Aturan_Penerapan.md` bagian C. CK = Contoh kerja (1 slide, sekitar 2 menit): konsep dijalankan pada data atau angka nyata sesi ini. TD = Tebak dulu (2 slide, sekitar 3 menit): slide pertama pertanyaan (trainer berhenti 30-45 detik), slide kedua jawaban berupa angka dari hands-on dan satu kalimat alasan. Semua item ditempatkan di bagian Konsep (waktu Konsep di agenda tidak berubah; slide definisi dipadatkan menjadi sekitar 40%, penerapan sekitar 60%). Angka harus sama dengan checkpoint; angka yang bukan checkpoint diberi label "contoh satu uji" atau "Ilustrasi". Jawaban TD masuk Answer Key dan "Cek pemahaman" di Modul Praktikum.

| Kode | Setelah konsep | Isi slide | Angka dan sumber | Komponen slide |
|---|---|---|---|---|
| S10-CK1 | Fitur dan data leakage | Satu store-day: JAK-01, 2025-07-20, revenue 396.831.000. Tujuh hari sebelumnya (13 sampai 19 Juli): 537.995.000; 376.554.000; 542.578.000; 474.401.000; 424.509.000; 463.468.000; 568.459.000. `roll7` aman (7 hari sebelumnya) = 483.994.857. `roll7_leak` (6 hari sebelumnya plus hari itu) = 463.828.571, memuat target | Langkah 3 | `addLabelRowsSlide` |
| S10-CK2 | Data quality | Dari transaksi ke target: 1.000.000 baris menjadi 900.347 COMPLETED menjadi 14.600 store-day (40 toko x 365 hari); missing days 0; transaksi per store-day 17 sampai 186 (median 48); revenue maksimum 856.590.000 vs median sekitar 184,5 juta (skewness 1,37) | Langkah 1 dan 2 | `addBeforeAfterSlide` |
| S10-CK3 | Time-based split | Warm-up membuang 1.120 baris (40 toko x 28 hari), 14.600 menjadi 13.480; training set 9.800 baris (2025-01-29 sampai 2025-09-30); test set 3.680 baris (2025-10-01 sampai 2025-12-31) | Langkah 4 | `addTimelineSlide` |
| S10-TD1 | Data leakage | Tebak: bila fitur memuat hari yang diprediksi, WAPE turun dari 20,1% menjadi berapa? Jawaban: 13,6% (MAE 45,1 juta menjadi 30,5 juta), tanpa pengetahuan baru | Langkah 6 | `addTwoPanelSlide`, `addBeforeAfterSlide` |
| S10-TD2 | Baseline | Tebak: GradientBoosting atau baseline rata-rata toko, siapa yang menang? Jawaban: baseline (WAPE 0,1994 vs 0,2014); data sintetis tidak punya pola selain level toko | Langkah 5 | `addTwoPanelSlide`, `addComparisonTableSlide` |
| S10-TD3 | Rekayasa fitur | Tebak: `lag_7` atau `roll28`, mana yang lebih baik? Jawaban: `roll28` (WAPE 0,2012 vs 0,2776); satu hari mentah membawa seluruh derau hari itu | Langkah 5 | `addTwoPanelSlide`, `addStatSlide` |

## Komponen slide yang disarankan per bagian
Acuan: `brand/slide-templates/Template_Training_Insignia.pdf`.
- Penerapan teori: sisipkan slide Contoh kerja (CK) dan Tebak dulu (TD) sesuai bagian "Penerapan teori di PPT"; komponen per item ada di tabel itu.
- Pembuka: `addCoverSlide`, `addAgendaSlide` (tabel agenda di atas), `addCardGridSlide` (4 tujuan belajar), `addTimelineSlide` (peta 10 sesi, Sesi 10 ditandai)
- Dari pipeline ke data untuk ML: `addSectionSlide`, `addBeforeAfterSlide` (laporan revenue Sesi 7 vs feature table plus target Sesi 10), `addLabelRowsSlide` (unit prediksi: satu baris per toko per hari; target; fitur)
- Data quality untuk ML: `addSectionSlide`, `addChecklistSlide` (nulls, duplikat, invalid values, status transaksi, missing days, skew), `addStatSlide` (satu angka: COMPLETED 900.347 dari 1.000.000 transaksi; sumber: hasil hands-on dataset sintetis)
- Fitur dan split waktu: `addSectionSlide`, `addComparisonTableSlide` (fitur yang aman vs yang bocor: window sebelum hari itu vs termasuk hari itu), `addTimelineSlide` (garis waktu: training set sebelum 2025-10-01, test set sesudahnya)
- Kebocoran: `addSectionSlide`, `addBeforeAfterSlide` (tanpa kebocoran: WAPE 20,1%; dengan kebocoran: WAPE 13,6%), `addTwoPanelSlide` (baseline dulu; cara mencurigai hasil yang terlalu bagus)
- Hands-on: `addSectionSlide`, `addChecklistSlide` (verifikasi environment, Java, versi library, berkas data), `addStepsCheckpointSlide` (langkah 1-4 lalu langkah 5-8), `addCodeSlide` (maks 18 baris: window function Spark untuk `lag_1`, `roll7`, dan `roll7_leak`)
- Penutup: `addNumberedListSlide` (lima butir daftar periksa data preparation untuk ML; satu poin sekilas tentang versi dataset dan drift), `addClosingSlide` (ringkasan modul 10 sesi dari data mentah sampai data siap AI/ML), `addThankYouSlide`

## Pesan kunci untuk trainer dan pertanyaan yang sering muncul
Pesan kunci:
- Kualitas model dibatasi data quality. Persiapan data yang benar lebih penting daripada model yang rumit.
- Mulai dari baseline sederhana. Model baru bernilai jika mengalahkannya.
- Hasil yang terlalu bagus adalah tanda bahaya, sering data leakage.
- Fitur untuk hari H hanya boleh memakai informasi yang sudah ada sebelum hari H.
- Untuk data berurutan, uji di masa depan dari training set.
- Data di sesi ini sintetis dan tidak punya pola; di data nyata hasil dan manfaat fitur akan berbeda.

Pertanyaan yang kemungkinan muncul:
- "Kenapa modelnya tidak lebih baik dari baseline?" Jawab: data sintetis dibuat acak per transaksi, tanpa pola hari atau bulan; yang bisa ditebak hanya level toko. Itu sengaja ditunjukkan agar peserta terbiasa membandingkan dengan baseline.
- "Kenapa pakai Spark kalau datanya cuma 14.600 baris?" Jawab: agregasi dari 1 juta transaksi dikerjakan Spark; pada data nyata puluhan atau ratusan juta baris, langkah ini yang berat. Feature table hasilnya kecil sehingga model boleh dilatih di pandas.
- "Kenapa MAE dan WAPE, bukan MAPE?" Jawab: WAPE stabil bila ada nilai kecil; MAPE membengkak pada nilai mendekati nol.
- "Kenapa `lag_7` lebih buruk dari baseline?" Jawab: satu hari yang diambil mentah mengandung seluruh derau hari itu; rata-rata toko meredam derau.
- "Kenapa `roll28` hampir sama dengan baseline?" Jawab: rata-rata panjang mendekati level toko.
- "Apakah `roll7_leak` pernah dipakai di praktik?" Jawab: kesalahan seperti ini umum, misalnya rata-rata window yang ikut menghitung hari yang diprediksi.
- "Bagaimana dengan feature store dan MLOps?" Jawab: di luar cakupan modul; hanya satu slide sekilas.
- "Bisa pakai data pelanggan?" Jawab: data retail kita tidak punya `customer_id`; use case pelanggan butuh data lain.

## Risiko teknis dan hal yang dicek sebelum sesi
- Hasil model bergantung pada versi scikit-learn dan numpy. Kunci versi dan perbarui checkpoint bila versi diubah.
- Peserta mungkin mengira model harus mengalahkan baseline. Siapkan penjelasan di Catatan Trainer bahwa hasil tanpa keunggulan adalah temuan yang sah.
- Peserta mungkin menyimpulkan "fitur lag tidak berguna" secara umum. Jelaskan bahwa kesimpulan itu hanya berlaku untuk data sintetis ini.
- Perbedaan `dayofweek` antara Spark (1 Minggu) dan pandas (0 Senin) bisa membingungkan; satu anchor markdown.
- PySpark di Windows asli gagal menulis Parquet; peserta Windows memakai WSL2 dengan `.venv` baru. Laptop RAM 8 GB sungguhan belum diuji.
- Pembaca CSV 93 MB oleh Spark pada laptop lambat bisa memakan waktu; cadangan: gunakan berkas Parquet dari Sesi 3 bila CSV terlalu lambat (pastikan skema dan angka tetap sama).
- Hands-on 65 menit padat (delapan langkah). Cadangan bila waktu mepet: langkah 7 (simpan Parquet) dan langkah 8 (daftar periksa) dibawakan trainer. Dicek saat gladi.
- Rujukan lintas sesi: "partition" di sesi ini hanya muncul sebagai `partitionBy` pada window Spark, bukan partisi folder, Spark partition, atau Kafka partition; sebut konteksnya bila dipakai.

## Istilah yang harus konsisten di semua file
- data preparation for ML, feature table, feature, target, label
- baseline, MAE, WAPE (definisi: jumlah selisih absolut dibagi jumlah revenue aktual)
- data leakage, `roll7_leak`, time-based split, training set, test set
- lag, rolling window, window function, `lag_1`, `lag_7`, `roll7`, `roll28`, `cnt28`, warm-up
- revenue = quantity x unit_price; transaksi COMPLETED; revenue harian per toko
- data quality: nulls, duplicates, invalid values, missing days, skew
- Nama dataset: `retail_transactions.csv` (1.000.000 baris, Sesi 1), `stores.csv`, tabel fitur `features_s10.parquet`
- partition: pada sesi ini hanya `partitionBy` pada window; empat arti lain di modul (folder `parts/` Sesi 2, folder `month=` Sesi 3, 6, 7, Spark partition Sesi 4, Kafka partition Sesi 5 dan 8), selalu sebut konteksnya
- Aturan bahasa istilah: lihat `_GLOSARIUM_dan_Aturan_Penerapan.md` (bagian A dan B). Istilah teknis tetap bahasa Inggris; padanan Indonesia hanya penjelasan singkat dalam kurung pada kemunculan pertama.
- Nama sesi sesuai peta 10 sesi di atas

## Hasil build dan uji (11 November 2026)
Bagian ini adalah status terbaru dan menggantikan kalimat "belum diverifikasi", "wajib menjalankan ulang", atau butir keputusan terbuka di bagian lain bila bertentangan.
- Paket Sesi 10 dibangun dan notebook dijalankan sebagai kernel Jupyter di WSL Ubuntu dengan Python 3.13.18, PySpark 4.3.0, pandas 3.0.5, numpy 2.5.4, pyarrow 26.0.1, scikit-learn 1.9.1, Java 21. Seluruh angka sama dengan Brief. Notebook selesai sekitar 37 detik; puncak RAM seluruh sistem WSL sekitar 1,8 GB.
- Median revenue harian: Spark `percentile_approx` mencetak 184452000, pandas median tepat 184465500. Keduanya benar; bukan checkpoint. Notebook mencetak angka Spark dan Answer Key menjelaskan perbedaannya (contoh bahwa fungsi perkiraan di big data bisa sedikit berbeda dari hitungan tepat).
- Ridge mencetak `LinAlgWarning: An ill-conditioned matrix detected`; angka tetap sama dengan Brief, jangan menambah penskalaan atau tuning.
- Latihan Mandiri `roll14` (rata-rata 14 hari sebelumnya, GradientBoosting): MAE 45209318, WAPE 0,2018, tidak lebih baik dari baseline 0,1994.
- Percobaan random split (WAPE 0,1962) berasal dari Brief dan tidak dijalankan ulang di notebook; alasan time-based split disampaikan sebagai konsep.
- Belum diuji: Windows asli (tidak didukung; peserta memakai WSL2) dan laptop RAM 8 GB sungguhan.

## Keputusan terbuka
1. Teks asli poin 11 outline Mas Lindo belum saya terima. Isi sesi disusun dari judul sesi dan keputusan Fahmi. Cocokkan sebelum finalisasi paket.
2. Dataset 1 juta baris Sesi 1 dipakai karena cukup untuk membuat tabel harian per toko (14.600 baris) dan ringan. Dataset 10 juta baris Sesi 3 dan 7 belum dicoba; bila dipakai, angka checkpoint harus dihitung ulang.
3. Data sintetis tidak punya pola sehingga model tidak mengalahkan baseline. Alternatif: menambahkan pola musiman ke generator data agar fitur bermakna. Itu mengubah dataset di seluruh modul, jadi tidak saya lakukan tanpa persetujuan.
4. Hands-on 65 menit dengan delapan langkah dinilai padat. Cadangan: langkah 7 dan 8 oleh trainer.
5. Laptop RAM 8 GB sungguhan belum diuji. Hasil model dari scikit-learn 1.9.1; angka bisa bergeser pada versi lain.
6. Tanggal pasti dan urutan hari untuk sesi ini belum ditetapkan (sesi dimulai awal Desember 2026). Jadwal perlu disetujui Mas Lindo dan Ko Richard.
