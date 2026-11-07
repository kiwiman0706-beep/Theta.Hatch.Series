// 生成ファイル：tools/gen_skins.py で design/skins/skins.json から作る。手で直さない。
// Theta.Home.Hatch の ui/Theme.kt と同じ Palette。アプリに入れるときは package を合わせる。
package app.thetahatch.skin

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

data class Palette(
    val bg: Color,
    val panel: Color,
    val raised: Color,
    val fg: Color,
    val muted: Color,
    val faint: Color,
    val line: Color,
    val accent: Color,
    val onAccent: Color,
    val widget: Color,
    val launch: Color,
    val zebra: Color,
    val accent2: Color,
    val accent3: Color,
    /** POP：角を丸め、線を太く、ボタンに影、書体はゴシック。 */
    val pop: Boolean = false,
    /** 背景の模様："" なし・"scan"（走査線）・"grid"（方眼）。 */
    val backdrop: String = "",
    /** 見出しの上の警告の帯の太さ。 */
    val hazard: Dp = 4.dp,
    /** 作り：hud・pop・term・braun・soft・window・lcd（枠・時計・見出しの形の種類）。 */
    val style: String = "hud",
    /** 角丸の大きさ。 */
    val radius: Dp = 0.dp,
    /** 書体：hud＝Oswald＋Share Tech Mono・sans＝端末のゴシック・mono＝全部 Share Tech Mono。 */
    val font: String = "hud",
    /** 影：none・hard（右下 3dp の fg 色）・soft（ぼかした浮き出し）。 */
    val shadow: String = "none",
    /** アイコンの台：square・round（角丸 24%）・circle。 */
    val iconShape: String = "square",
) {
    fun group(g: Int) = when (g) {
        0 -> accent
        1 -> widget
        else -> launch
    }
}

/** ダーク：計器盤（HUD）風：黒地にオレンジ 1 色、細い線、四角い角 */
val DarkPalette = Palette(
    bg = Color(0xFF0A0A0B),
    panel = Color(0xFF111113),
    raised = Color(0xFF19191C),
    fg = Color(0xFFEDEDED),
    muted = Color(0xFFA3A3A3),
    faint = Color(0xFF858585),
    line = Color(0xFF333336),
    accent = Color(0xFFFF6B1A),
    onAccent = Color(0xFF0A0A0B),
    widget = Color(0xFFEDEDED),
    launch = Color(0xFF7A7A7E),
    zebra = Color(0x0FFFFFFF),
    accent2 = Color(0xFFFF6B1A),
    accent3 = Color(0xFFFF6B1A),
    pop = false,
    backdrop = "",
    hazard = 4.dp,
    style = "hud",
    radius = 0.dp,
    font = "hud",
    shadow = "none",
    iconShape = "square",
)

/** ライト：明るい地の計器盤：紙のような地に墨色の文字、オレンジは文字にも使えるよう濃いめ */
val LightPalette = Palette(
    bg = Color(0xFFF4F3EE),
    panel = Color(0xFFFFFFFF),
    raised = Color(0xFFE9E8E2),
    fg = Color(0xFF121212),
    muted = Color(0xFF474747),
    faint = Color(0xFF5E5E5E),
    line = Color(0xFFBDBCB4),
    accent = Color(0xFFB8400C),
    onAccent = Color(0xFFFFFFFF),
    widget = Color(0xFF121212),
    launch = Color(0xFF6A6A6A),
    zebra = Color(0x0D000000),
    accent2 = Color(0xFFB8400C),
    accent3 = Color(0xFFB8400C),
    pop = false,
    backdrop = "",
    hazard = 4.dp,
    style = "hud",
    radius = 0.dp,
    font = "hud",
    shadow = "none",
    iconShape = "square",
)

