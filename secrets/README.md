# 共通の鍵（署名鍵・Secret）

**このフォルダに鍵そのものは入れません。** ここに書くのは「どの鍵を、どの名前で、どこに置くか」だけです。
（Git に一度入れた鍵は履歴から消しにくく、clone した端末・Claude のスレッドすべてに広がります。`.gitignore` で `*.jks` などを弾いています。）

## 1. 仕組み

GitHub Actions の Secret は **リポジトリごと** です。あるリポジトリのワークフローから、別のリポジトリ（このリポジトリ）の Secret は読めません。個人アカウントには「全リポジトリ共通の Secret」もありません（Organization にはある）。

そこで、**値は手元の 1 か所だけに置き、同じ値を各リポジトリへスクリプトで配る**ことにします。

```
手元（PC）の鍵ファイル ──tools/sync-secrets──▶ 各アプリのリポジトリの Secret（同じ名前・同じ値）
                                                   └─ release.yml が Secret で APK に署名
```

- 鍵を 1 つにすれば、**全アプリの SHA-1 が同じ**になります（Google Cloud の Android 用 OAuth クライアントに入れる値が全部同じ）。
- 新しいアプリを作ったら `tools/repos.txt` に 1 行足して、スクリプトをもう一度実行するだけ。

> 別の方法：無料の GitHub Organization を作ってリポジトリを移すと、Organization の Secret を全リポジトリで共有できます。ただしリポジトリの URL が変わり、アプリの自動更新（Release を見に行く URL）に影響するので、今はおすすめしません。

## 2. シリーズの署名鍵（Android）

| 項目 | 値 |
| --- | --- |
| 鍵 | Meishi の鍵 `meishiclaude-release.jks`（すでに Meishi・Memo が使っている。仕様 `spec/THETA_GOOGLE_SETUP.md` で「シリーズ共通」と決めたもの） |
| 別名（alias） | `meishiclaude` |
| SHA-1 | `A1:13:EA:34:83:60:56:32:E7:F5:94:4E:4E:8C:20:55:DD:AE:28:BA` |
| パスワード | Meishi のときに一緒に渡された `keystore-password.txt` の中身 |
| 置き場所（正本） | 自分の PC／パスワード管理。**Google ドライブの Theta Vault や Git には置かない** |

> **GitHub の Secret からは取り出せません**（登録した値は誰にも読めない）。`meishiclaude-release.jks` と `keystore-password.txt` が手元に無ければ、下の「新しく作る場合」で作ります。
> 全アプリがアプリ ID の変更で一度入れ直しになるので、**今なら新しい鍵にしても失うものはほぼありません**（Meishi も ID が変わるため）。ただし Google Cloud に古い SHA-1 で登録済みなら、登録し直しになります。
> 一度決めたら**鍵は作り直さない**。作り直すと全アプリの OAuth クライアントの SHA-1 を直すことになります。

### 新しく作る場合

Android Studio に付いている `keytool` を使います（Windows の PowerShell）。

```powershell
& "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" -genkeypair -v `
  -keystore theta-hatch-release.jks -alias thetahatch -keyalg RSA -keysize 4096 -validity 36500 `
  -dname "CN=Theta Hatch"
# SHA-1 を確かめる（Google Cloud に登録する値）
& "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" -list -v -keystore theta-hatch-release.jks -alias thetahatch
```

Mac は `keytool`（Android Studio を入れていれば `/Applications/Android Studio.app/Contents/jbr/Contents/Home/bin/keytool`）で同じ指定。
作ったら、上の表の鍵・別名・SHA-1 をこの README に書き換え、`ANDROID_KEY_ALIAS` は `thetahatch` で配ります（`sync-secrets` の `-Alias thetahatch`）。

### Secret の名前（全アプリ共通）

| Secret | 中身 |
| --- | --- |
| `ANDROID_KEYSTORE_B64` | 鍵ファイル（.jks）を Base64 にしたもの |
| `ANDROID_KEYSTORE_PASSWORD` | 鍵ストアのパスワード |
| `ANDROID_KEY_ALIAS` | `meishiclaude` |
| `ANDROID_KEY_PASSWORD` | 鍵のパスワード（鍵ストアと同じなら同じ値） |

各アプリの `release.yml` はこの 4 つを読むように揃えます（Meishi・Memo・Mensetsu はすでにこの名前）。

## 3. いまの各アプリの署名（2026-10-26 時点）

