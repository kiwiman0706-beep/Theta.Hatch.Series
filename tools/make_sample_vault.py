"""見本の Theta Vault（Obsidian で開くと見え方を確かめられる）を samples/theta-vault/ に作る。

    python tools/make_sample_vault.py

中身は架空のデータ。画像は Pillow で描く。各アプリのノートの形は spec/THETA_VAULT_SPEC.md と
各アプリの Vault 仕様（Meishi・Memo・Mensetsu・Oekaki）に合わせ、一覧用の .base（Obsidian Bases）を置く。
"""
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "samples" / "theta-vault"
VAULT = OUT / "Theta Vault"

FONT_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
]


def font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def write(rel, text):
    p = VAULT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip("\n"), encoding="utf-8", newline="\n")


def save(img, rel):
    p = VAULT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)


# ---- 画像 ----

def card(name, kana, company, title, accent):
    img = Image.new("RGB", (910, 550), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 910, 40], fill=accent)
    d.text((60, 90), company, font=font(34), fill="#333")
    d.text((60, 150), title, font=font(26), fill="#666")
    d.text((60, 220), name, font=font(72), fill="#111")
    d.text((64, 310), kana, font=font(26), fill="#888")
    d.text((60, 420), "TEL 03-0000-0000　example@example.com", font=font(24), fill="#444")
    d.text((60, 460), "東京都千代田区（見本）", font=font(24), fill="#444")
    return img


def portrait(color):
    img = Image.new("RGB", (300, 400), "#EEF1F4")
    d = ImageDraw.Draw(img)
    d.ellipse([90, 70, 210, 190], fill=color)
    d.rounded_rectangle([50, 210, 250, 420], radius=80, fill=color)
    return img


def resume_page():
    img = Image.new("RGB", (850, 1200), "white")
    d = ImageDraw.Draw(img)
    d.text((330, 60), "履 歴 書（見本）", font=font(40), fill="#111")
    for i in range(14):
        y = 180 + i * 70
        d.line([60, y, 790, y], fill="#999", width=2)
    return img


def ink(lines):
    img = Image.new("RGB", (900, 360), "white")
    d = ImageDraw.Draw(img)
    for i, t in enumerate(lines):
        d.text((40, 40 + i * 90), t, font=font(56), fill="#1a3d8f")
    return img


def doodle(kind):
    img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if kind == "hero":
        d.ellipse([100, 120, 300, 320], fill="#FFB347", outline="#333", width=8)
        d.ellipse([110, 40, 170, 150], fill="#FFB347", outline="#333", width=8)
        d.ellipse([230, 40, 290, 150], fill="#FFB347", outline="#333", width=8)
        d.ellipse([150, 190, 175, 215], fill="#333")
        d.ellipse([225, 190, 250, 215], fill="#333")
        d.arc([170, 220, 230, 270], 0, 180, fill="#333", width=6)
    else:
        d.pieslice([80, 60, 320, 300], 180, 360, fill="#B9A7F0", outline="#333", width=8)
        d.polygon([(80, 180), (80, 340), (130, 300), (200, 345), (270, 300), (320, 340), (320, 180)],
                  fill="#B9A7F0", outline="#333")
        d.ellipse([140, 150, 175, 195], fill="#333")
        d.ellipse([225, 150, 260, 195], fill="#333")
    return img


def photo():
    img = Image.new("RGB", (800, 500), "#cfe8ff")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 330, 800, 500], fill="#9ccc65")
    d.ellipse([600, 50, 700, 150], fill="#ffd54f")
    d.polygon([(150, 330), (300, 140), (450, 330)], fill="#8d6e63")
    return img


# ---- ノート ----

def meishi():
    people = [
        ("p1", "山田 太郎", "やまだ たろう", "サンプル株式会社", "営業部", "部長", "#E85D3A", "2024-03-05", "展示会", ["取引先", "展示会"]),
        ("p2", "佐藤 花子", "さとう はなこ", "サンプル株式会社", "企画部", "課長", "#E85D3A", "2025-06-12", "打ち合わせ", ["取引先"]),
        ("p3", "鈴木 一郎", "すずき いちろう", "テスト医療機器", "東京支店", "担当", "#2E7DD7", "2026-09-30", "院内説明会", ["業者", "医療機器"]),
    ]
    for pid, name, kana, company, dept, title, accent, met, place, tags in people:
        save(card(name, kana, company, f"{dept}　{title}", accent), f"Meishi/_files/{pid}0000a1-0.jpg")
        write(f"Meishi/People/{name}（{company}）.md", f"""
---
theta: meishi/person@1
rev: 000000000000
id: 0000000-{pid}
name: {name}
kana: {kana}
company: "[[{company}]]"
department: {dept}
title: {title}
email: [{pid}@example.com]
phone: [03-0000-0000]
tags: [{", ".join(tags)}]
met: {met}
met_place: {place}
status: confirmed
contact_registered: true
created: {met}T10:00:00+09:00
updated: 2026-10-26T09:00:00+09:00
pages:
- Meishi/_files/{pid}0000a1-0.jpg
---

![[Meishi/_files/{pid}0000a1-0.jpg|360]]

## メモ
- {met} 10:00 {place}でご挨拶。 ^m{pid}a
- 2026-10-20 15:30 見積もりを送付。来週フォロー ^m{pid}b

## 名刺の全文
```text
{company}
{dept} {title}
{name}
TEL 03-0000-0000
```

<!-- ここから下は自由に書けます（アプリは変更しません） -->
""")
    write("Meishi/サンプル株式会社.md", """
会社のノート（任意）。名刺の `company: "[[サンプル株式会社]]"` から、この会社の人がバックリンクに並ぶ。
""")


