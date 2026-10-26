package jp.yaegaki.theta.hud

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 見本の画面：キットの部品をひと通り並べる。新しいアプリでは、これを見ながら画面を組む。
 * setContent { HudTheme(dark = true) { HudSample() } }
 */
@Composable
fun HudSample() {
    val p = LocalPalette.current
    var q by remember { mutableStateOf("") }
    Row(Modifier.fillMaxSize().background(p.bg)) {
        Column(
            Modifier.weight(1f).verticalScroll(rememberScrollState()).padding(horizontal = 16.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            // 見出し：小さな四角＋等幅の英字ラベル、その下に大きな Oswald
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Box(Modifier.size(6.dp).background(p.accent))
                Text("SYS.EQUIPMENT", color = p.faint, fontSize = 10.sp, fontFamily = Hud.mono, letterSpacing = 2.sp)
            }
            Text("EQUIPMENT", color = p.fg, fontSize = 44.sp, fontFamily = Hud.display, fontWeight = FontWeight.Light)
            Ticks(Modifier.fillMaxWidth().height(6.dp))
            Field(q, { q = it }, "SEARCH  検索", leading = { GlyphIcon(Glyph.SEARCH, p.accent) })

            // 計器の読み：ラベル（等幅・灰）＋値。問題があるものだけオレンジ
            Row(horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                Readout("ITEMS", "042")
                Readout("CHECKED", "039")
                Readout("MISSING", "003", accent = true)
            }

            // 区画：細い線の枠＋四隅のかぎ括弧
            Column(Modifier.fillMaxWidth().border(1.dp, p.line).corners(p.accent, 8.dp).padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("[ LIST ]", color = p.accent, fontSize = 11.sp, fontFamily = Hud.mono, letterSpacing = 2.sp)
                    Text("持ち物", color = p.muted, fontSize = 11.sp)
                    Stripes(Modifier.weight(1f).height(5.dp), color = p.line)
                }
                // 一覧：縞模様（zebra に並び順）、左に種類の札
                listOf("カメラ" to "CAM", "三脚" to "TRI", "充電器" to "PWR", "SD カード" to "MEM").forEachIndexed { i, (name, code) ->
                    RowButton(onClick = {}, zebra = i) {
                        Badge(code, highlight = i == 0)
                        TwoLines(name, if (i == 3) "足りません" else "OK", Modifier.weight(1f))
                    }
                }
            }

            SectionTitle("ACTIONS / 操作")
            FlowRow2 {
                PillButton("確認する", {}, primary = true)
                PillButton("書き出す", {})
                PillButton("使えない", {}, enabled = false)
            }
            Note("注記は灰色の小さな字で。説明は短く。")
            Stripes(Modifier.fillMaxWidth().height(8.dp))
        }
        // 端のタブ（横書きを 90 度倒す）。選んだものはオレンジで塗る
        Column(Modifier.width(46.dp).padding(vertical = 12.dp), verticalArrangement = Arrangement.spacedBy(5.dp), horizontalAlignment = Alignment.End) {
            listOf("LIST", "CHECK", "HISTORY").forEachIndexed { i, label ->
                val on = i == 0
                Box(Modifier.width(40.dp).background(if (on) p.accent else p.bg).border(1.dp, if (on) p.accent else p.line)) {
                    Column(Modifier.padding(top = 4.dp, bottom = 10.dp).align(Alignment.Center), horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("%02d".format(i + 1), color = if (on) p.onAccent else p.faint, fontSize = 9.sp, fontFamily = Hud.mono)
                        VerticalLabel(label, if (on) p.onAccent else p.fg)
                    }
                }
            }
        }
    }
}

/** 押せる部品を横に並べて折り返す。 */
@OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
@Composable
fun FlowRow2(content: @Composable () -> Unit) {
    androidx.compose.foundation.layout.FlowRow(
        Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) { content() }
}
