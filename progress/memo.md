# Theta Memo Hatch（memo）の移行メモ

- 更新：2026-11-12
- スレッド：https://claude.ai/code/session_01H9m1j4wPmRzXQbzu7zWADS
- 状態：実機確認待ち（0.3.0 を Releases に公開：v0.3.0、APK は app.thetahatch.memo・共通鍵）

## 今と目標

| | 今（0.2.0、ブランチ `claude/laughing-cray-pwzv3j`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Memo.Hatch`（既定ブランチは作業ブランチのまま。Release・タグはまだ無い） | 同じ（改名なし）。既定ブランチを `main` に |
| アプリ ID | `jp.yaegaki.theta.memo`（Java のパッケージも同じ） | `app.thetahatch.memo`（パッケージも `app.thetahatch.memo`） |
| 署名 | 配ったのはデバッグ鍵のお試し版だけ。`release.yml` は `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD` と、`build.sh` に別名 `meishiclaude` を直接書いている | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS`）。APK 名 `ThetaMemoHatch-<版>.apk` |
| 更新 | 自前の更新（`UpdateCheck`・`UpdateInstaller`、`REQUEST_INSTALL_PACKAGES`・`UPDATE_PACKAGES_WITHOUT_USER_ACTION`） | ハブに頼む（`app.thetahatch.action.UPDATE`、無ければ Releases を開く）。インストール権限と `UpdateInstaller` を外す。確認と帯は残す |
| 共通設定 | 自分で持つ（Gemini キー・モデル、書き起こし、テーマ）。`SeriesProvider` で Meishi と Gemini キーの貸し借り（権限 `jp.yaegaki.theta.permission.SHARE`）。`.theta/settings.json` は未対応、スキン無し | ハブ（`app.thetahatch.home.theta`／`kidshome.theta`）の `info`（`ui.skin`・`gemini.model`・`google.account`）と `secret/gemini.key`（承認つき）を読む。Vault の `.theta/settings.json` の読み書き。権限は `app.thetahatch.permission.SHARE` |
| データの置き場所 | Google ドライブの Theta Vault（`Memo/`）。端末内にも全件を持つ（ローカルファースト） | **NAS（正本）＋ Google ドライブ**（決定）。NAS → ドライブ → 変化があれば NAS の順に同期。`Memo/メモ.base` を置く |
| 対応 OS | Android。Windows・Mac は Drive for desktop＋Obsidian で読み書き（アプリは無い） | Android。Windows・Mac 版（Electron）は次の版から（決定 2026-11-07） |
| スキン | Keep 風の独自の色（ライト／ダーク、メモの 12 色） | `design/skins/theta-skins.css`（system・dark・light・pop・alert・scifi）。画面の枠はスキン、メモの色は残す（下の「決めてほしいこと」） |

## 方針

### 移行の順番（決定 2026-11-07）

1. 橋渡し版は作らない（お試し版にデータが無いため）。お試し版はアンインストール
2. **0.3.0**（`app.thetahatch.memo`・共通鍵・ハブに頼む更新・共通設定・スキン・NAS 正本＋ドライブ）＝初めての Release。コードは main に済み
3. Windows・Mac 版（Electron）は次の版から

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

- [x] お試し版のデータ → 無いので橋渡し版は作らない（2026-11-07）
- [x] データの置き場所 → NAS と Google ドライブの両方、NAS が正本（2026-11-07）
- [x] スキン → 画面の枠はスキン、メモのカードは Keep の 12 色（スキンの明暗に合わせる）（2026-11-07）
- [x] Windows・Mac 版 → 次の版から（2026-11-07）
- [x] 既定ブランチを `main` に → `main` を作成済み。GitHub の Settings → Branches で既定を `main` に切り替えるのは利用者（Claude の道具では変えられない）
- [x] Theta.Hatch.Series の README の作品一覧（0.3.0・NAS 対応）・`catalog/apps.json`（current・synology・secureSignIn）・APP_IDS を Release に合わせた（2026-11-10）
- [ ] 既定ブランチを `main` に切り替える（GitHub の Settings → General → Default branch。利用者）。今は作業ブランチが既定のまま。Release は `main` への push で動く

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に
- [x] signing：共通鍵の Secret で署名
- [x] update：更新をハブに頼む形に（ハブはハブ機能）
- [x] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した
- [x] release：新しい版を Releases に出した

メモ：0.3.0 を 2026-11-10 に公開（`ThetaMemoHatch-0.3.0.apk`＋`SHA256SUMS-0.3.0.txt`、draft・prerelease でない、`tools/check_apk.py` で app.thetahatch.memo 0.3.0・シリーズ共通の鍵を確認）。`main` に版を上げて push すると Actions がタグと Release を自動で作る（spec §6.1 の条件 2）。

## 棚（`/shelf`、spec `THETA_SHARED_SETTINGS.md` §4.2）— 0.3.1 で対応（2026-11-12）

