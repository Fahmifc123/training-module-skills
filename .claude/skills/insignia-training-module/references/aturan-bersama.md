# Aturan Bersama Semua Skill insignia-*

File ini satu-satunya sumber aturan lintas skill. Skill lain merujuk ke sini, jangan menyalin ulang isinya.

## 1. Bahasa dan gaya

- Bahasa Indonesia sebagai bahasa utama. Istilah teknis, nama tool, dan nama tombol UI tetap bahasa Inggris sesuai tampilan aslinya.
- Tanpa emoji atau ikon dekoratif di semua file yang dilihat peserta. Simbol fungsional (centang dan silang di Before/After) boleh.
- Copy untuk peserta ringkas. Penjelasan panjang masuk speaker notes, catatan trainer, atau materi Mentor Only.
- Markdown di notebook hanya anchor ringkas, karena pengajar menjelaskan secara live sambil merekam.

## 2. Kode

- Kode hands-on lengkap dan runnable, tanpa label TODO atau placeholder yang tertinggal.
- Jalankan kode sebelum diserahkan, dan laporkan hasilnya.
- Jangan merujuk file yang tidak benar-benar dibuat di paket.

## 3. Data dan fakta

- Jangan mengarang data internal Insignia atau klien. Pakai dataset sintetis dan sebutkan bahwa datanya sintetis.
- Fakta yang bisa berubah (versi library, harga cloud, nama fitur tool) dicek ke sumber terkini sebelum ditulis.
- Nama klien di materi mengikuti keputusan di Brief.

## 4. Brand

- Warna dan font hanya dari `brand/colors.json`. Logo dari `brand/logo-light-bg.png` dan `brand/logo-dark-bg.png`.
- Baca `colors.json` dari kode (jangan hardcode warna). Path dihitung dari root repo: `<root>/brand/colors.json`.
- Acuan visual deck: `brand/slide-templates/Template_Training_Insignia.pdf`.

## 5. Konsistensi paket

- Nama use case, angka, istilah, dan nama file harus sama persis di semua file dalam satu paket.
- Revisi di satu file wajib dicek dampaknya ke file lain di paket yang sama.
- Istilah penting didaftarkan di bagian "Istilah yang harus konsisten" pada Brief.

## 6. Path output

- Semua output ditulis ke `output/<Workstream>/...`, dengan struktur folder sesuai mode di `modes/`.
- Folder `output/` tidak di-commit ke repo.

## 7. Keputusan manusia

Keputusan yang menjadi hak pengguna (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu, gaya, pilihan visual) tidak diambil diam-diam. Panggil skill `grill-me`, selesaikan wawancara dan Decision Log, baru lanjut bekerja. Keputusan teknis murni (nama variabel, cara implementasi, perbaikan bug yang jawabannya jelas) diputuskan sendiri dan cukup dilaporkan.
