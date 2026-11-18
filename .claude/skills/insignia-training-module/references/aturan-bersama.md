# Aturan Bersama Semua Skill insignia-*

File ini satu-satunya sumber aturan lintas skill. Skill lain merujuk ke sini, jangan menyalin ulang isinya.

## 0. Kit root dan project root

Skill dipasang global (lihat `install_skills.bat` di repo), jadi ada dua lokasi yang berbeda:

- **Kit root**: repo `training-module-skills`. Isinya skill, `brand/`, `insignia_deck_lib.js`, `node_modules/`, dan `briefs/templates/`. Lokasinya dibaca dari environment variable `TRAINING_KIT_HOME`. Jika variabel itu kosong, kit root adalah folder tiga tingkat di atas folder skill ini setelah symlink atau junction di-resolve. Jika keduanya gagal, tanya pengguna.
- **Project root**: folder tempat `claude` dijalankan. Isinya `briefs/`, `materi_rujukan/`, dan `output/` milik project itu.

Aturan:
- Baca aset (brand, template, deck lib) dari kit root. Tulis semua hasil ke project root.
- Jangan pernah menulis output, Brief, atau file project ke dalam kit root.
- Panggil script skill dengan path lengkap dari kit root, misalnya `python "$TRAINING_KIT_HOME/.claude/skills/insignia-xlsx-tracker/generate_xlsx.py" ...` (Git Bash) atau `python "%TRAINING_KIT_HOME%\.claude\skills\..."` (CMD).
- Jika project root sama dengan kit root, ingatkan pengguna bahwa project sebaiknya dibuat di folder terpisah (`new_project.bat`), lalu tanya apakah tetap mau lanjut.

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

- Warna dan font hanya dari `<kit root>/brand/colors.json`. Logo dari `<kit root>/brand/logo-light-bg.png` dan `logo-dark-bg.png`.
- Baca `colors.json` dari kode (jangan hardcode warna). Generator bawaan sudah mencari kit root sendiri.
- Acuan visual deck: `<kit root>/brand/slide-templates/Template_Training_Insignia.pdf`.

## 5. Konsistensi paket

- Nama use case, angka, istilah, dan nama file harus sama persis di semua file dalam satu paket.
- Revisi di satu file wajib dicek dampaknya ke file lain di paket yang sama.
- Istilah penting didaftarkan di bagian "Istilah yang harus konsisten" pada Brief.

## 6. Path output

- Semua output ditulis ke `<project root>/output/<Paket>/...`, dengan struktur folder sesuai mode di `modes/`. `<Paket>` adalah `Sesi_NN_<Judul>` (Live Session) atau `<Nama_Program>` (Preparation).

## 7. Keputusan manusia

Keputusan yang menjadi hak pengguna (ruang lingkup, definisi konsep, isi atau angka Brief, prioritas temuan, trade-off waktu, gaya, pilihan visual) tidak diambil diam-diam. Panggil skill `grill-me`, selesaikan wawancara dan Decision Log, baru lanjut bekerja. Keputusan teknis murni (nama variabel, cara implementasi, perbaikan bug yang jawabannya jelas) diputuskan sendiri dan cukup dilaporkan.