- `content://app.thetahatch.memo.theta/shelf`（権限 `app.thetahatch.permission.SHARE`）：ピン留めしたメモを 1 行 1 つ、最大 30 件、新しい順
  - `section`=`pinned`、`sectionTitle`=`ピン留め`、`id`、`title`（無ければ本文の 1 行目）、`subtitle`=空、`text`（本文の頭、チェックリストは ☐/☑、200 字まで）、`color`（`#RRGGBB`、色なしは空）
  - `action`：そのメモを開く Intent（`MainActivity`、extra `open`=id）の `toUri(URI_INTENT_SCHEME)`
  - `image`：写真・手書きのあるメモだけ `content://app.thetahatch.memo.theta/image/<name>`（同じプロバイダの `openFile` がサムネイルの JPEG を返す。棚に出ているメモの絵だけ）
- メモが変わると約 2 秒後に `notifyChange(content://app.thetahatch.memo.theta/shelf)`
- 設定「ピン留めしたメモを Theta Home Hatch の棚に並べる」（既定オン）で出さないようにできる
- 未確認：Home 1.9.0 以降で実際に並ぶか・押してメモが開くか

## 0.3.2（2026-11-12）

- スキャン（Meishi・Chirashi と同じ Google のスキャナ）。1 ページは画像、複数ページは 1 つの PDF（設定でページごとの画像にも）
- メモの「⋮」→「ホーム画面に置く」：そのメモのウィジェットを `requestPinAppWidget` で置く（置かれたウィジェットの id をコールバックで受けてメモを結ぶ）
- 写真は、Theta Camera Hatch が `ACTION_IMAGE_CAPTURE`（`EXTRA_OUTPUT` に書いて返す）を受けられるならそちらへ。**今の Camera Hatch（0.13 系）にはこの入口が無い**ので、端末のカメラのまま。Camera Hatch のスレッドで入口を足せば Memo 側は変更なしで使われる
- spec §6.2 の `SCAN` を受ける（Memo：新しいメモでスキャン、`mode=pick` は画像・ファイル選び、メモを閉じると `RESULT_OK` で戻る）。**§6.2 の表に Memo を足すのは Series のスレッドで**

## 0.3.3（2026-11-12）— Camera Hatch の `CAPTURE` を使う

- 「写真を撮る」「スキャン」：`Intent("app.thetahatch.action.CAPTURE").setPackage("app.thetahatch.camera")` を `resolveActivity` で確かめて開く（`source`=memo、`mode`=photo／scan、`modes`=photo・video・scan、`multiple`=true、`scanFormat`=設定の pdf／images）
- 結果の `ClipData`（無ければ `data`）の各 URI を `openInputStream` ですぐコピーしてメモへ。写真・動画はそのまま、PDF は「スキャン 日時.pdf」の名前で。HEIC はエディタでもサムネイル（JPEG）で表示
- Camera Hatch が無い・古いときは端末のカメラと Google のスキャナ（0.3.2 のまま）
- Manifest：`app.thetahatch.permission.SHARE` の uses-permission と `<queries>` の `app.thetahatch.camera` は 0.3.2 から入っている
- 0.3.2 の「`ACTION_IMAGE_CAPTURE` を Camera Hatch に送る」はやめた（`CAPTURE` に置き換え）

## 0.3.4（2026-11-13）— 撮ったものを落とさない

- 一覧の下のバー：📷（カメラが 1 回で起動）と 🖼（写真・ファイルを選ぶ）を分けた。メモの下のバーにも 📷
- Camera Hatch から `RESULT_OK` 以外で戻っても、`ClipData` があれば取り込む
- 待っている依頼（どのメモへ入れるか）を保存しておき、Memo が閉じられていても戻ったらそのメモ（無ければ新しいメモ）に入れる
- `SCAN`（Home から）は、Camera Hatch があればカメラ（写真・動画・スキャン）を開く
- **Camera Hatch への依頼**：`CAPTURE` でも写真と動画のシャッターを両方出す／「完了」を押さずに戻る・ホームへ出るときも撮った分を返す（黙って消さない）
- **Home Hatch への依頼**：「撮影」は Memo 経由（`SCAN`＋`setPackage("app.thetahatch.memo")`）にすると Memo に入る

## 実機で確かめること

- [ ] NAS（DS1825+、Tailscale）：接続・Secure SignIn のコード（次から不要）・自己署名証明書・同期（作成・編集・削除・添付）
- [ ] NAS と ドライブの両方：ドライブ側（PC の Obsidian）の編集が NAS に届く、どちらで消しても戻らない
- [ ] 新しいアプリで Drive の許可と同期（新 ID の OAuth クライアント）
- [ ] Home（ハブ）からの更新と、ハブが無いときに Releases が開くこと
- [ ] Home から Gemini キー・スキンを受け取る
- [ ] Camera Hatch 0.14.0 と：写真・動画・スキャンを何枚か撮って「完了」→ そのメモに全部入る、HEIC が表示される、Camera のギャラリーに残らない
- [ ] スキャン（1 ページ・複数ページ PDF）、「ホーム画面に置く」でそのメモのウィジェットが出る
- [ ] Home の「MemoHatch」タブ（棚）にピン留めのメモが並ぶ・写真付きは写真が出る・押すとそのメモが開く・ピン留めを外すと消える
