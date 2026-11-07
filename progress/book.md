# Theta Book Hatch（book）の移行メモ

- 更新：2026-11-07（2 回目）
- スレッド：https://claude.ai/code/session_01VBri9A5SpavPKRqvCQZARs
- 状態：作業中

## 今と目標

| | 今（DSBooks Claude 1.0.0、ブランチ `claude/vigilant-ramanujan-4v5vsv`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Book.Hatch`（旧 `dsbooks`、改名済み・private） | 同じ。hub が Releases を読めるよう public に（決めてほしいこと 2） |
| アプリ ID | `jp.shinwakai.dsbooks.claude`（**catalog の current は `…dsbooks.preview` だが、これは ChatGPT 版**。利用者が使っているのは `.claude` のはず → 決めてほしいこと 1）。Java の名前空間は `jp.shinwakai.dsbooks.preview`、build.sh が包装時に改名 | `app.thetahatch.book`（表示名 Theta Book Hatch） |
| 署名 | Claude 版の鍵（alias `dsbooks-claude`、SHA-256 `27c01a80…d16490`）。手元でビルド・署名 → `release-upload.yml` が Release に載せる | 共通鍵（Secret の 4 つ、別名 thetahatch）。`release.yml` が CI でビルド・署名 |
| 更新 | アプリ内の更新なし。Release は prerelease、APK 名 `DSBooks-<版>.apk` | ハブに頼む（`app.thetahatch.action.UPDATE`、ハブが無ければ Releases を開く）。インストール権限なし。タグ `v<版>`、prerelease にしない、APK は 1 つ `ThetaBookHatch-<版>.apk` |
| 共通設定 | 自分で持つ（NAS：接続先・アカウント・パスワード・SID は端末内で暗号化、Gemini キー（0.9.6〜）は localStorage） | ハブ（`app.thetahatch.home.theta`）から受け取る：スキン・Gemini キー／モデル・NAS（接続先・アカウント・パスワード・デバイストークン）。ハブが無ければ今どおり |
| データの置き場所 | 本は NAS（File Station API、原本は触らない）。読書位置・栞・メモは端末＋NAS の `_DSBooksSync/` に端末別 JSON。書誌は NAS 上の Obsidian 互換 Markdown | 読書の記録（位置・栞・メモ・読了）を **Theta Vault**（`Theta Book Hatch/` に 1 冊＝1 ファイル）へ。置き場所は NAS（今の接続を使う）と Drive。本そのものは NAS のまま |
| 対応 OS | Android・Android TV、Windows／Mac（Python＋pywebview、DeskHatch のドロワー対応）。姉妹アプリ Theta.Jisui.Viewer（Android・Windows・Mac）も同じリポジトリ | 同じ。版番号を全プラットフォームで揃え、1 つの Release に |
| スキン | 独自（木目の本棚＋濃緑のバー） | `ui.skin` の 6 つ（`theta-skins.css`）。本棚の木目は「本棚の見た目」として残すか相談（決めてほしいこと 6） |

## 方針

### 移行（Home がまとめて行う。docs/MIGRATION.md §3、Book はデータの移行が必要）

1. **橋渡し版 1.0.1**（古い ID `jp.shinwakai.dsbooks.claude`・古い鍵のまま。手で上書き、または Home が入れる）
   - `app.thetahatch.action.EXPORT` を受ける画面と、設定に「新しいアプリへ移る」
2. **新しい版 1.1.0**（`app.thetahatch.book`・共通鍵・CI ビルド）
   - `app.thetahatch.action.IMPORT` を受ける画面と、初回起動の「前の DSBooks から読み込む」
3. 古い ChatGPT 版（`jp.shinwakai.dsbooks.preview`、別の鍵・別のブランチ `ccr-fbd7a73d-mp81q5`）は、このスレッドでは橋渡し版を作れない（鍵が無い）。入っていれば、読書データの書き出し（0.5.x からある JSON）→ 新しい版で読み込み、を手で

### EXPORT／IMPORT の取り決め（案。Meishi・Chirashi と揃えたいので、Series 側で決めてほしい）

- **EXPORT**（橋渡し版）：`Intent("app.thetahatch.action.EXPORT")` を `startActivityForResult` で起動
  - 画面で中身（本の数・栞やメモの数・含めるもの）を見せ、利用者が「書き出す」を押したときだけ作る
  - 結果は `RESULT_OK` と、zip の `content://`（FileProvider、`FLAG_GRANT_READ_URI_PERMISSION`、`ClipData` 付き）
  - extra に `packageName`（自分）、`format`（`theta-export-1`）、`versionName`、`sha256`
  - 呼び出し元は `getCallingPackage()` がハブ（`app.thetahatch.home`／`app.thetahatch.kidshome`、移行中は古い ID も）のときだけ受ける。それ以外から呼ばれても書き出さず、手で保存する画面（ファイルの保存先を選ぶ）にする
  - ハブはすぐに自分の領域へコピーする
