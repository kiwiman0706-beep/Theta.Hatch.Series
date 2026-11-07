# 「入れ替えだけ」のアプリに送る文

データの移行が要らないアプリ（Meishi・Chirashi・Book 以外）のスレッドへ。`PROMPT_JOIN.md` のあとに送る。

---

このアプリは、データの移行は要りません（まだあまり使っていないので）。橋渡し版も作らなくてかまいません。
**新しいアプリ ID・共通鍵の版を 1 つ出して、Theta Home Hatch から入れられるようにする**ことだけをお願いします。古いアプリの削除は Home が案内します。

Theta.Hatch.Series の `spec/THETA_HATCH_SPEC.md` §6.1「**ハブが入れられる Release の条件**」を全部満たしてください。特に：

- 版を上げて既定ブランチに push したら、Actions が**自動で** `v<版>` のタグと Release を作る（手で Release を作らなくてよいように）
- Release は draft・prerelease にしない
- Android の APK は 1 つだけ、名前は `Theta<名前>Hatch-<版>.apk`
- パッケージ名は `docs/APP_IDS.md` の新しい ID、署名はシリーズ共通の鍵（Secret の 4 つ。登録済み）
- リポジトリは公開のまま

Release が出たら、Theta.Hatch.Series の `tools/check_apk.py <APK>` で「パッケージ名」と「シリーズ共通の鍵」を確かめ、結果を `progress/<id>.md` に書いてください。
