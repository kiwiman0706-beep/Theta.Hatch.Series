# 見本の Theta Vault

Obsidian で開くと、Theta Hatch シリーズのデータがどう見えるかを確かめられる見本です。データはすべて架空です。

## 開き方
1. Obsidian を入れる（Windows：`winget install Obsidian.Obsidian`、Mac：`brew install --cask obsidian`）。1.9 以降が必要（一覧に Bases を使うため）
2. [`theta-vault/theta-vault-sample.zip`](theta-vault/theta-vault-sample.zip) を展開する
3. Obsidian の「フォルダを保管庫として開く」で、展開した `Theta Vault` フォルダを選ぶ
4. 最初に `ホーム.md` を開く

## 見どころ
| 開くもの | 見えるもの |
| --- | --- |
| `ホーム.md` | 名刺とおえかき図鑑の一覧が埋め込まれた表紙 |
| `Meishi/名刺.base` | 名刺の画像付きカード、表、会社ごと |
| `Meishi/People/` のノート | 右上の「プロパティ」に名前・会社など、本文に名刺画像・メモ |
| `Meishi/サンプル株式会社.md` | バックリンクにこの会社の人 |
| `Memo/メモ.base` | Keep 風のカード。ノートを開くとチェックリスト・表・手書き |
| `Mensetsu/応募者.base` | 選考状況ごとの表、顔写真のカード |
| `Oekaki/おえかき図鑑.base` | 絵のギャラリー、描いた人ごと |
| グラフビュー | 名刺と会社のつながり |

## 作り直し
`python tools/make_sample_vault.py`（Pillow が必要）。ノートの形を変えたら、ここも直す。

## まだ確かめていないこと
`.base` は Obsidian の公式の書式に合わせて書きましたが、実物の Obsidian ではまだ開いていません。カードに画像が出ない・絞り込みが効かないなどがあれば、Obsidian 上で表示を直し、その `.base` の中身をこのリポジトリに戻してください。
