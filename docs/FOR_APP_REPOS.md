# 各アプリのリポジトリ・スレッドから、このリポジトリを参照させる

## 1. 各アプリの `CLAUDE.md` に足す文

各アプリのリポジトリの直下に `CLAUDE.md`（無ければ作る）を置き、次を貼ります。
Claude Code はスレッドの最初に `CLAUDE.md` を必ず読むので、**これからそのリポジトリで開くスレッドはすべて**ここを参照するようになります。

```markdown
## Theta Hatch シリーズ共通（必ず参照）

このアプリは Theta Hatch シリーズの 1 つです。シリーズ共通の仕様・デザイン・鍵の決まりは
GitHub の kiwiman0706-beep/Theta.Hatch.Series にあり、このリポジトリの docs より優先します。

- 作業を始める前に、Theta.Hatch.Series を読める状態にする
  （クラウドのスレッドでは add_repo で kiwiman0706-beep/Theta.Hatch.Series を追加して clone する）
- 読むもの：
  - `spec/THETA_HATCH_SPEC.md`（共通仕様）、`spec/THETA_VAULT_SPEC.md`、`spec/THETA_SHARED_SETTINGS.md`、`spec/THETA_GOOGLE_SETUP.md`
  - `design/README.md`（スキン：system・dark・light・pop・alert・scifi。色は `design/skins/skins.json`）
  - `spec/THETA_HATCH_SPEC.md` §6.1（アプリ内自動更新は必須）、`docs/MIGRATION.md`・`catalog/apps.json`（このアプリの目標の ID・リポジトリ名）
  - `secrets/README.md`（署名鍵はシリーズ共通。Secret の名前は ANDROID_KEYSTORE_B64・ANDROID_KEYSTORE_PASSWORD・ANDROID_KEY_ALIAS・ANDROID_KEY_PASSWORD）
- 共通仕様の写しをこのリポジトリに増やさない（変えるときは Theta.Hatch.Series 側を直す）
- 鍵・パスワード・API キーをリポジトリに入れない
- 作品の版や概要が変わったら、Theta.Hatch.Series の README の一覧も直す
```

## 2. いま開いているスレッドへ

すでに進んでいるスレッドには、次の 1 文を送れば十分です（`CLAUDE.md` を足したあとなら、次の新しいスレッドからは不要）。

```
Theta Hatch シリーズ共通の仕様・デザイン（スキン）・署名鍵の決まりを kiwiman0706-beep/Theta.Hatch.Series にまとめました。
add_repo でこのリポジトリを追加して README・spec/・design/・secrets/ を読み、このアプリの CLAUDE.md に
docs/FOR_APP_REPOS.md の §1 の文を足してください。そのうえで、このアプリがスキン（ui.skin）と共通署名鍵に
対応するために何が必要かを一覧にして、私に確認してから進めてください。
```

## 3. 新しいスレッドを作るとき

スレッドを作る画面でリポジトリを選ぶとき、そのアプリのリポジトリに加えて **Theta.Hatch.Series も一緒に選ぶ**と、最初から両方が手元にある状態で始まります。
