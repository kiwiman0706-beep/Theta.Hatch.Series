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
)

/** 設定 ui.skin の値（system・dark・light・pop・alert・scifi）から配色を決める。 */
fun paletteFor(skin: String, systemDark: Boolean): Palette = when (skin) {
    "pop" -> PopPalette
    "alert" -> AlertPalette
    "scifi" -> SciFiPalette
    "light" -> LightPalette
    "dark" -> DarkPalette
    else -> if (systemDark) DarkPalette else LightPalette
}
