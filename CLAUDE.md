# Theta.Hatch.Series

Theta Hatch シリーズ（Theta.xxx.Hatch）の作品一覧と、シリーズ共通の仕様・デザイン・鍵の決まりの正本。

- `README.md`：先頭に「最新ガイドラインの要点」、その下に作品一覧。spec・design・secrets を変えたら要点の表も必ず直す。作品の版・概要が変わったら一覧を直す
- `spec/`：共通仕様（Hatch・Vault・設定の引き継ぎ・Google 連携）
- `design/`：スキン。正本は `design/skins/skins.json`。`theta-skins.css`・`ThetaSkins.kt` は `python tools/gen_skins.py` で生成し、手で直さない。直したら `preview.png` も撮り直す
- `secrets/`：鍵の置き場所と名前だけ。**鍵・パスワード・API キーそのものは絶対にコミットしない**
- `catalog/apps.json`：アプリ一覧（今と目標の ID・リポジトリ、自動更新の有無）。移行や新アプリのたびに直す
- `tools/`：生成スクリプト、Secret を配るスクリプト（`repos.txt` が配る先）
- `docs/FOR_APP_REPOS.md`：各アプリから参照させる方法

文章は日本語、短く。

## 移行のタスク管理（Hatch 移行ボード）

- ボード：https://claude.ai/artifact/39gPQjDjBrTmp3WwbAPM4S （ページは `tracker/migration-board.html`、データは Artifact の db：`apps/<id>`・`global/<id>`・`meta/run`）
- 利用者が付ける「済」は `done`。Claude は `done` を書き換えない（利用者に頼まれたときだけ）
- 「チェックして」と言われたら：
  1. `list_repos` の full_name を JSON 配列にして保存
  2. `python tools/check_progress.py <作業フォルダ> <その JSON>` → progress.json
  3. 各スレッドを `get_session` で見て、sources に Theta.Hatch.Series があれば `addref` を ok（progress.json に足す）
  4. `python tools/board_seed.py check progress.json` → ArtifactData の batch（既存の文書は `list` で version を読んで `if_version` を付ける）
  5. 結果を一言で報告し、catalog・README・APP_IDS（`python tools/gen_app_ids.py`）も実態に合わせる
- 全体の作業（`global`）を足すときは `tools/board_seed.py` の GLOBAL にも足す
