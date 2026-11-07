# Theta Meishi Hatch（meishi）の移行メモ

- 更新：2026-11-07（1.0.0）
- スレッド：https://claude.ai/code/session_016tfKWDzu24Zp9FBxh4cjKS
- 状態：作業中（橋渡し版 0.19.0 を Releases に公開済み。新しい版 1.0.0 は作成済みで、Home の移行機能ができてからリリース）

## 今と目標

| | 今（0.18.5） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Meishi.Hatch`（旧 `MeishiApp`。コード・ワークフロー・Web版の URL は旧名のまま） | 同じ。旧名の参照をすべて直す |
| アプリ ID | Android `jp.yaegaki.meishiclaude`（Java のパッケージ `jp.yaegaki.meishinote`）、デスクトップ `jp.yaegaki.theta.meishi` | `app.thetahatch.meishi`（Java のパッケージ・デスクトップの appId も） |
| 署名 | 共通鍵（Secret `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`）。ただし `android/build.sh` が別名 `meishiclaude` を直接書いている | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS` から） |
| 更新 | Android：アプリ自身が Releases を見て PackageInstaller で入れる（`REQUEST_INSTALL_PACKAGES`・`UPDATE_PACKAGES_WITHOUT_USER_ACTION`）。Windows：electron-updater。Mac：通知。Web：自動 | Android：ハブに頼む（インストール権限なし。ハブが無ければ Releases を開く）。Windows・Mac・Web は今のまま |
| 共通設定 | Vault の `.theta/settings.json`（モデル・形式・Google アカウント・カレンダー）。Gemini キーは同じ鍵のアプリから借りる `SeriesProvider`（権限 `jp.yaegaki.theta.permission.SHARE`） | ハブ（Home・KidsHome）の `info`／`secret/gemini.key` から受け取る。権限・action を `app.thetahatch.*` に |
| データの置き場所 | Google ドライブの Theta Vault（Android・Web は Drive API、PC は Google ドライブ for デスクトップのフォルダ） | 同じ（Drive）。NAS は「決めてほしいこと」 |
| 対応 OS | Android・Windows・Mac（Electron）・Web（PWA、iPhone） | 同じ |
| スキン | 独自の緑の画面（色は CSS 変数） | `design/skins` の 6 つ（`theta-skins.css`、`data-theta-skin`）。`ui.skin` をハブ・Vault から |

## 方針

### Home との受け渡し（0.19.0 で実装。新しい版にも同じものが入る）

移行は Home がまとめて行う（`docs/MIGRATION.md` §3）。Meishi 側の入口は `MigrationActivity`。

| | 書き出し（橋渡し版 0.19.0、古い ID） | 読み込み（新しい版、新しい ID） |
| --- | --- | --- |
| 呼び方 | `startActivityForResult(Intent("app.thetahatch.action.EXPORT").setPackage("jp.yaegaki.meishiclaude"))` | `startActivityForResult(Intent("app.thetahatch.action.IMPORT").setPackage("app.thetahatch.meishi").setDataAndType(zip の URI, "application/zip").addFlags(FLAG_GRANT_READ_URI_PERMISSION))`（`EXTRA_STREAM` でも可） |
| 確かめること | 呼び出し元が同じ署名（`checkSignatures`）、結果を受け取る形で呼ばれた、利用者が「書き出す」を押した | 同じ |
| 結果 OK | data＝zip の `content://` URI（読み取り許可付き。**古いアプリを消すと読めなくなるので、Home が自分の領域へコピーしておく**）、extra `app.thetahatch.extra.FORMAT`＝`meishi-migration/1`、`app.thetahatch.extra.COUNT`＝名刺の件数 | extra `app.thetahatch.extra.COUNT`＝新しく加えた名刺の件数（Vault から先に戻った名刺は数えず、端末だけの項目だけ足す） |
| 結果 NG | `RESULT_CANCELED`、extra `app.thetahatch.extra.ERROR`＝理由（取りやめも含む） | 同じ |
| zip の中身 | `data.json`（名刺。連絡先・予定の行などの端末だけの項目も、`settings`＝設定、`migration`＝元の ID と時刻）、`media/`（画像・録音・手書き） | — |
| 入れないもの | Gemini の API キー、Google の許可（新しい ID で取り直し）、取り込みフォルダの権限 | — |

### 移行の順番（ID は変わるが鍵はすでに共通）

1. **橋渡し版 0.19.0**（古い ID のまま。今のアプリ内更新か Home で上書き）：上の書き出し。メニューに「新しい Theta Meishi Hatch へ移る」（Home を開く／無ければ Home の入手ページ）
2. **新しいアプリ 1.0**（`app.thetahatch.meishi`、Release の APK 名は `ThetaMeishiHatch-<版>.apk`）
   - 上の読み込み（Home から呼ばれる）
   - 自分で入れる更新の仕組みを外し、ハブに頼む形に
   - Web 版は Pages の URL が `…/Theta.Meishi.Hatch/` に変わる（オリジンは同じなので Web 用 OAuth クライアントはそのまま。ホーム画面のアイコンは入れ直し）

### 端末の中だけのデータと移し方

