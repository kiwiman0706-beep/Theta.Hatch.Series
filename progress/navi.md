# Theta Navi Hatch（navi）の移行メモ

- 更新：2026-11-24
- スレッド：https://claude.ai/code/session_012DXkc1s7r9pPQgcG7FqRha
- 状態：実機確認待ち（v0.3.0 を Releases に公開。catalog に登録済み）

## 今と目標

| | 今（0.3.0） | 目標 |
| --- | --- | --- |
| リポジトリ名 | `Theta.Navi.Hatch` | 同じ |
| アプリ ID | `app.thetahatch.navi`（0.2.1 までは `com.theta.navihatch`） | 同じ |
| 署名 | 共通鍵（Secret の 4 つ、別名 thetahatch）。`release.yml` が CI でビルド・署名し SHA-256 を確かめる | 同じ |
| 更新 | 「更新を確認」でハブに `UPDATE` を頼む（無ければ Releases を開く）。インストール権限なし | 同じ |
| 共通設定 | 自分で持つ（Navigation／Gemini／Places のキーを Keystore で暗号化） | Gemini のキー・モデルをハブから受け取る。Navigation SDK のキーはこのアプリだけ |
| データの置き場所 | 端末の中（キー・診断ログ） | 履歴・お気に入りができたら Vault（P4） |
| 対応 OS | Android（車載タブレット iPlay60 Pro＋Android Auto） | 同じ |
| スキン | なし（独自の暗い色） | タブレット側の画面を `ui.skin` に合わせる（車側は Android Auto の決まりのまま） |

## 方針

- 0.2.1（外部で作った試作）を引き継ぎ。ID が変わるので**入れ直し**。データは移さない（キーは入れ直し）。橋渡し版は作らない（`migration.bridge: false`）
- Navigation SDK の API キーのアプリ制限を `app.thetahatch.navi`＋共通鍵の SHA-1 で登録し直す
- 実車検証（P0）の間は release も debuggable（ADB の `run-as` で診断ログを回収するため）。製品版で外す
- Home との連動：まず**連動**（別アプリのまま、`signature` 権限の ContentProvider `app.thetahatch.navi.theta` と Intent で Home に「ドライブ」パネル）。内蔵は APK の大きさ・地図キー・落ちたときの影響から後回し。案は Theta.Navi.Hatch の `docs/HOME_LINK_JA.md`

## 決めてほしいこと

- [x] `catalog/apps.json` に navi を足す（2026-11-24、利用者の了承でこのスレッドから）
- [ ] Home 連動の Intent・ContentProvider を spec §6.2 に足すか

## 進み具合

- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に
- [x] signing：共通鍵の Secret で署名（release.yml で SHA-256 を照合済み）
- [x] update：更新をハブに頼む形に（ハブはハブ機能）
- [ ] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した
- [x] release：新しい版を Releases に出した（v0.3.0、2026-11-24）

## 実機で確かめること

- [ ] 0.3.0 が 0.2.1 と並んで入る／新しいキー制限で地図が出る
- [ ] Android Auto の一覧に出る経路（Play 内部共有か、AA の開発者設定「提供元不明」か）
- [ ] ハブからの更新（Home が navi を catalog で知ってから）
