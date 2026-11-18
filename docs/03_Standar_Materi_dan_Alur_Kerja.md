# Standar Materi dan Alur Kerja

## 1. Alur dua tahap

| Tahap | Di mana | Hasil |
|---|---|---|
| A. Belajar dan brainstorming | Project Claude (claude.ai) | Pemahaman topik, outline, Brief yang disetujui |
| B. Generate paket materi | Claude Code + repo training-module-skills | Paket sesuai mode Brief |
| C. Review dan status | Kembali ke Project | Daftar temuan, Update Status |

Urutan: Belajar, Brief (disetujui), Generate di Claude Code, Review di Project, perbaikan di Claude Code, Update Status.

## 2. Dua jenis Brief

| | Live Session | Preparation |
|---|---|---|
| Untuk | Satu sesi yang dibawakan mentor dan direkam | Modul self-study yang dibagikan (misalnya onboarding via HR) |
| Nama file | `Brief_Sesi_NN_<Judul>.md` | `Brief_Preparation_<Nama_Program>.md` |
| Template | `briefs/templates/Brief_Live_Session_TEMPLATE.md` | `briefs/templates/Brief_Preparation_TEMPLATE.md` |
| Output | 1_PPT, 2_Modul_Praktikum, 3_Starter_Kit_Peserta, 4_Instructor_Only | 1_Modul_Sheet (format DE), 2_Materi_Baru, 3_Materi_Rujukan, 4_Mentor_Only |

Header lama `BRIEF SESI` tetap dikenali sebagai Live Session. Brief disimpan di `briefs/<Workstream>/`.

Semua bidang Brief wajib diisi sebelum dibawa ke Claude Code.

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

Ikuti `briefs/templates/Brief_Preparation_TEMPLATE.md` di repo training-module-skills. Strukturnya per Modul dan Sub Modul, mengikuti kolom modul sheet (format DE): Materi, Category, Learning Objectives, Difficulty, Output / Deliverable, Material Source, link PPT, Video, External, dan Referensi Section. Setiap modul diakhiri Mini Project dan Test Modul.

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
- Setiap sub modul punya Learning Objectives dan Output / Deliverable yang bisa diverifikasi; setiap modul diakhiri Test Modul
- Setiap file di kolom Internal Link PPT ada di 2_Materi_Baru atau 3_Materi_Rujukan
- Skrip baru dijalankan tanpa error, hasilnya cocok dengan Answer Key
- Setiap Mini Project punya rubrik

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
