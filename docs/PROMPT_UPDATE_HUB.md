# 更新ハブを作る依頼文（Home・KidsHome のスレッドへ）

Theta Home Hatch と Theta KidsHome Hatch のスレッドに送る。`PROMPT_JOIN.md`（シリーズへの参加）を送ったあと、または一緒に。

---

シリーズの Android アプリの更新を、このアプリ（と、もう一方のホームアプリ）でまとめて行う「更新ハブ」にしたいです。
ねらいは、ほかのアプリにインストールの権限（`REQUEST_INSTALL_PACKAGES`）を持たせなくて済むようにすることです。

kiwiman0706-beep/Theta.Hatch.Series を参照してください（見えなければ add_repo で追加して clone）。決まりは `spec/THETA_HATCH_SPEC.md` の **§6.1** に書きました。要点：

- 対象のアプリは `catalog/apps.json`（Android 版があるもの）。APK にも同じ一覧を同梱し、ネットで読めたほうを使う。
- 端末に入っているアプリについて、各リポジトリの Releases の最新版を確認し、Wi-Fi で取得、GitHub の SHA-256・パッケージ名・**シリーズ共通の鍵の署名**（`secrets/README.md`）を照合してから `PackageInstaller` で入れる。共通の鍵でない APK は入れない。
- ほかのアプリからは `Intent("app.thetahatch.action.UPDATE")`（extra `packageName`）で頼まれるので、そのアプリの更新画面を開く。
- 一覧に「入っている版・新しい版・更新・すべて更新・入れる」。自分自身の更新もここから。
- 移行（アプリ ID の変更）にも使う：`catalog/apps.json` の `current.packageName`（古い ID）が入っていて `target.packageName`（新しい ID）が無ければ、「新しいアプリに移る」案内（新しいアプリを入れる → データの読み込み → 古いアプリの削除画面）を出す（`docs/MIGRATION.md`）。
- Home と KidsHome の両方が入っている端末で、同じアプリを同時に入れないようにする。
- KidsHome は、更新の操作をおうちの人の画面に置く（子どもの画面には出さない）。

Home には `HatchInstaller.kt`（Hatch ドロワーからの導入）、KidsHome には `SelfUpdate.kt` がすでにあるので、それを土台にしてください。
Android 12 以降の「確認なしの更新」は、ハブがそのアプリを入れた側のときだけ効くはずです。ブラウザで入れたアプリを更新したときの動きは、実機で確かめる項目として `TESTING.md` などに書いてください。

最初の返事では、まだ変更はせず、作り方の計画（画面・使うクラス・Manifest の変更・テスト）と、決めてほしいことを見せてください。