def memo():
    save(photo(), "Memo/_files/7a1c0000.jpg")
    save(ink(["牛乳 2本", "卵、パン"]), "Memo/_files/9c1e0000.ink.png")
    notes = [
        ("買い物", "yellow", True, ["家"], """
- [ ] 牛乳
- [x] パン
- [ ] 卵

![[Memo/_files/9c1e0000.ink.png]]
> 牛乳 2本 卵、パン
"""),
        ("旅行のアイデア", "teal", False, ["旅行"], """
## 行きたいところ
| 場所 | 季節 | メモ |
| --- | --- | --- |
| 箱根 | 秋 | 紅葉と温泉 |
| 伊豆 | 夏 | ==海水浴== |

![[Memo/_files/7a1c0000.jpg]]
"""),
        ("面接の質問リスト", "", False, ["仕事"], """
1. 志望動機
2. 夜勤の可否
3. 通勤時間
"""),
    ]
    for i, (title, color, pinned, tags, body) in enumerate(notes):
        fm = [f"theta: memo/note@1", "rev: 000000000000", f"id: 0000000-n{i}", f"title: {title}"]
        if color:
            fm.append(f"color: {color}")
        if pinned:
            fm.append("pinned: true")
        fm += ["tags:"] + [f"- {t}" for t in tags]
        fm += [f"created: 2026-10-2{i}T10:00:00.000+09:00", f"updated: 2026-10-2{i}T10:05:00.000+09:00"]
        write(f"Memo/Notes/{title}.md", "---\n" + "\n".join(fm) + "\n---\n" + body.lstrip("\n"))


def mensetsu():
    applicants = [
        ("a1", "高橋 美咲", "たかはし みさき", "看護師", "病棟看護師（夜勤可）", "scheduled", "4", "#7FB3D5", "2026-11-05 14:00"),
        ("a2", "伊藤 健", "いとう けん", "医療事務", "受付・会計", "interviewed", "3", "#A9CCE3", "2026-10-28 10:00"),
        ("a3", "渡辺 さくら", "わたなべ さくら", "看護師", "外来看護師", "offered", "5", "#F5B7B1", "2026-10-15 13:00"),
    ]
    for aid, name, kana, cat, pos, stage, rating, color, interview in applicants:
        save(portrait(color), f"Mensetsu/_files/{aid}0000p.jpg")
        save(resume_page(), f"Mensetsu/_files/{aid}0000r-0.jpg")
        write(f"Mensetsu/Applicants/{name}（{cat}）.md", f"""
---
rev: 000000000000
theta: mensetsu/applicant@1
id: 0000000-{aid}
name: {name}
kana: {kana}
category: {cat}
position: {pos}
employment: 常勤
stage: {stage}
rating: "{rating}"
applied: 2026-10-10
source: 求人サイト
interview: {interview}
interviewers: 看護部長
tags: [見本]
status: confirmed
created: 2026-10-10T09:00:00+09:00
updated: 2026-10-26T09:00:00+09:00
pages: [Mensetsu/_files/{aid}0000r-0.jpg]
portrait: Mensetsu/_files/{aid}0000p.jpg
---

![[Mensetsu/_files/{aid}0000p.jpg|120]] ![[Mensetsu/_files/{aid}0000r-0.jpg|360]]

## 面接メモ
- 2026-10-26 14:40 受け答えが丁寧。 ^i{aid}

## 採用手続き
- [ ] 健康診断書の提出 ^c{aid}1
- [ ] 免許証の写しの提出 ^c{aid}2
""")


def oekaki():
    drawings = [("d1", "ぴょんた", "りさ", ["hero"], "hero", True), ("d2", "おばけ", "けん", ["enemy"], "ghost", False)]
    for did, title, artist, roles, kind, fav in drawings:
        uid = f"{did}000000-0000-4000-8000-000000000000"
        save(doodle(kind), f"Oekaki/images/{uid}.png")
        tags = ["おえかき", "しゅじんこう" if "hero" in roles else "てき", artist]
        write(f"Oekaki/drawings/{title}-{did}.md", f"""
---
oekaki-id: {uid}
title: {title}
artist: {artist}
roles:
{chr(10).join("  - " + r for r in roles)}
image: images/{uid}.png
favorite: {str(fav).lower()}
created: 2026-10-18T10:15:00
updated: 2026-10-18T10:15:00
tags:
{chr(10).join("  - " + t for t in tags)}
---

![[{uid}.png]]

## メモ

おばあちゃんの家で描いた。
""")


