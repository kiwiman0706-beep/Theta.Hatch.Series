# Theta.Hatch.Series

Theta.xxx.Hatch シリーズの作品一覧と、シリーズ共通のガイドライン（仕様・デザイン・鍵）の正本です。

## 最新ガイドラインの要点（2026-10-26 時点）

新しいアプリを作るときは、まず「このガイドラインに合わせるか」を決めます。合わせる場合の要点は次のとおりです（詳しくはリンク先）。

| # | 分野 | 要点 | 詳しく |
| --- | --- | --- | --- |
| 1 | 名前 | 表示名は `Theta <名前> Hatch`。applicationId・appId は `app.thetahatch.<名前>`（個人名は入れない）。版番号は全プラットフォームで同じ、タグは `v<版>` | [spec §2](spec/THETA_HATCH_SPEC.md) |
| 2 | データ | 正本は **Theta Vault**（Google ドライブ、または NAS の共有フォルダ `Obsidian` の中。音楽・動画・写真はそれぞれの共有フォルダに置いたまま参照）（Obsidian で開ける Markdown＋添付）。1件＝1ファイル、`id` で同一性、削除は `.theta/trash/` へ、大量欠落では削除しない。Obsidian で一覧・ギャラリーが見られるよう、各アプリは自分のフォルダに `.base`（Obsidian Bases）を置く。見本は [`samples/theta-vault`](samples/README.md) | [Vault 仕様](spec/THETA_VAULT_SPEC.md) |
| 3 | 原則 | ローカルファースト（オフラインで動き、同期は後から）。独自サーバーを持たない。消さない・戻せる | [spec §1](spec/THETA_HATCH_SPEC.md) |
| 4 | プラットフォーム | UI は1つ（HTML/CSS/JS）を共有し、Android（APK＋ホーム画面ウィジェット）・Windows/Mac（Electron）・Web（PWA、iPhone）で動かす。端末機能はブリッジ `Native.call` / `window.onNative` で差し替え アプリ同士の呼び出し（更新・書き出し・撮って登録 `SCAN`）は spec §6.2 の Intent の一覧 | [spec §4・§6.2](spec/THETA_HATCH_SPEC.md) |
| 5 | デザイン | 見た目は Home.Hatch の**スキン**に揃える：`system`（既定）・`dark`・`light`・`pop`・`alert`・`scifi`・`term`・`braun`・`soft`・`window`・`lcd`（10 種）。色は直接書かず役割（accent・widget・launch…）から取る。書体は Oswald＋Share Tech Mono | [design](design/README.md) |
| 6 | 設定の共有 | シリーズ共通の設定は Vault の `.theta/settings.json`（スキン `ui.skin`、Gemini のモデル、Google アカウントなど）。項目ごとに「シリーズに合わせる／このアプリだけ」を選べる。初回起動で引き継ぎを聞く | [設定の引き継ぎ](spec/THETA_SHARED_SETTINGS.md) |
| 7 | 秘密 | API キー・NAS のパスワード・トークンはクラウドにも Git にも置かない。端末内で暗号化。**同じ端末では Home・KidsHome（設定のハブ）が預かって配る**（共通の署名鍵で守った ContentProvider、秘密は利用者の承認で）。共有するのは Gemini API キー、NAS の接続先・パスワード・デバイストークン、使う Google アカウント、スキン。Google のログイン自体はアプリごとに 1 回 | [設定の引き継ぎ §4](spec/THETA_SHARED_SETTINGS.md) |
| 8 | 署名鍵 | Android は**シリーズ共通の鍵**（Meishi の鍵、SHA-1 `A1:13:EA:…:28:BA`）。CI の Secret 名は `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD`。`tools/sync-secrets` で全リポジトリへ配る | [secrets](secrets/README.md) |
| 9 | AI・Google | Gemini は利用者自身の API キー。Google Cloud はシリーズで1プロジェクト、新しいアプリは Android 用 OAuth クライアント（パッケージ名＋共通の SHA-1）を足すだけ。設定手順はアプリ内のガイドで案内 | [Google 連携](spec/THETA_GOOGLE_SETUP.md) |
| 10 | リリース・**自動更新（必須）** | GitHub Actions の `release.yml` で全プラットフォームを1つの Release に。Web 版は `pages.yml`。**Android の更新は Home・KidsHome（更新ハブ）がまとめて行う**：Releases を12時間ごとに確認、Wi-Fi で取得、SHA-256・パッケージ名・共通鍵の署名を照合して PackageInstaller で更新。ほかのアプリはインストールの権限を持たず、ハブに頼む（ハブが無ければ Releases ページを開く）。リポジトリは公開。**Release の条件**（自動でタグと Release・prerelease にしない・APK は 1 つ・新しい ID・共通鍵）は spec §6.1、APK は `tools/check_apk.py` で確かめる | [spec §6・§6.1](spec/THETA_HATCH_SPEC.md) |
| 11 | 連携 | デスクトップ版は DeskHatch のドロワーとして表示できるように。テレビへは Theta Link（LAN 内で発見・ペアリング）。アプリ同士の呼び出し（ハブへの更新、撮って登録、Camera で撮って返す `CAPTURE` など）は §6.2 の一覧に従う | [spec §6.2・§7・§8](spec/THETA_HATCH_SPEC.md) |
| 12 | 品質 | Vault の往復テスト、2台の同期テスト、320〜768px 幅ではみ出さない、JS エラー0。実機で確かめていないことは `TESTING.md` に「未確認」と書く | [spec §9](spec/THETA_HATCH_SPEC.md) |
| 13 | 新しいアプリの手順 | 各アプリの `CLAUDE.md` にこのリポジトリを参照する一文を入れる。完成したら下の作品一覧に追加し、`tools/repos.txt` に足して Secret を配る | [FOR_APP_REPOS](docs/FOR_APP_REPOS.md) |
| 14 | 移行 | 名前・ID・リポジトリ名・署名鍵を揃える作業中。移行の操作は **Theta Home Hatch がまとめて行う**（橋渡し版への更新 → 書き出し → 新しい版を入れる → 読み込み → 古いアプリの削除）。データを移すのは Meishi・Chirashi・Book だけ、ほかは入れ直し | [MIGRATION](docs/MIGRATION.md) |
| 15 | PC から操作（構想） | ADB（USB・Wi-Fi）で PC から入れる・初期設定・設定・状態・操作。各アプリは `dumpsys` の状態と、`android.permission.DUMP` で守った操作の窓口を持つ。PC の CLI（hatchctl）と画面（Theta Console Hatch）、ローカルの Claude に「やっといて」 | [ADB 仕様](spec/THETA_ADB_SPEC.md) |
| 16 | TV（構想） | Android TV／Google TV を中心に、できる物は webOS にも。Book・Movie・Music・Photo を TV で、Home は広告のない軽いスマート TV のホームに。リモコンだけで操作、10 フィートの画面、同じ APK に TV の画面を足す | [TV 仕様](spec/THETA_TV_SPEC.md) |
| 17 | NAS のライブラリ | 映画・音楽・写真・本の並べ方と名前（Jellyfin・Synology Photos・Calibre などでもそのまま読める形）。整理は Claude に任せてよいが、スナップショット→変更案 CSV→確認→実行→記録、消さない | [ライブラリ規則](spec/THETA_LIBRARY_SPEC.md)・[依頼文](docs/PROMPT_NAS_ORGANIZE.md) |

