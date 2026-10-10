#!/usr/bin/env python3
"""Скачать сырые модели Tripo с Google Диска автора в tripo/ по списку tripo/drive.json (имя → id файла).
Уже скачанные пропускает (--force — заново). Файлы в git не попадают (.gitignore)."""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = os.path.join(ROOT, "tripo", "drive.json")
URL = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"

def main():
    force = "--force" in sys.argv
    items = {k: v for k, v in json.load(open(LIST, encoding="utf-8")).items() if not k.startswith("_")}
    for name, fid in items.items():
        out = os.path.join(ROOT, "tripo", name + ".glb")
        if os.path.exists(out) and not force:
            print("есть:", name)
            continue
        data = urllib.request.urlopen(URL.format(fid)).read()
        if data[:4] != b"glTF":
            print("НЕ GLB (нет доступа по ссылке?):", name)
            continue
        open(out, "wb").write(data)
        print("скачано: %s (%.1f МБ)" % (name, len(data) / 1e6))

main()
