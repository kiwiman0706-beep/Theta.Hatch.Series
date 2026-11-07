# 名前・ID・リポジトリ・署名鍵を揃える（移行）

目標：全アプリを `Theta <名前> Hatch`／`app.thetahatch.<名前>`／リポジトリ `Theta.<名前>.Hatch`／シリーズ共通の署名鍵／アプリ内自動更新（spec §6.1）に揃える。
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
| Meishi | `MeishiApp` → `Theta.Meishi.Hatch` | 変える | 済み | あり | Vault |
| Book | `dsbooks` → `Theta.Book.Hatch` | 変える | 変える | 要確認 | 要確認 |
| Memo | — | 変える | 済み | あり | Vault |
| Mensetsu | — | 変える | Secret を入れる | **Android に追加** | Vault |
| Home | — | 変える | 変える | あり（Hatch ドロワーを catalog に） | 設定の書き出しあり |
| KidsHome | — | 変える | 変える（公開鍵を廃止） | あり | 要確認 |
| Oekaki | — | 変える | 変える | **追加** | Vault |
| Travel・Item・Kamigata・DoorPhoto・Label・Device | — | 変える | 変える | **追加** | **端末内の可能性。書き出し・読み込みを用意** |

## 3. 手順（ID・鍵を変えるアプリ）

**移行の操作は Theta Home Hatch（ハブ）がまとめて行う**（KidsHome も同じことができるが、主に Home）。利用者は Home の画面で進めるだけにする。

### データを移すアプリは 3 つだけ（2026-11-07 決定）

| アプリ | データの移行 | 橋渡し版 |
| --- | --- | --- |
| Meishi | **必要**（名刺・メモ・設定。Vault にあるものは Vault から戻るが、端末だけの情報も移す） | 作る |
| Chirashi | **必要**（読み取ったチラシ・画像・設定） | 作る |
| Book | **必要**（本棚の設定・読書の記録・NAS の接続先） | 作る |
| ほか全部 | 不要（まだあまり使っていないので、入れ直して最初から） | 作らない |

### 橋渡し版を作る 3 つ（Meishi・Chirashi・Book）

1. **橋渡し版**を出す（古い ID・**古い鍵のまま**、版だけ上げる）。中身はデータの書き出し（1 つの zip、または Vault への同期の完了）と、「新しいアプリへ移る」案内。
2. **新しい版**を出す（新しい ID・共通鍵・最初の起動で書き出しを読み込む）。
3. Home がこの順に進める：
   1. 古いアプリを**橋渡し版に更新**（入っているアプリと同じ署名なので上書きできる）
   2. 橋渡し版を開いて**データを書き出す**（Home が橋渡し版の書き出し画面を開く：`Intent("app.thetahatch.action.EXPORT")`）
   3. **新しい版を入れる**（新しい ID なので別のアプリとして入る）
   4. 新しい版を開いて**読み込む**（`Intent("app.thetahatch.action.IMPORT")`、書き出したファイルを渡す）
   5. 読み込みができたら、**古いアプリを削除**（Home から削除の確認画面を出す。利用者が「OK」を押す）

### 書き出し・読み込みの受け渡し（EXPORT・IMPORT の約束）

Home・Meishi・Chirashi・Book で揃える（2026-11-07、Home と Book の案から）。

**書き出し（橋渡し版）**
- `Intent("app.thetahatch.action.EXPORT")` を `startActivityForResult` で受ける。画面で中身（件数・含めるもの）を見せ、利用者が「書き出す」を押したときだけ作る。
- 終わったら `setResult(RESULT_OK, Intent().setData(<zip の content:// URI>).addFlags(FLAG_GRANT_READ_URI_PERMISSION))`（FileProvider、`ClipData` にも同じ URI）。zip は 1 つ。取り消しは `RESULT_CANCELED`。
- extra：`packageName`（自分）、`format`（`theta-export-1`）、`versionName`、`sha256`（zip の）。
- 呼び出し元（`getCallingPackage()`）がハブ（`app.thetahatch.home`・`app.thetahatch.kidshome`、移行中は古い ID も）のときだけ返す。ほかから呼ばれたら返さず、保存先を選ぶ画面にする（手で保存）。

**zip の中身**
- `manifest.json`：`format`・元のアプリ（パッケージ名と版）・作った日時・ファイル一覧と各 SHA-256。
- アプリのデータ（JSON など）。**パスワード・トークン・API キーは入れない**（新しい版はハブから受け取るか、入れ直す）。
- 大きい物（取り込んだ本・画像など）を含めるかは、書き出し画面で選べるようにする。NAS や Drive にある物は入れず、新しい版で取り直す。

**ハブ（Home）**
- 受け取った zip はすぐ自分のフォルダにコピーし、読み込みが済むまで消さない。
- 結果が `RESULT_OK` で返らないとき（結果を返さない作りなど）は、「書き出したファイルを選ぶ」画面で続けられるようにする。

**読み込み（新しい版）**
- `Intent("app.thetahatch.action.IMPORT")`、`data` にハブの FileProvider の URI（読む権限付き）。画面で中身を見せて「読み込む」。
- 成功は `RESULT_OK`、失敗は `RESULT_CANCELED`＋extra `error`（理由の文）。
- すでにデータがあるときは上書きせずに足す（同じ id は新しい方を残す）。手で選んだ zip からも同じ処理。

### それ以外のアプリ

Home が「新しい版を入れる → 古いアプリを削除」だけを案内する。橋渡し版もデータの移行も作らない。

### 共通

- Google Cloud に新しい ID の Android 用 OAuth クライアントを登録（2026-11-06 済み）。
- 終わったら、このリポジトリの `catalog/apps.json`（current を target に）・README の一覧・`tools/repos.txt` を直す（各スレッドは `progress/<id>.md` に書き、反映はこのリポジトリのスレッドが行う）。

## 4. 進める順番（案）

1. このリポジトリを公開にする（鍵は入っていない。Home などが `catalog/apps.json` を読めるように）
2. Home：catalog を読む Hatch ドロワー＋共通鍵（ほかのアプリの入れ直しの入口になるので最初に）
3. Vault を使うアプリ（Oekaki・Mensetsu）：データが消えないので楽
4. 端末内データのアプリ（Item・Kamigata・DoorPhoto・Travel・Label・Device・KidsHome）：橋渡し版から
5. リポジトリ名の変更（MeishiApp・dsbooks）。Meishi の Web 版は URL が変わる
