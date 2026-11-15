# Theta TVhome Hatch（tvhome）の方針と進み具合

<!-- このアプリのスレッドが書く。ほかのアプリのファイルは触らない -->

- 更新：2026-11-15
- スレッド：https://claude.ai/code/session_012DXkbyha4qRNRU1wCiPjQm
- 状態：実機確認待ち（0.3.0 を Releases に出した。はじめの形はクロスバー＋計器盤）

## 今と目標

| | 今 | 目標 |
| --- | --- | --- |
| リポジトリ名 | Theta.TVhome.Hatch（新しく作った） | 同じ |
| アプリ ID | app.thetahatch.tvhome | 同じ |
| 署名 | 共通鍵（Secret の 4 つ）。v0.1.0 で SHA-256 を確認済み | 共通鍵（Secret の 4 つ、別名 thetahatch） |
| 更新 | **ハブ**（TV ではこのアプリ）。自分と Hatch アプリを 12 時間ごと、SHA-256・ID・共通鍵を照合して PackageInstaller | 同じ |
| 共通設定 | 設定のハブ `content://app.thetahatch.tvhome.theta`（Home 1.0.0 と同じ返し方） | 同じ |
| データの置き場所 | 端末の中だけ（並び・入口・秘密は Keystore で暗号化） | 並びは Vault の `apps.tvhome` も検討 |
| 対応 OS | Android TV（minSdk 28）。AQUOS 4T-C65DQ2 で使う | 同じ |
| スキン | シリーズの 10 種（ThetaSkins.kt の写し）。TV の既定は dark | 同じ |

## 方針

- Home・KidsHome から一部を切り出した、**テレビ専用の軽いホーム**（Compose の foundation だけ、APK 約 2.5MB）。THETA_TV_SPEC §3 の「Home の TV 版」を、Home と**別の APK**で作る（利用者が決定、2026-11-15）
- 子どもでも迷わない：大きなタイル・ひらがな、子どもモードとおうちの人の番号
- テレビの入口（地デジ・BS・録画・HDMI）は機種ごとに違うので、ADB で調べて `SET entry.<key>` で入れる（手順はアプリの `docs/ADB.md`）
- ADB の作業は別のスレッド（PC のローカル）。調べた結果はアプリの `docs/device/4T-C65DQ2.md`
- これからの順番：アプリの `docs/ROADMAP.md`（USB HDD → NAS・キャッシュ → SwitchBot → 家族の通話（Chat Plus／Meet β）→ Tapo の小窓）

## シリーズへの依頼（このリポジトリのスレッドへ）

- [ ] `catalog/apps.json` に tvhome を足す（platforms `androidtv`、`updateHub: true`、repo `Theta.TVhome.Hatch`）
- [x] `tools/repos.txt` に `kiwiman0706-beep/Theta.TVhome.Hatch` を足し、Secret を配った
- [ ] spec §6.1・共通設定 §4.0 の「ハブ」に TVhome を足す。受け持ちの決まり（実装済み）：既定のホームが TVhome なら TVhome、Home・KidsHome なら そちら、どれでもなければ Home・KidsHome が入っていない時だけ TVhome。`UPDATE_BUSY` は 3 つの間で送り合う
- [ ] ほかのアプリの `<queries>`・`UPDATE` の送り先に `app.thetahatch.tvhome` を足す（TV に入れる Music・Book・Photo・Movie）
- [ ] THETA_TV_SPEC §2・§3 を「Home の TV 版は TVhome（別 APK）」に直す
- [ ] README の作品一覧に追加

## 決めてほしいこと

- [ ] 動画の上に重ねるバー・ホームボタンの 1 回／2 回押し・「あと 15 分」タイマー（重ねて表示の権限とユーザー補助サービスを使う。ADB で AQUOS での可否を確かめてから）

- [ ] 事務作業（BT キーボード）：Memo・Photo の TV 版は作らない決まり（TV 仕様 §1）。テレビでは Web 版をブラウザで開く入口にするか、TV 版を作るか
- [ ] 家族の通話：Chat Plus／Meet（β）をまず試す（テレビにアプリが入るか・USB カメラ・相手を指定して開けるか）。だめなときの代わり（NAS の Jitsi など）

## 進み具合

- [x] claudemd：CLAUDE.md に Theta.Hatch.Series への参照
- [x] appid：アプリ ID を新しい ID に
- [x] signing：共通鍵の Secret で署名
- [x] update：更新をハブに頼む形に（ハブはハブ機能）
- [x] settings：共通設定をハブから受け取る（ハブは配る側）
- [x] rename：改名後の名前に合わせて URL・リンクを直した
- [x] release：新しい版を Releases に出した（v0.3.0）

## 実機で確かめること

- [ ] ADB で入れて起動・リモコンで操作（決定の長押しでメニューが出るか）
- [ ] テレビの入口：HDMI の切り替え、地デジ・BS・録画の Intent（`dumpsys … probe`）
- [ ] 自動更新：Release を見つけて確認なしで入れられるか
- [ ] 既定のホームにしたときのホームボタン・再起動・電源の入れ直し
