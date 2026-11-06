# アプリ ID とリポジトリ名（決定版）

生成ファイル：`python tools/gen_app_ids.py` で `catalog/apps.json` から作る（2026-11-06 時点）。
各スレッドはこの表の自分の行に合わせる。ID は `app.thetahatch.<名前>`、リポジトリ名は `Theta.<名前>.Hatch`。

| アプリ | 新しいアプリ ID | 今のアプリ ID | 新しいリポジトリ名 | 今のリポジトリ名 | 変更 |
| --- | --- | --- | --- | --- | --- |
| Theta Book Hatch | `app.thetahatch.book` | `jp.shinwakai.dsbooks.preview` | `Theta.Book.Hatch` | `Theta.Book.Hatch` | ID |
| Theta Meishi Hatch | `app.thetahatch.meishi` | `jp.yaegaki.meishiclaude` | `Theta.Meishi.Hatch` | `Theta.Meishi.Hatch` | ID |
| Theta Item Hatch | `app.thetahatch.item` | `jp.omoide.closet` | `Theta.Item.Hatch` | `Theta.Item.Hatch` | ID |
| Theta Kamigata Hatch | `app.thetahatch.kamigata` | `jp.yaegaki.kururihair` | `Theta.Kamigata.Hatch` | `Theta.Kamigata.Hatch` | ID |
| Theta DoorPhoto Hatch | `app.thetahatch.doorphoto` | `jp.yaegaki.omoide` | `Theta.DoorPhoto.Hatch` | `Theta.DoorPhoto.Hatch` | ID |
| Theta Label Hatch | `app.thetahatch.label` | `jp.yaegaki.tepravoice` | `Theta.Label.Hatch` | `Theta.Label.Hatch` | ID |
| Theta Device Hatch | `app.thetahatch.device` | `jp.yaegaki.equipment` | `Theta.Device.Hatch` | `Theta.Device.Hatch` | ID |
| Theta Travel Hatch | `app.thetahatch.travel` | `jp.theta.travelhatch` | `Theta.Travel.Hatch` | `Theta.Travel.Hatch` | ID |
| Theta Oekaki Hatch | `app.thetahatch.oekaki` | `jp.theta.oekakihatch` | `Theta.Oekaki.Hatch` | `Theta.Oekaki.Hatch` | ID |
| Theta Mensetsu Hatch | `app.thetahatch.mensetsu` | `jp.yaegaki.theta.mensetsu` | `Theta.Mensetsu.Hatch` | `Theta.Mensetsu.Hatch` | ID |
| Theta Home Hatch | `app.thetahatch.home` | `jp.yaegaki.theta.home` | `Theta.Home.Hatch` | `Theta.Home.Hatch` | ID |
| Theta Memo Hatch | `app.thetahatch.memo` | `jp.yaegaki.theta.memo` | `Theta.Memo.Hatch` | `Theta.Memo.Hatch` | ID |
| Theta KidsHome Hatch | `app.thetahatch.kidshome` | `com.theta.kidshome` | `Theta.KidsHome.Hatch` | `Theta.KidsHome.Hatch` | ID |
| Theta Hitsudan Hatch | `app.thetahatch.hitsudan` | `—` | `Theta.Hitsudan.Hatch` | `Theta.Hitsudan.Hatch` | なし |
| Theta Music Hatch | `app.thetahatch.music` | `com.thetahatch.theta_music` | `Theta.Music.Hatch` | `Theta.Music.Hatch` | ID |
| Theta Photo Hatch | `app.thetahatch.photo` | `photo.theta.theta_photo_hatch` | `Theta.Photo.Hatch` | `Theta.Photo.Hatch` | ID |
| Theta Mitene Hatch（構想中） | `app.thetahatch.mitene` | `—` | `Theta.Mitene.Hatch` | `Theta.Mitene.Hatch` | なし |
| Theta Movie Hatch（設計中） | `app.thetahatch.movie` | `—` | `Theta.Movie.Hatch` | `Theta.Movie.Hatch` | なし |
| Theta File Hatch（試作） | `app.thetahatch.file` | `—` | `Theta.File.Hatch` | `Theta.File.Hatch` | なし |
| Theta Chirashi Hatch | `app.thetahatch.chirashi` | `jp.yaegaki.theta.chirashi` | `Theta.Chirashi.Hatch` | `THETA.Chirashi.Hatch` | ID・リポジトリ名 |
| DeskHatch | `app.thetahatch.desk` | `—` | `deskhatch` | `deskhatch` | なし |

- Google Cloud の Android 用 OAuth クライアントには「新しいアプリ ID」＋共通の SHA-1 を登録する（`secrets/README.md`）。
- Android 版の無いアプリ（Hitsudan・File・DeskHatch）の ID は、デスクトップ版などを作るときに使う。