## 作品一覧

2026-11-08 時点。開始日の古い順。

| # | 作品 | 概要 | 最新版 | GitHub | Claude スレッド | 開始日 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Theta.Book.Hatch**<br>（DSBooks） | 自炊本・PDF・コミック・EPUB・Markdown の本棚／リーダー。全画面読書、見開き・縦スクロール表示。Home の「本」に表紙（アプリの棚）。姉妹アプリ Theta.Jisui.Viewer も同じリポジトリ | 1.1.1（新しい ID、移行済み、アプリの棚） | [Theta.Book.Hatch](https://github.com/kiwiman0706-beep/Theta.Book.Hatch)（旧 dsbooks） | [Theta.Book.Hatch](https://claude.ai/code/session_01VBri9A5SpavPKRqvCQZARs) | 2026-10-15 |
| 2 | **Theta.Meishi.Hatch**<br>（旧 Meishi-Claude） | 名刺を撮影 → Gemini で読み取り → Google 連絡先に登録。名刺画像・メモ・録音を人ごとに保存、カレンダー・地図・Drive 同期。シリーズ共通仕様（Theta Vault）の元 | 1.0.0（新しい ID、移行済み） | [Theta.Meishi.Hatch](https://github.com/kiwiman0706-beep/Theta.Meishi.Hatch)（旧 MeishiApp） | [Theta.Meishi.Hatch](https://claude.ai/code/session_016tfKWDzu24Zp9FBxh4cjKS) | 2026-10-16 |
| 3 | **Theta.Item.Hatch**<br>（おもいでクローゼット） | 小さくなった子ども服などを手放す前に写真で残し、スマホのクローゼットのように眺めて楽しむ記録アプリ | 1.3.0 | [Theta.Item.Hatch](https://github.com/kiwiman0706-beep/Theta.Item.Hatch) | [Theta.Item.Hatch](https://claude.ai/code/session_01QGzXdJYduLXUGSNC9NMCDu) | 2026-10-17 |
| 4 | **Theta.Kamigata.Hatch**<br>（くるりヘア） | 子どもの髪型を前後左右・斜め・真上から撮影し、指のドラッグで角度を切り替えて見返す（QuickTime VR の Object Movie 風） | 1.1.0 | [Theta.Kamigata.Hatch](https://github.com/kiwiman0706-beep/Theta.Kamigata.Hatch) | [Theta.Kamigata.Hatch](https://claude.ai/code/session_01De2aFah9Lcgtf5wm3XZKDX) | 2026-10-17 |
| 5 | **Theta.DoorPhoto.Hatch**<br>（おもいで年表） | 玄関ドアに instax 写真で作る家族の「サムネイル年表」用。写真・出来事を登録し、月末にコラージュを作って instax・A4・テプラへ出力 | 1.7.0 | [Theta.DoorPhoto.Hatch](https://github.com/kiwiman0706-beep/Theta.DoorPhoto.Hatch) | [引き継ぎとAPKリリース](https://claude.ai/code/session_01EBZjKxFPPAcMuVaRQmJaEM) | 2026-10-17 |
| 6 | **Theta.Label.Hatch**<br>（声でテプラ） | テプラ PRO SR5900P へ音声でラベル印刷。「話す → 確認 → 1回押して印刷」 | 1.0.0 | [Theta.Label.Hatch](https://github.com/kiwiman0706-beep/Theta.Label.Hatch) | [引き継ぎとAPKリリース](https://claude.ai/code/session_01SsMo5spj81EiVV3fsBYJwr) | 2026-10-17 |
| 7 | **Theta.Device.Hatch**<br>（機器台帳） | PC・電子機器の銘板や設置風景を撮影して機器台帳を作成。OCR＋Gemini で転記補助、ログイン情報を暗号化保存、QR 付き管理ラベルをテプラで印刷 | 1.1.0 | [Theta.Device.Hatch](https://github.com/kiwiman0706-beep/Theta.Device.Hatch) | [APKリリースと機能構想](https://claude.ai/code/session_01MfF9qvjEzW47oy37eYGX2f) | 2026-10-17 |
| 8 | **Theta.Travel.Hatch**<br>（TravelHatch／旧 たびのたね） | 「行ってみたい」を貯め、天気・時間・泊数などの条件で行き先を選び、旅のしおりから思い出まで一続きで残す | 0.1.1 | [Theta.Travel.Hatch](https://github.com/kiwiman0706-beep/Theta.Travel.Hatch) | [APKリリースと要件整理](https://claude.ai/code/session_01AvSnwTjAMGxxrwossSH8b5) | 2026-10-17 |
| 9 | **Theta.Oekaki.Hatch**<br>（おえかきハッチ） | 子どもが描いた絵を取り込むと、主人公や敵になってゲーム（ぼうけん・レース）で動きだす。絵は Obsidian Vault 形式で蓄積、Drive 同期 | — | [Theta.Oekaki.Hatch](https://github.com/kiwiman0706-beep/Theta.Oekaki.Hatch) | [APKリリース](https://claude.ai/code/session_01LmiStbYTVdJCtU26X4VDQh) | 2026-10-17 |
| 10 | **Theta.Mensetsu.Hatch** | 医療機関の職員採用面接の管理。履歴書を Gemini で読み取り、選考状況・面接メモ（手書き・録音の文字起こし）・書類・通勤費概算を管理。Meishi.Hatch ベース | 0.2.0 | [Theta.Mensetsu.Hatch](https://github.com/kiwiman0706-beep/Theta.Mensetsu.Hatch) | [採用面接管理アプリ](https://claude.ai/code/session_01UZcNkbW2pixSpi59267B3r) | 2026-10-22 |
| 11 | **Theta.Home.Hatch** | 背景（デスクトップ）にファイラーを置き、画面端のタブでドロワーやウィジェットを切り替える Android ホームアプリ。狭い画面では予定・天気のダッシュボード | 1.1.1（新しい ID・ハブ） | [Theta.Home.Hatch](https://github.com/kiwiman0706-beep/Theta.Home.Hatch) | [Theta.Home.Hatch](https://claude.ai/code/session_01GMSgoGarRChJJQLGtjAFKY) | 2026-10-22 |
| 12 | **Theta.Memo.Hatch** | Google Keep 風の付箋メモ。データは Obsidian 形式（Theta Vault）で、Synology の NAS（正本）と Google ドライブに保存。リッチテキスト・表・手書き・音声・ファイル添付、GTD とアイゼンハワーマトリクス、入れ子・マインドマップ（その場で編集・線・かっこ・吹き出し・写真）、カード DB、表計算、スライド、Keep からの取り込み | 0.7.2 | [Theta.Memo.Hatch](https://github.com/kiwiman0706-beep/Theta.Memo.Hatch) | [アプリ開発](https://claude.ai/code/session_01H9m1j4wPmRzXQbzu7zWADS) | 2026-10-23 |
| 13 | **Theta.KidsHome.Hatch**<br>（キッズホーム） | 子ども用タブレット向けのかわいいホーム画面。アプリ・おえかき・でんわ・時計・天気、動画ロック、おうちの人からの呼びかけ | 1.0.3（新しい ID） | [Theta.KidsHome.Hatch](https://github.com/kiwiman0706-beep/Theta.KidsHome.Hatch) | [子供用ホーム画面アプリ](https://claude.ai/code/session_01NhS3xRwFVfssMDMXfSoJEv) | 2026-10-24 |
| 14 | **Theta.Hitsudan.Hatch**<br>（筆談・翻訳表示） | 診察室で医師の言葉を音声認識し、外国語の患者には翻訳、耳の不自由な患者には日本語のまま、手元の電子ペーパー（M5PaperS3）やタブレットに大きな文字で表示。医師が確認してから送る。操作はログに残る | — | [Theta.Hitsudan.Hatch](https://github.com/kiwiman0706-beep/Theta.Hitsudan.Hatch) | [音声認識翻訳表示システム](https://claude.ai/code/session_01B9UWzs14Mh99ti9U7GyxZV) | 2026-10-27 |
| 15 | **Theta.Music.Hatch**<br>（Theta Music） | Tailscale 経由で NAS の音楽を再生するプレーヤー（Flutter）。WebDAV か Synology Audio Station に接続。iPod classic 風と Home.Hatch 風（6 テーマ）のスキン。ライブラリを Obsidian の Markdown に書き出し | 1.0.0 | [Theta.Music.Hatch](https://github.com/kiwiman0706-beep/Theta.Music.Hatch) | [NAS音楽再生アプリ](https://claude.ai/code/session_012DXkc2Wd5iBmicj8ba39vG) | 2026-10-27 |
| 16 | **Theta.Photo.Hatch** | 「まず撮る → あとで仕分け」。カメラの写真を固定の仕分け先フォルダ（家族共有・家族・メモ・非公開）へ移し、名前の付け直しと XMP（分類・イベント・☆）の書き込み。Amazon フォト・Synology Photos・みてねのバックアップはフォルダ単位で任せる | 0.1.0 | [Theta.Photo.Hatch](https://github.com/kiwiman0706-beep/Theta.Photo.Hatch) | [ファイル管理構想](https://claude.ai/code/session_012DXkby1gTG6FFj5k36BF48) | 2026-10-29 |
| 17 | **Theta.Mitene.Hatch**（構想中） | 「みてね」の代わり。Synology Photos の写真を家族で見る | — | [Theta.Mitene.Hatch](https://github.com/kiwiman0706-beep/Theta.Mitene.Hatch)（まだ空） | [みてね代替案検討](https://claude.ai/code/session_012DXkc1gdp42YFc5gM1nwUj) | 2026-11-03 |
| 18 | **Theta.Movie.Hatch**（設計中） | Synology の動画プレイヤー（Video Station）の代わり。NAS 上の Jellyfin（Docker、Tailscale 経由）を土台に、他のソフトでも読めるファイル名規則（`docs/naming-convention.md`）を作成中 | — | [Theta.Movie.Hatch](https://github.com/kiwiman0706-beep/Theta.Movie.Hatch) | [動画プレイヤー代替アプリ](https://claude.ai/code/session_012DXkbxgRpZwVsU9fra6sF1) | 2026-11-03 |
| 19 | **Theta.File.Hatch**（試作） | Theta Vault を NAS などに置いたまま、フォルダごとにふさわしい見え方で眺めるファイラーの試作。見え方もファイル（`.view.yaml`）で持つ。ブラウザで見られるデモ付き | — | [Theta.File.Hatch](https://github.com/kiwiman0706-beep/Theta.File.Hatch) | [ObsidianFS 構想](https://claude.ai/code/session_012DXkbxcLWLwFVYWM9tVHxb) | 2026-11-05 |
| 20 | **Theta.Chirashi.Hatch** | 製薬会社の勉強会などのチラシをスキャン → Gemini で読み取り → Google カレンダーに登録（チラシ画像は Drive に保存して添付）。QR コード読み取り、月のカレンダー表示。Meishi.Hatch と同じつくり | 0.3.0（撮って登録 SCAN に対応） | [Theta.Chirashi.Hatch](https://github.com/kiwiman0706-beep/Theta.Chirashi.Hatch) | [アプリ開発](https://claude.ai/code/session_012DXkbxUnbUEgxEY1bfHP77) | 2026-11-06 |
| 21 | **Theta.Camera.Hatch** | Galaxy Z Fold5 専用のカメラ。起動後ワンタップ録画・録画中の写真、開いたら外画面で自撮り、外画面ライブ、Flex モード、スロー 240fps・HDR、全体を残して表示範囲を記録する HEIF（clap）、イベント・☆・タグ・コメント（XMP／JSON）。純正カメラの置き換えが目標。ADB の窓口あり | 0.16.0（新しい ID・共通鍵、撮って返す、スキャンの AI-OCR） | [Theta.Camera.Hatch](https://github.com/kiwiman0706-beep/Theta.Camera.Hatch) | [カメラアプリ](https://claude.ai/code/session_012DXkbx4X64tseX2Fpu1dRb) | 2026-11-08 |

### 関連（Theta.xxx.Hatch の名前ではないもの）

| 作品 | 概要 | 最新版 | GitHub | Claude スレッド | 開始日 |
| --- | --- | --- | --- | --- | --- |
| **DeskHatch** | 画面最上部に常駐するランチャーバー。ボタンで真下にドロワーが開き、Gmail・カレンダー等の Web アプリ、ファイル、クリップ、各種ツールを置ける。共通仕様 §7 で Hatch 各作品との統合先 | 0.1.72-beta.2 | [deskhatch](https://github.com/kiwiman0706-beep/deskhatch) | [Deskhatch2](https://claude.ai/code/session_018tmaD8HpkoGTEfY5qob4Dd) | 2026-09-15 |
| **Theta.Kidshome.Hatch.Closed** | キッズホームの、公開できない素材（購入した 3D モデル、キャラクターの素材）を置く非公開リポジトリ。VRM のガイド役は Actions で連番の絵にして入れる | — | [Theta.Kidshome.Hatch.Closed](https://github.com/kiwiman0706-beep/Theta.Kidshome.Hatch.Closed)（private） | [子供用ホーム画面アプリ](https://claude.ai/code/session_01NhS3xRwFVfssMDMXfSoJEv) | 2026-11-03 |
| **Theta.Hatch.Suite** | 2026-10-26 に別スレッドで作った作品一覧（この README の元。アーカイブする） | — | [Theta.Hatch.Suite](https://github.com/kiwiman0706-beep/Theta.Hatch.Suite) | [series overview](https://claude.ai/code/session_01Xuw9YGgEFk7uAVjKZTRiUo) | 2026-10-26 |

## 対応状況

2026-11-03 時点で、各リポジトリの最新のブランチのコードを調べた結果です（README・計画書にだけ書かれているものは「予定」）。

○ 対応　△ 一部（注釈）　× なし　予定 ＝計画のみ

### プラットフォーム・自動更新・設定の書き出し

| # | 作品 | Windows | Mac | Android | Android TV | その他 | 自動更新 | 設定の一括書き出し |
| --- | --- | :-: | :-: | :-: | :-: | --- | --- | --- |
| 1 | Book | ○ デスクトップ版・Jisui.Viewer（※） | ○ 同左（※） | ○ | ○ | — | × | △ 読書記録だけ |
| 2 | Meishi | ○ Electron | ○ Electron | ○ | × | Web（PWA・iPhone） | ○ Android・Windows（Mac は通知） | △ シリーズ設定は Vault で共有、データは ZIP バックアップ |
| 3 | Item | × | × | ○ | × | — | × | △ データのバックアップ（ZIP・Drive） |
| 4 | Kamigata | × | × | ○ | × | 書き出した HTML を PC で見られる | × | △ データのバックアップ・復元 |
| 5 | DoorPhoto | 予定（PWA） | 予定（PWA） | ○ | × | — | × | △ 写真込みのバックアップ ZIP |
| 6 | Label | × | × | ○ | × | — | × | × |
| 7 | Device | × | × | ○ | × | — | × | △ 暗号化したバックアップ（パスワード付き） |
| 8 | Travel | × | × | ○ | × | — | × | △ バックアップ JSON（端末だけの項目は除く） |
| 9 | Oekaki | △ ブラウザ版 | △ ブラウザ版 | ○ 横画面 | × | — | × | △ 絵の ZIP |
| 10 | Mensetsu | ○ Electron | ○ Electron | ○ | × | Web（PWA） | △ デスクトップだけ | △ データは Vault |
| 11 | Home | × | × | ○ | × | — | ○ | ○ 設定を書き出す・読み込む（JSON） |
| 12 | Memo | △ Drive＋Obsidian で読み書き | △ 同左 | ○ | × | — | ○ | × データは Vault |
| 13 | KidsHome | × | × | ○ タブレット | ○ | — | ○ | ○ 設定を .xlsx で書き出し |
| 14 | Hitsudan | ○ PC のサーバー | ○ PC のサーバー | × | × | ブラウザ（タブレット）・M5PaperS3 | × | × |
| 15 | Music | × | × | ○ | × | — | × | × |
| 16 | Photo | 予定（Flutter の雛形あり） | 予定（同左） | ○ | × | — | × | × |
| 17 | Mitene | 構想中 | | | | | | |
| 18 | Movie | 設計中（サーバーは NAS の Jellyfin） | | | | | | |
| 19 | File | △ ブラウザのデモ | △ ブラウザのデモ | × | × | Python のデモ作成ツール | × | × |
| 20 | Chirashi | × | × | ○ | × | — | × | × |
| 21 | Camera | × | × | ○ Fold5 専用 | × | — | ○（ハブ、無ければ単体） | × |
| — | DeskHatch | ○ | ○ | × | × | — | ○ | ○ エクスポート・インポート |

- **自動更新**は spec §6.1 で必須。○ は 6 つだけです（Meishi・Memo・Home・KidsHome・DeskHatch、Mensetsu はデスクトップのみ）。
- **設定の一括書き出し**：○ は「設定をファイルに書き出して、別の端末で読み込める」もの。△ はデータ全体のバックアップで、設定が含まれるかはアプリごとに未確認。移行（`docs/MIGRATION.md`）の橋渡し版で使う。
- **Android TV**：Leanback に対応しているのは KidsHome と Book だけ。
- ※ Book（dsbooks）はブランチが 2 本に分かれています：`claude/vigilant-ramanujan-4v5vsv`（10-25、DSBooks 1.0.0・Windows/Mac のデスクトップ版と Jisui.Viewer あり）と `ccr-fbd7a73d-mp81q5`（10-28、Android の 0.8.7-preview、デスクトップ版なし）。どちらを本線にするか決めて合わせる必要があります。

### 連携

| # | 作品 | Obsidian Vault | Google ドライブ | Synology | Secure SignIn（2 段階認証） |
| --- | --- | --- | --- | --- | --- |
| 1 | Book | △ NAS 上に Obsidian 互換の蔵書メタデータ（Theta Vault ではない） | × | ○ File Station API で NAS の本棚 | △ 確認コードの入力のみ（毎回。デバイストークンなし） |
| 2 | Meishi | ○ Theta Vault（正本） | ○ Vault の同期・取り込み（＋連絡先・カレンダー） | × | × |
| 3 | Item | × | ○ Drive にバックアップ（Drive 全体の権限） | × | × |
| 4 | Kamigata | × | × | × | × |
| 5 | DoorPhoto | × | 予定（1.8.0 で Drive 同期） | × | × |
| 6 | Label | × | × | × | × |
| 7 | Device | × | × | × | × |
| 8 | Travel | × | × | × | × |
| 9 | Oekaki | △ Obsidian 形式だが独自のルート（`Oekaki Hatch/`）・独自の項目 | ○ Drive に同期（Drive 全体の権限） | × | × |
| 10 | Mensetsu | ○ Theta Vault | ○ Vault の同期（＋連絡先） | × | × |
| 11 | Home | 予定（PLAN） | ○ 読み取りのみ（ファイラーで Drive を辿る） | ○ File Station API（ファイラーで NAS） | ○ 確認コード＋デバイストークン（2 回目から不要） |
| 12 | Memo | ○ Theta Vault | ○ Vault の同期 | ○ File Station API（NAS の Vault が正本） | ○ 確認コード＋デバイストークン |
| 13 | KidsHome | × | × | 予定（WebDAV・Synology Photos・Synology Chat） | × |
| 14 | Hitsudan | × | × | × | × |
| 15 | Music | △ NAS 上の Vault にライブラリを書き出し（Dataview。Theta Vault ではない） | × | ○ Audio Station API・WebDAV・File Station | ○ 確認コード＋デバイストークン |
| 16 | Photo | 予定（イベントの索引・日記。写真は NAS のパスで参照） | × | △ Synology Photos のバックアップ機能に任せる（API 接続なし） | × |
| 17 | Mitene | 構想中 | | 前提（Synology Photos） | |
| 18 | Movie | △ 作品情報を NFO と Markdown に（予定） | × | 前提（NAS 上の Jellyfin） | × |
| 19 | File | ○ Theta Vault を表示（`.view.yaml`） | × | 予定（NAS の Vault を表示） | × |
| 20 | Chirashi | × 端末内（Markdown で保存は可） | ○ チラシ画像を Drive に保存（＋カレンダー） | × | × |
| 21 | Camera | △ 写真ごとの XMP・JSON（Theta Vault ではない） | × | × | × |
| — | DeskHatch | △ クリップを Obsidian 向けの Markdown で保存 | △ Drive のフォルダを箱として使う | × | × |

- **Secure SignIn**：Synology の 2 段階認証。アプリからは「確認コード（OTP）を入れる → デバイストークンを受け取って、次からは聞かない」形で対応します（Home・Music の方式）。Secure SignIn アプリの「承認」ボタンでのログインは、アプリからは使えない前提です（未確認）。
- **Synology の接続のしかたがアプリごとに別々**です（Book・Home・Music がそれぞれ DSM ログインを持つ）。共通の部品と、接続先・デバイストークンの引き継ぎ（`spec/THETA_SHARED_SETTINGS.md`）を仕様にする候補です。
- Drive の権限は、Home が読み取りのみ、Item・Oekaki が Drive 全体、Meishi・Memo・Mensetsu が Vault の同期用です。

## メモ

- 最新版は各リポジトリの README・`versionName`・`package.json` の値です。「—」は確認できなかったもの。
- Meishi・Mensetsu・Memo・Oekaki は「Theta Vault」（Obsidian で開ける Markdown フォルダ）を共有する設計です。シリーズ共通仕様は [`spec/`](spec/) にあります。
- 多くの作品は README に「実機での確認はまだ」と書かれています。
- Claude スレッドは、各リポジトリを開発した主なスレッドです。

## このリポジトリの中身

| 場所 | 中身 |
| --- | --- |
| [`spec/`](spec/) | シリーズ共通仕様（[ADB](spec/THETA_ADB_SPEC.md)・[TV](spec/THETA_TV_SPEC.md)（構想）・[NAS ライブラリ](spec/THETA_LIBRARY_SPEC.md)・[Hatch](spec/THETA_HATCH_SPEC.md)・[Vault](spec/THETA_VAULT_SPEC.md)・[設定の引き継ぎ](spec/THETA_SHARED_SETTINGS.md)・[Google 連携](spec/THETA_GOOGLE_SETUP.md)）。MeishiApp/docs から移設 |
| [`design/`](design/README.md) | デザインガイドラインとスキン（Home.Hatch の dark・light・pop・alert・scifi）、HUD キット |
| [`secrets/`](secrets/README.md) | 共通の署名鍵・Secret の名前と置き場所（鍵そのものは入れない） |
| [`progress/`](progress/_TEMPLATE.md) | 各アプリのスレッドが書く移行メモ（方針・決めてほしいこと・進み具合）。`progress/<id>.md` |
| [`tools/`](tools/) | スキンの生成（`gen_skins.py`）、Secret を全リポジトリへ配る（`sync-secrets.ps1` / `.sh`） |
| [`samples/`](samples/README.md) | Obsidian で開ける見本の Theta Vault（架空のデータ・一覧用の `.base` 付き） |
| [`catalog/apps.json`](catalog/apps.json) | アプリ一覧（機械が読む用）：今と目標のリポジトリ名・ID、自動更新の有無。Home の Hatch ドロワーの正本 |
| [`docs/MIGRATION.md`](docs/MIGRATION.md) | 名前・ID・リポジトリ・鍵を揃える手順と影響。各スレッドに送る文は [`PROMPT_JOIN.md`](docs/PROMPT_JOIN.md)（最初の一通）・[`PROMPT_SWAP.md`](docs/PROMPT_SWAP.md)（入れ替えだけのアプリへ）・[`PROMPT_UPDATE_HUB.md`](docs/PROMPT_UPDATE_HUB.md)（Home・KidsHome へ）・ [`PROMPT_MIGRATION.md`](docs/PROMPT_MIGRATION.md)。ID の一覧は [`APP_IDS.md`](docs/APP_IDS.md)、進み具合は [Hatch 移行ボード](https://claude.ai/artifact/39gPQjDjBrTmp3WwbAPM4S) |
| [`docs/FOR_APP_REPOS.md`](docs/FOR_APP_REPOS.md) | 各アプリ・各スレッドからここを参照させる方法 |