| データ | 移し方 |
| --- | --- |
| 名刺・メモ・手書き・録音・画像 | Vault（Drive 同期）から戻る。同期をオフで使っていた人のために、橋渡し版で「同期を済ませる」か既存のバックアップ ZIP を案内 |
| Google 連絡先との結び付け（`contactRawId`） | 端末ごとの値。連絡先の行に付けた印（MIME `vnd.jp.yaegaki.meishinote`＋名刺の id）から新しいアプリで結び直す。印は新しい名前に変え、古い印も読む |
| カレンダーの予定との結び付け | 同様に結び直すか、登録済みの予定は作り直さない（交換日で照合） |
| 設定（自動読み取り・連絡先の写真・登録先・ScanSnap のフォルダ・Drive のファイル改名の対応表など） | 橋渡し版で書き出し → 新しいアプリで読み込み |
| Gemini API キー | 書き出さない。ハブから受け取るか入れ直す |
| ウィジェット・通知・連絡先などの権限、Google の許可 | 新しいアプリで入れ直し（案内に書く） |

### 改名・ID 変更で直すところ

- `android/app/build.gradle`：applicationId・namespace。Java のパッケージ `jp.yaegaki.meishinote` → `app.thetahatch.meishi`（全ファイルとテスト、`android/tests/android`）
- `AndroidManifest.xml`：権限 `jp.yaegaki.theta.permission.SHARE` → `app.thetahatch.permission.SHARE`、action `jp.yaegaki.theta.HATCH` → `app.thetahatch.HATCH`、`<queries>` にハブ（`app.thetahatch.home`・`app.thetahatch.kidshome`）、`REQUEST_INSTALL_PACKAGES`・`UPDATE_PACKAGES_WITHOUT_USER_ACTION` を外す。ContentProvider の authority は `${applicationId}.theta` なので自動
- コードの文字列：連絡先の印の MIME（`Contacts.MARKER`）、ウィジェットの action（`jp.yaegaki.meishinote.SCAN`）、WebView の仮ホスト `app.meishinote.local`、書き出しのファイル名（`meishinote-…`）
- 更新：`UpdateCheck`（`repos/kiwiman0706-beep/MeishiApp`）→ 新しい名前、APK の選び方を `ThetaMeishiHatch-*.apk` に。`UpdateInstaller` は外して「ハブに頼む／Releases を開く」に
- `android/build.sh`：別名を `ANDROID_KEY_ALIAS` から、鍵のパスワードも `ANDROID_KEY_PASSWORD` から。出力名を `ThetaMeishiHatch-<版>.apk`
- `.github/workflows/release.yml`（4 つの Secret、APK 名）・`pages.yml`（コメントの URL・監視するパス）
- デスクトップ：`desktop/package.json` の `appId`（Windows では別のアプリとして入る → 古い方のアンインストールを案内）・`publish.repo`・`repository.url`、`desktop/main.js` の Releases の URL
- Web：`web/test/e2e.cjs` のパス（`/MeishiApp/`）、`WEB_SETUP.md` の URL
- README・docs（DRIVE_SETUP・WEB_SETUP・RELEASING・HANDOFF・TESTING）・`tools/make_hatch_kit.sh` のパスとリンク
- Google Cloud：`app.thetahatch.meishi` の Android 用クライアントは登録済み（APP_IDS.md）。アプリ内ガイドの表示値は自動（インストールされたアプリから読む）
- 個人名：上のほか、コード・画面・ID に `yaegaki`・`kiwiman` が残らないことを検索で確かめる（GitHub の URL の `kiwiman0706-beep` は除く）

### Windows・Mac

すでに Electron で動いている（Windows はインストーラーと自動更新、Mac は通知）。appId の変更で Windows は別アプリ扱いになるので、新しい版の初回に古い版の削除を案内する。

## 決めてほしいこと

決まったこと（2026-11-07）：NAS は後の版（今は Drive）／スキンは後の版／新しい版は 1.0.0／デスクトップの appId も `app.thetahatch.meishi`／移行は Home がまとめて行う（EXPORT・IMPORT）。


- [x] NAS：後の版（移行では Drive のまま）
- [x] スキン：後の版
- [x] 新しいアプリは 1.0.0
- [x] デスクトップの appId も変える（Windows は古い版を手で削除）

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照（1.0.0）
- [x] appid：アプリ ID を新しい ID に（1.0.0：`app.thetahatch.meishi`、Java のパッケージ・デスクトップの appId も）
- [x] signing：共通鍵の Secret で署名（0.19.0 から 4 つの Secret。CI で署名できることを確認）
- [x] update：更新をハブに頼む形に（1.0.0：インストール権限を外し、`app.thetahatch.action.UPDATE`、ハブが無ければ Releases）
- [x] settings：共通設定をハブから受け取る（1.0.0：`info` の `gemini.model`・`google.account` を取り込み・書き戻し、`secret/gemini.key`。スキンは後の版）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（Releases・更新の確認・Pages・ワークフロー・README・デスクトップの更新先）
- [ ] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] 橋渡し版 0.19.0 がアプリ内更新か Home で入り、Home の EXPORT で zip を受け取れる（確認の画面が出る）
- [ ] 新しい版が Home の IMPORT で読み込める。読み込み後に名刺・画像・連絡先とのつながり・設定が揃っている
- [ ] 新しいアプリで Vault から名刺・画像が戻り、Google 連絡先との結び付けが戻る
- [ ] Home（ハブ）から Meishi の更新ができる。ハブが無い端末では Releases が開く
- [ ] ハブの Gemini キー・スキン・Google アカウントを受け取れる
- [ ] Windows：新しい appId の版を入れたとき、古い版の削除の案内が出る
- [ ] Web：新しい URL で、Drive 同期・ログインが動く
