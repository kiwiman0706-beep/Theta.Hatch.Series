# 名前・ID・リポジトリ・署名鍵を揃える（移行）

目標：全アプリを `Theta <名前> Hatch`／`jp.yaegaki.theta.<名前>`／リポジトリ `Theta.<名前>.Hatch`／シリーズ共通の署名鍵／アプリ内自動更新（spec §6.1）に揃える。
各アプリの今と目標は [`catalog/apps.json`](../catalog/apps.json)。

## 1. 変えるものと影響

| 変えるもの | 影響 |
| --- | --- |
| 表示名 | アプリ名の表示が変わるだけ |
| 署名鍵 | 上書きできない → アンインストールが必要。**端末の中だけのデータは消える** |
| applicationId | Android では別のアプリ。新規インストールになり、データ・ウィジェット・権限・通知はやり直し。Google の Android 用 OAuth クライアントも新しく登録（SHA-1 は共通） |
| リポジトリ名 | GitHub が古い名前から転送する（git・Web・API）。**古い名前で新しいリポジトリを作らない**（転送が切れ、古いアプリの更新確認が迷子になる） |
| Web 版の URL（Pages） | 転送されない。ブラウザ内のデータは空、PWA は入れ直し（Vault から戻る） |
| Vault のフォルダ名 | **変えない**（Drive 上のデータの移動が要るため） |

鍵を変えるアプリは、どうせ入れ直しになるので **ID と鍵を同じ版で変える**。

## 2. アプリごとの作業

| アプリ | リポジトリ名 | ID | 鍵 | 自動更新 | データ |
| --- | --- | --- | --- | --- | --- |
| Meishi | `MeishiApp` → `Theta.Meishi.Hatch` | そのまま | 済み | あり | Vault |
| Book | `dsbooks` → `Theta.Book.Hatch` | 変える | 変える | 要確認 | 要確認 |
| Memo | — | — | 済み | あり | Vault |
| Mensetsu | — | — | Secret を入れる | **Android に追加** | Vault |
| Home | — | — | 変える | あり（Hatch ドロワーを catalog に） | 設定の書き出しあり |
| KidsHome | — | 変える | 変える（公開鍵を廃止） | あり | 要確認 |
| Oekaki | — | 変える | 変える | **追加** | Vault |
| Travel・Item・Kamigata・DoorPhoto・Label・Device | — | 変える | 変える | **追加** | **端末内の可能性。書き出し・読み込みを用意** |

## 3. 手順（ID・鍵を変えるアプリ）

自動更新を使って、できるだけ手作業を減らす。

1. **橋渡し版**を出す（古い ID・古い鍵のまま、版だけ上げる）
   - 自動更新があるアプリは、これが自動で入る。無いアプリはこの版だけ手で入れる（古い鍵なので上書きできる）
   - 中身：データの書き出し（1 つの zip。Vault を使うアプリは同期の完了を確かめるだけ）と「新しいアプリへ移る」画面
2. 共通 Secret を配り（`tools/sync-secrets`）、**新しい版**を出す（新しい ID・共通鍵・自動更新（§6.1）・読み込み）
   - リポジトリ名を変えるならこのとき。Release は同じリポジトリに続けて出す
3. 橋渡し版の自動更新が新しい版を見つける → パッケージ名が違うので「移行」として扱う（§6.1）
   - 書き出し → 新しいアプリを取得・インストール（利用者が確認）→ 新しいアプリで読み込み → 古いアプリの削除画面（`ACTION_DELETE`）
4. Google Cloud に新しい ID の Android 用 OAuth クライアントを追加（Google 連携があるアプリ）
5. このリポジトリの `catalog/apps.json`（current を target に）・README の一覧・`tools/repos.txt` を直す。Home の Hatch ドロワーにも反映

ID・鍵を変えないアプリ（Meishi・Memo・Mensetsu・Home）は、共通鍵での署名と自動更新（§6.1）を満たすだけ。Home は鍵を変えるので、上の手順で「設定を書き出す／読み込む」を使う。

## 4. 進める順番（案）

1. このリポジトリを公開にする（鍵は入っていない。Home などが `catalog/apps.json` を読めるように）
2. Home：catalog を読む Hatch ドロワー＋共通鍵（ほかのアプリの入れ直しの入口になるので最初に）
3. Vault を使うアプリ（Oekaki・Mensetsu）：データが消えないので楽
4. 端末内データのアプリ（Item・Kamigata・DoorPhoto・Travel・Label・Device・KidsHome）：橋渡し版から
5. リポジトリ名の変更（MeishiApp・dsbooks）。Meishi の Web 版は URL が変わる
