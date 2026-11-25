# Theta Navi Hatch（navi）の移行メモ

- 更新：2026-11-25
- スレッド：https://claude.ai/code/session_012DXkc1s7r9pPQgcG7FqRha
- 状態：実機確認中（P0 第1回 2026-11-25。v0.3.2 を公開。Android Auto の一覧に出すため Play 内部テストを準備中）

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

結果の詳細は Theta.Navi.Hatch の `docs/p0/RESULT_20261125.md`（単体テスト・実機SDK・DHU・実車を分けて記録）。

- [x] 0.3.0 が入る：iPlay60 Pro（Android 15・Android Auto 18.0）に SHA256SUMS と共通鍵の署名を確かめて導入できた（2026-11-25）。0.2.1 はこの端末に無く「並んで入る」は未確認
- [x] 新しいキー制限で地図が出る：0.3.1 でタブレットに Google の実地図（2026-11-25）。DHU では車側にも実地図
- [x] 二画面の同期：DHU の dualcheck のずれ（約 75 m）は SDK の「現在地を追う」表示が原因。0.3.2 で追う表示を解くようにして DHU の dualcheck が通過（差 0 m、2026-11-25）。実車は未確認
- [x] Navi のアイコンが白い丸：0.3.2 で青い台の矢印（アダプティブアイコン）に。DHU で確認（2026-11-25）
- [x] Android Auto の一覧に出る経路を決めた：AA の開発者設定「提供元不明のアプリ」は**だめ**（AA 18 の CAR.VALIDATOR が adb で入れた Car App Library アプリを拒否。メディアアプリは出る）→ **Play Console の内部テスト**で入れる（利用者が開発者アカウントを作る。内部アプリ共有は署名が変わるので使わない）
- [ ] Play 内部テストから入れて AA の一覧に出る（0.3.2 以降の AAB。アプリ署名鍵に共通鍵を登録して SHA-1 を変えない）
- [ ] 車とタブレットの二画面・ジョグダイヤル・車両位置の診断（実車、利用者が停車中に）
- [ ] ハブからの更新（Home が navi を catalog で知ってから。Play から入れた後はインストール元が Play になる点に注意）

## メモ（P0 で分かったこと）

- 0.3.1 から release は debuggable でない（Play が受け付けないため）。ADB の診断は `cmd export` で回収
- Release に Play 用の AAB も置く（APK は 1 つのまま。§6.1 に合う）
- ワイヤレスデバッグは Wi-Fi 接続中でないと ON にできない。テザリングで pair → `adb tcpip 5555` にすれば Tailscale 越しに使える（再起動で切れる）
