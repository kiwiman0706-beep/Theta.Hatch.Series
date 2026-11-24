# Theta Mensetsu Hatch（mensetsu）の移行メモ

- 更新：2026-11-25（1.0.4）
- スレッド：https://claude.ai/code/session_01UZcNkbW2pixSpi59267B3r
- 状態：実機確認待ち（1.0.0 を Releases に公開、2026-11-24。Android・Windows・Mac。1.0.1 で読み込んだ人の顔写真をまとめて切り出せるように）

## 今と目標

| | 今（0.2.0） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Mensetsu.Hatch`（既定ブランチが作業用の `claude/affectionate-sagan-re88lc` のまま） | 同じ（改名なし）。既定ブランチを `main` に |
| アプリ ID | Android `jp.yaegaki.theta.mensetsu`（Java のパッケージも同じ）、デスクトップ `jp.yaegaki.theta.mensetsu` | `app.thetahatch.mensetsu`（Java のパッケージ・デスクトップの appId も） |
| 署名 | Secret（`ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`）があればその鍵、**無ければリポジトリ内の開発用の鍵** `android/signing/mensetsu-dev.jks`（0.2.0 の APK はこれで署名）。`ANDROID_KEY_PASSWORD` は読んでいない | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS` から）。開発用の鍵とその代わりの処理を外す |
| 更新 | Android：自分では入れない（インストール権限なし）が、更新の確認・ハブへの依頼も無い。Windows：electron-updater。Mac：通知。Web：Service Worker | Android：設定に「今の版・更新を確認」→ ハブに `UPDATE`（無ければ Releases を開く）。ほかは今のまま |
| 共通設定 | 各アプリで入力（Gemini キーは端末内で暗号化）。Vault の `.theta/settings.json` は未対応 | Android はハブの `info`／`secret/gemini.key` から受け取り、書き戻し。全版で `.theta/settings.json` の series（`ui.skin`・`gemini.model`・`google.account`）を読み書き |
| データの置き場所 | Google ドライブの Theta Vault（`Mensetsu/Applicants/`。Android・Web は Drive API、PC は Drive API かフォルダの同期） | 同じ（Drive）。NAS は「決めてほしいこと」 |
| 対応 OS | Android・Windows・Mac（Electron）・Web（PWA） | 同じ |
| スキン | 独自の青の画面（CSS 変数） | `design/skins` のスキン（`theta-skins.css`、`data-theta-skin`）。`ui.skin` をハブ・Vault から |

## 方針

### 移行（catalog：`migration.bridge` false・`data` none）

- 橋渡し版は作らない。新しい ID・共通鍵の版を出し、Home が「新しい版を入れる → 古いアプリを削除」を案内する。
- 応募者のデータは Vault（Drive）から戻る。

### 端末の中だけのデータと移し方

| データ | 移し方 |
| --- | --- |
| 応募者・面接メモ・手書き・録音・書類・評価・手続き | Vault から戻る。**同期をオンにしていない端末では、削除の前に同期を始めておく**（アプリに「同期していない応募者が n 人います」の注意を出す） |
| アプリの設定（職種の一覧・採用手続きのひな形・勤務先の住所・連絡先のラベルの設定・自動読み取りなど） | 今は端末ごと。**Vault の `.theta/settings.json` の `apps.mensetsu` に移す**（PC 同士でも揃う。新しいアプリでもそこから戻る） |
| Gemini API キー | 移さない。ハブから受け取るか入れ直す |
| Google の許可・カメラ／マイクの許可 | 新しいアプリで取り直す |

### 改名・ID 変更で直すところ

- `android/app/build.gradle`：applicationId・namespace、署名を 4 つの Secret（`SIGNING_*` の代わりに `ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD` も）から。開発用の鍵への代わりを消す
- Java のパッケージ `jp.yaegaki.theta.mensetsu` → `app.thetahatch.mensetsu`（`MainActivity`・`SecretBox`、フォルダごと）
- `AndroidManifest.xml`：`<queries>` にハブ（`app.thetahatch.home`・`app.thetahatch.kidshome`）、ハブの設定を読む権限 `app.thetahatch.permission.SHARE`。FileProvider の authority は `${applicationId}.files` なので自動
- `android/signing/mensetsu-dev.jks` と `.gitignore` の例外を消す（公開リポジトリにあったので、この鍵は今後使わない。Google Cloud に古い SHA-1 のクライアントを作っていたら消す）
- `.github/workflows/release.yml`：4 つの Secret（無ければ失敗させる）、`tools/check_apk.py` 相当の確かめ（パッケージ名・版・共通鍵の SHA-256）、版を上げて `main` に push したら自動で Release
- `desktop/package.json`：`appId`（Windows では別アプリとして入る → 古い版の削除を案内）、`author` から個人名を外す
- `android/tests/page.e2e.cjs`・`android/README.md`・`docs/SETUP.md`・リリースノートのパッケージ名
- `docs/THETA_HATCH_SPEC.md`・`docs/THETA_VAULT_SPEC.md`（シリーズ仕様の古い写し）を消し、Theta.Hatch.Series へのリンクに
- `CLAUDE.md` を作り、`docs/FOR_APP_REPOS.md` §1 の文を入れる
- Obsidian Bases：`Mensetsu/応募者.base` を無いときだけ作る（Vault 仕様）
- URL（Releases・Pages）はリポジトリ名が変わらないのでそのまま

