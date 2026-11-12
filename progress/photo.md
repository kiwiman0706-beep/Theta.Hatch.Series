# Theta Photo Hatch（photo）の移行メモ

- 更新：2026-11-12
- スレッド：https://claude.ai/code/session_012DXkby1gTG6FFj5k36BF48
- 状態：計画OK待ち

## 今と目標

| | 今（0.1.0、ブランチ `claude/laughing-galileo-hsri6y`） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Photo.Hatch`（ブランチは作業ブランチだけ。`main`・Release・タグ無し） | 同じ（改名なし）。`main` を作って既定ブランチに |
| アプリ ID | `photo.theta.theta_photo_hatch`（Kotlin の package も同じ）。表示名「Photo Hatch」 | `app.thetahatch.photo`、表示名「Theta Photo Hatch」 |
| 署名 | デバッグ鍵（`flutter build apk` の既定。0.1.0 はスレッドから直接渡した APK） | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS`）。`release.yml` で `ThetaPhotoHatch-<版>.apk` を 1 つ |
| 更新 | 仕組み無し。インストール権限も無い | ハブに頼む（`app.thetahatch.action.UPDATE`、無ければ Releases を開く）。設定に「今の版」「更新を確認」 |
| 共通設定 | 無し（スキンも NAS もまだ無い） | ハブの `info`（`ui.skin`・`nas.url`・`nas.user`・`nas.shareRoot`・`google.account`）と `secret/nas.password`・`secret/nas.deviceToken`（承認つき）。ハブが無ければこのアプリで入力 |
| データの置き場所 | 写真は端末の `Pictures/Hatch_*`（Amazon フォト・Synology Photos のバックアップに任せる）。分類・イベント・☆・キーワードは XMP（JPEG は埋め込み、ほかは `.xmp`）。仕分けの記録（元に戻す用）と設定は端末内 | 写真は NAS の `photo`・各自の `Photos`（ライブラリ規則 §5）。XMP はそのまま。イベントの索引だけ Theta Vault の `Photo/`（`theta: photo/event@1`、`Photo/イベント.base`）。NAS は Tailscale ＋ File Station API、Secure SignIn に対応 |
| 対応 OS | Android 11 以降 | Android＋Windows・Mac（Flutter のデスクトップ版。カメラ・GoPro の SD カードの仕分けとアップ） |
| スキン | 無し（Material 3 のオレンジ） | `ui.skin` の 11 種（`skins.json` から Flutter のテーマを作る） |

## 方針

### 移行の順番

1. 橋渡し版は作らない（端末内だけのデータが小さく、0.1.0 はデバッグ鍵なので橋渡し版を同じ鍵で作れない）
2. 新しい版（新しい ID・共通鍵・ハブに頼む更新・共通設定・スキン）＝最初の Release
3. その後の版で機能を足す：USB 取り込み、Wi-Fi で NAS へアップ、THETA の 360° 写真、Camera Hatch との連携、Vault の索引、Windows・Mac 版

### 改名・ID 変更で直すところ

- `app/android/app/build.gradle.kts`：`namespace`・`applicationId` → `app.thetahatch.photo`
- Kotlin のフォルダ `photo/theta/theta_photo_hatch` → `app/thetahatch/photo`（`MainActivity.kt` の package）
- `AndroidManifest.xml`：表示名 → `Theta Photo Hatch`、`<queries>` にハブ 2 つ（`app.thetahatch.home`・`app.thetahatch.kidshome`）と `app.thetahatch.camera`
- macOS：`AppInfo.xcconfig` の `PRODUCT_BUNDLE_IDENTIFIER`（`photo.theta.thetaPhotoHatch`）・`PRODUCT_NAME`・著作権表示、`project.pbxproj` のテスト用 ID
- Windows：`Runner.rc` の CompanyName・ProductName など（`photo.theta`）、`CMakeLists.txt` の `BINARY_NAME`
- XMP の独自の名前空間 `http://ns.theta.photo/hatch/1.0/`（ドメイン風の名前が古い ID 由来）→ シリーズの名前に。0.1.0 で書いた XMP は読めるように両方を読む
- ワークフロー：`build-apk.yml`（デバッグ鍵・Artifacts）→ `release.yml`（Secret 4 つ、`main` への push で `v<版>` のタグと Release）。`tools/check_apk.py` で確かめる
- README・`docs/flow.md` のリンク・ビルド手順。Releases の URL `https://github.com/kiwiman0706-beep/Theta.Photo.Hatch/releases/latest`
- 変えないもの：Dart のパッケージ名 `theta_photo_hatch`、MethodChannel `hatch/native`（アプリの中だけ）、仕分け先フォルダ名 `Pictures/Hatch_*`（Amazon フォト・Synology の設定が変わるため）
- ContentProvider・FileProvider は今は無い（`/shelf`・共通設定を読むために足す）

