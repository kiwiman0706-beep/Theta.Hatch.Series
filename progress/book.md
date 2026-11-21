# Theta Book Hatch（book）の移行メモ

- 更新：2026-11-21
- スレッド：https://claude.ai/code/session_01VBri9A5SpavPKRqvCQZARs
- 状態：実機確認待ち（移行まわり・アプリの棚）。スキン・共通設定・Vault は作業中

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

## TVhome を更新のハブに（1.1.3）

- progress/tvhome.md の依頼どおり、`<queries>` と `UPDATE` の送り先に `app.thetahatch.tvhome` を足した。既定のホームがハブ（Home・KidsHome・TVhome）ならそこ、無ければ Home → KidsHome → TVhome。EXPORT を受ける相手（移行のハブ）には足していない

## FullOCR の新しい出力（1.1.2）

- `v1.1.2`（versionCode 79）。FullOCR のスレッドが用意したブランチ `claude/fullocr-callout-math` を取り込み、レビューで 2 つ直した
- 同じフォルダの `X.pdf`（原本）と `X.jisui`（FullOCR の出力。原文 PDF は sidecar で `X.pdf`）を 1 冊（PDF + JISUI）に。表の顔は PDF
- 「表のテキスト」「図中のテキスト」（`> [!info]- 題`）はたたんだ枠、`$$…$$` は数式の枠（組版なし）、`> ` の引用の不具合を修正
- レビューで修正：⑧ の接頭辞で走査する時に `.jisui` を拾っていなかった（0.9.7 から）。枠・数式の中のページの印を、文字にせずページ位置として残す
- 原文 PDF が端末に無い時は、本の画面から保存して開く（数百 MB のスキャン PDF でこれでよいかは実機で判断）

## アプリの棚（/shelf、THETA_SHARED_SETTINGS §4.2）

1.1.1 で対応（`v1.1.1`、共通鍵のビルドだけ）。

- プロバイダ：authority `app.thetahatch.book.theta`、`android:permission="app.thetahatch.permission.SHARE"`（Book も signature で宣言）
- `query content://app.thetahatch.book.theta/shelf`：1 行 1 冊、30 冊まで、出したい順、同じ本は 1 回だけ
  - section：`reading`（読みかけ）→ `favorites`（お気に入り）→ `recent`（最近）。sectionTitle は「読みかけ」「お気に入り」「最近」。各区画 12 冊まで
  - title：書名。subtitle：著者・巻・`12/200ページ`（ページが無ければ ％、読み終わりは「読了」）。text・color は空
  - image：`content://app.thetahatch.book.theta/cover/<file>.jpg`（表紙のキャッシュ、縦長、openFile で出す）。まだ表紙を取っていない NAS の本は空
  - action：`Intent.ACTION_MAIN`＋`MainActivity`＋extra `dsbooks.widget.book_id` を `URI_INTENT_SCHEME` にした文字。その本を続きから開く
- 本棚を保存するたびに作り直し、中身が変わった時だけ `notifyChange(content://app.thetahatch.book.theta/shelf)`
- 本文・メモ・NAS の接続先・アカウントは入れない。設定 →「ウィジェット：Theta Home の本棚」で区画を選べる
- 橋渡し版（`jp.shinwakai.dsbooks.claude`、Claude 版の鍵）とビューアには入れない（別の鍵で同じ signature 権限を宣言すると、後から入れる方がインストールできなくなるため）。Home は新しい ID の方を見てほしい
- 表紙が後から取れても notifyChange はしない（次に本棚を保存した時に出る）

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

## NAS 整理のスレからの依頼（2026-11-22）

- **NAS の「フォルダ検索」が終わらない**：`/8Books` を ▶ 棚に整理した後、設定で 8Books・接頭辞 `▶` を選んで検索すると「指定フォルダ内を確認中… 1370フォルダ・24644項目・対象5047件」のまま長く続く。原因は `▶青空文庫` が **1 冊 1 フォルダ（著者/題名/本.epub＋.opf）で 9,771 フォルダ**あるため（ほかの ▶ 棚は全部で約 270 フォルダ）。フォルダを 1 つずつ一覧する今の方式だと 1 万回近く DSM を呼ぶ
  - 案 1：`SYNO.FileStation.Search`（`recursive=true`、`pattern` に拡張子）で棚ごとに 1 回の検索にする（プロトタイプ `dsbooks-prototype.html` の 249 行目は Search を使っている）
  - 案 2：進み具合に「残りの見込み」を出し、途中で止めても見つかった分は本棚に出す。次回は前回の続きから（変わったフォルダだけ）
  - NAS 側でも、青空文庫を `▶青空文庫/<著者>/<題名>.epub` に平らにしてフォルダを約 1,000 に減らす案を利用者に出している
  - **→ 1.1.3 で対応（2026-11-21）**：案 1 のとおり、接頭辞の棚も `SYNO.FileStation.Search` を 1 回（棚をまとめて `folder_path` に）で調べるようにした。フォルダごとの一覧は Search API の無い DSM だけ。案 2（途中から続ける）は Search で要らなくなったのでしていない。青空文庫を平らにするかは NAS の都合で決めてよい（Book はどちらでも読める。シリーズの「次巻」は同じフォルダの中だけなので、平らにすると著者のフォルダの中でつながる）

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に（`app.thetahatch.book`、1.1.0、versionCode 77。橋渡し版 1.0.1 は古い ID）
- [x] signing：共通鍵の Secret で署名（`release.yml`。v1.1.0 の CI で署名が共通鍵の SHA-256 と一致を確認）
- [x] update：更新をハブに頼む形に（設定 →「更新を確認」で `app.thetahatch.action.UPDATE`、無ければ Releases。インストール権限なし）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（README・docs・AGENTS.md・更新の URL）
- [x] release：新しい版を Releases に出した（`v1.1.0` の `ThetaBookHatch-1.1.0.apk`、SHA-256 `e46b1c11…672002`。橋渡し版は `v1.0.1` の `ThetaBookHatch-1.0.1.apk`、古い ID・Claude 版の鍵、SHA-256 `0fd1cb36…fae9fd`。どちらも prerelease でない）

ほかに残っていること：スキン 6 つ（スキンの時は木目もやめる）、読書の記録を Theta Vault へ、デスクトップ版を 1.1.0 にそろえて同じ Release に、Theta.Jisui.Viewer を別リポジトリへ（リポジトリができたら）。

## 実機で確かめること

- [ ] 橋渡し版（1.0.1）が今の DSBooks Claude に上書きできる
- [ ] Home から EXPORT → zip を受け取れる。ハブ以外から呼ぶと手で保存する画面になる
- [ ] 新しい版を入れ、Home から IMPORT → 本棚・読書位置・栞・メモ・NAS の接続先が戻る（パスワードはハブから or 再入力）
- [ ] NAS の本を開くと、保存済みだった本は取り直しになり、位置はそのまま
- [ ] ハブの「更新する」で Releases から更新される
- [ ] 1.1.3：接頭辞 ▶ で 8Books のスキャンがすぐ終わる。TV で「更新を確認」→ TVhome
- [ ] 1.1.2：NAS の X.pdf と X.jisui が 1 冊、「原文 p.N」と「本文へ」で行き来できる、表のテキスト・数式・引用の見た目（Android と PC）
- [ ] 1.1.1：Home の「本」と「＋」の Book タブに表紙が並び、押すとその本が続きから開く。設定で区画を外すと消える
