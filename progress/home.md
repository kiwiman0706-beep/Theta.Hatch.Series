# Theta Home Hatch（home）の移行メモ

- 更新：2026-11-07
- スレッド：https://claude.ai/code/session_01GMSgoGarRChJJQLGtjAFKY
- 状態：1.0.0 公開済み（実機の確認はこれから）

## 今と目標

| | 今（0.42.0-alpha） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Home.Hatch` | 同じ（改名なし） |
| アプリ ID | `jp.yaegaki.theta.home`（Kotlin の namespace も同じ） | `app.thetahatch.home`（namespace も `app.thetahatch.home`） |
| 署名 | Home だけの鍵（SHA-256 `c2b829ea…`）。手元でビルドし、署名済み APK を `releases/` にコミット → `release-apk.yml` が Release に載せるだけ | 共通鍵（Secret の 4 つ、別名 thetahatch）。`release.yml` が CI でビルド・署名。APK はコミットしない |
| 更新 | 自分の更新（`SelfUpdate.kt`）＋ Hatch ドロワーからほかのアプリを入れる（`HatchInstaller.kt`、アプリ内の固定の一覧） | **更新ハブ**（spec §6.1）：`catalog/apps.json` を読む、12 時間ごとの確認・Wi-Fi で取得・SHA-256／パッケージ名／共通鍵の照合・PackageInstaller・`app.thetahatch.action.UPDATE` を受ける・移行の案内 |
| 共通設定 | 自分で持つ（スキン・Gemini キー／モデル・NAS・Google アカウント。秘密は Android Keystore で暗号化、書き出しには入れない） | **設定のハブ**（共通設定 §4.0・§4.1）：`app.thetahatch.home.theta` の ContentProvider で配る。設定に「Hatch シリーズの共通設定」 |
| データの置き場所 | 端末の中（設定・タブ・カテゴリー・ピン留めなど）。設定の書き出し／読み込み（JSON）あり。Drive・NAS はファイラーで読む | 同じ（ホームなので Vault の正本は持たない）。共通設定は Vault の `.theta/settings.json` も読み書き（後で） |
| 対応 OS | Android（スマホ・Fold・タブレット） | 同じ。Windows・Mac は DeskHatch が受け持つ（ホームアプリなので移植しない） |
| スキン | dark・light・pop・alert・scifi・system に加えて、term・braun・soft・window・lcd（0.36） | 6 つは `design/skins/skins.json` と同じ値に揃える。増やした 5 つは skins.json に足すか相談 |

## 方針

### 移行（ID と鍵を同じ版で変える）

2026-11-07 の `docs/MIGRATION.md` §3 の決定で、Home は**データを移さないアプリ**（catalog の `migration.bridge: false`）。橋渡し版 0.43 は作らない。

1. **新しいアプリ 1.0.0**（`app.thetahatch.home`・共通鍵・CI ビルド・prerelease にしない）を出す
2. 古い Home（`jp.yaegaki.theta.home`）の「更新」から 1.0.0 を取ると、別のアプリとして入る（ID が違うので上書きではない）
3. 新しい Home を既定のホームにする → 設定は今ある「設定を書き出す」（古い Home）→「前の設定を読み込む」（新しい Home の初めの案内）で持ち越せる（任意）
4. 新しい Home のハブが、古い Home が入っていることに気づき「古いアプリを削除」を出す（`ACTION_DELETE`）
- 既定のホーム・通知へのアクセス・使用状況・ほかのアプリの上に表示・すべてのファイルへのアクセス・ウィジェット・Dimple の割り当ては、新しいアプリでやり直し（README と 1.0.0 の Release の本文に書く）

### 移行のハブ（ほかのアプリの移行を Home が進める）

- catalog の `current.packageName` が入っていて `target.packageName` が無いアプリを、一覧のいちばん上に「移行が必要」として出す
- `migration.bridge: true`（Meishi・Chirashi・Book）：
  1. 古いアプリを橋渡し版へ更新（current のリポジトリの最新 Release。同じ鍵なので上書き）
  2. 書き出し：`startActivityForResult(Intent("app.thetahatch.action.EXPORT").setPackage(<古い ID>))`
  3. 新しい版を入れる（target の Release）
  4. 読み込み：`Intent("app.thetahatch.action.IMPORT").setPackage(<新しい ID>)`、`data` に書き出したファイル（下の約束）
  5. 読み込みが済んだら、古いアプリの削除（`ACTION_DELETE`、`package:<古い ID>`。読み込みの前には出さない）
- `migration.bridge: false`：新しい版を入れる → 古いアプリの削除、だけ
- 進み具合（どの手順まで済んだか）はアプリごとに Home が覚え、途中でやめても続きから

**ファイルの受け渡しの約束（案。橋渡し版を作るアプリと揃えたい）**
- 書き出し（橋渡し版）：`EXPORT` を受けたら書き出し画面を出し、終わったら `setResult(RESULT_OK, Intent().setData(<zip の content:// URI>).addFlags(FLAG_GRANT_READ_URI_PERMISSION))` で返す。zip は 1 つ
- Home：受け取った zip を自分のフォルダにコピーして持つ（読み込みが済むまで消さない）
- 読み込み（新しい版）：`IMPORT` の `data` に Home の FileProvider の URI（読む権限付き）。読み込んだら `setResult(RESULT_OK)`、失敗なら `RESULT_CANCELED`＋extra `error`（理由の文）
- 結果が `RESULT_OK` で返ってこないとき（書き出し画面が結果を返さない作りなど）は、Home が「書き出したファイルを選ぶ」（ファイルを選ぶ画面）で続けられるようにする

### 改名・ID 変更で直すところ

- `build.gradle.kts`：applicationId・namespace、署名の変数名（`HOME_KEYSTORE…` → `ANDROID_KEYSTORE_B64` ほか 4 つ）
- Kotlin のパッケージ（`jp.yaegaki.theta.home.*` → `app.thetahatch.home.*`、全ファイル）
- Manifest・`res/xml/shortcuts.xml`：エッジの入口の action（`…SHOW_TABS`・`QUICK`・`VOICE_APP`）、activity-alias（`ShowTabs`・`QuickInput`）、`targetPackage`／`targetClass`、FileProvider の authority（`${applicationId}.files` なので自動）、taskAffinity
- コードの中の文字列：エッジの `ACTION_STOP`／`ACTION_OPEN`、alias の ComponentName（`HomeModel.aliasOn`）
- ほかのアプリの ID：MemoHatch（`jp.yaegaki.theta.memo` と SeriesProvider の authority・権限 `jp.yaegaki.theta.permission.SHARE`）、DSBooks、Theta Music、Hatch の一覧（固定 → catalog を読む）。移行の間は**古い ID と新しい ID の両方**を探す
- ワークフロー：`release-apk.yml`（Home の鍵の SHA-256 で確かめている）→ `release.yml`（CI ビルド、共通鍵の SHA-256 で確かめる）。prerelease をやめる（下の「決めてほしいこと」）
- README・`docs/index.html`・CHANGELOG のリンク、Dimple・モードとルーチンに割り当てた入口（利用者が選び直す）

### 更新のハブ（spec §6.1）

- 土台：`hatch/HatchInstaller.kt`（取得・SHA-256 照合・インストール画面）と `hatch/SelfUpdate.kt`、Hatch ドロワー・設定の「HATCH / Theta Hatch シリーズ」
- 新しく作るクラス
  - `hub/Catalog.kt`：`catalog/apps.json` を読む（ネット → 失敗したら APK に同梱した `assets/apps.json`）。`platforms` に android、current／target の repo・packageName
  - `hub/UpdateHub.kt`：入っているアプリ（current と target の両方を探す）の Releases を最大 12 時間に 1 回確認（起動時・WorkManager の定期実行）。Wi-Fi なら先に取得。`digest` の SHA-256 → `getPackageArchiveInfo` でパッケージ名・版・**署名（共通鍵の SHA-256 `F4:77:40:…`）**・入っているアプリと同じ署名かを確かめる
  - `hub/HubInstaller.kt`：`PackageInstaller` のセッションで入れる（Android 12 以上は `setRequireUserAction(USER_ACTION_NOT_REQUIRED)`）。まとめて更新は 1 つずつ順に、結果を一覧に
  - `hub/UpdateActivity.kt`：`app.thetahatch.action.UPDATE`（extra `packageName`）を受けて、そのアプリの更新画面を開く（エッジと同じ透ける画面か、ホームの Hatch ドロワーを開く）
  - 両方のハブ：更新中は `app.thetahatch.action.UPDATE_BUSY` を送る／受けたら待つ。設定に「この端末の更新は KidsHome に任せる」
- 画面：Hatch ドロワーと設定の一覧を catalog から作る。入っている版・新しい版・「更新」「すべて更新」「入れる」・変更点（Release の本文）・失敗の理由と「Releases を開く」。設定に「自動で更新する（既定オン）」「モバイル回線でも取得する（既定オフ）」
- 移行の案内：current が入っていて target が無い → 「新しいアプリに移る」（そのアプリの橋渡し版の書き出し画面を開く → 新しいアプリを入れる → 古いアプリの削除画面 `ACTION_DELETE`）
- Manifest：`REQUEST_INSTALL_PACKAGES`（今もある）・`UPDATE_PACKAGES_WITHOUT_USER_ACTION`・`<queries>`（catalog の全パッケージ。数が多いので `QUERY_ALL_PACKAGES` は使わず列挙）

### 設定のハブ（共通設定 §4.0・§4.1）

- `hub/SettingsProvider.kt`：authority `app.thetahatch.home.theta`、`<permission android:name="app.thetahatch.permission.SHARE" android:protectionLevel="signature">` を宣言して守る
  - `query /info`：`ui.skin`・`gemini.model`・`nas.url`・`nas.user`・`nas.shareRoot`・`google.account` と、それぞれの `at`（最後に変えた時刻）・書いたアプリ
  - `query /secret/<キー>`：`gemini.key`・`nas.password`・`nas.deviceToken`。読まれたら通知（「〇〇 Hatch が NAS のパスワードを使い始めました」）
  - `update /info`：ほかのアプリからの書き戻し（「シリーズに合わせる」項目だけ）。書いたアプリと時刻を記録
- 設定画面に「Hatch シリーズの共通設定」：スキン・Gemini（キー・モデル）・NAS（接続先・アカウント・パスワード・デバイストークン）・Google アカウントをまとめて入力。秘密は今と同じく Android Keystore で暗号化（`nas/Secret.java`）、書き出し・バックアップに入れない
- KidsHome も入っている端末：Home が正本。KidsHome の値の方が新しければ取り込む
- 移行の間は MemoHatch の古い SeriesProvider（`jp.yaegaki.theta.memo.theta`）からも Gemini キーを借りられるように残す

### テスト

- 単体：catalog の読み込み（ネット失敗 → 同梱）、版の比べ方、SHA-256・署名の照合（共通鍵で署名した見本 APK と、別の鍵の APK で拒否）、移行の判定（current だけ入っている）
- Robolectric：Hatch ドロワーの一覧（入っている・新しい版・入れる・移る）、ContentProvider の info／secret／update（権限なしは拒否）、`UPDATE` の Intent で更新画面が開く
- 実機は下の「実機で確かめること」

## 決めてほしいこと

利用者の答え（2026-11-06）：

- [x] 1. Releases は prerelease にしない。新しいアプリは 1.0.0（タグ `v1.0.0`）から → **OK**
- [x] 2. CI で共通鍵でビルドし、APK のコミットはやめる。今の `releases/` は**しばらく残す** → OK
- [x] 3. Kotlin のパッケージ名も `app.thetahatch.home` に → **OK**
- [x] 4. 橋渡し版の書き出し：設定の JSON＋記録＋Clip＋アイコンの型 → **OK**。ただし 2026-11-07 の MIGRATION §3 で Home はデータを移さないアプリになったので、橋渡し版は作らない（設定は今ある書き出し・読み込みで任意に持ち越す）
- [x] 5. スキン 5 つを `design/skins/skins.json` に足す → **お願いします**（下の「Series のスレッドへの依頼」）
- [x] 6. 自動の確認は WorkManager で 12 時間ごと、モバイル回線では取得しない → **OK**
- [x] 7. 両方のハブがある端末 → **OK。ただし「ホーム画面アプリに設定されている側に任せる」ができるならそちら**。→ できる：既定のホーム（`Intent.ACTION_MAIN`＋`CATEGORY_HOME` を受けるアプリ）が Home なら Home、KidsHome なら KidsHome が更新し、もう一方は任せる。どちらも既定のホームでないとき（One UI ホームなど）は Home。KidsHome のスレッドにも同じ決まりが要る（spec §6.1 の「ハブが両方入っている端末」に足すと分かりやすい）

## Series のスレッドへの依頼

### EXPORT・IMPORT のファイルの受け渡し

上の「ファイルの受け渡しの約束（案）」を、よければ `docs/MIGRATION.md` §3 か spec §6.1 に足してほしい（Meishi・Chirashi・Book の橋渡し版と新しい版が同じ形にするため）。

### 設定のハブの返し方（Home 1.0.0 の形。よければ THETA_SHARED_SETTINGS §4.0 に）

- `query /info` → 列 `key`・`value`・`by`・`at`（1 項目 1 行。`at` は ISO 8601、記録が無い項目は空）
- `query /secret/<キー>` → 列 `key`・`value`（`gemini.key`・`nas.password`・`nas.deviceToken`。無ければ 0 行、ほかのキーは null）
- `update /info`（ContentValues：キー → 値の文字列）→ 受け付けた数。`key`・`token`・`secret`・`password` を含む名前は受け付けない。知らない項目も預かって `info` で返す
- 書いたアプリは呼び出し元のパッケージ名から catalog の id で記録

### 橋渡し版の見分け方

Home は公開版を新しい順に取得して、古い ID・入っているものと同じ署名の APK を橋渡し版とみなしている（1 つずつ取得して確かめるので重い）。catalog の `migration` に `bridgeVersion`（例 `"0.9.1"`）を足してもらえれば、そのタグだけを見るようにする。

### スキン 5 つ（0.36 で Home に足したもの）を skins.json に

`skins` に次の 5 つを足し、`setting.values` にも足してほしい。今の 6 つに無い項目として `style`（作り：枠・時計・見出しの形を変える種類）・`radius`（角丸の大きさ dp）・`font`（`hud`＝Oswald＋Share Tech Mono／`sans`＝端末のゴシック／`mono`＝全部 Share Tech Mono）・`shadow`（`none`／`hard`＝右下 3dp の fg 色の影／`soft`＝ぼかした浮き出し）・`iconShape`（アイコンの台：`square`・`round`＝角丸 24%・`circle`）を持つ。`backdrop` に新しく `rain`（縦に流れる文字の列：18dp ごとの列に accent の点、最大 10%）・`lines`（白い方眼：36dp ごと、白の 22%）・`pixel`（液晶の横線：3dp ごと、fg の 3.5%）。WebView 版が作りまで真似できないときは、色だけ使えば十分。

```json
{
 "term": {
  "label": "TERMINAL（緑の端末）",
  "summary": "黒地に蛍光の緑、見出しは反転した帯、文字は全部等幅、背景に流れる文字の列",
  "color": {
   "bg": "#030805",
   "panel": "#06100A",
   "raised": "#0B1E12",
   "fg": "#8CFFB0",
   "muted": "#4FC97A",
   "faint": "#358A55",
   "line": "#1D5531",
   "accent": "#3DFF7F",
   "onAccent": "#031006",
   "widget": "#C9FFD9",
   "launch": "#2E9E58",
   "zebra": "#143DFF7F",
   "accent2": "#C9FFD9",
   "accent3": "#2E9E58"
  },
  "pop": false,
  "backdrop": "rain",
  "hazard": 0,
  "style": "term",
  "radius": 8,
  "font": "mono",
  "shadow": "none",
  "iconShape": "square"
 },
 "braun": {
  "label": "BRAUN（白い家電）",
  "summary": "生成りの地にオレンジ 1 色。めくり時計、丸い日付の文字盤、浮き出た角丸の台、丸いアイコン",
  "color": {
   "bg": "#E9E7E1",
   "panel": "#F6F5F1",
   "raised": "#DDDAD2",
   "fg": "#2A2A2A",
   "muted": "#575757",
   "faint": "#6E6B64",
   "line": "#BFBBB1",
   "accent": "#E8711A",
   "onAccent": "#FFFFFF",
   "widget": "#5E7A68",
   "launch": "#3A3A3A",
   "zebra": "#0A000000",
   "accent2": "#5E7A68",
   "accent3": "#C9C5BA"
  },
  "pop": true,
  "backdrop": "",
  "hazard": 4,
  "style": "braun",
  "radius": 14,
  "font": "sans",
  "shadow": "soft",
  "iconShape": "circle"
 },
 "soft": {
  "label": "SOFT（浮き出し）",
  "summary": "線を使わず影で台が浮き出る。大きな角丸、淡いオレンジ・青・緑・赤",
  "color": {
   "bg": "#ECEDF0",
   "panel": "#F3F4F7",
   "raised": "#E3E5EA",
   "fg": "#262A33",
   "muted": "#545B68",
   "faint": "#6B7280",
   "line": "#D9DCE2",
   "accent": "#F0A23A",
   "onAccent": "#262A33",
   "widget": "#5FA8DC",
   "launch": "#7FC08E",
   "zebra": "#08000000",
   "accent2": "#E8606F",
   "accent3": "#7FC08E"
  },
  "pop": true,
  "backdrop": "",
  "hazard": 4,
  "style": "soft",
  "radius": 18,
  "font": "sans",
  "shadow": "soft",
  "iconShape": "round"
 },
 "window": {
  "label": "WINDOW（昔のパソコン）",
  "summary": "水色の地に白い方眼、クリームの窓にオレンジのタイトルバーと「_ □ ×」、こげ茶の太い線と右下の影",
  "color": {
   "bg": "#52C3D6",
   "panel": "#FFF8EA",
   "raised": "#FBEBCF",
   "fg": "#3B2C27",
   "muted": "#5E4C44",
   "faint": "#7D6A60",
   "line": "#3B2C27",
   "accent": "#F5A33A",
   "onAccent": "#3B2C27",
   "widget": "#7C8DF2",
   "launch": "#F28DB2",
   "zebra": "#14F5A33A",
   "accent2": "#7C8DF2",
   "accent3": "#F28DB2"
  },
  "pop": true,
  "backdrop": "lines",
  "hazard": 4,
  "style": "window",
  "radius": 6,
  "font": "sans",
  "shadow": "hard",
  "iconShape": "round"
 },
 "lcd": {
  "label": "LCD（液晶ゲーム機）",
  "summary": "くすんだ黄緑の地に濃い緑の太い線と文字、全部等幅、液晶の数字の時計、画素の細い横線",
  "color": {
   "bg": "#8E9B69",
   "panel": "#99A673",
   "raised": "#A6B27F",
   "fg": "#1C2610",
   "muted": "#2F3D1C",
   "faint": "#45542C",
   "line": "#1C2610",
   "accent": "#1C2610",
   "onAccent": "#A6B27F",
   "widget": "#3C5568",
   "launch": "#6B4A33",
   "zebra": "#101C2610",
   "accent2": "#3C5568",
   "accent3": "#6B4A33"
  },
  "pop": false,
  "backdrop": "pixel",
  "hazard": 0,
  "style": "lcd",
  "radius": 8,
  "font": "mono",
  "shadow": "none",
  "iconShape": "square"
 }
}
```

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に
- [x] signing：共通鍵の Secret で署名
- [x] update：更新をハブに頼む形に（ハブはハブ機能）
- [x] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した
- [x] release：新しい版を Releases に出した

## 1.0.0 でしたこと（2026-11-07）

- ID `app.thetahatch.home`・Kotlin のパッケージも同じ。署名は CI（`release.yml`、Secret の共通鍵。署名者の SHA-256・パッケージ・版を確かめてから公開）
- 更新のハブ：`hub/Catalog.kt`（同梱の apps.json＋ネット）・`hub/Verify.kt`（照合）・`hub/UpdateHub.kt`（確認・取得・PackageInstaller・受け持ち・UPDATE_BUSY・通知）・`hub/UpdateWorker.kt`（12 時間）・`hub/UpdateActivity.kt`（`app.thetahatch.action.UPDATE`）
- 移行：`hub/Migration.kt`、Hatch の一覧の上に段階ごとのボタン。古い Home（`jp.yaegaki.theta.home`）は「古いアプリを削除」
- 設定のハブ：`hub/SettingsProvider.kt`（`app.thetahatch.home.theta`、権限 `app.thetahatch.permission.SHARE` signature）、設定 → SERIES
- Memo・Book・Music は新旧どちらの ID でも連携
- 試験：`HubTest`（catalog・照合・橋渡し・受け持ち・digest・移行の段階・設定のハブ）

## 実機で確かめること

- [ ] 橋渡し版の書き出し → 新しいアプリで読み込み → 古いアプリの削除、既定のホームの切り替え
- [ ] ハブから入れたアプリの「確認なしの更新」（Android 12 以上、installer of record がハブのとき）
- [ ] ブラウザなどで入れたアプリをハブが更新したとき：最初の 1 回は確認が出るか、2 回目から確認なしになるか（未確認）
- [ ] 共通鍵でない APK を拒否するか（見本で確かめる）
- [ ] KidsHome と同時に入れようとしたときに待つか
- [ ] 設定のハブ：ほかのアプリ（Memo・Meishi など）が info・secret を読めるか、読まれたときに通知が出るか
- [ ] NAS のデバイストークンをほかのアプリで使い回せるか（Synology 次第、未確認）