### 端末の中にしか無いデータ

| もの | 移し方 |
| --- | --- |
| 写真そのもの（`Pictures/Hatch_*`）と XMP | 移行不要（アプリを消しても端末に残る。XMP はファイルの中か隣） |
| 分類（仕分け先フォルダ）・未処理として見るフォルダ・最近のキーワード／イベント | 0.1.0 は書き出しが無いので入れ直し（既定の 4 分類なら何もしなくてよい）。新しい版に設定の書き出し・読み込みを付ける |
| 仕分けの記録（`journal.jsonl`、元に戻す用） | 移さない（入れ直すと「元に戻す」が使えなくなるだけ） |

### 追加の要望（2026-11-12）

- **USB 取り込み（出先）**：USB-C で、デジカメ・GoPro・THETA（MTP／PTP）と SD カードリーダー（USB ストレージ）から取り込んで仕分ける。取り込みは端末の `Pictures/Hatch_Inbox/<機器>/` へコピー（元は消さない、取り込み済みはハッシュで飛ばす）
- **Wi-Fi で NAS へアップ**：Tailscale 経由で File Station API に、Wi-Fi のときだけ（WorkManager）。アップ後に NAS 側の大きさ・ハッシュを確かめてから端末から消す（Synology Photos のバックアップに任せる今の流れとどちらかを選べる）
- **THETA の 360° 写真**：GPano（`ProjectionType=equirectangular`）を見分けて 360° ビューアで表示。360° 動画も。THETA 本体から Wi-Fi で取り込む（THETA Web API）のは後の版
- **Camera Hatch との連携**：`DCIM/ThetaCamera/<フォルダ>/` を未処理に入れる。`Documents/ThetaCamera/<フォルダ>/` の `.theta.json`・`.xmp`（イベント・☆・タグ・コメント）を読んで仕分けの初期値に。動かすときはサイドカーも一緒に動かし、名前を合わせる。ビューアは HEIF の clap（表示範囲）に従って切って見せる（Samsung ギャラリー・Google フォトは正しく切らないため）
- **一体化**：カメラと仕分けは別アプリのまま、メタデータ形式（`theta.capture/1` と XMP）を共通にし、Camera のギャラリーを Photo のビューアに任せる案（決めてほしいこと）

### Windows・Mac

- Flutter のデスクトップ版で可能（`windows/`・`macos/` は作成済み、未ビルド）。SD カード・NAS のネットワークドライブを直接読み書き。USB の MTP（GoPro を直接つなぐ）は Windows のみ見込みあり、Mac は SD カードリーダー経由
- シリーズの「UI は HTML/CSS/JS を共有」とは違う（Music と同じく Flutter の UI を全 OS で共有）

## 決めてほしいこと

- [ ] Photo と Camera を一体化するか（提案：別アプリのまま、Camera のギャラリーを Photo に任せる）
- [ ] Camera の写真を Photo が動かしてよいか（動かすと Camera のギャラリー・索引から見えなくなる。Camera 側にも読み戻しが要る）
- [ ] 端末から消す役：Synology Photos の「空き容量を確保」のままか、Photo が NAS へ上げて確かめてから消すか
- [ ] UI は Flutter のままでよいか（シリーズの HTML 共有 UI にしない）
- [ ] XMP の独自名前空間の新しい名前（案：`https://thetahatch.app/ns/photo/1.0/`）

## 進み具合

- [ ] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [ ] appid：アプリ ID を新しい ID に
- [ ] signing：共通鍵の Secret で署名
- [ ] update：更新をハブに頼む形に（ハブはハブ機能）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [ ] rename：改名後の名前に合わせて URL・リンクを直した
- [ ] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] 0.1.0 をアンインストールして新しい版を入れ、仕分け済みの写真と XMP が残っていること
- [ ] ハブ（Home・KidsHome）の Hatch ドロワーに出て、更新できるか
- [ ] Amazon フォト・Synology Photos のフォルダ選択で `Hatch_*` を選べるか
- [ ] USB：GoPro・THETA・デジカメ・SD カードリーダーが見えるか（機種ごと）
- [ ] Camera Hatch の HEIF（clap）が正しい範囲で表示されるか
