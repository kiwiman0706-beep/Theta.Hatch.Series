# Theta Chirashi Hatch（chirashi）の移行メモ

- 更新：2026-11-06
- スレッド：https://claude.ai/code/session_012DXkbxUnbUEgxEY1bfHP77
- 状態：計画OK待ち

## 今と目標

| | 今（0.1.0、2026-11-06 初版） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `THETA.Chirashi.Hatch`（大文字の THETA） | `Theta.Chirashi.Hatch`（大文字・小文字だけの改名） |
| アプリ ID | `jp.yaegaki.theta.chirashi`（Java の package も同じ） | `app.thetahatch.chirashi`（namespace・package も同じに） |
| 署名 | Secret（`ANDROID_KEYSTORE_B64`・`_PASSWORD`・`ANDROID_KEY_ALIAS`）があればそれ、無ければ**リポジトリ内の開発用鍵** `android/signing/chirashi-dev.jks`（パスワードは build.gradle に記載）。`ANDROID_KEY_PASSWORD` は読んでいない。SHA-1 `75:5E:7B:…` | 共通鍵（Secret の 4 つ、別名 thetahatch）。開発用の鍵・パスワードはリポジトリから外す。Secret が無ければ失敗させる（署名なし APK は出さない） |
| 更新 | なし（インストール権限もなし） | ハブに頼む：設定に「今の版」「更新を確認」（Releases の latest を見る）、「更新する」→ `app.thetahatch.action.UPDATE`、ハブが無ければ Releases ページ |
| 共通設定 | 自分で持つ（Gemini キーは Android Keystore で暗号化、モデル・Google アカウントは端末内） | ハブ（Home・KidsHome）から受け取る：`ui.skin`・`gemini.model`・`google.account` は `info`、`gemini.key` は承認して `secret/gemini.key`。ハブが無ければ今までどおり入力 |
| データの置き場所 | 端末の中だけ（`files/chirashi.json`＋`files/media/*.jpg`）。チラシ画像はカレンダー登録時に Drive の「Theta Chirashi Hatch」フォルダへ（`drive.file`） | Theta Vault（Google ドライブ）：`Chirashi/Events/<日付> <会の名前>.md`（1 件 1 ファイル、frontmatter `type: chirashi/event@1`）＋`Chirashi/_files/`（チラシ画像）＋一覧用の `.base`。NAS は後から（下の「決めてほしいこと」） |
| 対応 OS | Android 8.0 以上 | Android。Windows・Mac は下の方針 |
| スキン | 独自（クリーム地＋オレンジ、角丸） | `design/skins/theta-skins.css` の 6 つ（system 既定）。色は役割から取る |

## 方針

### 移行

- 0.1.0 は今日出したばかりで、入れている端末は利用者の 1 台だけ（データもほぼ無い想定）。
- 署名鍵と ID を**同じ版（0.2.0）で変える**。入れ直しになるので、0.2.0 に「読み込み」を付ける。
- 端末の中にしか無いデータ：記録（JSON）とチラシ画像。0.1.0 の「バックアップ（JSON）」は画像を含まない。
  - 案A（おすすめ）：橋渡し版は出さず、0.1.0 で「バックアップ（JSON）」を保存 → 0.2.0 で読み込み。画像はカレンダー登録済みなら Drive にあるので、0.2.0 が Drive から取り戻す。未登録の画像は撮り直し。
  - 案B：橋渡し版 0.1.1（古い ID・開発用の鍵）で画像込みの zip 書き出しを足す。手で上書きインストールが要る（更新の仕組みが無いため）。
- 0.2.0 以降は Vault が正本になるので、次からの入れ直しではデータは消えない。

### 改名・ID 変更で直すところ

- `android/app/build.gradle`：applicationId・namespace・署名（Secret 4 つ、`SIGNING_*` の環境変数名、開発用鍵の既定値を削除）
- Java の package（`jp/yaegaki/theta/chirashi` → `app/thetahatch/chirashi`、3 ファイル）
- `android/signing/chirashi-dev.jks` を削除（履歴には残るので、共通鍵には使わない）
- `.github/workflows/release.yml`：`ANDROID_KEY_PASSWORD` を読む、別名は Secret から、APK 名 `ThetaChirashiHatch-<版>.apk`（済み）
- README のリンク（`THETA.Chirashi.Hatch` → `Theta.Chirashi.Hatch`）・パッケージ名・SHA-1（共通の `A1:13:EA:…:28:BA`）
- アプリ内：設定の GitHub リンク、初期設定ガイドの「Android クライアントを作る」（登録済みなので「済み」と表示に変える）
- テスト（`test/ui.e2e.cjs` の package 名）
- Drive の旧フォルダ「Theta Chirashi Hatch」：新しいアプリは `drive.file` が別アプリ扱いになり見えない → Vault の `Chirashi/_files/` に置き直す（旧フォルダは手で消すか残す）
- Google カレンダーに登録済みの予定：イベント ID は残るので、新しいアプリからも更新・削除できる（同じアカウントなら）

### Windows・Mac

- 画面はすでに HTML/CSS/JS（WebView）なので、Meishi・Mensetsu と同じ形（Electron、Vault フォルダを直接読む）にできる。
- ただしスキャン・QR・カメラはスマホ向けで、PC では「Vault の一覧・カレンダー表示・編集・カレンダー登録」が中心。PC で画像を取り込んで読む（Gemini）ことはできる。
- 先に Android を Vault 対応にし、PC 版はその次（0.3.0 以降）にしたい。Obsidian で `Chirashi/` を開けば、それまでも PC で一覧は見られる。

## 決めてほしいこと

- [ ] 端末内データの移し方：案A（JSON で移して画像は Drive から取り戻す・未登録分は撮り直し）か、案B（橋渡し版 0.1.1 で画像込みの zip）か
- [ ] データの置き場所：まず Google ドライブの Theta Vault だけでよいか（NAS・Secure SignIn は後の版）。Vault の同期には Drive 全体の権限（`drive`、Meishi と同じ）が要る
- [ ] Windows・Mac 版を作るか（作るなら Electron、Android の Vault 対応の後）
- [ ] Releases の URL・GitHub リンクの `kiwiman0706-beep`（GitHub のアカウント名）は残る。アプリの画面には出さず、更新確認の URL にだけ使う形でよいか

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

- [ ] 共通鍵で署名した APK の SHA-1 が `A1:13:EA:…:28:BA`
- [ ] Google ログイン（`app.thetahatch.chirashi` は Google Cloud に登録済み）→ カレンダー登録・画像の添付
- [ ] ハブ（Home）から Gemini キー・スキンを受け取れる
- [ ] 「更新する」でハブの更新画面が開く／ハブが無ければ Releases ページ
- [ ] スキャン・QR 読み取り・Gemini の読み取り（0.1.0 から未確認）