/** POP（カラフル）：クリームの地に墨色の太い線、コーラル・イエロー・ミント。角丸と右下の影、書体はゴシック */
val PopPalette = Palette(
    bg = Color(0xFFFAF6EC),
    panel = Color(0xFFFFFFFF),
    raised = Color(0xFFF2EDE0),
    fg = Color(0xFF2B2B2B),
    muted = Color(0xFF4F4F4F),
    faint = Color(0xFF6B6B6B),
    line = Color(0xFF2B2B2B),
    accent = Color(0xFFEF6F51),
    onAccent = Color(0xFFFFFFFF),
    widget = Color(0xFF7FCFB5),
    launch = Color(0xFFF2BE2E),
    zebra = Color(0x26F5C842),
    accent2 = Color(0xFFF5C842),
    accent3 = Color(0xFFA8E2CF),
    pop = true,
    backdrop = "",
    hazard = 4.dp,
    style = "pop",
    radius = 10.dp,
    font = "sans",
    shadow = "hard",
    iconShape = "round",
)

/** ALERT（警報画面）：黒地に橙の文字、警告の赤と正常の緑。見出しの上に太い警告の帯、背景に走査線 */
val AlertPalette = Palette(
    bg = Color(0xFF050404),
    panel = Color(0xFF0D0908),
    raised = Color(0xFF1A110C),
    fg = Color(0xFFFFD9B0),
    muted = Color(0xFFD6955C),
    faint = Color(0xFF9C6A42),
    line = Color(0xFF5C3418),
    accent = Color(0xFFFF7A00),
    onAccent = Color(0xFF050404),
    widget = Color(0xFFFF2A2A),
    launch = Color(0xFF39E07A),
    zebra = Color(0x14FF7A00),
    accent2 = Color(0xFFFF2A2A),
    accent3 = Color(0xFF39E07A),
    pop = false,
    backdrop = "scan",
    hazard = 10.dp,
    style = "hud",
    radius = 0.dp,
    font = "hud",
    shadow = "none",
    iconShape = "square",
)

/** SCI-FI（操作卓）：黒に近い青緑の地に方眼、黄・水色・緑 */
val SciFiPalette = Palette(
    bg = Color(0xFF060C0E),
    panel = Color(0xFF0B1519),
    raised = Color(0xFF112128),
    fg = Color(0xFFDDF6FF),
    muted = Color(0xFF8FB8C4),
    faint = Color(0xFF5F8794),
    line = Color(0xFF1F3C46),
    accent = Color(0xFFF2E21B),
    onAccent = Color(0xFF060C0E),
    widget = Color(0xFF3FD0E8),
    launch = Color(0xFF7BE38B),
    zebra = Color(0x123FD0E8),
    accent2 = Color(0xFF3FD0E8),
    accent3 = Color(0xFF7BE38B),
    pop = false,
    backdrop = "grid",
    hazard = 6.dp,
    style = "hud",
    radius = 0.dp,
    font = "hud",
    shadow = "none",
    iconShape = "square",
)

/** TERMINAL（緑の端末）：黒地に蛍光の緑、見出しは反転した帯、文字は全部等幅、背景に流れる文字の列 */
val TermPalette = Palette(
    bg = Color(0xFF030805),
    panel = Color(0xFF06100A),
    raised = Color(0xFF0B1E12),
    fg = Color(0xFF8CFFB0),
    muted = Color(0xFF4FC97A),
    faint = Color(0xFF358A55),
    line = Color(0xFF1D5531),
    accent = Color(0xFF3DFF7F),
    onAccent = Color(0xFF031006),
    widget = Color(0xFFC9FFD9),
    launch = Color(0xFF2E9E58),
    zebra = Color(0x143DFF7F),
    accent2 = Color(0xFFC9FFD9),
    accent3 = Color(0xFF2E9E58),
    pop = false,
    backdrop = "rain",
    hazard = 0.dp,
    style = "term",
    radius = 8.dp,
    font = "mono",
    shadow = "none",
    iconShape = "square",
)

/** BRAUN（白い家電）：生成りの地にオレンジ 1 色。めくり時計、丸い日付の文字盤、浮き出た角丸の台、丸いアイコン */
val BraunPalette = Palette(
    bg = Color(0xFFE9E7E1),
    panel = Color(0xFFF6F5F1),
    raised = Color(0xFFDDDAD2),
    fg = Color(0xFF2A2A2A),
    muted = Color(0xFF575757),
    faint = Color(0xFF6E6B64),
    line = Color(0xFFBFBBB1),
    accent = Color(0xFFE8711A),
    onAccent = Color(0xFFFFFFFF),
    widget = Color(0xFF5E7A68),
    launch = Color(0xFF3A3A3A),
    zebra = Color(0x0A000000),
    accent2 = Color(0xFF5E7A68),
    accent3 = Color(0xFFC9C5BA),
    pop = true,
    backdrop = "",
    hazard = 4.dp,
    style = "braun",
    radius = 14.dp,
    font = "sans",
    shadow = "soft",
    iconShape = "circle",
)

