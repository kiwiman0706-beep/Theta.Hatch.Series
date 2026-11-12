# Theta Hatch シリーズ 設定の引き継ぎ（共通設定）v1

> 正本はこのリポジトリ（kiwiman0706-beep/Theta.Hatch.Series の `spec/`）。2026-10-26 に MeishiApp/docs から移しました。

一つのアプリで設定したことを、シリーズの他のアプリでも使えるようにする約束ごと。
**無条件に共有はしない**。項目ごとに「シリーズに合わせる／このアプリだけの値にする」を選べ、秘密（APIキー等）はクラウドに置かない。

## 1. 3つの範囲

| 範囲 | どこに置くか | 例 | 他のアプリへ |
| --- | --- | --- | --- |
| **シリーズ**（series） | Vaultの `.theta/settings.json` の `series` | 見た目のスキン（`ui.skin`）、Geminiのモデル、Googleアカウント（どのアカウントを使うか）、Web用OAuthクライアントID、Google Cloudのプロジェクト名、カレンダーの登録先、地図の利用 | 各アプリが「シリーズに合わせる」を選んだ項目だけ |
| **アプリ**（app） | Vaultの `.theta/settings.json` の `apps.<アプリ>`（端末間で同じにしたいもの）／端末内 | 取り込み後に自動で読み取る、連絡先の写真の種類、ScanSnapフォルダ | 引き継がない（同じアプリの別の端末には届く） |
| **端末**（device） | 端末の中だけ | Gemini APIキー、OAuthトークン、連絡先の行ID、ウィジェット、通知の許可 | 原則なし。**同じ端末の中で、利用者が承認したときだけ**コピー（§4） |

- Vaultは Google ドライブ等で全端末・全アプリが共有しているので、`series` と `apps` はそのまま全端末に届く。
- 端末の範囲に置くものは、Vault・バックアップ・Gitに入れない。

## 2. `.theta/settings.json`

```json
{
  "spec": 1,
  "updated": "2026-10-22T10:00:00Z",
  "series": {
    "ui.skin":             { "value": "pop",              "by": "home",   "at": "2026-10-26T10:00:00Z" },
    "gemini.model":        { "value": "gemini-2.5-flash", "by": "meishi", "at": "2026-10-22T10:00:00Z" },
    "gemini.format":       { "value": "legacy",           "by": "meishi", "at": "…" },
    "google.account":      { "value": "taro@example.com", "by": "meishi", "at": "…" },
    "google.webClientId":  { "value": "1234-abc.apps.googleusercontent.com", "by": "meishi", "at": "…" },
    "google.cloudProject": { "value": "meishi",           "by": "meishi", "at": "…" },
    "calendar.id":         { "value": "taro@example.com", "by": "meishi", "at": "…" },
    "map.enabled":         { "value": true,               "by": "meishi", "at": "…" }
  },
  "apps": {
    "meishi": { "autoRecognize": true, "contactPhoto": "card" }
  }
}
```

- キーは `<分類>.<名前>`。値はJSONの値。`by`（書いたアプリ）と `at`（書いた時刻）を付け、同時編集は `at` が新しい方を採用（項目単位）。
- 知らない項目は消さずに残す（新しいアプリが足した項目を古いアプリが壊さない）。
- **秘密は書かない**（APIキー、トークン、パスワード、クライアントシークレット）。読み込み時にそれらしい項目（`key`、`token`、`secret` を含む名前）があれば無視する。
- 書き込みは「読み込み → 1項目更新 → 書き戻し」。ファイルが無ければ作る。Obsidianで手で直してもよい（JSONとして読めなければ無視して警告）。

## 3. 各アプリの持ち方（「シリーズに合わせる」）

各アプリは自分の設定（端末内）に、シリーズ項目ごとの **追従フラグ** を持つ。

```
follow["gemini.model"] = true   … シリーズの値を使う。このアプリで変えたら、次の同期で series に書く（他のアプリにも反映）
follow["gemini.model"] = false  … このアプリだけの値を使う。series は読むだけ・変えない
```

