# 新しいアプリの Secret 登録を、ローカルの Claude Code に頼む文

自分の PC（Windows）で動く Claude Code のスレッドに貼る。最初の 1 回は「準備」から、2 回目からは「新しいアプリができたら」だけでよい。

---

Theta Hatch シリーズの APK 署名鍵の Secret 登録を、これから代わりにやってほしいです。

## 前提

- シリーズの決まりは GitHub の `kiwiman0706-beep/Theta.Hatch.Series`（公開）にあります。手元の clone は `＜例：C:\Users\Kiwiman\Theta.Hatch.Series＞` です（無ければ `gh repo clone` で）。作業の前に `git pull` してください。
- 鍵の決まりは `secrets/README.md`、登録スクリプトは `tools/sync-secrets.ps1`、配る先の一覧は `tools/repos.txt` です。
- 鍵は、1Password ではなく**この PC のフォルダ**に置きます：
  - 鍵ファイル：`＜例：C:\Users\Kiwiman\ThetaHatchKeys\theta-hatch-release.jks＞`
  - パスワード：`＜例：C:\Users\Kiwiman\ThetaHatchKeys\keystore-password.txt＞`
- 正しい鍵は、別名 `thetahatch`、SHA-1 `A1:13:EA:34:83:60:56:32:E7:F5:94:4E:4E:8C:20:55:DD:AE:28:BA` です。

## 準備（最初の 1 回だけ）

1. 鍵のフォルダが **OneDrive・Google ドライブなどの同期フォルダの中に無い**ことを確かめてください。中にあれば、私に知らせて場所を相談してください。
2. 鍵のフォルダを、自分のアカウントだけが読めるようにしてください（`icacls` で継承を切り、自分だけにフルコントロール）。変える前に、何をするかを見せてください。
3. `keytool -list -v` で、別名と SHA-1 が上の値と同じことを確かめてください（パスワードは画面に出さない）。
4. `gh auth status` で GitHub にログインできていることを確かめてください。
5. このスレッドで今後も同じことができるよう、この PC の `C:\Users\Kiwiman\.claude\CLAUDE.md` に次を足してください（無ければ作る）：
   > Theta Hatch の新しいアプリの Secret 登録を頼まれたら、Theta.Hatch.Series の `docs/PROMPT_LOCAL_NEW_APP.md` の「新しいアプリができたら」に従う。鍵は `＜鍵のフォルダ＞` にある。鍵・パスワード・Base64 の値は表示しない。

## 新しいアプリができたら

私が「Theta.Xxx.Hatch の Secret を入れて」と頼んだら：

1. そのリポジトリが GitHub にあり、名前が `Theta.<名前>.Hatch` の形か確かめる（違えば私に聞く）。
2. `tools/repos.txt` に無ければ 1 行足して、Theta.Hatch.Series にコミットして push する（`git pull --rebase` してから）。
3. そのリポジトリだけに登録する：
   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -Keystore "＜鍵ファイル＞" -PasswordFile "＜パスワードのファイル＞" -OnlyRepo kiwiman0706-beep/Theta.Xxx.Hatch
   ```
   （`-OnlyRepo` はまだ Windows で動かしたことがありません。動かなければ直して、直したものを Theta.Hatch.Series に push してください）
4. `gh secret list -R kiwiman0706-beep/Theta.Xxx.Hatch` で、`ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD` の 4 つがあることを確かめる。
5. 結果を短く報告する（どのリポジトリに入れたか、直したこと）。私がそれをクラウドの「Theta.xxx.Hatch作品一覧」スレッドに伝えます。

ついでに「全部のリポジトリに 4 つそろっているか確かめて」と頼んだら、`tools/repos.txt` の全部で `gh secret list` を見て表にしてください。

## 守ってほしいこと

- **鍵ファイル・パスワード・Base64 の値を、画面に出したり、ファイル・ログ・コミットに残したりしない。** 表示してよいのは SHA-1 と Secret の名前だけ。
- 鍵ファイルを、鍵のフォルダの外（リポジトリの中、デスクトップ、同期フォルダ）にコピーしない。
- SHA-1 が上の値と違ったら、何も登録せずに止まって知らせる。
- 鍵を作り直したり、別名を変えたりしない（頼まれても、まず影響を説明して確認を取る）。
