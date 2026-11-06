# Theta Home Hatch（home）の移行メモ

- 更新：2026-11-06
- スレッド：https://claude.ai/code/session_01GMSgoGarRChJJQLGtjAFKY
- 状態：計画OK待ち

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

1. **橋渡し版 0.43**（古い ID・古い鍵のまま。今の自動更新で上書き）
   - 「新しいアプリに移る」画面：書き出し（1 つの zip：設定の JSON＋記録（録音・手書き・写真）＋Clip＋Gemini で作ったアイコンの型）→ 新しいアプリの Releases を開く（入れたら、新しいアプリで読み込み → 古いアプリの削除画面）
   - 既定のホーム・通知へのアクセス・使用状況・ほかのアプリの上に表示・すべてのファイルへのアクセス・ウィジェットは、新しいアプリで入れ直し（案内に書く）
2. **新しいアプリ 1.0**（`app.thetahatch.home`・共通鍵・CI ビルド）
   - 初回起動の案内（0.35 からある）で「前のホームから読み込む」を先頭に
   - 秘密（Gemini キー・NAS のパスワード）は zip に入れない（再入力。ほかのシリーズのアプリから借りられる）
3. このあと Home がほかのアプリの移行の入口になる（`catalog/apps.json` の current が入っていて target が無い → 案内）

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

- [ ] 1. 版の名前：Releases を **prerelease にしない**（spec は `releases/latest` を読むので、今の alpha の Release はハブから見えない）。新しいアプリは **1.0.0** から、タグ `v1.0.0` でよいか
- [ ] 2. ビルド：CI（GitHub Actions）で共通鍵の Secret を使ってビルド・署名し、**APK をリポジトリにコミットするのをやめる**（今の `releases/` は 209MB。古いものは消すか、そのまま残すか）。Theta.Home.Hatch に Secret の 4 つが入っているか確認をお願いしたい
- [ ] 3. Kotlin のパッケージ名（namespace）も `app.thetahatch.home` に変えてよいか（全ファイルの機械的な置き換え。個人名がコードに残らない）
- [ ] 4. 橋渡し版で書き出すもの：設定の JSON＋記録＋Clip＋アイコンの型、でよいか（ウィジェットと各種の許可は入れ直し）
- [ ] 5. 0.36 で足したスキン 5 つ（term・braun・soft・window・lcd）を `design/skins/skins.json` に足してよいか（このスレッドは Series の自分以外のファイルを直さないので、足すなら Series のスレッドに頼む）
- [ ] 6. 更新の自動実行：WorkManager で 12 時間ごと（端末がスリープでも動く）でよいか。モバイル回線では取得しない（既定）
- [ ] 7. 両方のハブがある端末：既定は「Home が更新する、KidsHome は任せる」でよいか

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

- [ ] 橋渡し版の書き出し → 新しいアプリで読み込み → 古いアプリの削除、既定のホームの切り替え
- [ ] ハブから入れたアプリの「確認なしの更新」（Android 12 以上、installer of record がハブのとき）
- [ ] ブラウザなどで入れたアプリをハブが更新したとき：最初の 1 回は確認が出るか、2 回目から確認なしになるか（未確認）
- [ ] 共通鍵でない APK を拒否するか（見本で確かめる）
- [ ] KidsHome と同時に入れようとしたときに待つか
- [ ] 設定のハブ：ほかのアプリ（Memo・Meishi など）が info・secret を読めるか、読まれたときに通知が出るか
- [ ] NAS のデバイストークンをほかのアプリで使い回せるか（Synology 次第、未確認）
