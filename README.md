# training-module-skills

Kit skill Claude Code untuk membuat materi training Data & AI Insignia dari Brief yang disusun di Project claude.ai.

## Konsep

Repo ini hanya berisi skill dan aset brand (**kit root**). Setiap project materi punya folder sendiri, selevel dengan repo ini (**project root**):

```
Documents\github\
  training-module-skills\       repo ini (kit root)
  Onboarding_MLE_Dify\          project (project root)
    briefs\  materi_rujukan\  output\
  Big_Data\
    briefs\  output\
```

Skill dipasang global sekali, sehingga `claude` bisa dijalankan dari folder project mana pun. Cukup panggil satu skill, `insignia-training-module`. Skill itu yang memanggil skill lain sesuai kebutuhan.

## Setup satu kali (Windows)

1. Clone repo ke `Documents\github\`:
   ```cmd
   git clone https://github.com/Fahmifc123/training-module-skills.git
   ```
2. Jalankan `install_skills.bat` dari folder repo. Script ini:
   - membuat junction dari setiap skill ke `%USERPROFILE%\.claude\skills\`
   - set `TRAINING_KIT_HOME` ke folder repo
   - menjalankan `npm install`
3. `pip install python-docx openpyxl`
4. Tutup dan buka ulang terminal.

Cek: jalankan `claude` di folder mana pun, lalu ketik `/skills`. Ketujuh skill harus muncul.

## Alur per project

1. Buat project dari folder repo:
   ```cmd
   new_project.bat Onboarding_MLE_Dify
   ```
   Folder dibuat di sebelah repo, berisi `briefs\`, `materi_rujukan\`, `output\`, dan `CLAUDE.md`.
2. Simpan Brief dari Project claude.ai ke `briefs\`, dan materi lama ke `materi_rujukan\`.
3. Masuk ke folder project, jalankan `claude`, lalu kirim:
   ```
   Pakai skill insignia-training-module dengan brief briefs/<nama_file>.md
   ```
4. Hasil tersimpan di `output\` milik project. Bawa ke Project claude.ai untuk Mode Review.

## Dua mode

| | Live Session | Preparation |
|---|---|---|
| Untuk | Satu sesi yang dibawakan mentor | Modul self-study yang dibagikan (misalnya onboarding via HR) |
| Header Brief | `BRIEF LIVE SESSION` | `BRIEF PREPARATION` |
| Output | `1_PPT`, `2_Modul_Praktikum`, `3_Starter_Kit_Peserta`, `4_Instructor_Only` | `1_Modul_Sheet` (format DE), `2_Materi_Baru`, `3_Materi_Rujukan`, `4_Mentor_Only` |
| Detail | `.claude/skills/insignia-training-module/modes/live-session.md` | `.claude/skills/insignia-training-module/modes/preparation.md` |

## Daftar skill

| Skill | Fungsi |
|---|---|
| insignia-training-module | Pintu masuk utama. Orkestrator dua mode yang memanggil skill lain. Aturan lintas skill di `references/aturan-bersama.md` |
| insignia-ppt-deck | Deck .pptx dengan `insignia_deck_lib.js` |
| insignia-docx-module | .docx: Modul Praktikum dan Panduan Bagian (`generate_docx.py`) |
| insignia-xlsx-tracker | .xlsx: Tracker dan Modul Sheet format DE (`generate_xlsx.py`) |
| html-to-png-render | HTML ke PNG via Playwright |
| insignia-image-gen | Foto stok Unsplash dengan atribusi |
| grill-me | Wawancara keputusan milik pengguna, menghasilkan Decision Log |

## Uji cepat generator

Dari folder project mana pun (CMD):

```cmd
python "%TRAINING_KIT_HOME%\.claude\skills\insignia-docx-module\generate_docx.py" demo output\_demo
python "%TRAINING_KIT_HOME%\.claude\skills\insignia-xlsx-tracker\generate_xlsx.py" demo output\_demo
```

Opsional: set `UNSPLASH_ACCESS_KEY` untuk skill image-gen, dan `npx playwright install chromium` untuk render HTML ke PNG. Jangan commit key ke repo.

## Mengupdate skill

1. Ubah skill di repo ini. Aturan yang berlaku untuk semua skill diubah di `aturan-bersama.md`, jangan disalin ke tiap skill.
2. Jalankan uji cepat generator jika `generate_*.py` berubah.
3. Catat di `CHANGELOG.md`, lalu `git add -A`, `git commit`, `git push`.
4. Patch dari Project claude.ai: simpan file `.patch` di folder repo, lalu `git am <file>.patch` dan `git push`.
5. Di komputer lain cukup `git pull`. Karena skill dipasang lewat junction, semua project langsung memakai versi terbaru. Jalankan ulang `install_skills.bat` hanya jika ada skill baru atau repo dipindah.

Jangan menjalankan `claude` di dalam folder repo ini untuk membuat materi, karena skill akan terbaca dua kali (dari repo dan dari level user). Buka repo ini hanya untuk mengedit skill.

## Struktur repo

```
.claude/skills/        tujuh skill
brand/                 colors.json, logo, fonts, slide-templates
briefs/templates/      template Brief Live Session dan Preparation
briefs/Big_Data/       arsip Brief Big Data dan glosarium (salin ke project Big_Data)
docs/                  teks pengganti file 03 dan 06 di Project claude.ai
examples/              arsip generator dan contoh sebagai acuan kualitas
project-template/      isi awal folder project (dipakai new_project.bat)
install_skills.bat     pasang skill global
new_project.bat        buat folder project baru
insignia_deck_lib.js   library deck (dipakai insignia-ppt-deck)
```
