"""Generate Modul Praktikum Big Data Sesi 3 - Big Data Storage.

Kode di setiap langkah diambil langsung dari generate_notebook_sesi03.CELLS
supaya isi modul selalu sama dengan notebook peserta.
"""
from pathlib import Path

from docx import Document

from generate_modul_sesi01 import add_code, add_para
from generate_notebook_sesi03 import CELLS
from insignia_docx_lib import (
    add_bullets, add_checkpoint, add_heading1, add_heading2, add_substep, add_title_block,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "Big_Data" / "Sesi_03_Big_Data_Storage" / "2_Modul_Praktikum" / "Modul_Praktikum_Big_Data_Storage.docx"

CODE = [src for kind, src in CELLS if kind == "code"]  # urutan: L0, L1, L2, L3a, L3b, L4, L5, Pembersihan

MODULE_TITLE = "Big Data Storage"
MODULE_SUBTITLE = "Big Data - Sesi 3: CSV vs Parquet, column pruning, dan partitioning pada 10 juta transaksi"

LEARNING_OBJECTIVES = [
    "Peserta mampu menjelaskan perbedaan format row-based (CSV) dan kolumnar (Parquet), dan kapan masing-masing cocok.",
    "Peserta mampu menjelaskan partitioning dan manfaatnya: hanya membaca bagian data yang diperlukan.",
    "Peserta mampu membedakan data lake, data warehouse, dan lakehouse dari sisi tujuan dan trade-off.",
    "Peserta mampu memilih format dan cara menyimpan data untuk sebuah kasus.",
]

OVERVIEW = [
    "Pertanyaan bisnis: bagaimana menyimpan 10 juta transaksi supaya kueri tertentu (hanya beberapa kolom, atau hanya satu bulan) "
    "tidak perlu membaca semuanya? Dataset: retail_transactions_10m.csv dari Sesi 2, 10.000.000 baris.",
    "Empat percobaan penyimpanan dalam satu notebook: (1) simpan sebagai CSV dan Parquet; (2) column pruning, baca dua kolom saja; "
    "(3) partitioning per bulan dan baca satu bulan; (4) terlalu banyak partition pada 100.000 baris pertama retail_transactions.csv "
    "(Sesi 1). Langkah 5 menutup dengan tabel keputusan.",
    "Istilah: chunk = potongan saat membaca satu file; partition = bagian data yang disimpan terpisah (satu folder per nilai kolom). "
    "Di langkah 2, total quantity x unit_price dihitung untuk semua status, bukan hanya transaksi COMPLETED seperti revenue di Sesi 1 dan 2.",
    "Dataset bersifat sintetis (bukan data internal Insignia atau klien). Angka waktu dan jumlah file persis berbeda di setiap laptop, "
    "jadi yang dipakai sebagai checkpoint hanya nilai hasil: jumlah baris, total, dan jumlah folder. Ukuran file ditulis sebagai sekitar.",
    "Hands-on hanya memakai pandas, pyarrow, dan numpy di laptop masing-masing. Data lake, data warehouse, dan lakehouse dibahas di slide, tanpa hands-on.",
]

PREP_CHECKLIST = [
    "Python 3.12 ke atas (pandas 3.0.5 dan numpy 2.5.4 tidak tersedia untuk Python 3.10 dan 3.11).",
    "Library terpasang dari requirements.txt: pandas 3.0.5, pyarrow 26.0.1, numpy 2.5.4. Lihat README_Setup.md.",
    "RAM minimal 8 GB. Notebook membaca data per chunk dan per batch, jadi puncak memori proses sekitar 2,5 GB (terukur di langkah 2, saat sengaja membaca seluruh Parquet sebagai pembanding). Tutup aplikasi berat sebelum hands-on.",
    "Ruang disk kosong minimal 3 GB (CSV sekitar 945 MB, Parquet sekitar 177 MB, versi terpartisi sekitar 225 MB, ditambah file kerja).",
    "Folder 3_Starter_Kit_Peserta sudah disalin: Notebook_Big_Data_Storage.ipynb, retail_transactions.csv, make_data_s02.py, "
    "requirements.txt, README_Setup.md.",
    "retail_transactions_10m.csv sudah ada di folder yang sama dengan notebook. Peserta yang belum punya menjalankan "
    "python make_data_s02.py SEBELUM hari sesi (butuh beberapa menit).",
]

STEPS = [
    {
        "title": "Langkah 0 - Verifikasi Environment dan Data",
        "substeps": [
            ("0.1", "Buka Notebook_Big_Data_Storage.ipynb di Jupyter atau VS Code, lalu pilih kernel .venv."),
            ("0.2", "Klik sel Langkah 0, lalu tekan Shift+Enter. Sel ini cepat (tidak memuat data): hanya cek versi, file, dan path hasil."),
            ("0.3", "Jika muncul FileNotFoundError, baca pesannya: salin retail_transactions_10m.csv dari Starter Kit Sesi 2, atau jalankan python make_data_s02.py --tanpa-parts di folder ini, lalu jalankan ulang sel."),
        ],
        "code": [CODE[0]],
        "checkpoint": "pandas : 3.0.5, pyarrow : 26.0.1, numpy : 2.5.4. File 10m: 945-955 MB (955 di Windows, 945 di macOS/Linux, karena akhir baris berbeda).",
    },
    {
        "title": "Langkah 1 - Simpan sebagai CSV dan Parquet",
        "substeps": [
            ("1.1", "Jalankan sel Langkah 1. retail_transactions_10m.csv dibaca per chunk 1 juta baris (cara chunked dari Sesi 2), dan setiap chunk ditulis ke hasil_s03/retail_10m.csv dan hasil_s03/retail_10m.parquet. Sel ini butuh sekitar satu menit; selama tanda [*] masih muncul, notebook sedang bekerja."),
            ("1.2", "Bandingkan ukuran dan waktu tulis kedua format. lineterminator=\"\\n\" membuat ukuran CSV sama di Windows, macOS, dan Linux."),
            ("1.3", "Karena dibaca per chunk, hanya satu chunk ada di memori pada satu waktu. Langkah 2 sampai 5 membaca dari file di hasil_s03, jadi sel-selnya bisa dijalankan ulang satu per satu."),
        ],
        "code": [CODE[1]],
        "checkpoint": "Jumlah baris: 10,000,000 (10 juta). CSV sekitar 945 MB, Parquet sekitar 177 MB, Parquet sekitar 5 kali lebih kecil. Tulis Parquet lebih cepat dari CSV; angka detik berbeda di setiap laptop.",
    },
    {
        "title": "Langkah 2 - Column Pruning",
        "substeps": [
            ("2.1", "Jalankan sel Langkah 2. Kedua file dibaca hanya kolom quantity dan unit_price (usecols untuk CSV, columns untuk Parquet)."),
            ("2.2", "Perhatikan: CSV tetap memindai seluruh file walau hanya dua kolom yang diambil, sedangkan Parquet hanya membaca dua kolom itu."),
            ("2.3", "Jika waktu baca Parquet terlihat janggal lama, jalankan ulang sel. Di Windows, pembacaan pertama file yang baru ditulis bisa lambat, kemungkinan karena antivirus memindai file baru."),
        ],
        "code": [CODE[2]],
        "checkpoint": "Total quantity x unit_price (semua status): 36,364,051,240,000 (36,4 triliun) di CSV dan Parquet. Sama: True.",
    },
    {
        "title": "Langkah 3 - Partitioning per Bulan",
        "substeps": [
            ("3.1", "Jalankan sel Langkah 3a. Sel ini membaca retail_10m.parquet per batch 1 juta baris, membuat kolom month dari transaction_ts, lalu setiap batch ditulis dengan partition_cols=[\"month\"]. Folder lama dihapus dulu, jadi sel aman dijalankan ulang."),
            ("3.2", "Satu folder bulan bisa berisi beberapa file (satu per batch yang memuat bulan itu). Yang dihitung adalah jumlah folder."),
            ("3.3", "Jalankan sel Langkah 3b. Maret 2025 dibaca dengan filters, jadi hanya folder month=2025-03 yang dibuka. Pembandingnya file tanpa partisi: kolom transaction_ts dari semua bulan (10 juta baris) harus dibaca dulu untuk menemukan Maret. Perhatikan jumlah baris yang dibaca, bukan hanya detiknya."),
        ],
        "code": [CODE[3], CODE[4]],
        "checkpoint": "Jumlah folder: 12, dari month=2025-01 sampai month=2025-12. Ukuran total sekitar 225 MB. "
                      "Dengan filters: baca 844,330 baris. 1 kolom, semua bulan: baca 10,000,000 baris. Maret dari pembanding: 844,330 baris. Jumlah baris sama: True.",
    },
    {
        "title": "Langkah 4 - Terlalu Banyak Partition",
        "substeps": [
            ("4.1", "Jalankan sel Langkah 4. Sel ini mengambil 100.000 baris pertama retail_transactions.csv, lalu menyimpannya sebagai satu file Parquet dan sebagai partisi per product_id."),
            ("4.2", "Tunggu sampai selesai. Sel ini wajar lama (belasan detik sampai beberapa menit, apalagi dengan antivirus aktif). Jangan buka folder hasil_s03 di file explorer."),
            ("4.3", "Perhatikan max_partitions=10_000. Tanpa parameter ini pyarrow menolak dengan ArrowInvalid: ... exceeds the maximum of 1024, batas pengaman terhadap partisi berlebihan."),
        ],
        "code": [CODE[5]],
        "checkpoint": "Nilai unik product_id: 5000. Belasan ribu file, ukuran total sekitar 93 MB dibanding sekitar 1,9 MB satu file, "
                      "rata-rata beberapa KB per file. Jumlah file persis berbeda antar mesin dan bukan kriteria berhasil.",
    },
    {
        "title": "Langkah 5 - Tabel Keputusan",
        "substeps": [
            ("5.1", "Jalankan sel Langkah 5. Tabel berisi tiga kasus dengan format, kolom partisi, dan alasannya."),
            ("5.2", "Jelaskan dengan kata-katamu sendiri kenapa tiap kasus memakai pilihan itu. Bandingkan dengan hasil langkah 1 sampai 4."),
        ],
        "code": [CODE[6]],
        "checkpoint": "Tabel tampil dengan 3 baris: CSV tanpa partisi, Parquet partisi month, Parquet tanpa partisi. Kamu bisa menjelaskan alasan ketiganya.",
    },
    {
        "title": "Langkah 6 - Pembersihan",
        "substeps": [
            ("6.1", "Setelah sesi selesai, jalankan sel Pembersihan untuk menghapus folder hasil_s03."),
            ("6.2", "Penghapusan belasan ribu file bisa butuh beberapa menit di Windows. Tunggu sampai sel selesai."),
        ],
        "code": [CODE[7]],
        "checkpoint": "hasil_s03 ada: False. Ruang disk sekitar 1,4 GB kembali tersedia.",
    },
]

SELF_PRACTICE = [
    "Partisi data 10 juta baris per city (8 nilai unik) dengan pola per batch dari langkah 3a, lalu baca hanya Jakarta dengan filters. Bandingkan jumlah folder dan ukuran total dengan partisi per month.",
    "Simpan retail_10m.parquet dengan compression=\"gzip\" dan bandingkan ukuran serta waktu tulis dengan bawaan (snappy). Tulis gzip bisa butuh lebih dari satu menit.",
    "Coba partition_cols=[\"month\", \"city\"]. Hitung jumlah file dan pikirkan kapan dua kolom partisi masih masuk akal.",
]


def build() -> None:
    doc = Document()
    add_title_block(doc, kicker="Modul Praktikum", title=MODULE_TITLE, subtitle=MODULE_SUBTITLE)

    add_heading1(doc, 1, "Tujuan Pembelajaran")
    add_bullets(doc, LEARNING_OBJECTIVES)

    add_heading1(doc, 2, "Gambaran Alur Percobaan Penyimpanan")
    for text in OVERVIEW:
        add_para(doc, text)

    add_heading1(doc, 3, "Persiapan Sebelum Mulai")
    add_bullets(doc, PREP_CHECKLIST)

    add_heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    add_para(doc, "Semua sel di notebook sudah terisi lengkap. Jalankan sel secara berurutan dari atas. "
                  "Jika kernel mati, pilih Restart Kernel, jalankan Langkah 0 (cepat, tidak memuat data), lalu lanjut dari langkah mana pun setelah langkah 1. "
                  "Langkah 1 cukup dijalankan sekali, karena file hasilnya tersimpan di hasil_s03.", italic=True)
    for step in STEPS:
        add_heading2(doc, step["title"])
        for label, text in step["substeps"]:
            add_substep(doc, label, text)
        for code in step["code"]:
            add_code(doc, code)
        add_checkpoint(doc, step["checkpoint"])

    add_heading1(doc, 5, "Latihan Mandiri")
    add_bullets(doc, SELF_PRACTICE)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("->", OUT)


if __name__ == "__main__":
    build()
