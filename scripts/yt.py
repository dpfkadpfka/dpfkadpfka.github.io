# 예람쌤 유튜브 채널 최신 영상(쇼츠·롱폼)을 yt.json으로 가져오기
import json, re, os, urllib.request, http.client, xml.etree.ElementTree as ET
HANDLE = "%EC%98%88%EB%9E%8C%EC%8C%A4"  # @예람쌤
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.9"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
old = {}
try: old = json.load(open("yt.json", encoding="utf-8"))
except Exception: pass
cid = old.get("cid")
if not cid:
    page = get(f"https://www.youtube.com/@{HANDLE}")
    m = re.search(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', page) or re.search(r'channel/(UC[\w-]{22})', page)
    cid = m.group(1)
ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
known = {v["id"]: v for v in old.get("items", [])}
def is_short(vid):
    c = http.client.HTTPSConnection("www.youtube.com", timeout=20)
    c.request("HEAD", f"/shorts/{vid}", headers=UA); r = c.getresponse()
    return r.status == 200
items = []
for e in root.findall("a:entry", ns):
    vid = e.findtext("yt:videoId", namespaces=ns)
    t = (e.findtext("a:title", namespaces=ns) or "").strip()
    d = e.findtext("a:published", namespaces=ns) or ""
    if vid in known: k = known[vid]["k"]
    else:
        try: k = "short" if is_short(vid) else "long"
        except Exception: k = "long"
    items.append({"id": vid, "t": t, "k": k, "d": d})
json.dump({"cid": cid, "items": items}, open("yt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(cid, len(items), [ (i["k"], i["t"][:20]) for i in items[:5] ])