| アプリ | applicationId | いまの署名 | 共通鍵へ |
| --- | --- | --- | --- |
| Meishi | `jp.yaegaki.meishiclaude` | 共通鍵（Secret） | ✔ 済み |
| Memo | `jp.yaegaki.theta.memo` | 共通鍵（Secret、Meishi と同じ） | ✔ 済み |
| Mensetsu | `jp.yaegaki.theta.mensetsu` | Secret があれば共通名の Secret、無ければ**リポジトリ内の開発用鍵** `android/signing/mensetsu-dev.jks` | Secret を入れる |
| Home | `jp.yaegaki.theta.home` | `HOME_KEYSTORE` などの環境変数 | 変数名を揃える |
| KidsHome | `com.theta.kidshome` | **リポジトリ内の鍵** `app/kidshome.jks`（パスワードも build.gradle に記載、公開リポジトリ） | 要切り替え（下の注意） |
| Oekaki | `jp.theta.oekakihatch` | `OEKAKI_*` の環境変数（引き継ぎ用の鍵） | 変数名を揃える |
| Travel | `jp.theta.travelhatch` | `TRAVEL_*` の環境変数 | 変数名を揃える |
| Item | `jp.omoide.closet` | `OMOIDE_*` の環境変数（個人の鍵） | 変数名を揃える |
| Device | `jp.yaegaki.equipment` | `release-signing.jks`（ローカルにあれば） | 変数名を揃える |
| DoorPhoto・Label・Kamigata | `jp.yaegaki.omoide`・`jp.yaegaki.tepravoice`・`jp.yaegaki.kururihair` | 個別（ソースが archives 内で未確認） | 確認して揃える |
| Book（dsbooks） | `jp.shinwakai.dsbooks.preview` | 未確認（非公開リポジトリ） | 確認して揃える |
| Music | `com.thetahatch.theta_music` | `android/key.properties` があればその鍵、無ければデバッグ鍵（環境ごとに違う） | Secret 名を揃える |

### 注意：鍵を変えると、入っているアプリは上書きできない

Android は署名が違う APK での上書きを拒否します。共通鍵に切り替えた最初の版だけは、**一度アンインストールしてから入れ直し**になります（端末の中だけのデータは消えるので、Vault・Drive 同期やバックアップを先に）。

### 注意：公開リポジトリに入っている鍵

`Theta.KidsHome.Hatch/app/kidshome.jks`（パスワード付き）と `Theta.Mensetsu.Hatch/android/signing/mensetsu-dev.jks` は公開リポジトリにあるので、誰でもその鍵で同じ署名の APK を作れます。**この 2 つは共通鍵には使わない**でください。共通鍵へ切り替えるときに、リポジトリからも外します。

## 4. 配り方

### 画面から 1 つずつ登録する場合

各リポジトリの **Settings → Secrets and variables → Actions → New repository secret** で、上の 4 つを登録します。
`ANDROID_KEYSTORE_B64` の値は、PowerShell で次を実行するとクリップボードに入ります。

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\path\meishiclaude-release.jks")) | Set-Clipboard
```

### まとめて登録する場合（おすすめ）

1. GitHub CLI を入れてログイン（初回だけ）
   - Windows：`winget install GitHub.cli` → `gh auth login`
   - Mac：`brew install gh` → `gh auth login`
2. 配る先は `tools/repos.txt`（1 行 1 リポジトリ。**改名後の名前**なので、先にリポジトリ名を変えておく）
3. 実行（パスワードは画面で聞かれる。ファイルや履歴には残らない）
   - Windows：`powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -Keystore C:\path\meishiclaude-release.jks`
   - Mac：`bash tools/sync-secrets.sh ~/path/meishiclaude-release.jks`
4. 各リポジトリで release.yml を動かし、APK の SHA-1 が上の値と同じことを確かめる

## 5. 鍵以外の秘密

| 秘密 | 置き場所 |
| --- | --- |
| Gemini API キー | 各端末のアプリ内（暗号化）。同じ端末の別アプリへは利用者の承認で貸し借り（`spec/THETA_SHARED_SETTINGS.md` §4。これも**同じ署名鍵のアプリ同士でしか動かない**） |
| Google の OAuth | 鍵は不要。Google Cloud のプロジェクトは 1 つ、Android 用クライアントをアプリ（パッケージ名）ごとに追加。SHA-1 は上の 1 つ（`spec/THETA_GOOGLE_SETUP.md`） |
| Mac の署名・Apple ID・winget | DeskHatch だけが使用（`MAC_CSC_LINK` など）。必要になったら同じスクリプトで配る |
