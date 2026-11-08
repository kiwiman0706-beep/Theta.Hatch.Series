# Theta Hatch シリーズ ADB 仕様 v0（構想）

> 正本はこのリポジトリ（kiwiman0706-beep/Theta.Hatch.Series の `spec/`）。2026-11-08 作成。まだ構想で、実装はこれから。

PC から ADB（USB または Wi-Fi）で、Android 端末のシリーズのアプリを**入れる・初期設定する・設定を変える・状態を見る・操作する**ための約束ごと。
最終的には、PC の Claude（ローカルの Claude Code）に「この端末をいつもの設定にしておいて」と頼めば済むようにする。

## 1. 全体の形

```
  PC                                                      Android 端末
 ┌─────────────────────────┐   adb（USB / Wi-Fi）   ┌──────────────────────────┐
 │ Theta Console Hatch（GUI）│ ─────────────────────▶ │ Home（ハブ）              │
 │        ↓ 使う             │   install / shell      │  └ 共通設定・更新・状態    │
 │ hatchctl（CLI、JSON で返す）│ ◀───────────────────── │ 各アプリ                  │
 │        ↑ 使う             │   dumpsys / broadcast  │  └ 状態・操作の窓口        │
 │ Claude（ローカル）         │                        └──────────────────────────┘
 └─────────────────────────┘
```

- **hatchctl**：PC で動く CLI。全部の操作をこれで行い、結果は JSON で返す。GUI も Claude もこれを使う（Claude が安全に「やっといて」できるのは、決まった操作だけを持つ CLI があるから）。
- **Theta Console Hatch**：hatchctl の画面版（Windows・Mac）。DeskHatch のドロワーにも置ける。新しいリポジトリ `Theta.Console.Hatch` で作る（予定）。
- **端末側の窓口**：各アプリが持つ「ADB の窓口」（§3）。ほとんどの設定は Home（設定のハブ）が預かるので、Home の窓口が中心。

## 2. つなぎ方

| | 手順 | 備考 |
| --- | --- | --- |
| USB | 端末の「開発者向けオプション」→「USB デバッグ」をオン → PC で `adb devices` → 端末で許可 | 初期設定はこちらが確実 |
| Wi-Fi（Android 11 以上） | 「ワイヤレス デバッグ」→「ペア設定コードによるペア設定」→ PC で `adb pair <IP:ポート> <コード>` → `adb connect <IP:ポート>` | 同じ LAN、または Tailscale の IP でも可 |
| 一度 USB でつないだ端末 | `adb tcpip 5555` → `adb connect <IP>:5555` | 再起動で切れる |

- hatchctl は `adb` を呼ぶだけ（PC に Android の platform-tools が要る。Windows は `winget install Google.PlatformTools`、Mac は `brew install android-platform-tools`）。
- **安全**：ADB でつながる PC は端末の全部を操作できる。使い終わったらワイヤレス デバッグを切る。子ども用の端末（KidsHome）は、設定が済んだら開発者向けオプションごと切る。

## 3. 端末側の窓口（各アプリ）

ADB のシェル（`shell` ユーザー）だけが使えるように、**権限 `android.permission.DUMP` で守る**（シェルは持っているが、普通のアプリは持てない）。

### 3.1 状態を見る：`dumpsys`

```
adb shell dumpsys activity service app.thetahatch.<名前>/app.thetahatch.adb.StatusService
```

- 各アプリは `StatusService`（`exported="true"`・`android:permission="android.permission.DUMP"`）を持ち、`dump()` で **1 行の JSON** を返す。
- 中身：`app`（catalog の id）・`packageName`・`versionName`・`versionCode`・`skin`・設定（**秘密は入れない**。入っているかどうかだけ `"gemini.key": true`）・同期（最後に同期した時刻・失敗の理由）・権限（足りないものの一覧）・エラー（直近 10 件）。
- Home はこれに加えて、ハブの情報：入っている Hatch アプリと版、新しい版、移行が要るアプリ、共通設定（`info` と同じ。秘密は有無だけ）。

