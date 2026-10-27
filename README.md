# Theta.Hatch.Series

Theta.xxx.Hatch シリーズの作品一覧と、シリーズ共通のガイドライン（仕様・デザイン・鍵）の正本です。

## 最新ガイドラインの要点（2026-10-26 時点）

新しいアプリを作るときは、まず「このガイドラインに合わせるか」を決めます。合わせる場合の要点は次のとおりです（詳しくはリンク先）。

| # | 分野 | 要点 | 詳しく |
| --- | --- | --- | --- |
| 1 | 名前 | 表示名は `Theta <名前> Hatch`。applicationId・appId は `app.thetahatch.<名前>`（個人名は入れない）。版番号は全プラットフォームで同じ、タグは `v<版>` | [spec §2](spec/THETA_HATCH_SPEC.md) |
| 2 | データ | 正本は利用者の Google ドライブの **Theta Vault**（Obsidian で開ける Markdown＋添付）。1件＝1ファイル、`id` で同一性、削除は `.theta/trash/` へ、大量欠落では削除しない。Obsidian で一覧・ギャラリーが見られるよう、各アプリは自分のフォルダに `.base`（Obsidian Bases）を置く。見本は [`samples/theta-vault`](samples/README.md) | [Vault 仕様](spec/THETA_VAULT_SPEC.md) |
| 3 | 原則 | ローカルファースト（オフラインで動き、同期は後から）。独自サーバーを持たない。消さない・戻せる | [spec §1](spec/THETA_HATCH_SPEC.md) |
| 4 | プラットフォーム | UI は1つ（HTML/CSS/JS）を共有し、Android（APK＋ホーム画面ウィジェット）・Windows/Mac（Electron）・Web（PWA、iPhone）で動かす。端末機能はブリッジ `Native.call` / `window.onNative` で差し替え | [spec §4](spec/THETA_HATCH_SPEC.md) |
| 5 | デザイン | 見た目は Home.Hatch の**スキン**に揃える：`system`（既定）・`dark`・`light`・`pop`・`alert`・`scifi`。色は直接書かず役割（accent・widget・launch…）から取る。書体は Oswald＋Share Tech Mono | [design](design/README.md) |
| 6 | 設定の共有 | シリーズ共通の設定は Vault の `.theta/settings.json`（スキン `ui.skin`、Gemini のモデル、Google アカウントなど）。項目ごとに「シリーズに合わせる／このアプリだけ」を選べる。初回起動で引き継ぎを聞く | [設定の引き継ぎ](spec/THETA_SHARED_SETTINGS.md) |
| 7 | 秘密 | API キー・トークンはクラウドにも Git にも置かない。端末内で暗号化。同じ端末の別アプリへは、利用者の承認で貸し借り（同じ署名鍵のアプリ同士） | [設定の引き継ぎ §4](spec/THETA_SHARED_SETTINGS.md) |
| 8 | 署名鍵 | Android は**シリーズ共通の鍵**（Meishi の鍵、SHA-1 `A1:13:EA:…:28:BA`）。CI の Secret 名は `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD`。`tools/sync-secrets` で全リポジトリへ配る | [secrets](secrets/README.md) |
| 9 | AI・Google | Gemini は利用者自身の API キー。Google Cloud はシリーズで1プロジェクト、新しいアプリは Android 用 OAuth クライアント（パッケージ名＋共通の SHA-1）を足すだけ。設定手順はアプリ内のガイドで案内 | [Google 連携](spec/THETA_GOOGLE_SETUP.md) |
| 10 | リリース・**自動更新（必須）** | GitHub Actions の `release.yml` で全プラットフォームを1つの Release に。Web 版は `pages.yml`。**全アプリにアプリ内自動更新**：Android は Releases を12時間ごとに確認、Wi-Fi で取得、SHA-256・パッケージ名・署名を照合して PackageInstaller で更新（Android 12+ は確認なし）。リポジトリは公開 | [spec §6・§6.1](spec/THETA_HATCH_SPEC.md) |
| 11 | 連携 | デスクトップ版は DeskHatch のドロワーとして表示できるように。テレビへは Theta Link（LAN 内で発見・ペアリング） | [spec §7・§8](spec/THETA_HATCH_SPEC.md) |
| 12 | 品質 | Vault の往復テスト、2台の同期テスト、320〜768px 幅ではみ出さない、JS エラー0。実機で確かめていないことは `TESTING.md` に「未確認」と書く | [spec §9](spec/THETA_HATCH_SPEC.md) |
| 13 | 新しいアプリの手順 | 各アプリの `CLAUDE.md` にこのリポジトリを参照する一文を入れる。完成したら下の作品一覧に追加し、`tools/repos.txt` に足して Secret を配る | [FOR_APP_REPOS](docs/FOR_APP_REPOS.md) |
| 14 | 移行 | 名前・ID・リポジトリ名・署名鍵を揃える作業中。各アプリの今と目標は `catalog/apps.json`。鍵と ID は同じ版で変え、「橋渡し版」で自動更新からデータの書き出し→新アプリへ移る | [MIGRATION](docs/MIGRATION.md) |

