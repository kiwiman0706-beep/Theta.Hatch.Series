# <アプリ名>（<id>）の移行メモ

<!-- 各アプリのスレッドが書く。ファイル名は progress/<id>.md（<id> は catalog/apps.json の id）。自分のアプリのファイルだけを触る -->

- 更新：YYYY-MM-DD
- スレッド：https://claude.ai/code/session_…
- 状態：計画中 ／ 計画OK待ち ／ 作業中 ／ 実機確認待ち ／ 完了

## 今と目標

| | 今 | 目標 |
| --- | --- | --- |
| リポジトリ名 | | |
| アプリ ID | | |
| 署名 | | 共通鍵（Secret の 4 つ、別名 thetahatch） |
| 更新 | | ハブに頼む（インストール権限なし）／ハブ（Home・KidsHome） |
| 共通設定 | | ハブから受け取る |
| データの置き場所 | | Google ドライブ／NAS／両方（Theta Vault） |
| 対応 OS | | |
| スキン | | |

## 方針

（どう変えるか。橋渡し版が要るか、端末の中だけのデータとその移し方、Windows・Mac の見込み）

## 決めてほしいこと

- [ ] …

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [ ] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [ ] appid：アプリ ID を新しい ID に
- [ ] signing：共通鍵の Secret で署名
- [ ] update：更新をハブに頼む形に（ハブはハブ機能）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [ ] rename：改名後の名前に合わせて URL・リンクを直した
- [ ] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] …