### 3.2 操作する：ブロードキャスト

```
adb shell am broadcast -a app.thetahatch.adb.<命令> -n app.thetahatch.<名前>/app.thetahatch.adb.CommandReceiver [--es key 値 ...]
```

- 受け手 `CommandReceiver`（`exported="true"`・`android:permission="android.permission.DUMP"`）。結果は `setResultCode`（0＝成功）と `setResultData`（JSON）で返す（`am broadcast` がそのまま表示する）。

| 命令 | 引数 | すること |
| --- | --- | --- |
| `GET` | `key` | 設定を 1 つ返す（秘密は有無だけ） |
| `SET` | `key`・`value` | 設定を変える（Home では共通設定。ほかのアプリでは「このアプリだけ」の設定） |
| `SET_SECRET` | `key`・`file`（端末のファイルのパス） | 秘密を入れる。値は**コマンドに書かず**、`adb push` で一時ファイルに置き、読んだらアプリが消す（コマンド履歴やプロセス一覧に残さないため） |
| `SYNC` | — | すぐ同期する |
| `EXPORT` | `dir`（既定 `/sdcard/Download/ThetaHatch/`） | 移行と同じ書き出し（`docs/MIGRATION.md`）を、画面を出さずに作る |
| `IMPORT` | `file` | 書き出しを読み込む |
| `OPEN` | `screen`（`settings`・`guide` など） | 画面を開く |
| `CHECK_UPDATE` | — | Home のみ。新しい版を今すぐ確認 |
| `UPDATE` | `packageName`（省略で全部） | Home のみ。更新を入れる |

- 知らない命令は結果コード 1 と `{"error":"unknown command"}`。
- 窓口の処理は 10 秒以内に返す。長い処理（同期・更新）は受け付けたら返し、進み具合は `dumpsys` で見る。

### 3.3 Home（ハブ）がまとめて受け持つこと

- 共通設定（スキン・Gemini・NAS・Google アカウント）は Home の `SET`／`SET_SECRET` で入れる。ほかのアプリは Home から受け取る（`THETA_SHARED_SETTINGS.md` §4.0）。
- ほかのアプリの窓口は、そのアプリだけの設定と状態に絞る。

## 4. 入れる・初期設定（PC から）

### 4.1 入れる

1. `catalog/apps.json` を読み、各アプリの最新 Release の APK を取得（spec §6.1 の Release の条件を満たすもの）。SHA-256・パッケージ名・**シリーズ共通の鍵**を確かめる（`tools/check_apk.py` と同じ確認）。
2. `adb install -r -i app.thetahatch.home <APK>`
   - **`-i app.thetahatch.home` で「入れたのは Home」にしておく**。こうすると、あとで Home が確認なしで更新できる（Android 12 以上、spec §6.1）。
   - Home 自身は `-i` なしで入れる（最初の 1 本）。
3. 古い ID のアプリが残っていれば `adb uninstall <古い ID>`（`catalog/apps.json` の `previous.packageName`）。データの移行が要るアプリ（`migration.data` が `required`）は、先に `EXPORT`→ 新しい版で `IMPORT`。

### 4.2 初期設定（端末の許可）

| 許可 | adb のコマンド |
| --- | --- |
| 既定のホームアプリ | `adb shell cmd role add-role-holder android.app.role.HOME app.thetahatch.home`（KidsHome の端末なら kidshome） |
| ほかのアプリを入れる（Home） | `adb shell appops set app.thetahatch.home REQUEST_INSTALL_PACKAGES allow` |
| 実行時の権限（カメラ・マイク・位置・通知など） | `adb shell pm grant <パッケージ> android.permission.<名前>` |
| 使用状況へのアクセス | `adb shell appops set <パッケージ> GET_USAGE_STATS allow` |
| 通知へのアクセス | `adb shell cmd notification allow_listener <パッケージ>/<サービス>` |
| 電池の最適化から外す | `adb shell cmd deviceidle whitelist +<パッケージ>` |
| 全ファイルへのアクセス | `adb shell appops set <パッケージ> MANAGE_EXTERNAL_STORAGE allow` |

