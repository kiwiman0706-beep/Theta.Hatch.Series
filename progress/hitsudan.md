# Theta Hitsudan Hatch（hitsudan）の移行メモ

- 更新：2026-11-06
- スレッド：https://claude.ai/code/session_01B9UWzs14Mh99ti9U7GyxZV
- 状態：計画OK待ち

## 今と目標

| | 今（版なし。ブランチ `claude/ecstatic-bardeen-0jx5t8`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Hitsudan.Hatch`（改名不要） | 同じ |
| アプリ ID | なし（Python のサーバー＋ブラウザ 2 窓） | `app.thetahatch.hitsudan`（デスクトップ版の appId） |
| 署名 | なし（APK なし） | Android 版を作らないなら対象外。Windows・Mac は spec §6 のとおり（Mac はアドホック署名） |
| 更新 | なし | デスクトップの自動更新（Windows：取得して次の起動で入れ替え、Mac：通知とダウンロードページ）。Android のハブは対象外 |
| 共通設定 | 自分で持つ（Gemini キーは環境変数 `GEMINI_API_KEY`、モデル・その他は `config.local.json`） | Vault の `.theta/settings.json` から `ui.skin`・`gemini.model` を読む（「シリーズに合わせる」）。Gemini キーは端末内で暗号化（Windows の資格情報マネージャー・Mac のキーチェーン）。ハブ（ContentProvider）は Android だけなので使わない |
| データの置き場所 | PC の `logs/YYYY-MM-DD.jsonl`（診察の会話ログ。医療情報） | **下の「決めてほしいこと」1** |
| 対応 OS | Windows・Mac（Python 3.12＋Edge/Chrome）。患者側はブラウザ（タブレット）・M5PaperS3（USB） | 同じ。配布の形は「決めてほしいこと」2 |
| スキン | 独自（白地に青、角丸） | `design/skins/theta-skins.css` の 6 つ（system 既定）。**患者側の画面と電子ペーパーは白黒・大きな文字のまま**（読みやすさ優先。スキンは医師側だけ） |

## 方針

### このアプリの特徴（他のアプリと違うところ）

- 診察室の PC で動く業務用。中身は**患者との会話（医療情報）**。
- 音声認識は PC の中（faster-whisper、Python）。翻訳だけ Gemini に送る。
- 患者側の電子ペーパー用の画像を PC で作り（Pillow）、USB シリアルで送る。

### 改名・ID 変更で直すところ

- リポジトリ名はすでに目標どおり。コードに個人名（yaegaki・kiwiman）や古い名前は無い（確認済み）。
- 画面の表示名を「Theta Hitsudan Hatch」に（今は「筆談・翻訳（医師用）」）。
- `start.py` のブラウザのプロファイル置き場など、アプリ名を使う場所を `app.thetahatch.hitsudan` に揃える。
- M5PaperS3 のファームは ID と無関係（変更なし）。

### 端末の中にしか無いデータと移し方

- `logs/*.jsonl`（会話ログ）、`config.local.json`（設定）、環境変数の Gemini キー。録音は既定で保存しない。
- 移し方：新しい置き場所を選ぶと、起動時に「今の logs/ を移しますか」と聞いてコピーする（消さない。コピー後も元は残す）。設定は `config.local.json` を読み込んで新しい設定に変換。キーは初回に入れ直してもらう。
- APK が無いので「入れ直しでデータが消える」問題は無い。

### シリーズの仕様で、このアプリに合わないもの

- **Electron（spec §4）**：音声認識・画像作成・シリアルが Python なので、そのまま Electron にはできない。案は「決めてほしいこと」2。
- **ハブから設定を受け取る（決めたこと 2）**：ハブは Android の仕組み。デスクトップでは Vault の `.theta/settings.json` で代わりにする。
- **Android・Web（PWA）版**：医師側は PC 専用にしたい（マイク・GPU・USB 端末）。患者側の表示は今のブラウザ画面で足りる。
- **API にトークン（spec §4.1）**：今は 127.0.0.1 だけで待ち受けるがトークンなし。ほかの Web ページから送信 API を叩かれないよう、トークンを付ける（DeskHatch のドロワーにも載せられる）。

## 決めてほしいこと

- [ ] 1. **会話ログの置き場所**。医療情報なので、Google ドライブ（Vault）に置くのはおすすめしない。
  - 案A（おすすめ）：PC の中（今のまま）＋NAS の共有フォルダ（Tailscale 経由、SMB でつないだフォルダ）にもコピー。アプリは「フォルダに書く」だけなので NAS のログインや 2 段階認証は不要
  - 案B：Theta Vault 形式（1 診察＝1 Markdown）にして NAS の Vault に置く。Obsidian で読める
  - 案C：Google ドライブの Vault（院内の規程で許される場合だけ）
  - どの案でも、ログに患者の氏名は入れない（受付番号だけ）。
- [ ] 2. **Windows・Mac での配る形**
  - 案A（おすすめ）：Electron の外側＋中で Python を動かす（PyInstaller で 1 つにまとめた Python を同梱）。シリーズの形（インストーラー・自動更新・トレイ常駐）に揃えられる。サイズは大きい（音声認識のモデルは初回にダウンロード）
  - 案B：今の Python＋ブラウザ 2 窓のまま、PyInstaller で exe／app に。自動更新は「新しい版があります」の通知だけ
  - 案C：全部 Node（Electron）に書き直す（whisper.cpp・canvas・serialport）。手間が大きい
- [ ] 3. **Android 版を作るか**（作らないなら署名・ハブの項目は対象外）。おすすめは作らない
- [ ] 4. **リポジトリを公開にするか**（自動更新で Releases を読むのに必要。コードだけで、ログ・キーは入らない）
- [ ] 5. 患者側の画面・電子ペーパーはスキンを当てず白黒のままにしてよいか（おすすめ：白黒のまま）

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [ ] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [ ] appid：アプリ ID を新しい ID に
- [ ] signing：共通鍵の Secret で署名（APK なし：Android 版を作らないなら対象外）
- [ ] update：更新をハブに頼む形に（デスクトップの自動更新で代える）
- [ ] settings：共通設定をハブから受け取る（デスクトップは Vault の `.theta/settings.json`）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（改名なし。古い名前・個人名が無いことを確認）
- [ ] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] Windows：起動・2 窓・マイク・音声認識（GPU あり／なし）・Gemini 翻訳
- [ ] Mac：同上
- [ ] M5PaperS3：書き込み・表示・タッチの返答（ファームは未コンパイル）
- [ ] ログの移動（古い logs/ → 新しい置き場所）