- 画面では、シリーズ項目の設定の横に小さく「シリーズ共通」か「このアプリだけ」を表示し、切り替えられる。
- 同期で series の値が変わったら、`follow=true` の項目だけ反映する。
- 各アプリは「自分が使える項目」だけを引き継ぎ画面・設定画面に出す（例：Web版にカレンダーの登録先は出さない）。使えない項目も、自分の値があれば series に書き出す（他のアプリが使う）。
- 引き継ぎが決まるまで（初回同期の前・引き継ぎ画面に答える前）は、このアプリでの変更を series に書かない。他のアプリの値を、聞く前に上書きしないため。
- 共通の処理は `desktop/lib/series.js`（JS）と `SeriesSettings.java`（Android）。同じテストを両方で流している。

### 初回起動（引き継ぎ）

新しいアプリを初めて開き、Vaultを選んだ（同期を始めた）ときに `.theta/settings.json` があれば：

```
Theta Hatch の設定を引き継ぎますか？         （Meishi Hatch で設定済み）
 ☑ Geminiのモデル            gemini-2.5-flash
 ☑ Googleアカウント          taro@example.com
 ☑ Googleカレンダーの登録先   taro@example.com
 ☐ 地図を使う                 はい
 ☑ Gemini APIキー（この端末の Meishi Hatch から）   ← §4、端末にあるときだけ
              [選んだ項目を引き継ぐ]  [引き継がない]
```

- 既定でチェックするのは、困らないもの（モデル・アカウント・登録先）。秘密は毎回チェックを外した状態で出してもよい。
- チェックした項目は `follow=true`、外した項目は `follow=false` で始まる。あとから設定画面で変えられる。

## 4. 秘密（APIキー）を同じ端末の中で引き継ぐ

クラウドには置かず、**同じ端末にある別のシリーズアプリから、利用者が承認したときだけ** コピーする。

| 端末 | しくみ |
| --- | --- |
| Android | 各アプリが `ContentProvider`（authority `<applicationId>.theta`）を公開し、権限 `app.thetahatch.permission.SHARE`（`protectionLevel="signature"`）で守る。**同じ署名鍵**のアプリだけが読める。新しいアプリは `<queries>` で `app.thetahatch.HATCH` アクションを宣言したアプリを探し、引き継ぎ画面で「Meishi Hatch のAPIキーを使う」を選ばれたときだけ `content://<id>.theta/secret/gemini.key` を読む。提供側は、読まれたことを通知などで知らせる。 |
| Windows / Mac | 将来はデスクトップを1つの「Theta Hatch」ホスト（トレイ常駐、各アプリはその中のモジュール。DeskHatch連携と同じ形）にまとめ、設定と鍵を1か所に持つ。それまでは各アプリの設定画面に「他のTheta Hatchアプリから読み込む」を置き、`<ユーザーの設定フォルダ>/ThetaHatch/shared-secrets.json`（ユーザーだけが読める権限）を経由して、利用者の操作でコピーする。 |
| Web（PWA） | シリーズのWeb版を同じオリジン（`https://<user>.github.io/`）で配信すると、IndexedDB の共通データベース `theta-hatch-series` を全アプリが読める。秘密はそこに置き、各アプリは利用者の承認で読む。 |

- これに合わせ、**シリーズの署名鍵は共通**にする（2026-11-06 に全アプリの Secret へ登録済み。`secrets/README.md`）。共通の鍵で署名したアプリ同士でしか、この仕組みは動かない。

### 4.0 設定のハブ（Home・KidsHome）

同じ端末での共有は、**Theta Home Hatch と Theta KidsHome Hatch（設定のハブ）が預かって配る**形にする（更新のハブ：`THETA_HATCH_SPEC.md` §6.1 と同じ 2 つ）。

