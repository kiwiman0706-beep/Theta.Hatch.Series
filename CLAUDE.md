# Theta.Hatch.Series

Theta Hatch シリーズ（Theta.xxx.Hatch）の作品一覧と、シリーズ共通の仕様・デザイン・鍵の決まりの正本。

- `README.md`：作品一覧（作品の版・概要が変わったらここを直す）
- `spec/`：共通仕様（Hatch・Vault・設定の引き継ぎ・Google 連携）
- `design/`：スキン。正本は `design/skins/skins.json`。`theta-skins.css`・`ThetaSkins.kt` は `python tools/gen_skins.py` で生成し、手で直さない。直したら `preview.png` も撮り直す
- `secrets/`：鍵の置き場所と名前だけ。**鍵・パスワード・API キーそのものは絶対にコミットしない**
- `tools/`：生成スクリプト、Secret を配るスクリプト（`repos.txt` が配る先）
- `docs/FOR_APP_REPOS.md`：各アプリから参照させる方法

文章は日本語、短く。
