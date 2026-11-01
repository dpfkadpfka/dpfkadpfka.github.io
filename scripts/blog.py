import json, re, urllib.request, html, xml.etree.ElementTree as ET
URL = "https://rss.blog.naver.com/dpfkadpfka2.xml"
CAT = "최근활동"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items, cats = [], set()
for it in root.iter("item"):
    cat = (it.findtext("category") or "").strip()
    cats.add(cat)
    if CAT not in cat.replace(" ", ""):
        continue
    desc = it.findtext("description") or ""
    m = re.search(r'<img[^>]+src="([^"]+)"', desc)
    text = re.sub(r"<[^>]+>", " ", html.unescape(desc))
    text = re.sub(r"\s+", " ", text).strip()
    items.append({
        "t": (it.findtext("title") or "").strip(),
        "u": (it.findtext("link") or "").split("?")[0],
        "d": (it.findtext("pubDate") or "").strip(),
        "img": m.group(1) if m else "",
        "s": text[:110],
    })
json.dump({"items": items[:12], "cats": sorted(cats)}, open("blog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(items), sorted(cats))
