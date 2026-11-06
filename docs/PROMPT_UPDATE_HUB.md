# ハブを作る依頼文（Home・KidsHome のスレッドへ）

Theta Home Hatch と Theta KidsHome Hatch のスレッドに送る。`PROMPT_JOIN.md`（シリーズへの参加）を送ったあと、または一緒に。

---

シリーズの Android アプリの更新と共通設定を、このアプリ（と、もう一方のホームアプリ）でまとめて扱う「ハブ」にしたいです。まずは更新のハブです。
ねらいは、ほかのアプリにインストールの権限（`REQUEST_INSTALL_PACKAGES`）を持たせなくて済むようにすることです。

kiwiman0706-beep/Theta.Hatch.Series を参照してください（見えなければ add_repo で追加して clone）。決まりは `spec/THETA_HATCH_SPEC.md` の **§6.1** に書きました。要点：

- 対象のアプリは `catalog/apps.json`（Android 版があるもの）。APK にも同じ一覧を同梱し、ネットで読めたほうを使う。
- 端末に入っているアプリについて、各リポジトリの Releases の最新版を確認し、Wi-Fi で取得、GitHub の SHA-256・パッケージ名・**シリーズ共通の鍵の署名**（`secrets/README.md`）を照合してから `PackageInstaller` で入れる。共通の鍵でない APK は入れない。
- ほかのアプリからは `Intent("app.thetahatch.action.UPDATE")`（extra `packageName`）で頼まれるので、そのアプリの更新画面を開く。
- 一覧に「入っている版・新しい版・更新・すべて更新・入れる」。自分自身の更新もここから。
- **移行（アプリ ID の変更）も Home がまとめて行う**（`docs/MIGRATION.md` §3、spec §6.1「移行（ハブ）」）：古い ID が入っていて新しい ID が無いアプリについて、①橋渡し版への更新（Meishi・Chirashi・Book だけ。いま入っているアプリと同じ署名なら入れてよい）→ ②書き出し → ③新しい版を入れる → ④読み込み → ⑤古いアプリの削除、を順に案内する。ほかのアプリは「新しい版を入れる → 古いアプリの削除」だけ。
- Home と KidsHome の両方が入っている端末で、同じアプリを同時に入れないようにする。
- KidsHome は、更新の操作をおうちの人の画面に置く（子どもの画面には出さない）。

Home には `HatchInstaller.kt`（Hatch ドロワーからの導入）、KidsHome には `SelfUpdate.kt` がすでにあるので、それを土台にしてください。
Android 12 以降の「確認なしの更新」は、ハブがそのアプリを入れた側のときだけ効くはずです。ブラウザで入れたアプリを更新したときの動きは、実機で確かめる項目として `TESTING.md` などに書いてください。

## もう一つ：設定のハブ

同じ端末のシリーズのアプリ同士で、スキン・Gemini API キー・NAS の接続先とパスワードとデバイストークン（Synology Secure SignIn の確認コードを次から省くもの）・使う Google アカウントを共有したいです。これも、このアプリ（と、もう一方のホームアプリ）が預かって配る「設定のハブ」にしてください。決まりは `spec/THETA_SHARED_SETTINGS.md` の **§4.0・§4.1** です。要点：

- 共通の署名鍵のアプリだけが読める ContentProvider（権限 `app.thetahatch.permission.SHARE`、`protectionLevel="signature"`）で、設定（`info`）と秘密（`secret/<キー>`）を配る。
- 設定画面に「Hatch シリーズの共通設定」を置き、まとめて入力・変更できるようにする。秘密は Android Keystore で暗号化して持ち、書き出し・バックアップには入れない。
- ほかのアプリが秘密を読んだら通知で知らせる。KidsHome では、貸す操作をおうちの人の画面に置く。
- Google のログイン自体は共有できない（アプリごとに 1 回）ので、共有するのは「どのアカウントを使うか」だけ。

最初の返事では、まだ変更はせず、作り方の計画（画面・使うクラス・Manifest の変更・テスト）と、決めてほしいことを見せてください。ハブの計画も、`PROMPT_JOIN` で頼んだ移行メモ（`progress/<id>.md`）の「方針」に書いてください。
