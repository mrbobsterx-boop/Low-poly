#!/usr/bin/env python3
"""Скачать сырые модели Tripo с Google Диска автора (папка «Shelter Tripo», доступ по ссылке — чтение) в tripo/.
Файлы в git не попадают (.gitignore).

  python3 tools/drive_fetch.py                    — по списку tripo/drive.json (имя → id файла)
  python3 tools/drive_fetch.py --style-test       — проба стиля: папки A / B / C → tripo/style_test/a|b|c/<имя>.glb
  python3 tools/drive_fetch.py --folder <id> <куда> — вся папка Диска (с подпапками), имена как на Диске

Уже скачанное пропускает (--force — заново)."""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_URL = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"
LIST_URL = "https://drive.google.com/embeddedfolderview?id={}"
# «Shelter Tripo / 00 Проба стиля (одна комната)»: A — Low poly, B — Реализм, C — Рисованный
STYLE_FOLDERS = {"a": "1qA4e2Q_mlY-A9r1H0ISvimZEOuM2v_Ax", "b": "1S905P4R8n3u9w3lDNCNRTV4g_11NUMon",
                 "c": "1rU43buKkYxGWKvVDwYSDVmINl6WT59lJ"}
FORCE = "--force" in sys.argv


def listing(folder_id):
    """[(вид, id, имя)] — вид: file / folder."""
    html = urllib.request.urlopen(LIST_URL.format(folder_id)).read().decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'href="https://drive\.google\.com/(file/d|drive/folders)/([\w-]+)[^"]*".*?flip-entry-title">([^<]*)<', html, re.S):
        out.append(("file" if m.group(1) == "file/d" else "folder", m.group(2), m.group(3).strip()))
    return out


def fetch(fid, out):
    if os.path.exists(out) and not FORCE:
        print("есть:", os.path.relpath(out, ROOT))
        return
    data = urllib.request.urlopen(FILE_URL.format(fid)).read()
    if out.endswith(".glb") and data[:4] != b"glTF":
        print("НЕ GLB (нет доступа по ссылке?):", os.path.relpath(out, ROOT))
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "wb").write(data)
    print("скачано: %s (%.1f МБ)" % (os.path.relpath(out, ROOT), len(data) / 1e6))


def fetch_folder(folder_id, dest):
    for kind, fid, name in listing(folder_id):
        if kind == "folder":
            fetch_folder(fid, os.path.join(dest, name))
        elif name.lower().endswith((".glb", ".png", ".jpg", ".jpeg")):
            fetch(fid, os.path.join(dest, name.lower() if name.lower().endswith(".glb") else name))


def main():
    a = sys.argv[1:]
    if "--style-test" in a:
        for st, fid in STYLE_FOLDERS.items():
            fetch_folder(fid, os.path.join(ROOT, "tripo", "style_test", st))
    elif "--folder" in a:
        i = a.index("--folder")
        fetch_folder(a[i + 1], os.path.join(ROOT, a[i + 2]))
    else:
        items = json.load(open(os.path.join(ROOT, "tripo", "drive.json"), encoding="utf-8"))
        for name, fid in items.items():
            if not name.startswith("_"):
                fetch(fid, os.path.join(ROOT, "tripo", name + ".glb"))


main()
