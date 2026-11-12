# Standar Materi dan Alur Kerja

## 1. Alur dua tahap

| Tahap | Di mana | Hasil |
|---|---|---|
| A. Belajar dan brainstorming | Project Claude (claude.ai) | Pemahaman topik, outline, Brief yang disetujui |
| B. Generate paket materi | Claude Code + repo insignia-training-assets | Paket sesuai mode Brief |
| C. Review dan status | Kembali ke Project | Daftar temuan, Update Status |

Urutan: Belajar, Brief (disetujui), Generate di Claude Code, Review di Project, perbaikan di Claude Code, Update Status.

## 2. Dua jenis Brief

| | Live Session | Preparation |
|---|---|---|
| Untuk | Satu sesi yang dibawakan mentor dan direkam | Modul self-study yang dibagikan (misalnya onboarding via HR) |
| Nama file | `Brief_Live_<Workstream>_Sesi_NN_<Judul>.md` | `Brief_Preparation_<Nama_Modul>.md` |
| Template | `briefs/templates/Brief_Live_Session_TEMPLATE.md` | `briefs/templates/Brief_Preparation_TEMPLATE.md` |
| Output | 1_PPT, 2_Modul_Praktikum, 3_Starter_Kit_Peserta, 4_Instructor_Only | 1_Modul_Sheet, 2_Materi_Baru, 3_Materi_Rujukan, 4_Mentor_Only |

Brief yang sudah dibuat dengan nama lama (`Brief_Sesi_NN_<Judul>.md`, header `BRIEF SESI`) tetap dikenali sebagai Live Session.

Semua bidang Brief wajib diisi sebelum dibawa ke Claude Code. Brief final disimpan di folder `briefs/` pada repo.

## 3. Format Brief Live Session

```
BRIEF LIVE SESSION

Workstream:
Sesi: <nomor dan judul>
Tanggal mengajar:
Deskripsi satu kalimat:
Track:
Tujuan belajar (maksimal 4):
Konsep inti (urutan penyampaian):
Use case dan dataset sintetis:
Platform dan tools peserta:
Durasi total: <default 120 menit>
Agenda dan rentang waktu:
Rancangan hands-on (langkah, perkiraan menit, output tiap checkpoint):
Bentuk notebook peserta: <lengkap | ada bagian latihan yang dikosongkan>
Latihan Bertingkat: <tidak | ya>
Komponen slide yang disarankan per bagian:
Pesan kunci untuk trainer dan pertanyaan yang sering muncul:
Risiko teknis dan hal yang dicek sebelum sesi:
Istilah yang harus konsisten di semua file:
Keputusan terbuka:
```

## 4. Format Brief Preparation

```
BRIEF PREPARATION

Workstream:
Nama modul:
Deskripsi satu kalimat:
Target peserta dan prasyarat:
Cara distribusi:
Platform dan tools peserta:
Tujuan modul (maksimal 5):
Aturan untuk peserta:
Kebijakan nama klien di materi: <tetap | disamarkan>
Struktur blok dan bagian (per bagian: Blok, Judul, Topics, Objective, Deliverable, Bukti selesai, Dataset, Materi dipakai ulang atau baru, Kriteria cek mentor):
Spesifikasi modul sheet (nama file, tab Start here, kolom tab Modul, tab tambahan):
Materi lama yang dipakai ulang:
Materi baru yang perlu dibuat:
Answer key dan rubrik untuk mentor:
Risiko teknis dan hal yang perlu diverifikasi:
Istilah yang harus konsisten di semua file:
Keputusan terbuka:
```

## 5. Mode Belajar
- Mulai dari masalah yang diselesaikan topik tersebut, lalu mekanismenya, lalu tools.
- Gunakan analogi dari hal yang sudah familiar.
- Jalankan contoh kecil yang bisa dicoba pengguna. Jika butuh Docker atau cluster dan lingkungan tidak mendukung, tulis perintahnya lengkap untuk dijalankan di komputer pengguna.
- Sisipkan 3-5 pertanyaan cek pemahaman, jawaban dibuka setelah pengguna mencoba.
- Tutup dengan ringkasan: konsep yang wajib dibawakan, istilah yang perlu didefinisikan, dan ide hands-on.

## 6. Mode Review
Periksa hasil Claude Code terhadap Brief dan Definition of Done sesuai mode. Beri temuan berurutan dari yang paling penting, dengan lokasi file dan saran perbaikan yang bisa ditempel kembali ke Claude Code sebagai prompt revisi. Tandai inkonsistensi antar file (nama use case, angka, istilah) sekecil apa pun.

## 7. Definition of Done

Live Session:
- Brief disetujui pengguna
- Keempat folder terisi dan nama file konsisten dengan rujukan di Modul Praktikum
- Setiap CHECKPOINT di Modul Praktikum punya jawaban di Answer Key
- Notebook SOLUTION dijalankan penuh dari awal tanpa error, angka cocok dengan Answer Key
- Slide dirender dan dicek tidak ada teks terpotong

Preparation:
- Brief disetujui pengguna
- Setiap bagian di modul sheet punya Deliverable, Bukti Selesai, dan Kriteria Cek Mentor yang bisa diverifikasi
- Setiap file di kolom Materi ada di 2_Materi_Baru atau 3_Materi_Rujukan
- Skrip baru dijalankan tanpa error, hasilnya cocok dengan Answer Key
- Setiap deliverable proyek punya rubrik

Keduanya:
- Tidak ada emoji, tidak ada label TODO atau placeholder di file yang dilihat peserta atau direkam
- Fakta dan versi tools dicek ke sumber terkini
- Tracker diperbarui

## 8. Format blok "Update Status"

```
UPDATE STATUS - <tanggal>
Sesi / Modul: <nomor dan judul, atau nama modul>
Mode: <Live Session | Preparation>
Tahap sekarang: <Belajar | Brief | Generate | Review | QA | Selesai>
Selesai di sesi kerja ini: <1-3 poin>
File yang dihasilkan: <nama file>
Keputusan yang diambil: <jika ada>
Belum selesai / pertanyaan terbuka: <jika ada>
Langkah berikutnya: <1 poin>
```
