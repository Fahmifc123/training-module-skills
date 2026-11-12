---
name: grill-me
description: Wawancara keputusan gaya "grill me" sebelum Claude mengubah apa pun. Claude menginterogasi Fahmi satu pertanyaan per giliran sampai setiap keputusan yang menjadi hak manusia terkunci (ruang lingkup, definisi konsep, angka di Brief, trade-off), lalu menulis Decision Log. WAJIB dipanggil otomatis dari skill insignia-* mana pun begitu muncul keputusan milik manusia. Pakai juga saat Fahmi bilang "grill me", "tanya saya dulu", "interogasi", atau setelah review/uji menghasilkan daftar temuan yang perlu diputuskan sebelum diperbaiki.
---

# Grill Me: Kunci Keputusan Manusia Dulu, Baru Eksekusi

Tujuan: tidak ada keputusan milik manusia yang diambil diam-diam oleh Claude. Claude bertanya terus, satu per satu, sampai semua keputusan jelas, lalu baru bekerja.

## Kapan dipakai

- Setelah uji atau review menghasilkan daftar temuan (misal "11 hal membingungkan di Sesi 1").
- Sebelum fase baru di skill `insignia-training-module` bila Brief punya bagian ambigu.
- Kapan pun Fahmi meminta "grill me" atau "tanya saya dulu".

## Aturan wawancara

1. **Jangan ubah file apa pun selama wawancara.** Membaca file dan menjalankan uji boleh, untuk menyiapkan pertanyaan yang tajam.
2. **Pisahkan dulu: keputusan manusia vs keputusan teknis.**
   - Manusia: ruang lingkup, definisi konsep yang diajarkan, isi dan angka di Brief, prioritas, trade-off waktu kelas, gaya bahasa, apa yang boleh dibuang.
   - Teknis (Claude putuskan sendiri, cukup dilaporkan): nama variabel, cara implementasi, perbaikan bug yang jawabannya jelas.
   - Jangan menanyakan hal yang jawabannya sudah ada di Brief, memory, atau keputusan sebelumnya. Kutip sumbernya.
3. **Satu pertanyaan per giliran**, pakai tool `AskUserQuestion`:
   - 2-4 opsi konkret, opsi rekomendasi di urutan pertama dengan label "(Rekomendasi)".
   - Tiap opsi menyebut dampaknya: file mana berubah, apakah angka Brief berubah, berapa menit kelas bertambah.
   - Bila perlu membandingkan teks atau kode, isi `preview`.
4. **Gali, jangan langsung terima.** Setelah jawaban, tanyakan lanjutan bila:
   - jawaban samar ("terserah", "yang bagus aja") → minta pilih salah satu opsi atau beri kriteria;
   - jawaban bertentangan dengan Brief atau keputusan sebelumnya → tunjukkan konfliknya, minta pilih mana yang menang;
   - jawaban memunculkan kasus tepi (laptop 8 GB, peserta terlambat, restart kernel) → tanyakan penanganannya.
5. **Urutan pertanyaan:** keputusan yang mengubah Brief atau konsep dulu, lalu yang mengubah angka checkpoint, lalu format dan gaya. Kelompokkan temuan kecil yang setipe menjadi satu pertanyaan ("Terapkan format angka yang sama dengan Sesi 1?").
6. **Tantang diri sendiri juga.** Bila Fahmi memilih opsi yang Claude anggap berisiko, sampaikan risikonya sekali dengan bukti (angka uji, file, baris), lalu hormati keputusannya.
7. **Berhenti bertanya** bila semua keputusan manusia sudah terkunci, atau Fahmi bilang "cukup", "lanjut", atau "eksekusi".

## Decision Log

Setelah wawancara selesai, tampilkan Decision Log di chat sebelum mengerjakan apa pun:

| # | Keputusan | Pilihan Fahmi | Dampak (file, angka Brief) |
|---|---|---|---|

Lalu:
- Daftar **keputusan teknis** yang Claude ambil sendiri (satu baris per item).
- Daftar **teks Brief yang harus diperbarui** (lama vs baru), bila ada.
- Satu pertanyaan konfirmasi terakhir: "Eksekusi sesuai log ini?" Baru setelah dijawab ya, mulai mengubah file.

Bila keputusan bersifat jangka panjang (berlaku untuk sesi-sesi berikutnya, misal format angka checkpoint), tawarkan untuk menyimpannya ke memory.

## Contoh pembuka

> Ada 8 temuan di Sesi 2. 5 di antaranya teknis dan akan saya putuskan sendiri. 3 butuh keputusan Anda. Pertanyaan 1 dari 3: definisi "scale up" ...
