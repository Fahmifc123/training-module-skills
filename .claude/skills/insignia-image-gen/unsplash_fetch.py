"""Cari & unduh foto stok dari Unsplash untuk slide training Insignia.

Pemakaian:
    python unsplash_fetch.py "<query>" <output_dir> [--count 3] [--orientation landscape] [--prefix nama]

Access Key dibaca dari env var UNSPLASH_ACCESS_KEY (fallback: registry user Windows).
Setiap unduhan memicu endpoint download_location sesuai pedoman API Unsplash,
dan atribusi ditulis ke <output_dir>/CREDITS.json + CREDITS.md.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://api.unsplash.com"
UTM = "utm_source=insignia_training_assets&utm_medium=referral"


def get_key():
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key and sys.platform == "win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                key = winreg.QueryValueEx(k, "UNSPLASH_ACCESS_KEY")[0]
        except OSError:
            pass
    if not key:
        sys.exit("UNSPLASH_ACCESS_KEY belum di-set.")
    return key


def api_get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {key}", "Accept-Version": "v1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("output_dir")
    p.add_argument("--count", type=int, default=3)
    p.add_argument("--orientation", default="landscape", choices=["landscape", "portrait", "squarish"])
    p.add_argument("--prefix", default=None, help="prefix nama file (default: query)")
    p.add_argument("--width", type=int, default=1920, help="lebar unduhan (px)")
    a = p.parse_args()

    key = get_key()
    os.makedirs(a.output_dir, exist_ok=True)
    qs = urllib.parse.urlencode({"query": a.query, "orientation": a.orientation,
                                 "per_page": a.count, "content_filter": "high"})
    results = api_get(f"{API}/search/photos?{qs}", key)["results"]
    if not results:
        sys.exit(f"Tidak ada hasil untuk '{a.query}'.")

    prefix = a.prefix or "-".join(a.query.lower().split())
    credits_path = os.path.join(a.output_dir, "CREDITS.json")
    credits = json.load(open(credits_path, encoding="utf-8")) if os.path.exists(credits_path) else []

    for i, ph in enumerate(results, 1):
        fname = f"{prefix}-{i:02d}.jpg"
        fpath = os.path.join(a.output_dir, fname)
        img_url = f"{ph['urls']['raw']}&w={a.width}&fm=jpg&q=85&fit=max"
        urllib.request.urlretrieve(img_url, fpath)
        api_get(ph["links"]["download_location"], key)  # wajib per pedoman Unsplash

        entry = {
            "file": fname,
            "query": a.query,
            "description": ph.get("alt_description") or ph.get("description") or "",
            "photographer": ph["user"]["name"],
            "photographer_url": f"{ph['user']['links']['html']}?{UTM}",
            "photo_url": f"{ph['links']['html']}?{UTM}",
            "credit_text": f"Foto: {ph['user']['name']} / Unsplash",
            "width": ph["width"], "height": ph["height"],
        }
        credits = [c for c in credits if c["file"] != fname] + [entry]
        print(f"{fname} | {entry['photographer']} | {entry['description']}")

    with open(credits_path, "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)
    with open(os.path.join(a.output_dir, "CREDITS.md"), "w", encoding="utf-8") as f:
        f.write("# Kredit Foto (Unsplash)\n\n")
        for c in credits:
            f.write(f"- `{c['file']}`: [{c['photographer']}]({c['photographer_url']}) di [Unsplash]({c['photo_url']})\n")


if __name__ == "__main__":
    main()