- **IMPORT**（新しい版）：`Intent("app.thetahatch.action.IMPORT")`、data に zip の `content://`（読み取り許可付き）
  - 画面で中身を見せて「読み込む」→ 結果 `RESULT_OK`（失敗は `RESULT_CANCELED` と extra `error`）
  - すでにデータがある場合は、上書きせずに足す（bookId・位置は新しい方を残す）
  - 手で選んだ zip（ファイルを開く）からも同じ処理
- **zip の中身**（`manifest.json` に形式・元のアプリ・版・作成日時・ファイル一覧と SHA-256）
  - `storage.json`：`dsbooks.*` の全項目（本棚の一覧・bookId・読書位置・栞・メモ・読了・表示設定・NAS の共有フォルダとスキャン範囲・同期の設定・ダウンロードの対応表）
  - `nas.json`：接続先とアカウントだけ。**パスワード・SID・Gemini キーは入れない**（ハブから受け取るか、再入力）
  - `local/`：端末にだけある本（取り込んだ本・AI で作ったダイジェスト）。大きいので、含めるかは画面で選ぶ（既定：ダイジェストだけ含める）
  - NAS からダウンロードした本は入れない（新しい版で NAS から取り直す。bookId でつながる）

### 改名・ID 変更で直すところ

- `build.sh`：`APP_ID`（→ `app.thetahatch.book`）、鍵の変数（`DSBOOKS_KEYSTORE…` → `ANDROID_KEYSTORE_B64` など 4 つ、別名を直接書かない）、出力名
- Manifest：表示名、FileProvider の authority（`<appId>.files`、build.sh が照合）、`.jisui` の intent-filter、`<queries>` にハブ 2 つ
- Java：`MainActivity` の `getPackageName()` 判定（ビューアは `com.theta.jisui…`）、Secure SignIn・Tailscale の起動はそのまま
- JS：localStorage のキー（`dsbooks.*`）は**変えない**（読み込みでそのまま使う）。表示名の「DSBooks」→「Theta Book Hatch」
- ワークフロー：`release-upload.yml`（手元で署名）→ `release.yml`（CI で SDK を入れてビルド・共通鍵で署名・`v<版>`・prerelease なし）。デスクトップ版（Windows／Mac）も同じ Release に。`release-desktop*.yml`・`release-jisui-viewer.yml` を統合
- リポジトリ内の古い名前：README・docs・AGENTS.md・CHANGELOG のリンク（`dsbooks` → `Theta.Book.Hatch`）、`docs/FULLOCR_BUNDLING.md`（Release のタグ名）
- DeskHatch のプリセット（`expect: {app: 'dsbooks'}`、exe のパス）：デスクトップ版の改名と合わせて DeskHatch 側に依頼

### Windows・Mac