# ---- 一覧（Obsidian Bases） ----

BASES = {
    "Meishi/名刺.base": """
filters:
  and:
    - file.inFolder("Meishi/People")
formulas:
  card: link(note.pages[0])
properties:
  note.kana:
    displayName: よみ
  note.company:
    displayName: 会社
  note.department:
    displayName: 部署
  note.title:
    displayName: 役職
  note.met:
    displayName: 会った日
  note.tags:
    displayName: タグ
views:
  - type: cards
    name: 名刺
    image: formula.card
    imageFit: contain
    imageAspectRatio: 0.6
    order:
      - file.name
      - note.title
      - note.met
    sort:
      - property: note.met
        direction: DESC
  - type: table
    name: 一覧
    order:
      - file.name
      - note.kana
      - note.company
      - note.department
      - note.title
      - note.tags
      - note.met
    sort:
      - property: note.kana
        direction: ASC
  - type: table
    name: 会社ごと
    groupBy:
      property: note.company
      direction: ASC
    order:
      - file.name
      - note.department
      - note.title
      - note.met
""",
    "Memo/メモ.base": """
filters:
  and:
    - file.inFolder("Memo")
    - 'note.theta == "memo/note@1"'
    - "!note.archived"
    - "!note.trashed"
properties:
  note.title:
    displayName: タイトル
  note.tags:
    displayName: ラベル
  note.updated:
    displayName: 更新
views:
  - type: cards
    name: メモ
    order:
      - file.name
      - note.tags
      - note.updated
    sort:
      - property: note.pinned
        direction: DESC
      - property: note.updated
        direction: DESC
  - type: table
    name: 一覧
    order:
      - file.name
      - note.tags
      - note.pinned
      - note.updated
""",
    "Mensetsu/応募者.base": """
filters:
  and:
    - file.inFolder("Mensetsu/Applicants")
formulas:
  photo: link(note.portrait)
properties:
  note.category:
    displayName: 職種
  note.position:
    displayName: 募集
  note.stage:
    displayName: 選考
  note.rating:
    displayName: 評価
  note.interview:
    displayName: 面接日時
views:
  - type: table
    name: 選考状況
    groupBy:
      property: note.stage
      direction: ASC
    order:
      - file.name
      - note.category
      - note.position
      - note.interview
      - note.rating
  - type: cards
    name: 顔写真
    image: formula.photo
    imageFit: cover
    order:
      - file.name
      - note.category
      - note.stage
""",
    "Oekaki/おえかき図鑑.base": """
filters:
  and:
    - file.inFolder("Oekaki/drawings")
formulas:
  picture: link("Oekaki/" + note.image)
properties:
  note.title:
    displayName: なまえ
  note.artist:
    displayName: かいた ひと
  note.roles:
    displayName: やくわり
views:
  - type: cards
    name: ずかん
    image: formula.picture
    imageFit: contain
    order:
      - note.title
      - note.artist
      - note.roles
  - type: cards
    name: かいた ひとごと
    image: formula.picture
    imageFit: contain
    groupBy:
      property: note.artist
      direction: ASC
    order:
      - note.title
      - note.roles
""",
}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    meishi()
    memo()
    mensetsu()
    oekaki()
    for rel, text in BASES.items():
        write(rel, text)
    write(".theta/vault.json", json.dumps({"spec": 1, "apps": ["meishi", "memo", "mensetsu", "oekaki"]}, ensure_ascii=False) + "\n")
    write(".theta/settings.json", json.dumps({
        "spec": 1, "updated": "2026-10-26T09:00:00Z",
        "series": {"ui.skin": {"value": "system", "by": "home", "at": "2026-10-26T09:00:00Z"}},
        "apps": {},
    }, ensure_ascii=False, indent=2) + "\n")
    write("ホーム.md", """
# Theta Vault（見本）

Theta Hatch シリーズのデータ。各アプリのフォルダと、一覧（Bases）へのリンク。

| アプリ | 一覧 |
| --- | --- |
| 名刺（Meishi） | [[Meishi/名刺.base\\|名刺]] |
| メモ（Memo） | [[Memo/メモ.base\\|メモ]] |
| 面接（Mensetsu） | [[Mensetsu/応募者.base\\|応募者]] |
| おえかき（Oekaki） | [[Oekaki/おえかき図鑑.base\\|おえかき図鑑]] |

## 名刺
![[Meishi/名刺.base]]

## おえかき図鑑
![[Oekaki/おえかき図鑑.base]]
""")
    # 見本だけの Obsidian 設定：添付フォルダを検索・グラフから外す（本番の Vault にはアプリは .obsidian を作らない）
    write(".obsidian/app.json", json.dumps({
        "userIgnoreFilters": ["Meishi/_files/", "Memo/_files/", "Mensetsu/_files/", "Oekaki/images/"],
    }, indent=2) + "\n")
    shutil.make_archive(str(OUT / "theta-vault-sample"), "zip", OUT, "Theta Vault")
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
