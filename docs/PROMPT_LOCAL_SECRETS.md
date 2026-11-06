# Windows の Claude Code（ローカル）に、Secret の一括登録を頼む文

自分の PC（Windows）で動く Claude Code に貼る。鍵の値はこの PC の中だけで扱い、クラウドのスレッドには出さない。

---

Theta Hatch シリーズの Android アプリ全部に、APK の署名鍵を GitHub Actions の Secret として登録したいです。手伝ってください。

## 背景

- シリーズ共通の決まりは GitHub の `kiwiman0706-beep/Theta.Hatch.Series` にあります。手順は `secrets/README.md`、配る先は `tools/repos.txt`（改名後の名前）、登録スクリプトは `tools/sync-secrets.ps1` です。
- 鍵は 1Password の保管庫「個人」のアイテム「APK共通秘密鍵」に入っています。ファイルは 2 つで、`meishiclaude-release.jks`（鍵）と `keystore-password.txt`（パスワード）です。
- 正しい鍵は、SHA-1 が `A1:13:EA:34:83:60:56:32:E7:F5:94:4E:4E:8C:20:55:DD:AE:28:BA`、別名が `meishiclaude` のものです。
- 登録する Secret は、各リポジトリに次の 4 つです：`ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`（`meishiclaude`）・`ANDROID_KEY_PASSWORD`（鍵ストアと同じパスワード）。
- GitHub CLI（gh）と 1Password CLI（op）は winget で入れました。
- `gh auth login` が「error connecting to github.com」で失敗します。`curl.exe https://api.github.com` は 200 で、WinHTTP のプロキシはありません。

## やってほしいこと

1. **gh のログインを直す。** `$env:GH_DEBUG="api"` などで原因を調べてください。証明書の検査（セキュリティソフト）、IPv6、DNS などが考えられます。原因と直し方を説明してから直してください。終わったら `GH_DEBUG` は消してください。
2. **Theta.Hatch.Series を手元に用意する。** `gh repo clone kiwiman0706-beep/Theta.Hatch.Series`、または `git clone`。
3. **改名ができているか確かめる。** `tools/repos.txt` の各リポジトリが、その名前で存在するかを `gh repo view` で確かめてください。MeishiApp → Theta.Meishi.Hatch、dsbooks → Theta.Book.Hatch、THETA.Chirashi.Hatch → Theta.Chirashi.Hatch の 3 つが、まだ古い名前のことがあります。
   - まだなら、`gh repo rename` で改名してよいか**私に確認してから**行ってください。
4. **1Password CLI の準備。** 1Password アプリの 設定 → 開発者 →「1Password CLI と連携」をオンにし、`op` から読めることを確かめてください。日本語の保管庫名・アイテム名が文字化けして読めないときは、`op item list` などで ID を調べ、ID で指定してください。
5. **登録する。**
   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\sync-secrets.ps1 -OpKeystore "op://個人/APK共通秘密鍵/meishiclaude-release.jks" -OpPassword "op://個人/APK共通秘密鍵/keystore-password.txt"
   ```
   スクリプトは、まだ Windows で動かしたことがありません。動かなければ直してください。スクリプトの修正は Theta.Hatch.Series にコミットして push してかまいません（ブランチは今のデフォルトのまま）。
6. **確かめる。** 各リポジトリで `gh secret list -R kiwiman0706-beep/<リポジトリ>` を実行し、4 つの名前が並んでいることを確かめてください。結果をリポジトリごとの表にして見せてください。

## 守ってほしいこと

- **鍵ファイル・パスワード・Base64 の値を、画面に表示したり、ファイルやログに残したり、コミットしたりしないでください。** 表示してよいのは SHA-1 と Secret の名前だけです。
- 1Password から取り出した一時ファイルは、終わったら必ず消してください。
- 鍵の SHA-1 が上の値と違ったら、何も登録せずに止まって、私に知らせてください。
- 登録が終わったら、クラウドの「Theta.xxx.Hatch作品一覧」スレッドに伝える報告を、短くまとめてください。どのリポジトリに登録できたか、直したこと、残っていることを入れてください。