- 今ある（Python＋pywebview、ポート 47817、DeskHatch のドロワー対応）。spec の Electron ではないが、同じ HTML/CSS/JS を共有しているので、そのまま続けたい（決めてほしいこと 5）
- デスクトップは Home のハブが無いので、設定は今どおりアプリで入力

## 決めてほしいこと

利用者の答え（2026-11-07）：

- [x] 1. 端末に入っているのは Claude 版（`jp.shinwakai.dsbooks.claude`）→ 橋渡し版は Claude 版で作る。**catalog の `current.packageName` を `jp.shinwakai.dsbooks.claude` に直してほしい（Series のスレッドへ）**
- [x] 2. リポジトリを public にする → OK（利用者が設定）
- [x] 3. 本線は `claude/vigilant-ramanujan-4v5vsv` → OK（利用者がデフォルトに設定）
- [x] 4. Theta.Jisui.Viewer は別のリポジトリに分ける → OK（リポジトリは利用者が作る）
- [x] 5. デスクトップ版は pywebview のまま → OK、Electron はあとで考える
- [x] 6. スキンを使うときは木目もやめる（スキンに完全に揃える）
- [x] 7. 端末にだけある本は今は無いので、書き出しに含めない
- [x] 8. 新しい版は全プラットフォーム 1.1.0 から → OK
- [ ] 9. EXPORT／IMPORT の取り決め（上の案）を Series の spec に入れてもらえるか（Series のスレッドへ）

## Series のスレッドへの依頼

- `catalog/apps.json` の book：`current.packageName` を **`jp.shinwakai.dsbooks.claude`** に（利用者が使っているのは Claude 版）。`migration.bridgeVersion` を **`"1.0.1"`**（Home の提案のとおり、橋渡し版のタグは `v1.0.1`）
- EXPORT／IMPORT の約束：Book は Home の案（progress/home.md「ファイルの受け渡しの約束」）どおりに作った。`docs/MIGRATION.md` §3 に入れてもらえると Meishi・Chirashi とそろう。Book が足しているもの：EXPORT の結果に extra `packageName`・`format`（`theta-export-1`）・`versionName`・`sha256`、`ClipData` にも URI。呼び出し元がハブ（新旧の Home・KidsHome の ID）でなければ書き出さずに保存先を選ぶ画面にする。取り消しは `RESULT_CANCELED`
- Book のリポジトリの Release には、これまでのデスクトップ版・ビューア・Android（v0.9.x〜v1.0.0-claude、すべて prerelease）が並ぶ。ハブが見る `releases/latest` は v1.1.0（prerelease でない）になる

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に（`app.thetahatch.book`、1.1.0、versionCode 77。橋渡し版 1.0.1 は古い ID）
- [x] signing：共通鍵の Secret で署名（`release.yml`。v1.1.0 の CI 結果で確認）
- [x] update：更新をハブに頼む形に（設定 →「更新を確認」で `app.thetahatch.action.UPDATE`、無ければ Releases。インストール権限なし）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（README・docs・AGENTS.md・更新の URL）
- [ ] release：新しい版を Releases に出した

ほかに残っていること：スキン 6 つ（スキンの時は木目もやめる）、読書の記録を Theta Vault へ、デスクトップ版を 1.1.0 にそろえて同じ Release に、Theta.Jisui.Viewer を別リポジトリへ（リポジトリができたら）。

## 実機で確かめること

- [ ] 橋渡し版（1.0.1）が今の DSBooks Claude に上書きできる
- [ ] Home から EXPORT → zip を受け取れる。ハブ以外から呼ぶと手で保存する画面になる
- [ ] 新しい版を入れ、Home から IMPORT → 本棚・読書位置・栞・メモ・NAS の接続先が戻る（パスワードはハブから or 再入力）
- [ ] NAS の本を開くと、保存済みだった本は取り直しになり、位置はそのまま
- [ ] ハブの「更新する」で Releases から更新される