- **各アプリは、要る許可を `catalog/apps.json` の `adbSetup` に書く**（例：`{"grant": ["android.permission.CAMERA"], "appops": ["GET_USAGE_STATS"], "role": "HOME"}`）。hatchctl はこれを見て、まとめて許可する。
- Android や端末メーカーによって効かないものがある（その場合は hatchctl が「端末で手で許可してください」と画面を開く）。

### 4.3 設定を入れる

- 「いつもの設定」を PC の 1 つのファイル（`hatch-profile.json`）に持つ：スキン・Gemini のモデル・NAS の接続先・Google アカウント・入れるアプリの一覧・アプリごとの設定。**秘密は書かず**、1Password の参照（`op://…`）で書く。
- `hatchctl apply hatch-profile.json --device <端末>` で、入れる → 許可 → 設定 → 秘密（1Password から読んで `SET_SECRET`）まで一度に行う。
- Google アカウントのログインは ADB ではできない（Google の許可画面は人が押す）。hatchctl は最後に「Google の許可が要るアプリ」の一覧と、その画面を開くボタン（`OPEN guide`）を出す。

## 5. hatchctl（PC の CLI）

| コマンド | すること |
| --- | --- |
| `hatchctl devices` | つながっている端末と、入っている Hatch アプリ・版 |
| `hatchctl status [--app <id>]` | `dumpsys` の JSON をまとめて表示 |
| `hatchctl install <id>… / --all` | Release から取得・確認して入れる（§4.1） |
| `hatchctl update` | 新しい版がある物を入れる |
| `hatchctl setup` | 端末の許可（§4.2） |
| `hatchctl get / set <key> <value>` | 設定（Home の共通設定、`--app` でアプリごと） |
| `hatchctl secret <key> --from op://…` | 秘密を 1Password から読んで入れる |
| `hatchctl apply <profile>` | いつもの設定を丸ごと（§4.3） |
| `hatchctl export / import` | 書き出し・読み込み（PC に保存） |
| `hatchctl screenshot` | 画面を撮って PC に保存（`adb exec-out screencap -p`） |
| `hatchctl logs [--app <id>]` | `adb logcat` をシリーズのタグ（`ThetaHatch`）で絞って表示 |

- どのコマンドも `--json` で機械が読める形を返す。**秘密の値は出力しない**。
- 書き換える操作（install・set・secret・apply）は、`--dry-run` で何をするかだけを先に出せる。

## 6. Claude（ローカル）に「やっといて」

- `Theta.Console.Hatch` のリポジトリに、Claude 向けの手順（`CLAUDE.md`、またはスキル）を置く：「端末の状態は `hatchctl status --json`、変える前に `--dry-run` で見せて確認を取る、秘密は 1Password の参照で渡し値を表示しない」。
- 例：「Fold5 を いつもの設定にして」→ Claude が `hatchctl devices` で端末を見つけ、`hatchctl apply --dry-run` の結果を見せ、OK をもらってから実行し、最後に `hatchctl status` で確かめて報告。
- 将来は hatchctl を MCP サーバーにもできる（Claude Desktop・Claude Code からツールとして呼べる）。

## 7. 進め方（案）

1. **Home**：`StatusService`・`CommandReceiver`（§3）を入れる。共通設定の `SET`／`SET_SECRET`、`CHECK_UPDATE`／`UPDATE`。
2. **hatchctl**：まず `devices`・`status`・`install`・`setup` から（新しいリポジトリ `Theta.Console.Hatch`、Python 3.12）。
3. **catalog**：各アプリの `adbSetup`（要る許可）を足す。
4. **各アプリ**：`StatusService`・`CommandReceiver` を入れる（状態と、そのアプリだけの設定）。
5. **GUI**（Theta Console Hatch）と、Claude 向けの手順。
