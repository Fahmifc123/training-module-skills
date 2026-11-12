# insignia-training-assets

Kit skill Claude Code untuk membuat materi training Data & AI Insignia dari Brief yang disusun di Project claude.ai.

## Alur kerja

1. Susun Brief di Project claude.ai memakai template di `briefs/templates/`.
2. Simpan Brief yang sudah disetujui ke `briefs/`.
3. Jalankan `claude` dari root repo ini, lalu kirim:
   ```
   Pakai skill insignia-training-module dengan brief briefs/<nama_file>.md
   ```
4. Hasil tersimpan di `output/<Workstream>/...` (tidak di-commit).
5. Bawa hasilnya ke Project untuk Mode Review.

## Dua mode

| | Live Session | Preparation |
|---|---|---|
| Untuk | Satu sesi yang dibawakan mentor | Modul self-study yang dibagikan (misalnya onboarding via HR) |
| Header Brief | `BRIEF LIVE SESSION` | `BRIEF PREPARATION` |
| Output | `1_PPT`, `2_Modul_Praktikum`, `3_Starter_Kit_Peserta`, `4_Instructor_Only` | `1_Modul_Sheet`, `2_Materi_Baru`, `3_Materi_Rujukan`, `4_Mentor_Only` |
| Detail | `.claude/skills/insignia-training-module/modes/live-session.md` | `.claude/skills/insignia-training-module/modes/preparation.md` |

## Daftar skill

| Skill | Fungsi |
|---|---|
| insignia-training-module | Orkestrator dua mode. Aturan lintas skill ada di `references/aturan-bersama.md` |
| insignia-ppt-deck | Deck .pptx dengan `insignia_deck_lib.js` |
| insignia-docx-module | .docx: Modul Praktikum dan Panduan Bagian (`generate_docx.py`) |
| insignia-xlsx-tracker | .xlsx: Tracker dan Modul Sheet (`generate_xlsx.py`) |
| html-to-png-render | HTML ke PNG via Playwright |
| insignia-image-gen | Foto stok Unsplash dengan atribusi |
| grill-me | Wawancara keputusan milik pengguna, menghasilkan Decision Log |

## Setup satu kali

```bash
git clone <url-repo> insignia-training-assets
cd insignia-training-assets
npm install                              # pptxgenjs untuk deck
pip install python-docx openpyxl         # docx dan xlsx
npm install playwright && npx playwright install chromium   # jika butuh render HTML ke PNG
```

Uji cepat generator:

```bash
python .claude/skills/insignia-docx-module/generate_docx.py demo output/_demo
python .claude/skills/insignia-xlsx-tracker/generate_xlsx.py demo output/_demo
```

Opsional: set `UNSPLASH_ACCESS_KEY` untuk skill image-gen. Jangan commit key ke repo.

## Mengupdate skill

1. Buat branch: `git checkout -b update/<nama-skill>-<ringkas>`.
2. Ubah skill. Aturan yang berlaku untuk semua skill diubah di `aturan-bersama.md`, jangan disalin ke tiap skill.
3. Jalankan uji cepat generator jika `generate_*.py` berubah.
4. Catat di `CHANGELOG.md`, lalu commit dan buat PR.
5. Di komputer lain cukup `git pull`.

## Struktur repo

```
.claude/skills/        tujuh skill
brand/                 colors.json, logo, fonts, slide-templates
briefs/templates/      template Brief Live Session dan Preparation
briefs/                Brief yang sudah disetujui
docs/                  teks pengganti file 03 dan 06 di Project claude.ai
examples/              contoh paket sebagai acuan kualitas
output/                hasil generate (diabaikan git)
```

## Perlu ditambahkan sebelum push pertama

File berikut dirujuk skill tetapi belum ada di repo. Salin dari kit v2 ke root repo:

- `insignia_deck_lib.js` (wajib untuk insignia-ppt-deck)
- `generate_template_deck.js` (menghasilkan `brand/slide-templates/`)
- `package.json` (dan `package-lock.json` jika ada), berisi versi pptxgenjs yang dipakai library
- Brief yang sudah ada, ke folder `briefs/`
