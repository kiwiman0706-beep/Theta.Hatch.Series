# Theta KidsHome Hatch（kidshome）の移行メモ

- 更新：2026-11-07
- スレッド：https://claude.ai/code/session_01NhS3xRwFVfssMDMXfSoJEv
- 状態：作業中

## 今と目標

| | 今（0.60.1） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.KidsHome.Hatch`（公開）＋素材用 `Theta.Kidshome.Hatch.Closed`（非公開） | 同じ（改名なし。非公開も改名しない） |
| アプリ ID | `com.theta.kidshome`（namespace も同じ） | `app.thetahatch.kidshome`（namespace も） |
| 署名 | アプリだけの鍵 `app/kidshome.jks` を**リポジトリに同梱**、パスワードを `build.gradle.kts` に直書き | 共通鍵（Secret の 4 つ、別名 thetahatch）。鍵ファイルと直書きのパスワードは外す |
| 更新 | 自分の更新（`update/SelfUpdate.kt`：Releases を確認・取得・インストール画面）。SHA-256・署名の照合なし | **更新ハブ**（spec §6.1）。操作はおうちの人の画面（親モード） |
| 共通設定 | 自分で持つ（Gemini キー、非公開リポジトリのトークン、TEPRA など）。NAS・Google ログインは未使用 | **設定のハブ**（共通設定 §4.0・§4.1）：`app.thetahatch.kidshome.theta`。貸す操作は親モード |
| データの置き場所 | 端末の中（設定・子ども・絵・字・ポイントなど）。設定の一括書き出し（JSON・QR）あり。SD の動画・音楽 | 端末の中が基本（ホームなので）。絵・字・成長記録などは Theta Vault（Drive／NAS）へ書き出し（後で） |
| 対応 OS | Android（タブレット。おや の スマホ は「おやモード」） | 同じ。Windows・Mac はなし（下の理由） |
| スキン | 子ども向けの独自テーマ（`KidTheme`）。親モードは Material | 子どもの画面は今のまま。親モード・ハブの画面をシリーズのスキンに（相談） |

## 方針

### 移行（ID と鍵を同じ版で変える）

1. **橋渡し版 0.61**（古い ID・古い鍵のまま。今の自動更新で上書き）— **0.61.0 を出した（2026-11-07）**：親モード「📦 新しい キッズホーム へ 引っ越し」（書き出し・読み込み、往復テスト済み）、自動更新は `ThetaKidsHomeHatch-` の APK を入れず案内、ちがうパッケージの APK はインストールしない
   - 親モードに「新しいアプリに移る」：**引っ越し用 zip** を書き出す（SAF で SD／ダウンロードへ）→ 新しいアプリの Releases を開く → 新しいアプリで読み込み → 古いアプリの削除画面
   - 自動更新が、パッケージ名・署名の違う APK（新しいアプリの 1.0.0）を入れようとしないようにする（代わりに「新しいアプリに移る」を出す）
2. **新しいアプリ 1.0.0**（`app.thetahatch.kidshome`・共通鍵・CI ビルド）
   - 初回の案内に「前のキッズホームから読み込む」
   - 既定のホーム・各種の許可（写真・音楽・カメラ・マイク・通知・インストール）・クイック設定のレスキュータイルは入れ直し（案内に書く）
3. **おや の スマホ**（同じアプリの「おやモード」）も同じ手順で入れ替え、タブレットと**つなぎ直す**（ペアリングの鍵は移さない）

### 端末の中だけのデータと移し方（引っ越し用 zip）

| 入れる | 入れない（入れ直し・取り直し） |
| --- | --- |
| ホームの設定（子ども・タイル・カテゴリー・時間割・ロック・曲 など、`kidshome` の設定） | 秘密：Gemini キー、非公開リポジトリのトークン、チャットのあいことば以外の鍵（設定のハブ／QR で入れ直し） |
| 各機能の設定（`SettingsBundle` と同じ範囲）＋**ポイントの残高・りれき・こうかん済み**、暗証番号（ハッシュ） | おや の スマホ とのペアリング（つなぎ直す） |
| 絵（`drawings/`・`stickers/`）、スタンプ（`stamps/`）、字の練習（`moji/`）、家系図と顔写真（`kin/`）、旅行の写真（`japan/`）、チャットのりれき（`chat/`）、レジのラベル（`shop_items.json`・`shopitems/`）、自分で足した ぬりえ・ゆるキャラの絵 | 非公開パック（`packs/`：ガイド役・きせかえ・スタンプ・ぬりえ・ゆるキャラ）→「📥 とってくる」で取り直し |
| | 辞書（`dict/`。大きい。SD から読み直し）、見たところの記録 |

- 書き出しは 1 つの zip（中身の一覧 `manifest.json` 付き）。読み込みは新しいアプリの初回の案内と親モードから。
- 大きさの目安は絵と写真しだい（数十〜数百 MB）。

### 改名・ID 変更で直すところ（リポジトリ名は変わらない）

- `app/build.gradle.kts`：applicationId・namespace、署名を Secret の 4 つ（環境変数）から読む。`app/kidshome.jks` を消す（履歴に残るので、この鍵はもう使わない）
- Kotlin のパッケージ（`com.theta.kidshome.*` → `app.thetahatch.kidshome.*`、main・tepra・notepra・test の全ファイル）
- Manifest：レスキュー画面の `taskAffinity`（`com.theta.kidshome.rescue`）、FileProvider は `${applicationId}.files` なので自動
- 自動更新：APK の名前（今は `KidsHome-<版>.apk` と固定名 `KidsHome.apk`）→ spec の `ThetaKidsHomeHatch-<版>.apk` 1 つに。別のタブレットに入れる QR は、最新 の APK の URL を API で しらべて その場 で 作る
- `release.yml`：共通鍵で署名、APK を 1 つに、出来た APK の署名の SHA-256 を共通鍵と照合
- README のリンク・QR、`docs/`
- 変えなくてよい：QR の中身の `kidshome:setup?`・`kidshome:pair?`（アプリ ID ではない）、非公開リポジトリから取るパック（トークンで読む）

### 更新のハブ（spec §6.1）

- 土台：`update/SelfUpdate.kt`（Releases の確認・取得・インストール画面）
- 新しく：`hub/Catalog.kt`（`catalog/apps.json`、APK にも同梱）、`hub/UpdateHub.kt`（入っているアプリの確認・Wi-Fi で先に取得・digest の SHA-256・`getPackageArchiveInfo` でパッケージ名・版・**共通鍵の署名**の照合）、`hub/HubInstaller.kt`（`PackageInstaller` のセッション、Android 12 以上は確認なし）、`hub/UpdateActivity.kt`（`app.thetahatch.action.UPDATE` を受けて、**親モードのゲートを通してから**更新画面）
- 画面：親モード「🔧 キー・アップデート」に「Hatch シリーズのアプリ」：入っている版・新しい版・更新・すべて更新・入れる・移る・変更点・失敗の理由と Releases を開く。設定に「自動で更新する（既定オン）」「モバイル回線でも取得する（既定オフ）」「この端末の更新は Home に任せる」
- Home も入っている端末：**既定のホームに設定されているほう**がハブ。もう一方は更新・設定の配布をせず、ハブに頼む。念のため `app.thetahatch.action.UPDATE_BUSY` で同時に入れない
- 子どもの画面には出さない（今のホームの「新しい版」のしるしも親モードの中だけにする）

### 設定のハブ（共通設定 §4.0・§4.1）

- `hub/SettingsProvider.kt`：authority `app.thetahatch.kidshome.theta`、権限 `app.thetahatch.permission.SHARE`（signature）。`/info`（`ui.skin`・`gemini.model`・`nas.url`・`nas.user`・`nas.shareRoot`・`google.account`）、`/secret/<キー>`（`gemini.key`・`nas.password`・`nas.deviceToken`）、`update /info`
- 親モードに「Hatch シリーズの共通設定」：スキン・Gemini・NAS（接続先・アカウント・パスワード・デバイストークン、Secure SignIn）・Google アカウント。秘密は Android Keystore で暗号化、書き出し（設定の一括・引っ越し zip）には入れない
- 秘密を読まれたら通知。KidsHome は「秘密を貸す」を親モードの許可にする（許可したアプリだけ）
- Home も入っている端末：既定のホームのほうを正本として読み、もう一方はその値に合わせる
- キッズホーム自身の Gemini キー（ぬりえ・レジのラベルなど）も、ここに入れた値を使う

### Windows・Mac

- 作らない。キッズホームは Android の**ホームアプリ**（既定のホーム、ほかのアプリの起動・ロック、SD の動画、カメラ）で、パソコンでは役目がない。
- おや の スマホ の「おやモード」（呼びかけ・ロック・曲を送る）は、あとで Web 版にできる余地がある（相談）。

### テスト

- 単体：引っ越し zip の書き出し → 読み込みの往復（設定・ポイント・絵の数が同じ、秘密が入っていない）、catalog の読み込み（ネット失敗 → 同梱）、版の比べ方、SHA-256・署名の照合（共通鍵の見本と別の鍵で拒否）、移行の判定
- Robolectric：ContentProvider（権限なしは拒否）、`UPDATE` の Intent で親モードのゲート → 更新画面

## 決めてほしいこと

- [x] 1. （OK）新しいアプリは **1.0.0**（タグ `v1.0.0`）からでよいか。橋渡し版は 0.61
- [x] 2. （決定）APK は `ThetaKidsHomeHatch-<版>.apk` の 1 つだけ（spec どおり）。別の 端末 に 入れる QR は、キッズホーム が その場 で Releases の API から 最新 の APK の URL を しらべて 作る（読む と すぐ ダウンロード）。README の 固定 の リンク・QR は Releases の 最新 の ページ へ。自動更新・ハブ の「入れる／更新」は API で APK を 直接 取る ので 1 ボタン（Releases の ページ は 通らない）
- [x] 3. （OK）Kotlin のパッケージ名（namespace）も `app.thetahatch.kidshome` に変えてよいか（全ファイルの機械的な置き換え）
- [x] 4. （OK）引っ越し zip の中身（上の表）でよいか。特に**ポイントの残高**は移す（設定の一括書き出しでは移さない決まりにしていた）
- [x] 5. （OK）スキン：子どもの画面は今の子ども向けテーマのまま、親モードとハブの画面だけシリーズのスキン（system など）にする、でよいか
- [x] 6. （決定）Home と両方ある端末では、**既定のホームに設定されているほう**がハブ（更新・設定の配布）を受け持つ。もう一方は任せる。既定のホームを変えたら入れ替わる
- [x] 7. （不要）非公開リポジトリ `Theta.Kidshome.Hatch.Closed` を `Theta.KidsHome.Hatch.Closed` に改名するか（GitHub の転送があるので、タブレットに保存したリポジトリ名は直さなくても動く見込み）
- [x] 8. （OK）データの置き場所：絵・字の練習・（今後の）成長記録・日記を Theta Vault（Drive か NAS）に書き出すのは、移行のあと（別の版）でよいか

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

- [ ] 橋渡し版で引っ越し zip を書き出す → 新しいアプリで読み込む → 古いアプリの削除、既定のホームの切り替え（タブレット 2 台）
- [ ] おや の スマホ の入れ替えとつなぎ直し
- [ ] 古いアプリの自動更新が 1.0.0 を入れようとせず「新しいアプリに移る」を出すか
- [ ] ハブから入れたアプリの「確認なしの更新」（Android 12 以上）、ブラウザで入れたアプリの最初の更新（未確認）
- [ ] 共通鍵でない APK を拒否するか
- [ ] Home と同時に入れようとしたときに待つか
- [ ] 設定のハブ：ほかのアプリが info・secret を読めるか、親モードで許可したときだけ秘密を貸すか、通知が出るか
