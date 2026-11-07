#!/usr/bin/env python3
"""Pull the kid-safe 'Kids Display - Feed' Google Sheet and write feed.json.

The wall display (an old Android frame) can't reach Google directly, but GitHub
can — so this runs on GitHub Actions nightly, reads the public feed sheet, and
commits feed.json, which the frame fetches from raw.githubusercontent.com.
Only the columns date/kid/icon/title/detail are published (no grades, etc.).
"""
import json
import re
import urllib.request

FEED_ID = "1Ztzu2lS6TlYIfTWusaesQTGceX0ccIxX8lSfgl7bIz0"
URL = ("https://docs.google.com/spreadsheets/d/" + FEED_ID +
       "/gviz/tq?tqx=out:json&sheet=Sheet1")


def norm_date(v):
    if v is None:
        return ""
    m = re.match(r"Date\((\d+),(\d+),(\d+)", str(v))
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)) + 1, int(m.group(3))
        return "%04d-%02d-%02d" % (y, mo, d)
    return str(v)[:10]


def main():
    raw = urllib.request.urlopen(URL, timeout=30).read().decode("utf-8")
    blob = re.search(r"\{.*\}", raw, re.S).group(0)
    table = json.loads(blob)["table"]
    out = []
    for row in table.get("rows", []):
        c = row.get("c") or []

        def cell(i):
            return (str(c[i]["v"]) if i < len(c) and c[i] and c[i].get("v") is not None else "")

        date = norm_date(c[0]["v"] if c and c[0] else None)
        kid, icon, title, detail = cell(1), cell(2), cell(3), cell(4)
        if not date or not title:
            continue
        out.append({"date": date, "kid": kid or "Both",
                    "e": icon or "\U0001F4CC", "t": title, "s": detail})
    with open("feed.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote %d events" % len(out))


if __name__ == "__main__":
    main()
