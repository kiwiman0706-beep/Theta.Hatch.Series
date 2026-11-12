# Theta Camera Hatch（camera）の移行メモ

- 更新：2026-11-12
- スレッド：https://claude.ai/code/session_012DXkbx4X64tseX2Fpu1dRb
- 状態：作業中（新しい ID・共通鍵で Release 済み。Fold5 実機での確認中）

## 今と目標

| | 今 | 目標 |
| --- | --- | --- |
| リポジトリ名 | Theta.Camera.Hatch | Theta.Camera.Hatch |
| アプリ ID | app.thetahatch.camera（0.2.0〜。ChatGPT で作った 0.1.0 は com.theta.camera.hatch・別の鍵） | app.thetahatch.camera |
| 署名 | 共通鍵（Secret の 4 つ、別名 thetahatch）。release.yml が main への push で v<版> を自動で Release | 共通鍵 |
| 更新 | ハブに頼む（HatchUpdate.kt）。ハブが無ければアプリ単体で Releases を確認 → DownloadManager → SHA-256 照合 → 「ダウンロード」から入れる。インストール権限は持たない | ハブに頼む |
| 共通設定 | なし | ハブから受け取る |
| データの置き場所 | 写真・動画は DCIM/ThetaCamera/<フォルダ>、イベント・☆・タグ・コメントは Documents/ThetaCamera/<フォルダ>/ の .xmp と .theta.json | 写真は NAS、メタデータは持ち出せる形（Theta Vault との関係は未定） |
| 対応 OS | Android（Galaxy Z Fold5 専用でよい） | Android |
| スキン | なし（モノクロの線アイコン・全面プレビュー。カメラなのでネイティブ UI） | 検討 |

## 方針

- 目標は「Fold5 専用でよいので、純正カメラでできることをできるだけ全部、そのうえで細かい要望に応え、最終的に純正を置き換える」（CAM-037、リポジトリの STOCK_PARITY.md）。
- カメラは CameraX のネイティブ UI。シリーズ共通の HTML UI にはしない（映像・連写・外画面などの都合）。
- 0.1.0 からの橋渡し版は作らない。端末内のデータは写真ファイルだけで、DCIM に残る。
- ADB の窓口（StatusService・CommandReceiver、spec/THETA_ADB_SPEC.md）は 0.12.0 で実装済み。カメラ用の命令（PHOTO・VIDEO・ZOOM など）も持つ。テスト手順はリポジトリの TESTING.md。

- 撮って返す（spec §6.2 `CAPTURE`）を 0.14.0 で実装。Memo などから呼んで写真・動画・スキャンを受け取れる

## 決めてほしいこと

- [ ] スキン（ui.skin）に合わせるか（今はモノクロの線アイコンで固定）
- [ ] メタデータを Theta Vault（Obsidian）にも書くか（今は写真ごとの .xmp と .theta.json）

## 進み具合

- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に
- [x] signing：共通鍵の Secret で署名
- [x] update：更新をハブに頼む形に（ハブはハブ機能）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した
- [x] release：新しい版を Releases に出した

## 実機で確かめること

- [ ] ハブ（Home・KidsHome）の Hatch ドロワーに出て、更新できるか
- [ ] Memo から撮って返す（写真・動画・スキャン、1 つ／複数）
- [ ] Fold5 での撮影・録画・録画中の写真・外画面・Flex モード（一覧はリポジトリの TESTING.md）
