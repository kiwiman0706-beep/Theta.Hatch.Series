# Theta Movie Hatch（movie）の移行メモ

<!-- このアプリのスレッドが書く。ほかのアプリのファイルは触らない -->

- 更新：2026-11-17
- スレッド：https://claude.ai/code/session_012DXkbxgRpZwVsU9fra6sF1
- 状態：実機確認待ち（0.1.0 を Releases に公開：v0.1.0、check_apk.py で確認済み）

## 今と目標

| | 今 | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Movie.Hatch`（中身は `docs/naming-convention.md`・`server/jellyfin/` だけ。アプリはまだ無い） | 同じ（改名なし） |
| アプリ ID | 無し | `app.thetahatch.movie`（最初から） |
| 署名 | 無し | 共通鍵（Secret の 4 つ、別名は `ANDROID_KEY_ALIAS`）。最初の Release から |
| 更新 | 無し | ハブに頼む（`REQUEST_INSTALL_PACKAGES` なし。ハブが無ければ Releases を開く）。`release.yml` で `ThetaMovieHatch-<版>.apk` |
| 共通設定 | 無し | ハブの `info`（`ui.skin`・`nas.url`・`nas.user`・`nas.shareRoot`・`gemini.model`）と `secret/nas.password`・`secret/nas.deviceToken`・`secret/gemini.key`（承認つき）。ハブが無ければアプリで入力 |
| データの置き場所 | — | 動画は NAS の `video` に置いたまま（`THETA_LIBRARY_SPEC.md` §3）。作品・人物・視聴の記録は NAS の Theta Vault `Obsidian/Theta Vault/Movie/`（`theta: movie/title@1`・`movie/person@1`・`id`、`Movie/作品.base`）。オフラインのキャッシュは端末の中だけ |
| 対応 OS | — | Android → Android TV（同じ APK）→ Windows・Mac（Flutter のデスクトップ版）→ webOS（Web 版、LAN の中だけ） |
| スキン | — | シリーズの 11 種（`skins.json` から）。TV の既定は dark |

## 方針

### 作り

- **Flutter＋mpv（`media_kit`）**。mkv・HEVC・DTS・ARIB 字幕・二か国語の .ts を端末でそのまま再生（ダイレクト再生）するため、WebView の video では足りない。Music と同じく spec §4（共通 Web UI＋Electron）の例外
- NAS（DS1825+）は内蔵 GPU が無く変換が弱いので、**変換しないのが前提**。外では「家の Wi-Fi で先にダウンロード（オフラインのキャッシュ）」と「事前に作った軽い版」で補う
- 動画の読み方：NAS の `video` を直接読む（DSM の File Station API＝Secure SignIn の確認コード・デバイストークンに対応、または WebDAV）。作品の情報は `.nfo`・`poster.jpg`（ファイル名規則）と Vault のノートから。**Jellyfin は無くても動く**が、あれば公式アプリ・webOS 用に並べて使える（決めてほしいこと）
- 視聴の記録：見終わったかどうかは作品のノート、再生位置は `Movie/_state/<端末>.json`（端末ごとのファイルにして同期の衝突を避ける。読むときは全端末分の新しい方）
- Home の棚（`/shelf`）：「続きから見る」「最近追加」。TV のホームの「続きから」にも使う
- メタデータ取得・名前の整理（TMDB・Annict・しょぼいカレンダー・Wikipedia＋Gemini、変更案 CSV → 確認 → 実行 → 記録）は PC の Python ツール（`tools/`）。`THETA_LIBRARY_SPEC.md` §7 の約束どおり
- Video Station の旧データ（PostgreSQL の `video_metadata`）は PC ツールで Vault のノートと `.nfo` に移す（まず書き出してバックアップ）

### 改名・ID 変更で影響を受ける所

- 無し（新しいアプリで、最初から `app.thetahatch.movie`・`Theta.Movie.Hatch`）
- 注意：`spec/THETA_LIBRARY_SPEC.md` が `docs/naming-convention.md` を参照しているので、**このファイルの場所は変えない**

### 端末の中にしか無いデータ

- まだ無い（アプリが無い）。作るときも、正本は NAS（動画・`.nfo`）と Vault（ノート・視聴の記録）にして、端末に残るのはキャッシュ（作り直せる索引・ポスター・ダウンロードした動画）と秘密だけにする → 入れ直しで移すものは無い

### Windows・Mac

- Flutter のデスクトップ版と `media_kit` で、Android と同じコードで動く見込み。オフラインのキャッシュも同じ仕組み
- webOS は Flutter が動かないので Web 版を別に作る。再生はテレビの video なので、対応していない形式は Jellyfin の変換（HLS）か事前の軽い版が要る。最後に回す

## シリーズへの依頼（このリポジトリのスレッドへ）

- [x] `catalog/apps.json` の movie（2026-11-17 済み）：`platforms` に `android`、`autoUpdate` を true、`vault` は false のまま、`remark` を「Flutter＋mpv。NAS を直接読む（File Station・WebDAV）。Jellyfin は並べて使う」に（Home がハブとして一覧に出し、更新できるように）
- [x] `tools/repos.txt` に `Theta.Movie.Hatch` を足して、Secret 4 つを配る（2026-11-17 済み）

## 決めてほしいこと

- [x] この計画で進める。小分けに出す（0.1.0：一覧・再生・続きから → オフライン → Vault → Video Station の移行・整理ツール → TV → Win・Mac）（2026-11-17）
- [x] Jellyfin：並べて入れる（公式アプリ・webOS 用）。Movie は NAS を直接読む（2026-11-17）
- [x] 再生エンジン：mpv（`media_kit`）（2026-11-17）
- [x] NAS の読み方：File Station API（既定・2 段階認証）と WebDAV の両方を選べる（2026-11-17）
- [x] 劇場版：標準の置き方（映画フォルダに独立、`<set>` でつなぐ）。アニメ映画は `アニメ映画/` に分ける。アニメの期はシーズン（2026-11-17、`docs/naming-convention.md` v0.2）
- [x] `video` は暗号化していない（2026-11-17）
- [x] Video Station の書き出しはローカルの Claude に任せる（依頼文：`docs/PROMPT_VIDEOSTATION_BACKUP.md`）（2026-11-17）
- [x] このリポジトリに Secret 4 つを登録（2026-11-17、`tools/repos.txt` にも追加済み）
- [ ] 既定ブランチを `main` にするか（今は `ccr-59e6bcc5-seucnb`。`release.yml` は両方で動く）

## 進み具合

<!-- 移行ボードの手順と同じ名前。済んだら [x]。確認スクリプトがこの行を読む -->
- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に（最初から `app.thetahatch.movie`）
- [x] signing：共通鍵の Secret で署名（v0.1.0 の APK：署名 v2/v3、SHA-1 `A1:13:EA:…:28:BA`）
- [x] update：更新をハブに頼む形に（ハブはハブ機能）（インストール権限なし、`app.thetahatch.action.UPDATE`、無ければ Releases）
- [x] settings：共通設定をハブから受け取る（ハブは配る側）（`ui.skin` に追従、NAS の URL・ユーザー・パスワード・デバイストークン）
- [x] rename：改名後の名前に合わせて URL・リンクを直した（改名なし）
- [x] release：新しい版を Releases に出した（v0.1.0、`ThetaMovieHatch-0.1.0.apk` 61MB・ARM だけ、`REQUEST_INSTALL_PACKAGES` なし）

## 実機で確かめること

- [ ] Tailscale 経由で 10 分以上止まらずに再生できる（Video Station の裏技で止まっていた症状）
- [ ] mkv（HEVC 10bit）・.ts（ARIB 字幕・二か国語）・DTS が端末で再生できる
- [ ] Secure SignIn の確認コード → デバイストークンで次から省ける。ハブから借りたトークンが使えるか
- [ ] Android TV でリモコンだけで操作できる