### データの一括の書き出し・読み込み（利用者の依頼、2026-11-24）

- メニューに「すべて書き出す」「書き出したファイルを読み込む」（Android・Windows・Mac・Web の全版）。
- 1 つの zip：`manifest.json`（`format`＝`theta-export-1`、元のアプリと版、作った日時、ファイル一覧と各 SHA-256）＋ Vault と同じ形（`Mensetsu/Applicants/*.md`、`Mensetsu/_files/` の履歴書の画像・PDF 原本・顔写真・書類・録音・手書き）＋ `apps.mensetsu` の設定。zip を開けばそのまま Obsidian で読める。
- 書き出し画面で、件数・大きさと「録音を含める」などを選べる。全員か、今の絞り込みの人だけ。API キー・トークンは入れない。
- 読み込みは足すだけ（同じ id は新しい方を残す。画像・PDF は同じ名前なら飛ばす）。読み込む前に件数を見せる。
- Android では `app.thetahatch.action.EXPORT`／`IMPORT`（`docs/MIGRATION.md` §3）でも同じ処理を呼べるようにする（ハブからの移行・機種変更に使える）。
- 同期を使っていない端末からの引っ越しにも使う（上の「端末の中だけのデータ」）。

### Windows・Mac

すでに Electron で動いている（Windows はインストーラーと自動更新、Mac は通知）。appId を変えると Windows では別アプリになるので、新しい版の初回に古い版の削除を案内する。

## 決めてほしいこと

決まったこと（2026-11-24）：新しい版は 1.0.0／NAS・スキン・SCAN は後の版／デスクトップの appId も変える／一括の書き出し・読み込みを 1.0.0 に入れる（形式は Mensetsu の `docs/IMPORT_FORMAT.md`）／APK を急ぐ。4（設定を Vault へ）は説明待ち。

- [x] 1. 新しいアプリの版：**1.0.0**（Meishi と同じ）でよいか
- [x] 2. （後の版）NAS（Synology、Tailscale）：今回やるか、後の版か。PC はすでに「フォルダの同期に任せる」で NAS のフォルダを Vault にできる。Android は WebDAV か File Station API＋Secure SignIn（確認コード・デバイストークン）が要る。ブラウザ版は NAS の CORS の設定が要るので Drive のまま
- [x] 3. （後の版）スキン：今回やるか、後の版か（全画面の色を役割に置き換える作業。Meishi は後の版にした）
- [ ] 4. アプリの設定を Vault の `apps.mensetsu` に移してよいか
- [x] 5. デスクトップの appId も `app.thetahatch.mensetsu` に変えてよいか（Windows は古い版を手で削除）
- [x] 6. （後の版）撮って登録（`SCAN`）にも対応するか（Home から「履歴書を撮る」）
- [x] 7. 一括の書き出し・読み込みを、移行の作業と同じ版（1.0.0）に入れてよいか
- [ ] 8. このリポジトリに 4 つの Secret が入っているか（2026-11-06 に配布済みと聞いている）

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照（1.0.0）
- [x] appid：アプリ ID を新しい ID に（1.0.0：`app.thetahatch.mensetsu`、Java のパッケージ・デスクトップの appId も）
- [x] signing：共通鍵の Secret で署名（1.0.0：4 つの Secret。無ければ失敗。APK のパッケージ名・版・共通鍵の SHA-256 を CI で確かめる。開発用の鍵は削除）
- [x] update：更新をハブに頼む形に（1.0.0：メニュー「更新を確認」→ `app.thetahatch.action.UPDATE`、無ければ Releases。インストール権限なし）
- [x] settings：共通設定をハブから受け取る（1.0.0：`info` の `gemini.model`・`google.account`、`secret/gemini.key` は利用者が選んだとき。書き戻しもする。スキンは後の版）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（リポジトリ名は変わらない。古い ID・個人名を検索して直した）
- [x] release：新しい版を Releases に出した（1.0.0、2026-11-24。APK は共通鍵で署名、CI でパッケージ名・版・SHA-256 を確認）

## 実機で確かめること

- [ ] Home（ハブ）から新しい版を入れられ、古い版（`jp.yaegaki.theta.mensetsu`）の削除が案内される
- [ ] 新しい版で Google の許可が通り（`app.thetahatch.mensetsu`＋共通の SHA-1）、Vault から応募者・画像が戻る
- [ ] 「更新を確認」でハブの更新画面が開く。ハブが無い端末では Releases が開く
- [ ] ハブの Gemini キー・Google アカウント（・スキン）を受け取れる
- [ ] 書類スキャナー・共有からの取り込み・録音・手書き（0.2.0 から未確認のもの）
- [ ] Windows：新しい appId の版の初回に、古い版の削除の案内が出る
