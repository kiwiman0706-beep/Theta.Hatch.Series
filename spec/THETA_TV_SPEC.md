# Theta Hatch シリーズ TV 仕様 v0（構想）

> 正本はこのリポジトリ（kiwiman0706-beep/Theta.Hatch.Series の `spec/`）。2026-11-08 作成。まだ構想。

ねらい：**軽くて使いやすくて広告のないスマート TV**。家の NAS の本・映画・音楽・写真を、テレビでリモコンだけで手軽に見る。
中心は Android TV／Google TV。できるものは LG の webOS にも。

## 1. どのアプリを TV に

| アプリ | Android TV | webOS | TV でできること |
| --- | --- | --- | --- |
| **Home** | ○（TV 用のホーム画面） | — | 広告なしのホーム。続きから見る（映画・音楽・本）、Hatch アプリ、入力切替、NAS の状態 |
| **Movie** | ○ | ○ | 映画・ドラマ・アニメ・録画・ホームビデオを選んで再生（サーバーは NAS の Jellyfin） |
| **Music** | ○ | △ | アルバム・アーティスト・プレイリストを再生、歌詞・ジャケットを大きく |
| **Photo** | ○ | ○ | 年・イベントごとのスライドショー、「今日のおもいで」 |
| **Book** | ○（Leanback 対応済み） | △ | 漫画・写真集を大きく、オーディオブック |
| **KidsHome** | ○（対応済み） | — | 子ども向けのホーム（動画・おはなし） |
| Mitene | ○ | ○ | 家族の写真・動画（Photo と合わせるかは Mitene の構想次第） |

- ほかのアプリ（Meishi・Memo など）は TV では作らない（閲覧だけなら Web 版をブラウザで）。
- 映画は、まず **Jellyfin の公式アプリ（Android TV・webOS とも有り）で見られる**ように NAS を整える（`THETA_LIBRARY_SPEC.md`）。Theta Movie Hatch の TV 版は、そのあとスキン付きの軽い入口として作る。

## 2. Android TV の作り（全アプリ共通）

- **同じ APK** に TV 用の画面を足す（`THETA_HATCH_SPEC.md` §4）。TV 用の Activity に `LEANBACK_LAUNCHER`、Manifest に `<uses-feature android:name="android.software.leanback" android:required="false"/>` と `<uses-feature android:name="android.hardware.touchscreen" android:required="false"/>`、TV のバナー（320×180）。
- **リモコンだけで全部できる**：十字キーで動く、選んでいる所がはっきり分かる（accent の太い枠と少し拡大）、戻るボタンで必ず 1 つ前へ。再生・一時停止・早送りのボタン（`KEYCODE_MEDIA_*`）。
- **10 フィートの画面**：周り 5% は空ける（テレビの端が切れるため）、文字は大きく（本文 24sp 以上の目安）、1 画面に詰め込まない。横 1 行の棚を縦に並べる形（Netflix 型）を基本に。
- **スキン**：`design/skins` の 10 種をそのまま使う（暗いスキンが既定）。TV では縞模様や細い線は太めに。
- **軽く**：起動は速く、裏で重い処理をしない。広告・トラッキングは入れない。
- **NAS へのつなぎ方**：家の LAN を優先。外からは Tailscale（Android TV 用のアプリ有り）。NAS のログインは Home（設定のハブ）から受け取る。
- **入れ方**：Home（TV 版）が更新のハブ。最初の 1 本は ADB（`THETA_ADB_SPEC.md` §4）で入れる。Google TV のホームを Home に替えるのも ADB で行う（`cmd package set-home-activity …`。Google TV の更新で戻ることがある）。

## 3. Home の TV 版

- 広告・おすすめ・トラッキングのないホーム。上から：時計と天気／**続きから**（Movie・Music・Book の最後に見たもの）／Hatch アプリ／ほかのアプリ／入力切替（HDMI）・設定。
- 声での操作は後回し（Google アシスタントは使わない前提）。
- 子ども用のテレビは KidsHome（TV 対応済み）。

## 4. webOS（LG のテレビ）

- webOS のアプリは **HTML・CSS・JS**（Web アプリ）。シリーズの「画面は HTML で 1 つ」（spec §4）のアプリは移しやすい。Compose・Flutter で作ったアプリ（Home・Music など）はそのままでは動かないので、webOS 用には Web 版を作る。
- 入れ方：LG の「Developer Mode」アプリで開発者モードにし、PC から webOS CLI（`ares-package`・`ares-install`）で入れる。開発者モードには期限があり、ときどき延長が要る。hatchctl に `hatchctl webos install` を足す想定。
- 動画は HTML5 の video で、Jellyfin から HLS で受ける。Tailscale は無いので、LAN の中だけ（外からは見ない）。
- 手軽さ優先なら、まずは Jellyfin の webOS アプリ＋テレビのブラウザで Web 版（PWA）。

## 5. 進め方（案）

1. NAS を `THETA_LIBRARY_SPEC.md` の形に整え、Jellyfin（Android TV・webOS の公式アプリ）で見られるようにする。
2. Home の TV 版（ホーム画面・続きから・ハブ）。
3. Music・Photo・Book の TV 画面。
4. Movie の TV 版（Jellyfin を使う軽い入口）。
5. webOS：Photo・Movie の Web 版から。
