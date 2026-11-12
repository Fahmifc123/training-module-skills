"""Alur batch hemat kuota: kandidat -> pilih -> finalisasi.

1) candidates  : satu search per slot, unduh preview kecil (CDN, tidak memotong kuota API),
                 buat contact sheet per grup untuk dicek visual.
2) finalize    : unduh resolusi penuh foto terpilih + trigger download_location
                 (wajib pedoman Unsplash), tulis CREDITS.json/CREDITS.md di folder tujuan.

Pemakaian:
    python unsplash_batch.py candidates <plan.json> <work_dir> [--per 4]
    python unsplash_batch.py finalize   <plan.json> <work_dir> [--width 1920]

plan.json: [{"id": "s04-sec1", "group": "Sesi 04", "query": "server racks",
             "out": "output/.../photos/s04-sec1.jpg", "pick": 0}, ...]
"pick" (indeks kandidat) diisi setelah melihat contact sheet. Kedua langkah bisa diulang:
slot yang sudah selesai dilewati, dan proses berhenti rapi saat kuota habis (HTTP 403).
"""
import argparse
import io
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unsplash_fetch import API, UTM, api_get, get_key  # noqa: E402


def load(p, default):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def dump(obj, p):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def retrieve(url, path, tries=3):
    # CDN Unsplash sesekali timeout; ulangi beberapa kali sebelum menyerah.
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r, open(path, "wb") as f:
                f.write(r.read())
            return True
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
    print(f"  gagal unduh: {url[:60]}")
    return False


def contact_sheets(plan, cands, work):
    from PIL import Image, ImageDraw
    groups = {}
    for slot in plan:
        if slot["id"] in cands:
            groups.setdefault(slot.get("group", "all"), []).append(slot)
    tw, th, lab = 320, 180, 22
    for g, slots in groups.items():
        per = max(len(cands[s["id"]]) for s in slots)
        sheet = Image.new("RGB", (tw * per, (th + lab) * len(slots)), "white")
        d = ImageDraw.Draw(sheet)
        for r, s in enumerate(slots):
            y = r * (th + lab)
            d.text((4, y + 4), f"{s['id']} | {s['query']}", fill="black")
            for c, ph in enumerate(cands[s["id"]]):
                im = Image.open(os.path.join(work, ph["preview"])).convert("RGB")
                im.thumbnail((tw - 6, th - 4))
                sheet.paste(im, (c * tw + 3, y + lab))
                d.rectangle([c * tw + 3, y + lab, c * tw + 30, y + lab + 18], fill="red")
                d.text((c * tw + 10, y + lab + 3), str(c), fill="white")
        out = os.path.join(work, f"sheet_{g.replace(' ', '_')}.jpg")
        sheet.save(out, quality=80)
        print("contact sheet:", out)


def candidates(a, key):
    plan = load(a.plan, [])
    cpath = os.path.join(a.work, "candidates.json")
    cands = load(cpath, {})
    os.makedirs(os.path.join(a.work, "prev"), exist_ok=True)
    for slot in plan:
        if cands.get(slot["id"]):
            continue
        qs = urllib.parse.urlencode({"query": slot["query"], "orientation": "landscape",
                                     "per_page": a.per, "content_filter": "high"})
        try:
            res = api_get(f"{API}/search/photos?{qs}", key)["results"]
        except urllib.error.HTTPError as e:
            print(f"Berhenti di {slot['id']}: HTTP {e.code} (kuota habis?)")
            break
        lst = []
        for i, ph in enumerate(res):
            prev = f"prev/{slot['id']}_{i}.jpg"
            if not retrieve(ph["urls"]["small"], os.path.join(a.work, prev)):
                continue
            lst.append({"preview": prev, "raw": ph["urls"]["raw"], "download_location": ph["links"]["download_location"],
                        "photographer": ph["user"]["name"], "user_html": ph["user"]["links"]["html"],
                        "photo_html": ph["links"]["html"], "description": ph.get("alt_description") or ""})
        cands[slot["id"]] = lst
        dump(cands, cpath)
        print(f"{slot['id']}: {len(lst)} kandidat")
    contact_sheets(plan, cands, a.work)


def finalize(a, key):
    plan = load(a.plan, [])
    cands = load(os.path.join(a.work, "candidates.json"), {})
    for slot in plan:
        if slot.get("pick") is None or slot["id"] not in cands:
            continue
        ph = cands[slot["id"]][slot["pick"]]
        out = slot["out"]
        out_dir = os.path.dirname(out)
        os.makedirs(out_dir, exist_ok=True)
        cred_path = os.path.join(out_dir, "CREDITS.json")
        credits = load(cred_path, [])
        fname = os.path.basename(out)
        done = next((c for c in credits if c["file"] == fname and c["photo_url"].startswith(ph["photo_html"])), None)
        if done and os.path.exists(out):
            continue
        try:
            api_get(ph["download_location"], key)
        except urllib.error.HTTPError as e:
            print(f"Berhenti di {slot['id']}: HTTP {e.code} (kuota habis?)")
            break
        if not retrieve(f"{ph['raw']}&w={a.width}&fm=jpg&q=85&fit=max", out):
            continue
        entry = {"file": fname, "query": slot["query"], "description": ph["description"],
                 "photographer": ph["photographer"], "photographer_url": f"{ph['user_html']}?{UTM}",
                 "photo_url": f"{ph['photo_html']}?{UTM}", "credit_text": f"Foto: {ph['photographer']} / Unsplash"}
        credits = [c for c in credits if c["file"] != fname] + [entry]
        dump(credits, cred_path)
        with open(os.path.join(out_dir, "CREDITS.md"), "w", encoding="utf-8") as f:
            f.write("# Kredit Foto (Unsplash)\n\n")
            for c in credits:
                f.write(f"- `{c['file']}`: [{c['photographer']}]({c['photographer_url']}) di [Unsplash]({c['photo_url']})\n")
        print(f"{slot['id']} -> {out} ({ph['photographer']})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["candidates", "finalize"])
    p.add_argument("plan")
    p.add_argument("work")
    p.add_argument("--per", type=int, default=4)
    p.add_argument("--width", type=int, default=1920)
    a = p.parse_args()
    os.makedirs(a.work, exist_ok=True)
    key = get_key()
    candidates(a, key) if a.cmd == "candidates" else finalize(a, key)


if __name__ == "__main__":
    main()