- ハブは ContentProvider（authority `app.thetahatch.home.theta`／`app.thetahatch.kidshome.theta`、権限 `app.thetahatch.permission.SHARE`、`protectionLevel="signature"`）で、下の表の項目を持つ。設定画面に「Hatch シリーズの共通設定」（スキン・Gemini・NAS・Google アカウント）を置き、まとめて入力・変更できる。
- ほかのアプリは、`<queries>` にハブのパッケージ名を書き、起動時にハブの `info` を読む。秘密は、初めて使うときに「Home Hatch の設定を使う」を選んだら `secret/<キー>` を読んで自分の端末内に暗号化して持つ。
- アプリ側で設定を変えたら（「シリーズに合わせる」項目だけ）、ハブへ書き戻す：`update` を `content://app.thetahatch.home.theta/info` に。ハブは書いたアプリと時刻を記録する。
- ハブが無い端末では、各アプリが自分で入力する（今までどおり）。Home と KidsHome の両方がある端末では、Home を優先して読み、KidsHome は Home と同じ値に合わせる。
- 子ども用の端末（KidsHome）では、秘密を貸す操作をおうちの人の画面に置く。

**ContentProvider の返し方**（Home 1.0.0 の形）
- `query /info` → 列 `key`・`value`・`by`・`at`（1 項目 1 行。`by` は書いたアプリの catalog の id、`at` は ISO 8601、記録が無ければ空）。
- `query /secret/<キー>` → 列 `key`・`value`（`gemini.key`・`nas.password`・`nas.deviceToken`。無ければ 0 行、ほかのキーは null）。
- `update /info`（ContentValues：キー → 値の文字列）→ 受け付けた数。`key`・`token`・`secret`・`password` を含む名前は受け付けない。知らない項目も預かって `info` で返す。書いたアプリは呼び出し元のパッケージ名から catalog の id で記録。

### 4.1 同じ端末で共有する項目

| 項目 | キー | 種類 | 同じ端末での共有 | 別の端末へ |
| --- | --- | --- | --- | --- |
| スキン | `ui.skin` | 設定 | ContentProvider の `info` で今の値を返す（承認なしで読んでよい） | Vault の `.theta/settings.json`（§2） |
| Gemini API キー | `gemini.key` | 秘密 | `secret/gemini.key`（利用者の承認でコピー） | しない |
| Gemini のモデル | `gemini.model` | 設定 | `info` | Vault |
| NAS の接続先 | `nas.url`・`nas.user`・`nas.shareRoot` | 設定 | `info` | Vault（パスワードは入れない） |
| NAS のパスワード | `nas.password` | 秘密 | `secret/nas.password`（利用者の承認でコピー） | しない |
| NAS のデバイストークン（Secure SignIn の 2 段階認証を次から省くもの） | `nas.deviceToken` | 秘密 | `secret/nas.deviceToken`（承認でコピー。受け取ったアプリは確認コードなしでログインできる） | しない |
| Google アカウント（どのアカウントを使うか） | `google.account` | 設定 | `info`（メールアドレスだけ） | Vault |

- **Google のログインそのもの（アクセストークン）は共有できない。** Google のトークンはアプリ（パッケージ名＋署名）ごとに発行されるため。共有するのは「どのアカウントを使うか」だけで、各アプリは初回に Google の許可画面を 1 回通す（同じアカウントが選ばれた状態で出す）。
- 秘密を貸すときは、借りる側の画面で「〇〇 Hatch の NAS の設定を使う」のように、どのアプリから何を受け取るかを見せてから読む。貸した側は通知で知らせる。
- 秘密はどのアプリでも端末の中で暗号化して保存する（Android Keystore）。バックアップ・Vault・書き出しには入れない。
- 設定の正本は、どの端末でも「最後に変えたアプリ」の値（`at` が新しい方）。同じ端末では、ほかのアプリの `info` を見て、より新しい値があれば「シリーズに合わせる」項目だけ取り込む。
- デバイストークンを複数のアプリで使い回せるかは、Synology の動き次第（未確認）。使えなければ、アプリごとに一度だけ確認コードを入れる。

### 4.2 アプリの「棚」（`/shelf`）

各アプリが、自分の代表的な中身（ピン留めのメモ、お気に入りのアルバムなど）を Home に見せるための窓口（2026-11-12、Home 1.9.0 の提案から）。Home はアプリごとのタブ（棚）に並べ、Theta Music の棚は音楽が流れていないときにも出す。

