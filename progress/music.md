# Theta Music Hatch（music）の移行メモ

- 更新：2026-11-12
- スレッド：https://claude.ai/code/session_012DXkc2Wd5iBmicj8ba39vG
- 状態：計画OK待ち（棚 `/shelf` はコード済み：`1fc66d6`。Home から読めるのは新 ID・共通鍵の版から）

## 今と目標

| | 今（1.0.0+1、ブランチ `claude/exciting-allen-w4q8gm`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Music.Hatch`（既定ブランチが作業ブランチ。`main` が無い。Release・タグも無い） | 同じ（改名なし）。`main` を作り、既定ブランチを `main` に |
| アプリ ID | `com.thetahatch.theta_music`（Kotlin のパッケージも同じ） | `app.thetahatch.music`（Kotlin も `app.thetahatch.music`） |
| 署名 | `android/key.properties`（Git 管理外）があればその鍵、無ければデバッグ鍵。CI（`build-apk.yml`）はデバッグ鍵で Artifacts に置くだけ | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS`）。`release.yml` で `ThetaMusicHatch-<版>.apk` を Release に |
| 更新 | 仕組み無し（APK を手で入れ直し）。インストール権限も無い | ハブに頼む（`app.thetahatch.action.UPDATE`、無ければ Releases を開く）。設定に「今の版」「更新を確認」 |
| 共通設定 | 全部このアプリで入力（WebDAV／DSM の URL・ユーザー・パスワード・2 段階認証のデバイストークン、スキン） | ハブの `info`（`ui.skin`・`nas.url`・`nas.user`・`nas.shareRoot`）と `secret/nas.password`・`secret/nas.deviceToken`（承認つき）を読む。ハブが無ければ今までどおり |
| データの置き場所 | 曲は NAS の `music`（WebDAV か Audio Station で直接読む）。ノートは利用者が指定した NAS のフォルダに Obsidian 形式で書き出し（Dataview）。ライブラリの索引・お気に入り（アルバム・アーティスト・WebDAV の曲）は端末内。DS audio の曲のお気に入りは Audio Station の★評価 | 曲は今のまま（Vault に入れない）。ノートは NAS の Theta Vault（`Obsidian/Theta Vault/Music/`）に `theta: music/album@1`・`id` 付きで、`Music/アルバム.base` を置く。お気に入りもノートに持たせ、Vault から戻せるように |
| 対応 OS | Android | Android。Windows・Mac は Flutter のデスクトップ版で可能（下の方針） |
| スキン | iPod（クリックホイール）と Theta（HUD：dark・light・pop・alert・scifi・system） | Theta スキンを `ui.skin` の 11 種（term・braun・soft・window・lcd を追加、色は `skins.json`）に。iPod はこのアプリ独自の見た目として残す（決めてほしいこと） |

## 方針

### 移行の順番

1. 橋渡し版は作らない（catalog の決定どおり Music はデータ移行なし。端末だけのデータは下の表のとおり小さい）
2. 新しい版（`app.thetahatch.music`・共通鍵・ハブに頼む更新・共通設定・Theta Vault への書き出し）＝初めての Release
3. Windows・Mac 版は次の版から（Flutter のデスクトップビルド）

### 改名・ID 変更で直すところ

- `android/app/build.gradle.kts`：applicationId・namespace。Kotlin のフォルダ `com/thetahatch/theta_music` → `app/thetahatch/music`（`MainActivity.kt` の package）
- Manifest：表示名 `Theta Music` → `Theta Music Hatch`、`<queries>` にハブ 2 つ（`app.thetahatch.home`・`app.thetahatch.kidshome`）。ContentProvider・FileProvider は今は無い
- `lib/main.dart`：通知チャンネル ID `com.thetahatch.theta_music.playback` → `app.thetahatch.music.playback`
- MethodChannel 名 `theta_music/voice`・`theta_music/click` と Dart のパッケージ名 `theta_music`（`pubspec.yaml`・テストの import）はアプリの中だけなので変えない（変えても可）
- ワークフロー：`build-apk.yml`（デバッグ鍵・Artifacts）→ `release.yml`（Secret 4 つ、`main` への push で `v<版>` のタグと Release、APK は 1 つ）。`tools/check_apk.py` で確認
- README：署名の説明（`key.properties`）、ビルド手順、Release・自動更新、共通設定の説明
- 既定ブランチ：`main` を作る（Release は `main` への push で動かす）
- Releases の URL：`https://github.com/kiwiman0706-beep/Theta.Music.Hatch/releases/latest`（改名なしなので変わらない）
- Google Cloud：新 ID の Android クライアントは登録済み（2026-11-06）。今は Google 連携を使っていない

### 端末の中にしか無いデータ

