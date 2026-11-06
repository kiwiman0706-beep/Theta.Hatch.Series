# Theta Memo Hatch（memo）の移行メモ

- 更新：2026-11-06
- スレッド：https://claude.ai/code/session_01H9m1j4wPmRzXQbzu7zWADS
- 状態：計画OK待ち

## 今と目標

| | 今（0.2.0、ブランチ `claude/laughing-cray-pwzv3j`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Memo.Hatch`（既定ブランチは作業ブランチのまま。Release・タグはまだ無い） | 同じ（改名なし）。既定ブランチを `main` に |
| アプリ ID | `jp.yaegaki.theta.memo`（Java のパッケージも同じ） | `app.thetahatch.memo`（パッケージも `app.thetahatch.memo`） |
| 署名 | 配ったのはデバッグ鍵のお試し版だけ。`release.yml` は `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD` と、`build.sh` に別名 `meishiclaude` を直接書いている | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS`）。APK 名 `ThetaMemoHatch-<版>.apk` |
| 更新 | 自前の更新（`UpdateCheck`・`UpdateInstaller`、`REQUEST_INSTALL_PACKAGES`・`UPDATE_PACKAGES_WITHOUT_USER_ACTION`） | ハブに頼む（`app.thetahatch.action.UPDATE`、無ければ Releases を開く）。インストール権限と `UpdateInstaller` を外す。確認と帯は残す |
| 共通設定 | 自分で持つ（Gemini キー・モデル、書き起こし、テーマ）。`SeriesProvider` で Meishi と Gemini キーの貸し借り（権限 `jp.yaegaki.theta.permission.SHARE`）。`.theta/settings.json` は未対応、スキン無し | ハブ（`app.thetahatch.home.theta`／`kidshome.theta`）の `info`（`ui.skin`・`gemini.model`・`google.account`）と `secret/gemini.key`（承認つき）を読む。Vault の `.theta/settings.json` の読み書き。権限は `app.thetahatch.permission.SHARE` |
| データの置き場所 | Google ドライブの Theta Vault（`Memo/`）。端末内にも全件を持つ（ローカルファースト） | Google ドライブ（今のまま）＋ NAS（Synology、Tailscale）を選べるように。`Memo/メモ.base` を置く |
| 対応 OS | Android。Windows・Mac は Drive for desktop＋Obsidian で読み書き（アプリは無い） | Android ＋ Windows・Mac（Electron、DeskHatch のドロワーにも）。共通 UI（HTML/JS）はすでにブラウザで動く作り |
| スキン | Keep 風の独自の色（ライト／ダーク、メモの 12 色） | `design/skins/theta-skins.css`（system・dark・light・pop・alert・scifi）。画面の枠はスキン、メモの色は残す（下の「決めてほしいこと」） |

## 方針

### 移行の順番

1. **橋渡し版 0.2.1**（古い ID・お試し版と同じデバッグ鍵。上書きできる）：メニューに「Vault 形式で書き出す」（`Memo/Notes…`＋`_files` の ZIP）と「新しいアプリに移る」案内。お試し版は Drive 同期ができない（OAuth の SHA-1 が違う）ので、メモは端末の中だけにある。デバッグ鍵はこのスレッドの作業環境にしか無く、環境が消えると作れない → 先に出す
2. **新しい版 0.3.0**（`app.thetahatch.memo`・共通鍵・CI で署名・ハブに頼む更新・共通設定・スキン・「Vault の ZIP から読み込む」）。初めての Release
3. NAS の Vault（Synology File Station、Secure SignIn の確認コード＋デバイストークン。Home・Music と同じ方式）
4. Windows・Mac 版（Electron。Vault の読み書きを JS に移す）

### 改名・ID 変更で直すところ

- `build.gradle`：applicationId・namespace。Java のフォルダ `jp/yaegaki/theta/memo` → `app/thetahatch/memo`（テストも）
- Manifest：権限 `jp.yaegaki.theta.permission.SHARE` → `app.thetahatch.permission.SHARE`（release の manifest も）、action `jp.yaegaki.theta.memo.NEW` → `app.thetahatch.memo.NEW`、`<queries>` にハブ 2 つ、インストール権限を外す。FileProvider・`SeriesProvider` の authority は `${applicationId}` なので自動で変わる（`app.thetahatch.memo.files`・`.theta`）
- コードの文字列：`Widgets` の `jp.yaegaki.theta.memo.NEW.*`、`RecordingService` の `STOP_RECORDING`、`SeriesProvider` の貸し借り先、`UpdateCheck` の Release の URL と APK 名
- `build.sh`・`release.yml`：Secret 4 つ、別名を書かない、APK 名
- docs：`INTEGRATION.md`（Home 向けの authority・action）、`RELEASING.md`、README
- Home 側：Home の移行メモにある `jp.yaegaki.theta.memo` を新 ID に（移行中は両方を探す）
- Google Cloud：新 ID の Android クライアントは登録済み（APP_IDS.md）。Vault のフォルダ名 `Memo/` は変えない

### 端末の中にしか無いデータ

| もの | 移し方 |
| --- | --- |
| メモ・添付（お試し版で Drive 同期していない分） | 橋渡し版で ZIP に書き出し → 新しいアプリで読み込み。同期していれば Vault から戻る |
| 設定（書き起こし方式・テーマ・表示） | 入れ直し（数項目） |
| Gemini API キー | ハブ（Home）か Meishi から借りる、または入れ直し |
| ウィジェット | 置き直し |

## 決めてほしいこと

- [ ] お試し版にメモがどれくらいあるか。ほぼ無ければ橋渡し版を省いて 0.3.0 に進む
- [ ] データの置き場所：Drive のまま／NAS／両方。両方のときは「端末ごとにどちらか 1 つ」か「Drive を正本に NAS へ写す」か
- [ ] スキン：画面の枠（上の帯・メニュー・ボタン）はスキン、メモのカードは Keep の 12 色を残す（スキンごとに濃さを合わせる）、でよいか
- [ ] Windows・Mac 版を 0.3.0 の次にすぐ作るか、当面は Drive＋Obsidian で済ませるか
- [ ] 既定ブランチを `main` にしてよいか

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

- [ ] 橋渡し版で書き出し → 新しいアプリで読み込み（メモ・写真・手書き・録音）
- [ ] 新しいアプリで Drive の許可と同期（新 ID の OAuth クライアント）
- [ ] Home（ハブ）からの更新と、ハブが無いときに Releases が開くこと
- [ ] Home から Gemini キー・スキンを受け取る