- 場所：各アプリの設定のプロバイダ（authority `<applicationId>.theta`、権限 `app.thetahatch.permission.SHARE`、`protectionLevel="signature"`）に `/shelf` を足す。**共通の鍵で署名したアプリ同士でしか読めない**。
- `query content://<applicationId>.theta/shelf` → 1 行 1 つ。列：

  | 列 | 中身 |
  | --- | --- |
  | `section` | まとまりの名前（`pinned`・`favorites`・`recent` など） |
  | `sectionTitle` | まとまりの見出し（例「ピン留め」「お気に入り」「最近再生」） |
  | `id` | そのアプリの中での id |
  | `title`・`subtitle` | 見出しと補足 |
  | `text` | メモの本文の頭など（数行まで。長すぎない） |
  | `image` | ジャケット・写真の `content://` URI（同じプロバイダの `openFile` で出す）。無ければ空 |
  | `action` | 押したときの Intent を `Intent.toUri(Intent.URI_INTENT_SCHEME)` にした文字 |
  | `color` | `#RRGGBB`（メモの色など）。無ければ空 |

- 並びは出したい順。多くても 30 件くらい。中身が変わったら `notifyChange(content://<applicationId>.theta/shelf)` を呼ぶ（Home が読み直す）。
- 見せ方（Home）：`image` がある物（アルバム・写真）は横に並べ、無い物（メモ）は縦のカードにする。
- **安全**：Home は `action` を**そのアプリ宛てに限って**開く（`setPackage(<そのアプリ>)` を付け直し、ほかのアプリの `component` なら開かない）。`/shelf` には秘密（パスワード・トークン・API キー）や、人に見せたくない中身（非公開のメモなど）を入れない。どれを出すかは各アプリの設定で選べるようにする。
- 最初に対応するアプリ：**Memo**（ピン留めのメモ）、**Music**（お気に入り・最近再生したアルバム。押すと再生）。

## 5. Google Cloud は1つのプロジェクトで

手順の全体（共通の設定と、アプリごとの設定の分け方）は `THETA_GOOGLE_SETUP.md`。

- シリーズで1つのプロジェクト（`google.cloudProject` に名前を記録）。APIの有効化（Drive・People・Calendar）、同意画面、テストユーザーは**最初のアプリで1回だけ**。
- 2つ目以降のアプリで要るのは、**Android用OAuthクライアントの追加だけ**（パッケージ名が違うため。SHA-1は共通鍵なら同じ）。
- Web版は同じオリジンなら**同じWebクライアントID**をそのまま使える（`google.webClientId` を引き継ぐ）。
- アプリ内の「Google連携の初期設定ガイド」は、`series` に `google.cloudProject` があれば「プロジェクト作成」「API有効化」「同意画面」「テストユーザー」を済みとして畳み、残りの手順だけを出す。

## 6. Theta Meishi Hatch（最初のアプリ）の対応状況

0.16.0 で実装：

| | 書き出す項目 | 引き継げる項目 | `.theta/settings.json` を読み書きする時 |
| --- | --- | --- | --- |
| Android | モデル・呼び出し形式・Googleアカウント・カレンダー登録先・`google.cloudReady` | モデル・形式・アカウント（端末にあるものだけ）・カレンダー（アカウント＋名前で照合） | Drive同期のたび |
| Windows / Mac | モデル・形式 | モデル・形式 | 起動時と設定を変えた時（Vaultフォルダ＝Googleドライブ for デスクトップが運ぶ） |
| Web | モデル・形式・Googleアカウント・`google.webClientId` | モデル・形式 | Drive同期のたび |

- 画面：ホームに「シリーズの設定を引き継ぐ」（初回だけ）、メニュー →「Theta Hatch シリーズの設定」で項目ごとに「シリーズ共通／このアプリだけ」を切り替え。
- §4：Android の `SeriesProvider`（`content://<applicationId>.theta/info`、`/secret/gemini.key`）。Meishi にキーが無く、同じ鍵で署名したシリーズのアプリがキーを持っていれば、「Gemini APIキー・モデル」に「○○ のキーを使う」が出る。貸した側は通知で知らせる。
- 未実装：デスクトップの `shared-secrets.json`、Web の共通 IndexedDB（2つ目のアプリができた時に、そのアプリと一緒に入れる）、§5 のガイドの畳み込み（`google.cloudProject`）。
