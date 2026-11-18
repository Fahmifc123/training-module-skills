"""Generate Modul Praktikum Big Data Sesi 2 - Common vs Big Data.

Kode di setiap langkah diambil langsung dari generate_notebook_sesi02.CELLS
supaya isi modul selalu sama dengan notebook peserta.
"""
from pathlib import Path

from docx import Document

from generate_modul_sesi01 import add_code, add_para
from generate_notebook_sesi02 import CELLS
from insignia_docx_lib import (
    add_bullets, add_checkpoint, add_heading1, add_heading2, add_substep, add_title_block,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "Big_Data" / "Sesi_02_Common_vs_Big_Data" / "2_Modul_Praktikum" / "Modul_Praktikum_Common_vs_Big_Data.docx"

CODE = [src for kind, src in CELLS if kind == "code"]  # urutan: L0, L1, L2, L3, L4, L5a, L5b, L6

MODULE_TITLE = "Common vs Big Data"
MODULE_SUBTITLE = "Big Data - Sesi 2: tangga solusi di satu laptop, dari baseline sampai partition dan proses paralel"

LEARNING_OBJECTIVES = [
    "Peserta mampu membedakan data biasa dan big data dengan 5V (volume, velocity, variety, veracity, value) dan angka nyata.",
    "Peserta mampu menjelaskan scale up vs scale out dan kapan masing-masing dipilih.",
    "Peserta mampu menjelaskan ide distributed processing: bagi data (partition), proses paralel, gabungkan hasil.",
    "Peserta mampu menilai apakah sebuah kasus perlu tools big data atau cukup pendekatan klasik.",
]

OVERVIEW = [
    "Pertanyaan bisnis sama dengan Sesi 1: berapa revenue transaksi COMPLETED per kota? Bedanya, datanya 10 kali lebih besar: "
    "retail_transactions_10m.csv, 10.000.000 baris, hasil menggandakan retail_transactions.csv Sesi 1 sebanyak 10 kali.",
    "Tangga solusi, lima cara menjawab pertanyaan yang sama: (1) baseline, semua kolom di memori; (2) optimasi: tipe hemat dan kolom seperlunya; "
    "(3) optimasi: chunked processing; (4) partition tanpa paralel; (5) partition dan proses paralel. Nilai hasil harus sama di semua cara.",
    "Cara 1-3 adalah optimasi di mesin yang sama. Cara 5 memperlihatkan ide scale out: data dibagi, diproses paralel, lalu hasilnya digabung. "
    "Di sistem big data, worker-nya berada di banyak mesin. Scale up (mesin lebih besar) dibahas di slide, tidak di-hands-on.",
    "Istilah: chunk = potongan saat membaca satu file; partition = bagian data yang sudah terpisah di folder parts/. "
    "revenue = quantity x unit_price, hanya untuk transaksi COMPLETED.",
    "Dataset bersifat sintetis (bukan data internal Insignia atau klien). Angka waktu dan percepatan berbeda di setiap laptop, "
    "jadi yang dipakai sebagai checkpoint hanya nilai hasil: jumlah baris, total revenue, dan equal True. "
    "Semua cara dibandingkan dengan acuan dari Langkah 1 (data Sesi 1 dikali 10), jadi langkah 2-3 boleh dilewati.",
]

PREP_CHECKLIST = [
    "Python 3.12 ke atas (pandas 3.0.5 dan numpy 2.5.4 tidak tersedia untuk Python 3.10 dan 3.11).",
    "RAM minimal 8 GB. Langkah 2-3 butuh memori kosong sekitar 4 GB (puncak proses terukur 3,8 GB). Jika RAM di bawah 12 GB, lewati langkah 2-3 dan lihat demo trainer; langkah 4-6 tetap bisa dijalankan. Tutup aplikasi berat sebelum hands-on.",
    "Ruang disk kosong sekitar 2 GB untuk retail_transactions_10m.csv (945-955 MB, tergantung OS) dan folder parts/ (sekitar 950 MB).",
    "Folder 3_Starter_Kit_Peserta sudah disalin dari folder bersama: Notebook_Tangga_Solusi.ipynb, workers.py, make_data_s02.py, "
    "retail_transactions.csv, requirements.txt, README_Setup.md.",
    "make_data_s02.py sudah dijalankan SEBELUM hari sesi (butuh beberapa menit). Lihat README_Setup.md.",
]

STEPS = [
    {
        "title": "Langkah 0 - Verifikasi Environment dan Data",
        "substeps": [
            ("0.1", "Pastikan setup di README_Setup.md sudah selesai, termasuk python make_data_s02.py."),
            ("0.2", "Buka Notebook_Tangga_Solusi.ipynb di Jupyter atau VS Code, lalu pilih kernel .venv."),
            ("0.3", "Klik sel Langkah 0, lalu tekan Shift+Enter."),
            ("0.4", "Bandingkan angka Core dengan File parts/. Keduanya harus sama, kecuali make_data_s02.py dijalankan di laptop lain."),
        ],
        "code": CODE[0],
        "checkpoint": "pandas : 3.0.5. RAM minimal sekitar 8 GB. File 10m ada : True. File parts/ sama dengan jumlah core. "
                      "Jika RAM di bawah 12 GB, muncul baris Saran : RAM < 12 GB -> lewati langkah 2-3. Ikuti saran itu. "
                      "Jika File parts/ bernilai 0, jalankan python make_data_s02.py di terminal.",
    },
    {
        "title": "Langkah 1 - Kenali Data dan Siapkan Acuan",
        "substeps": [
            ("1.1", "Jalankan sel Langkah 1. Sel ini menghitung ukuran file dan jumlah baris tanpa memuat data ke memori."),
            ("1.2", "Sel ini juga membaca retail_transactions.csv Sesi 1 (1 juta baris) dan mengalikan revenue per kota dengan 10. Hasilnya, expected, menjadi acuan untuk semua cara. Data 10 juta baris adalah data Sesi 1 yang digandakan 10 kali."),
            ("1.3", "Variabel summary dibuat kosong di sel ini untuk mencatat hasil tiap cara, dipakai di langkah 6."),
        ],
        "code": CODE[1],
        "checkpoint": "Ukuran file: 955 MB di Windows, 945 MB di macOS/Linux (akhir baris berbeda). Jumlah baris: 10,000,000 (10 juta). Jumlah core sesuai laptop. "
                      "Total revenue acuan: 32,737,599,110,000 (32,7 triliun).",
    },
    {
        "title": "Langkah 2 - Baseline: Semua Kolom ke Memori",
        "substeps": [
            ("2.0", "RAM di bawah 12 GB: lewati langkah 2 dan 3, lanjut ke langkah 4. Langkah 4-6 tetap dibandingkan dengan acuan dari langkah 1."),
            ("2.1", "Jalankan sel Langkah 2. Pembacaan file butuh puluhan detik di sebagian laptop; selama tanda [*] masih muncul, notebook sedang bekerja."),
            ("2.2", "Catat memori dan total revenue. Bandingkan dengan Sesi 1: 155 MB untuk 1 juta baris."),
        ],
        "code": CODE[2],
        "checkpoint": "Memori: 1,575 MB (1.575 MB, sekitar 1,6 GB). Total revenue: 32,737,599,110,000 (32,7 triliun, tepat 10 kali Sesi 1). equal: True. "
                      "Jakarta teratas dengan 9181176340000 (9,18 triliun).",
    },
    {
        "title": "Langkah 3 - Optimasi: Tipe Hemat dan Kolom Seperlunya",
        "substeps": [
            ("3.0", "Ini optimasi di mesin yang sama, bukan scale up. Scale up berarti memakai mesin yang lebih besar."),
            ("3.1", "Jalankan sel Langkah 3. Kolom teks yang nilainya berulang diubah menjadi category, quantity dan unit_price menjadi int32."),
            ("3.2", "Bandingkan memori semua kolom dengan memori tanpa transaction_id dan transaction_ts. Tipe hemat saja memangkas 1.575 MB menjadi 620 MB; membuang dua kolom unik itu memangkasnya lagi menjadi 150 MB. Angka 150 MB inilah yang masuk ke tabel langkah 6."),
            ("3.3", "Baris terakhir sel menghapus df dan slim dengan del supaya memori lega untuk langkah berikutnya."),
        ],
        "code": CODE[3],
        "checkpoint": "Memori semua kolom: sekitar 620 MB. Memori tanpa id dan timestamp: sekitar 150 MB. equal: True.",
    },
    {
        "title": "Langkah 4 - Optimasi: Chunked Processing",
        "substeps": [
            ("4.1", "Jalankan sel Langkah 4. File dibaca per chunk 1 juta baris, hanya 4 kolom yang dibutuhkan (usecols)."),
            ("4.2", "Setiap chunk menghasilkan hasil parsial revenue per kota, lalu semua hasil parsial digabungkan."),
        ],
        "code": CODE[4],
        "checkpoint": "Jumlah chunk: 10. Memori satu chunk: sekitar 48 MB. equal: True.",
    },
    {
        "title": "Langkah 5a - Partition tanpa Paralel",
        "substeps": [
            ("5a.1", "Jalankan sel Langkah 5a. Setiap file di parts/ dibaca dan dihitung satu per satu oleh satu proses."),
            ("5a.2", "Catat waktunya. Angka ini menjadi pembanding untuk langkah 5b."),
        ],
        "code": CODE[5],
        "checkpoint": "Jumlah partition sama dengan File parts/ di langkah 0. equal: True.",
    },
    {
        "title": "Langkah 5b - Partition dan Proses Paralel (Ide Scale Out)",
        "substeps": [
            ("5b.1", "Jalankan sel Langkah 5b. multiprocessing.Pool menjalankan satu worker per partition. Fungsi worker diambil dari workers.py."),
            ("5b.2", "Bandingkan waktu dengan langkah 5a. Percepatan dibatasi jumlah core, kecepatan disk, dan biaya koordinasi proses."),
            ("5b.3", "Di laptop, semua worker berjalan di satu mesin. Di sistem big data, worker berada di banyak mesin. Itulah scale out."),
        ],
        "code": CODE[6],
        "checkpoint": "Jumlah worker sama dengan jumlah partition. equal: True. Angka lebih cepat berbeda di setiap laptop dan bukan kriteria berhasil.",
    },
    {
        "title": "Langkah 6 - Bandingkan Lima Cara",
        "substeps": [
            ("6.1", "Jalankan sel Langkah 6. Tabel merangkum memori, waktu, dan total revenue dari kelima cara. Cara yang dilewati tertulis dilewati."),
            ("6.2", "Perhatikan kolom waktu_untuk: waktu cara 2 hanya agregasi karena data sudah ada di memori."),
            ("6.3", "Kolom mem_data_mb adalah memori dataframe, bukan memori proses di Task Manager. Proses Python butuh lebih banyak; di cara 5 setiap worker memuat Python dan pandas sendiri, dan itu bagian dari biaya koordinasi."),
            ("6.4", "Jawab tiga pertanyaan checklist keputusan di sel terakhir, lalu pertanyaan penutup: kalau datanya 1 miliar baris dan satu laptop tidak cukup, apa yang kamu butuhkan dari sebuah sistem?"),
        ],
        "code": CODE[7],
        "checkpoint": "Semua hasil sama: True. Kolom total_revenue bernilai 32737599110000 (32,7 triliun) dan kolom sama bernilai True di setiap baris yang dijalankan.",
    },
]


def build() -> None:
    doc = Document()
    add_title_block(doc, kicker="Modul Praktikum", title=MODULE_TITLE, subtitle=MODULE_SUBTITLE)

    add_heading1(doc, 1, "Tujuan Pembelajaran")
    add_bullets(doc, LEARNING_OBJECTIVES)

    add_heading1(doc, 2, "Gambaran Alur Tangga Solusi")
    for text in OVERVIEW:
        add_para(doc, text)

    add_heading1(doc, 3, "Persiapan Sebelum Mulai")
    add_bullets(doc, PREP_CHECKLIST)

    add_heading1(doc, 4, "Langkah Mengerjakan (Detail)")
    add_para(doc, "Semua sel di notebook sudah terisi lengkap. Jalankan sel secara berurutan dari atas. "
                  "Jika kernel mati karena memori penuh, pilih Restart Kernel, jalankan Langkah 0 dan 1, lalu lanjut dari langkah 4 (lewati langkah 2-3).", italic=True)
    for step in STEPS:
        add_heading2(doc, step["title"])
        for label, text in step["substeps"]:
            add_substep(doc, label, text)
        add_code(doc, step["code"])
        add_checkpoint(doc, step["checkpoint"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("->", OUT)


if __name__ == "__main__":
    build()
