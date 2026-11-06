# 各スレッドに送る共通プロンプト（ID・リポジトリ名・署名鍵の移行）

全アプリ共通。このまま貼れば、各スレッドが自分のアプリの行を `catalog/apps.json` から探して進める。

---

Theta Hatch シリーズ全体で、アプリ ID・リポジトリ名・署名鍵・自動更新を揃えることにしました。このアプリもそれに合わせたいので、まず計画を立てて私に見せてください。**私が OK するまで、コードの変更・push・リリースはしないでください。**

## 前提

- シリーズ共通の決まりは GitHub の **kiwiman0706-beep/Theta.Hatch.Series**（private）にまとめました。このリポジトリの docs より優先します。add_repo で追加して clone し、次を読んでください。
  - `README.md`（先頭の「最新ガイドラインの要点」）
  - `catalog/apps.json`：**このアプリの行**（`current` が今、`target` が目標のリポジトリ名・ID）
  - `docs/MIGRATION.md`：移行の手順と影響
  - `spec/THETA_HATCH_SPEC.md`：§2 名前と識別子、§6・§6.1 リリースと自動更新（必須）
  - `secrets/README.md`：署名鍵の決まり
  - `docs/FOR_APP_REPOS.md`：このアプリの CLAUDE.md に足す文
- **アプリ ID**：全アプリ `app.thetahatch.<名前>` にします（個人名は入れない）。表示名は `Theta <名前> Hatch`。

  | アプリ | 新しい ID |
  | --- | --- |
  | Meishi・Memo・Mensetsu・Home・Book | `app.thetahatch.meishi`・`.memo`・`.mensetsu`・`.home`・`.book` |
  | Item・Kamigata・DoorPhoto・Label・Device | `app.thetahatch.item`・`.kamigata`・`.doorphoto`・`.label`・`.device` |
  | Travel・Oekaki・KidsHome・Music | `app.thetahatch.travel`・`.oekaki`・`.kidshome`・`.music` |
  | Hitsudan（Android 版なし） | デスクトップの appId を作るなら `app.thetahatch.hitsudan` |

  Android 版の無いアプリは、署名鍵と Android の自動更新は対象外。当てはまる所だけ進めてください。

- **署名鍵**：全アプリ共通の鍵（Meishi の鍵）で署名します。SHA-1 は `A1:13:EA:34:83:60:56:32:E7:F5:94:4E:4E:8C:20:55:DD:AE:28:BA`。
  - 鍵そのものは、このリポジトリの GitHub Actions Secret に入れてあります（入っていなければ私が入れます）。名前は `ANDROID_KEYSTORE_B64`（鍵ファイルの Base64）・`ANDROID_KEYSTORE_PASSWORD`・`ANDROID_KEY_ALIAS`・`ANDROID_KEY_PASSWORD`。release.yml はこの 4 つで署名するように揃えてください。
  - 鍵ファイル・パスワードをリポジトリに入れないこと。リポジトリ内に鍵（.jks など）やパスワードの直書きがあれば、外す計画に入れてください。
- **Google 連携**：新しい ID の Android 用 OAuth クライアント（上の SHA-1）は、Google Cloud に私が登録済みです。古い ID の登録も、移行が終わるまで残します。
- **リポジトリ名**：`catalog/apps.json` の `target.repo` と違う場合は、`Theta.<名前>.Hatch` に変えます。改名は私が GitHub の画面で行います。

## やってほしいこと

1. **影響の洗い出し**：古い ID・古いリポジトリ名・古い URL が使われている所を全部探して一覧にする。少なくとも次を見る。
   - `applicationId`・`namespace`、Manifest（ContentProvider・FileProvider の authority、intent の action、ウィジェット、ディープリンク、`<queries>`）
   - 自動更新が見に行く URL（`api.github.com/repos/…/releases/latest`）、Releases ページへのリンク
   - GitHub Pages（Web 版）の URL、Service Worker、Google の Web クライアントの設定
   - デスクトップ版の appId、electron-builder の publish 設定
   - README・docs・バッジ・ワークフロー（`release.yml` など）・テスト
   - Theta Home Hatch の Hatch ドロワーなど、ほかのアプリからこのアプリを指している所（気づいたら報告だけ）
2. **名前・ID・鍵を変える**：新しい ID・表示名・共通鍵の Secret に揃える。Kotlin/Java のパッケージ名（フォルダ）は無理に変えなくてよい。
3. **自動更新（spec §6.1）**：Android の更新は Home・KidsHome（更新ハブ）がまとめて行う。このアプリはインストールの権限を持たず、「更新する」でハブに `app.thetahatch.action.UPDATE` を送る（ハブが無ければ Releases ページを開く）。Home・KidsHome のスレッドは、ハブ側（全アプリの確認・取得・署名の照合・PackageInstaller）を作る。
4. **署名が変わって上書き更新できないことへの対策とアナウンス**（`docs/MIGRATION.md` §3）
   - **橋渡し版**：古い ID・古い鍵のまま版を上げた版を先に出す。中身は、データの書き出し（Vault を使うアプリは同期が済んでいることの確認）と、「新しいアプリに移ってください」の案内画面。自動更新があればこれは自動で入る。
   - **新しい版**：新しい ID・共通鍵。最初の起動で書き出したデータを読み込めるようにする。
   - 案内画面の流れ：データを書き出す → 新しいアプリを入れる → 新しいアプリで読み込む → 古いアプリを削除。
   - アナウンス：アプリ内の帯と案内画面、Release の本文、README の先頭に「移行のお知らせ」（なぜ入れ直しが必要か、手順、データは消えないか）。
   - 端末の中だけにあるデータ（写真・記録・設定・暗号化した情報）が何かを洗い出し、どう移すかを計画に書く。
5. **不具合が無いかの確認**
   - ビルドとテストを通す。改名後のリポジトリ名でワークフローが動くこと。
   - できた APK の署名の SHA-1 が上の値と同じこと（`apksigner verify --print-certs`）、パッケージ名が新しい ID であること。
   - 自動更新：古いリポジトリ名の URL・新しいリポジトリ名の URL の両方で最新版が取れること（GitHub は改名後も古い名前から転送する）。
   - Google ログイン・Drive 同期が新しい ID で動くこと（実機が要るものは「未確認」として TESTING.md などに書く）。
   - 古い名前・古い ID が残っていないか、最後にもう一度検索する。
6. **CLAUDE.md**：このリポジトリの `CLAUDE.md` に `docs/FOR_APP_REPOS.md` §1 の文を足す。
7. **Theta.Hatch.Series 側の更新**：終わったら `catalog/apps.json`（このアプリの `current` を新しい値に、`autoUpdate`）と README の作品一覧を直す。push できなければ、直す内容を私に報告する。

## 最初の返事でほしいもの

- このアプリの「今」と「目標」（リポジトリ名・ID・表示名・鍵・自動更新の有無・データの置き場所）
- 影響の一覧（1 の結果）
- 橋渡し版と新しい版、それぞれで変えること
- 端末の中だけにあるデータと、その移し方
- 私がやること（リポジトリの改名、Secret の登録、実機での確認など）と、その順番
- 分からないこと・決めてほしいこと