/** SOFT（浮き出し）：線を使わず影で台が浮き出る。大きな角丸、淡いオレンジ・青・緑・赤 */
val SoftPalette = Palette(
    bg = Color(0xFFECEDF0),
    panel = Color(0xFFF3F4F7),
    raised = Color(0xFFE3E5EA),
    fg = Color(0xFF262A33),
    muted = Color(0xFF545B68),
    faint = Color(0xFF6B7280),
    line = Color(0xFFD9DCE2),
    accent = Color(0xFFF0A23A),
    onAccent = Color(0xFF262A33),
    widget = Color(0xFF5FA8DC),
    launch = Color(0xFF7FC08E),
    zebra = Color(0x08000000),
    accent2 = Color(0xFFE8606F),
    accent3 = Color(0xFF7FC08E),
    pop = true,
    backdrop = "",
    hazard = 4.dp,
    style = "soft",
    radius = 18.dp,
    font = "sans",
    shadow = "soft",
    iconShape = "round",
)

/** WINDOW（昔のパソコン）：水色の地に白い方眼、クリームの窓にオレンジのタイトルバーと「_ □ ×」、こげ茶の太い線と右下の影 */
val WindowPalette = Palette(
    bg = Color(0xFF52C3D6),
    panel = Color(0xFFFFF8EA),
    raised = Color(0xFFFBEBCF),
    fg = Color(0xFF3B2C27),
    muted = Color(0xFF5E4C44),
    faint = Color(0xFF7D6A60),
    line = Color(0xFF3B2C27),
    accent = Color(0xFFF5A33A),
    onAccent = Color(0xFF3B2C27),
    widget = Color(0xFF7C8DF2),
    launch = Color(0xFFF28DB2),
    zebra = Color(0x14F5A33A),
    accent2 = Color(0xFF7C8DF2),
    accent3 = Color(0xFFF28DB2),
    pop = true,
    backdrop = "lines",
    hazard = 4.dp,
    style = "window",
    radius = 6.dp,
    font = "sans",
    shadow = "hard",
    iconShape = "round",
)

/** LCD（液晶ゲーム機）：くすんだ黄緑の地に濃い緑の太い線と文字、全部等幅、液晶の数字の時計、画素の細い横線 */
val LcdPalette = Palette(
    bg = Color(0xFF8E9B69),
    panel = Color(0xFF99A673),
    raised = Color(0xFFA6B27F),
    fg = Color(0xFF1C2610),
    muted = Color(0xFF2F3D1C),
    faint = Color(0xFF45542C),
    line = Color(0xFF1C2610),
    accent = Color(0xFF1C2610),
    onAccent = Color(0xFFA6B27F),
    widget = Color(0xFF3C5568),
    launch = Color(0xFF6B4A33),
    zebra = Color(0x101C2610),
    accent2 = Color(0xFF3C5568),
    accent3 = Color(0xFF6B4A33),
    pop = false,
    backdrop = "pixel",
    hazard = 0.dp,
    style = "lcd",
    radius = 8.dp,
    font = "mono",
    shadow = "none",
    iconShape = "square",
)

/** 設定 ui.skin の値（system・dark・light・pop・alert・scifi・term・braun・soft・window・lcd）から配色を決める。 */
fun paletteFor(skin: String, systemDark: Boolean): Palette = when (skin) {
    "dark" -> DarkPalette
    "light" -> LightPalette
    "pop" -> PopPalette
    "alert" -> AlertPalette
    "scifi" -> SciFiPalette
    "term" -> TermPalette
    "braun" -> BraunPalette
    "soft" -> SoftPalette
    "window" -> WindowPalette
    "lcd" -> LcdPalette
    else -> if (systemDark) DarkPalette else LightPalette
}