| もの | 移し方 |
| --- | --- |
| 接続設定（WebDAV／DSM の URL・ユーザー・パスワード・デバイストークン） | ハブから受け取る。ハブが無ければ入れ直し（パスワードは書き出さない） |
| ライブラリの索引（`library.json`）・ジャケットのキャッシュ | 移さない（NAS からもう一度スキャン・取得すれば同じものができる） |
| お気に入り（アルバム・アーティスト、WebDAV の曲） | 移行版で Vault のノート（`favorite: true`）から戻せるようにする。今の版から入れ替える分は、書き出し済みならノートから戻る。数が少なければ付け直し |
| お気に入り（DS audio の曲） | NAS の★評価なので移行不要 |
| 見た目・再生の設定（スキン・クリック音・シャッフルなど） | 入れ直し（数項目）。スキンはハブの `ui.skin` |

### Home の棚（`/shelf`、spec §4.2）— コード済み（2026-11-12、`1fc66d6`）

- `ShelfProvider`（authority `${applicationId}.theta`、読み書きとも権限 `app.thetahatch.permission.SHARE`）。`query /shelf` で 1 行 1 つ：
  - `favorites`「お気に入り」：お気に入りの曲（1 枚にまとめる）・アルバム・アーティスト
  - `recent`「最近再生」：最近再生したアルバム（新しい順、最大 20）
  - 合わせて 30 件まで。`text`・`color` は空。プレイリストはアプリに無いので出さない
- `image`：`content://<id>.theta/art/<md5>.img`（同じプロバイダの `openFile`、`r` だけ）
- `action`：`MainActivity` 宛ての `Intent`（action `app.thetahatch.music.PLAY`、extra `kind`＝album／artist／favsongs・`key`）を `toUri(URI_INTENT_SCHEME)`。押すと再生して Now Playing を出す
- 中身は Dart が `files/shelf/shelf.json` とジャケットに書くので、アプリが動いていなくても返せる。変わったら `notifyChange(content://<id>.theta/shelf)`
- 何を出すかは設定で選べる（お気に入り・最近再生、それぞれオン・オフ）
- 権限 `app.thetahatch.permission.SHARE` の**定義**は、本番の鍵で署名するときだけマニフェストに入れる（`src/series/`）。デバッグ鍵の APK に入れると、同じ権限を定義している Home（共通鍵）とぶつかって入らないため。今の ID のままだと authority は `com.thetahatch.theta_music.theta` なので、Home の棚に出るのは新 ID・共通鍵の版から

### Windows・Mac

- Flutter のデスクトップ版（Windows・macOS）でビルドできる見込み。WebDAV・Audio Station・スキャン・Vault への書き出しはそのまま動く
- 端末ごとに作り直す所：バックグラウンド再生（`just_audio_background` は Android のみ → デスクトップは不要か別の仕組み）、音声検索（Android の音声入力 → デスクトップは文字検索のみ）、クリック音（SoundPool → 音声ファイルで代用）
- シリーズの §4（共通 Web UI＋Electron）とは作りが違う。Web（PWA）版は、ブラウザから自宅 NAS（http・別オリジン）へは混在コンテンツと CORS で直接つなげないため難しい

## 決めてほしいこと

- [ ] iPod のクリックホイールの見た目を、このアプリ独自のスキンとして残すか（`ui.skin` は Theta スキン側に当てる案）
- [ ] Theta スキンを 11 種に増やすか（今は 6 種。増やすなら term・braun・soft・window・lcd は色と主な作り）
- [ ] ハブから NAS を受け取ったときの接続方式：DS audio（`nas.url` は DSM の URL なのでそのまま使える）を既定にするか、WebDAV も選べるようにするか
- [ ] Obsidian の書き出し先：NAS の Theta Vault（`Obsidian/Theta Vault/Music/`）に固定でよいか。Google ドライブの Theta Vault にも書くか（音楽は NAS にあるので NAS のみを提案）
- [ ] 書き出しのノートの形：Dataview のクエリをやめて `.base`（Obsidian Bases）に変えてよいか
- [ ] 最初の Release の版番号（今 `pubspec.yaml` は 1.0.0。0.x から始めるなら変える）
- [ ] Windows・Mac 版を次の版でよいか

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [ ] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [ ] appid：アプリ ID を新しい ID に
- [ ] signing：共通鍵の Secret で署名
- [ ] update：更新をハブに頼む形に（ハブはハブ機能）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [ ] rename：改名後の名前に合わせて URL・リンクを直した
- [x] shelf：Home の棚（`/shelf`）に対応（コード済み。効くのは新 ID・共通鍵の版から）
- [ ] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] 共通鍵の APK が入る（古いアプリはアンインストールしてから）
- [ ] ハブ（Home）から NAS の設定・パスワード・デバイストークンを受け取れる（デバイストークンの使い回しは Synology 次第で未確認）
- [ ] 「更新する」でハブの更新画面が開く／ハブが無ければ Releases が開く
- [ ] Theta Vault への書き出しと、ノートからのお気に入りの復元
- [ ] 再生・バックグラウンド再生・音声検索・クリック音（いずれも実機未確認）
- [ ] Home の棚にお気に入り・最近再生のジャケットが並び、押すと再生する（実機未確認）