## 作品一覧

2026-10-26 時点。開始日の古い順。

| # | 作品 | 概要 | 対応プラットフォーム | 最新版 | GitHub | Claude スレッド | 開始日 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Theta.Book.Hatch**<br>（DSBooks） | 自炊本・PDF・コミック・EPUB・Markdown の本棚／リーダー。全画面読書、見開き・縦スクロール表示。姉妹アプリ Theta.Jisui.Viewer も同じリポジトリ | Android / Windows / Mac | DSBooks 1.0.0、Jisui.Viewer 0.2.5 | [dsbooks](https://github.com/kiwiman0706-beep/dsbooks)（private） | [Theta.Book.Hatch](https://claude.ai/code/session_01VBri9A5SpavPKRqvCQZARs) | 2026-10-15 |
| 2 | **Theta.Meishi.Hatch**<br>（旧 Meishi-Claude） | 名刺を撮影 → Gemini で読み取り → Google 連絡先に登録。名刺画像・メモ・録音を人ごとに保存、カレンダー・地図・Drive 同期。シリーズ共通仕様（Theta Vault）の元 | Android / Windows / Mac / Web（iPhone は PWA） | — | [MeishiApp](https://github.com/kiwiman0706-beep/MeishiApp) | [Theta.Meishi.Hatch](https://claude.ai/code/session_016tfKWDzu24Zp9FBxh4cjKS) | 2026-10-16 |
| 3 | **Theta.Item.Hatch**<br>（おもいでクローゼット） | 小さくなった子ども服などを手放す前に写真で残し、スマホのクローゼットのように眺めて楽しむ記録アプリ | Android | 1.3.0 | [Theta.Item.Hatch](https://github.com/kiwiman0706-beep/Theta.Item.Hatch) | [Theta.Item.Hatch](https://claude.ai/code/session_01QGzXdJYduLXUGSNC9NMCDu) | 2026-10-17 |
| 4 | **Theta.Kamigata.Hatch**<br>（くるりヘア） | 子どもの髪型を前後左右・斜め・真上から撮影し、指のドラッグで角度を切り替えて見返す（QuickTime VR の Object Movie 風） | Android 8.0+ | 1.1.0 | [Theta.Kamigata.Hatch](https://github.com/kiwiman0706-beep/Theta.Kamigata.Hatch) | [Theta.Kamigata.Hatch](https://claude.ai/code/session_01De2aFah9Lcgtf5wm3XZKDX) | 2026-10-17 |
| 5 | **Theta.DoorPhoto.Hatch**<br>（おもいで年表） | 玄関ドアに instax 写真で作る家族の「サムネイル年表」用。写真・出来事を登録し、月末にコラージュを作って instax・A4・テプラへ出力 | Android 11+ | 1.7.0 | [Theta.DoorPhoto.Hatch](https://github.com/kiwiman0706-beep/Theta.DoorPhoto.Hatch) | [引き継ぎとAPKリリース](https://claude.ai/code/session_01EBZjKxFPPAcMuVaRQmJaEM) | 2026-10-17 |
| 6 | **Theta.Label.Hatch**<br>（声でテプラ） | テプラ PRO SR5900P へ音声でラベル印刷。「話す → 確認 → 1回押して印刷」 | Android 11+ | 1.0.0 | [Theta.Label.Hatch](https://github.com/kiwiman0706-beep/Theta.Label.Hatch) | [引き継ぎとAPKリリース](https://claude.ai/code/session_01SsMo5spj81EiVV3fsBYJwr) | 2026-10-17 |
| 7 | **Theta.Device.Hatch**<br>（機器台帳） | PC・電子機器の銘板や設置風景を撮影して機器台帳を作成。OCR＋Gemini で転記補助、ログイン情報を暗号化保存、QR 付き管理ラベルをテプラで印刷 | Android 11+ | 1.1.0 | [Theta.Device.Hatch](https://github.com/kiwiman0706-beep/Theta.Device.Hatch) | [APKリリースと機能構想](https://claude.ai/code/session_01MfF9qvjEzW47oy37eYGX2f) | 2026-10-17 |
| 8 | **Theta.Travel.Hatch**<br>（TravelHatch／旧 たびのたね） | 「行ってみたい」を貯め、天気・時間・泊数などの条件で行き先を選び、旅のしおりから思い出まで一続きで残す | Android 9+ | 0.1.1 | [Theta.Travel.Hatch](https://github.com/kiwiman0706-beep/Theta.Travel.Hatch) | [APKリリースと要件整理](https://claude.ai/code/session_01AvSnwTjAMGxxrwossSH8b5) | 2026-10-17 |
| 9 | **Theta.Oekaki.Hatch**<br>（おえかきハッチ） | 子どもが描いた絵を取り込むと、主人公や敵になってゲーム（ぼうけん・レース）で動きだす。絵は Obsidian Vault 形式で蓄積、Drive 同期 | Android 8.0+（横画面） / PC・Mac（ブラウザ版） | — | [Theta.Oekaki.Hatch](https://github.com/kiwiman0706-beep/Theta.Oekaki.Hatch) | [APKリリース](https://claude.ai/code/session_01LmiStbYTVdJCtU26X4VDQh) | 2026-10-17 |
| 10 | **Theta.Mensetsu.Hatch** | 医療機関の職員採用面接の管理。履歴書を Gemini で読み取り、選考状況・面接メモ（手書き・録音の文字起こし）・書類・通勤費概算を管理。Meishi.Hatch ベース | Android / Windows / Mac / Web（PWA） | 0.2.0 | [Theta.Mensetsu.Hatch](https://github.com/kiwiman0706-beep/Theta.Mensetsu.Hatch) | [採用面接管理アプリ](https://claude.ai/code/session_01UZcNkbW2pixSpi59267B3r) | 2026-10-22 |
| 11 | **Theta.Home.Hatch** | 背景（デスクトップ）にファイラーを置き、画面端のタブでドロワーやウィジェットを切り替える Android ホームアプリ。狭い画面では予定・天気のダッシュボード | Android 10+（Galaxy Z Fold5、iPlay 60/80、Titan 2 想定） | 0.27.0-alpha | [Theta.Home.Hatch](https://github.com/kiwiman0706-beep/Theta.Home.Hatch) | [Theta.Home.Hatch](https://claude.ai/code/session_01GMSgoGarRChJJQLGtjAFKY) | 2026-10-22 |
| 12 | **Theta.Memo.Hatch** | Google Keep 風の付箋メモ。データは Obsidian 形式（Theta Vault）で Google Drive に保存し、リッチテキスト・表・手書き・音声・ファイル添付、Keep からの取り込みに対応 | Android（PC・Mac は Drive＋Obsidian で読み書き） | 0.1.0 | [Theta.Memo.Hatch](https://github.com/kiwiman0706-beep/Theta.Memo.Hatch) | [アプリ開発](https://claude.ai/code/session_01H9m1j4wPmRzXQbzu7zWADS) | 2026-10-23 |
| 13 | **Theta.KidsHome.Hatch**<br>（キッズホーム） | 子ども用タブレット向けのかわいいホーム画面。アプリ・おえかき・でんわ・時計・天気、動画ロック、おうちの人からの呼びかけ | Android（タブレット、ALLDOCUBE iPlay60 など） | 0.4.0 | [Theta.KidsHome.Hatch](https://github.com/kiwiman0706-beep/Theta.KidsHome.Hatch) | [子供用ホーム画面アプリ](https://claude.ai/code/session_01NhS3xRwFVfssMDMXfSoJEv) | 2026-10-24 |

### 関連（Theta.xxx.Hatch の名前ではないもの）

| 作品 | 概要 | 対応プラットフォーム | 最新版 | GitHub | Claude スレッド | 開始日 |
| --- | --- | --- | --- | --- | --- | --- |
| **DeskHatch** | 画面最上部に常駐するランチャーバー。ボタンで真下にドロワーが開き、Gmail・カレンダー等の Web アプリ、ファイル、クリップ、各種ツールを置ける。共通仕様 §7 で Hatch 各作品との統合先 | Windows / Mac | 0.1.72-beta.2 | [deskhatch](https://github.com/kiwiman0706-beep/deskhatch) | [Deskhatch2](https://claude.ai/code/session_018tmaD8HpkoGTEfY5qob4Dd) | 2026-09-15 |
| **Theta.Hatch.Suite** | 今日、別スレッドで作った作品一覧（この README と同じ内容） | — | — | [Theta.Hatch.Suite](https://github.com/kiwiman0706-beep/Theta.Hatch.Suite) | [series overview](https://claude.ai/code/session_01Xuw9YGgEFk7uAVjKZTRiUo) | 2026-10-26 |

## メモ

- 最新版は各リポジトリの README・`versionName`・`package.json` の値です。「—」は確認できなかったもの。
- Meishi・Mensetsu・Memo・Oekaki は「Theta Vault」（Obsidian で開ける Markdown フォルダ）を共有する設計です。いまのシリーズ共通仕様は [MeishiApp/docs/THETA_HATCH_SPEC.md](https://github.com/kiwiman0706-beep/MeishiApp/blob/HEAD/docs/THETA_HATCH_SPEC.md)（v2）にあります。
- 多くの作品は README に「実機での確認はまだ」と書かれています。
- Claude スレッドは、各リポジトリを開発した主なスレッドです。

## このリポジトリの中身

| 場所 | 中身 |
| --- | --- |
| [`spec/`](spec/) | シリーズ共通仕様（[Hatch](spec/THETA_HATCH_SPEC.md)・[Vault](spec/THETA_VAULT_SPEC.md)・[設定の引き継ぎ](spec/THETA_SHARED_SETTINGS.md)・[Google 連携](spec/THETA_GOOGLE_SETUP.md)）。MeishiApp/docs から移設 |
| [`design/`](design/README.md) | デザインガイドラインとスキン（Home.Hatch の dark・light・pop・alert・scifi）、HUD キット |
| [`secrets/`](secrets/README.md) | 共通の署名鍵・Secret の名前と置き場所（鍵そのものは入れない） |
| [`tools/`](tools/) | スキンの生成（`gen_skins.py`）、Secret を全リポジトリへ配る（`sync-secrets.ps1` / `.sh`） |
| [`samples/`](samples/README.md) | Obsidian で開ける見本の Theta Vault（架空のデータ・一覧用の `.base` 付き） |
| [`catalog/apps.json`](catalog/apps.json) | アプリ一覧（機械が読む用）：今と目標のリポジトリ名・ID、自動更新の有無。Home の Hatch ドロワーの正本 |
| [`docs/MIGRATION.md`](docs/MIGRATION.md) | 名前・ID・リポジトリ・鍵を揃える手順と影響（各スレッドに送るプロンプトは [`PROMPT_MIGRATION.md`](docs/PROMPT_MIGRATION.md)） |
| [`docs/FOR_APP_REPOS.md`](docs/FOR_APP_REPOS.md) | 各アプリ・各スレッドからここを参照させる方法 |
