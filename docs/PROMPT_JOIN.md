# 各スレッドに送る文（シリーズへの参加）

各アプリのスレッドにそのまま貼る。アプリごとの違いは、スレッド側が `docs/APP_IDS.md` の自分の行を見て埋める。
（もっと細かい移行の指示は `PROMPT_MIGRATION.md`。こちらはシリーズに参加してもらうための最初の一通）

---

このスレッドで作ってきたアプリを、Theta.xxx.Hatch シリーズの 1 本にします。
シリーズで機能をそろえたり連携させたりするため、シリーズ全体の決まりをまとめたリポジトリ **kiwiman0706-beep/Theta.Hatch.Series** を参照してください（このスレッドで見えなければ、add_repo で追加して clone してください）。
開発はこれまでどおり元のリポジトリで続けてください。設計を決めるとき・新しい機能を足すときは、折に触れてこちらも見てください。

## まず読むもの（Theta.Hatch.Series）

- `README.md` の「最新ガイドラインの要点」
- `docs/APP_IDS.md` の**このアプリの行**（新しいアプリ ID とリポジトリ名）
- `secrets/README.md`（署名鍵）、`docs/MIGRATION.md`（移行の手順）
- `spec/`（共通仕様）、`design/README.md`（スキン）

## 決めたこと

1. **署名鍵をシリーズ共通にします。** APK の署名鍵（Theta Meishi Hatch と同じ鍵）を、このリポジトリの GitHub Secrets に登録します。名前は `ANDROID_KEYSTORE_B64`・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD` です。これからはこの 4 つで署名して APK を作ってください。リポジトリの中の鍵ファイルや、ワークフローに直接書いたパスワードがあれば外してください。
   鍵が変わるので、今入っているアプリには上書きできません。それは承知しています（一度アンインストールして入れ直します）。端末の中にしか無いデータがあるなら、移す方法（書き出し → 読み込み）を用意してください。
   ねらいは、鍵を揃えて SHA-1 を全アプリ共通にし、Google API（Drive・カレンダーなど）への登録を楽にすることです。
2. **データの置き場所。** 基本は Google ドライブか、Tailscale でつないだ自宅の NAS（Synology DS1825+）、またはその両方にします。形式は Obsidian の Vault（Markdown＋添付ファイル）を基本に、アプリが無くなっても読める、ベンダーロックインしない形にしてください（`spec/THETA_VAULT_SPEC.md`）。NAS へのログインは、Synology の 2 段階認証（Secure SignIn の確認コード）にも対応してください。
3. **名前を揃えます。** リポジトリ名を `Theta.<名前>.Hatch` に、アプリ ID を `app.thetahatch.<名前>` にします（`docs/APP_IDS.md`）。yaegaki・kiwiman などの個人名は、アプリの中や ID に出さないでください。リポジトリの改名は私が GitHub で行います。
4. **改名による不具合を確認してください。** リポジトリ名やアプリ ID が変わると、自動更新（Releases を見に行く URL）、Web 版の URL、ワークフロー、README のリンク、ContentProvider の authority などが壊れることがあります。古い名前が残っていないか探して直し、動くことを確かめてください。
5. **自動更新。** アプリ内の自動更新は全アプリ必須です（spec §6.1）。無ければ入れてください。
6. **見た目。** Theta Home Hatch から始めたスキン（dark・light・pop・alert・scifi・system）のかっこいい UI を踏襲してください（`design/README.md`）。
7. **Windows・Mac。** APK だけでなく、Windows や Mac でも動かせるか検討してください（難しければ理由を）。

## 進め方

最初の返事では、まだ変更はせず、次をまとめて見せてください。私が OK してから進めてください。

- このアプリの今と目標（リポジトリ名・アプリ ID・署名・自動更新・データの置き場所・対応 OS）
- 改名・ID 変更で影響を受ける所の一覧
- 端末の中にしか無いデータと、その移し方
- 私がやること（Secret の登録、改名、実機での確認など）
- 1〜7 のうち、このアプリで難しいこと・決めてほしいこと

作業が終わったら、このリポジトリの `CLAUDE.md` に `docs/FOR_APP_REPOS.md` §1 の文を足してください。
