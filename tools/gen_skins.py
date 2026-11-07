"""design/skins/skins.json から CSS と Kotlin（Compose）の配色を作る。

    python tools/gen_skins.py          … 書き出す
    python tools/gen_skins.py --check  … 書き出し済みのファイルが JSON と一致するか確かめる（CI 用）
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKINS = ROOT / "design" / "skins"
COLOR_KEYS = ["bg", "panel", "raised", "fg", "muted", "faint", "line", "accent", "onAccent",
              "widget", "launch", "zebra", "accent2", "accent3"]
KT_NAMES = {"dark": "DarkPalette", "light": "LightPalette", "pop": "PopPalette",
            "alert": "AlertPalette", "scifi": "SciFiPalette", "term": "TermPalette", "braun": "BraunPalette",
            "soft": "SoftPalette", "window": "WindowPalette", "lcd": "LcdPalette"}
GOTHIC = 'system-ui, "Noto Sans JP", sans-serif'
OSWALD = '"Oswald", "Noto Sans JP", sans-serif'
TECH = '"Share Tech Mono", ui-monospace, "Noto Sans JP", monospace'
# font の種類 → (見出し, ラベル・数字)
FONTS = {"hud": (OSWALD, TECH), "sans": (GOTHIC, GOTHIC), "mono": (TECH, TECH)}
SHADOWS = {"none": "none", "hard": "3px 3px 0 var(--fg)", "soft": "0 6px 16px rgba(0,0,0,.18)"}
ICON_RADIUS = {"square": "0", "round": "24%", "circle": "50%"}
# 背景の模様（.theta-backdrop に付ける）
BACKDROPS = {
    "scan": "repeating-linear-gradient(to bottom, color-mix(in srgb, var(--accent) 5%, transparent) 0 1px, transparent 1px 4px)",
    "grid": ("repeating-linear-gradient(to right, color-mix(in srgb, var(--widget) 7%, transparent) 0 1px, transparent 1px 28px),\n"
             "    repeating-linear-gradient(to bottom, color-mix(in srgb, var(--widget) 7%, transparent) 0 1px, transparent 1px 28px)"),
    "rain": "repeating-linear-gradient(to right, color-mix(in srgb, var(--accent) 10%, transparent) 0 2px, transparent 2px 18px)",
    "lines": ("repeating-linear-gradient(to right, rgba(255,255,255,.22) 0 1px, transparent 1px 36px),\n"
              "    repeating-linear-gradient(to bottom, rgba(255,255,255,.22) 0 1px, transparent 1px 36px)"),
    "pixel": "repeating-linear-gradient(to bottom, color-mix(in srgb, var(--fg) 3.5%, transparent) 0 1px, transparent 1px 3px)",
}


def css_name(key):
    return "--" + "".join("-" + c.lower() if c.isupper() else c for c in key)


def css_color(v):
    """#RRGGBB はそのまま、#AARRGGBB（Android の書き方）は rgba() にする。"""
    h = v.lstrip("#")
    if len(h) == 6:
        return "#" + h.upper()
    a, r, g, b = (int(h[i:i + 2], 16) for i in range(0, 8, 2))
    return f"rgba({r},{g},{b},{round(a / 255, 3)})"


def kt_color(v):
    h = v.lstrip("#").upper()
    return "0x" + ("FF" + h if len(h) == 6 else h)


def css_block(skin):
    lines = [f"  {css_name(k)}: {css_color(skin['color'][k])};" for k in COLOR_KEYS]
    display, mono = FONTS[skin.get("font", "hud")]
    lines += [
        f"  --radius: {skin.get('radius', 0)}px;",
        f"  --line-width: {'1.5px' if skin['pop'] else '1px'};",
        f"  --hazard: {skin['hazard']}px;",
        f"  --shadow: {SHADOWS[skin.get('shadow', 'none')]};",
        f"  --icon-radius: {ICON_RADIUS[skin.get('iconShape', 'square')]};",
        f"  --display: {display};",
        f"  --mono: {mono};",
        f"  color-scheme: {'dark' if is_dark(skin) else 'light'};",
    ]
    return "\n".join(lines)


def is_dark(skin):
    h = skin["color"]["bg"].lstrip("#")[-6:]
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.5


def make_css(data):
    s = data["skins"]
    out = [
        "/* 生成ファイル：tools/gen_skins.py で design/skins/skins.json から作る。手で直さない。",
        "   <html data-theta-skin=\"" + "|".join(s) + "|system\">（html 以外の要素に付けてもその中だけ切り替わる）。無い・system は端末のダーク／ライトに合わせる。",
        "   書体：<link href=\"https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600&family=Share+Tech+Mono&display=swap\" rel=\"stylesheet\">",
        "   （アプリに同梱するときは design/hud-kit/compose/res/font/ の ttf とライセンスを使う） */",
        ":root {", css_block(s["light"]), "}",
        "@media (prefers-color-scheme: dark) {",
        "  :root:not([data-theta-skin]), :root[data-theta-skin=\"system\"] {",
        "\n".join("  " + l for l in css_block(s["dark"]).splitlines()),
        "  }",
        "}",
    ]
    for name, skin in s.items():
        out += [f"[data-theta-skin=\"{name}\"] {{", css_block(skin), "}"]
    out += [
        "",
        "/* 背景の模様。地を塗る要素に .theta-backdrop を付ける */",
    ]
    for name, skin in s.items():
        if skin.get("backdrop"):
            out += [f"[data-theta-skin=\"{name}\"] .theta-backdrop, .theta-backdrop[data-theta-skin=\"{name}\"] {{",
                    f"  background-image: {BACKDROPS[skin['backdrop']]};", "}"]
    out += [
        "/* ボタン・台の影（POP・WINDOW は右下にずらした影、BRAUN・SOFT は浮き出し） */",
        ".theta-pop-shadow { box-shadow: var(--shadow); }",
        "",
    ]
    return "\n".join(out)


def make_kt(data):
    out = [
        "// 生成ファイル：tools/gen_skins.py で design/skins/skins.json から作る。手で直さない。",
        "// Theta.Home.Hatch の ui/Theme.kt と同じ Palette。アプリに入れるときは package を合わせる。",
        "package app.thetahatch.skin",
        "",
        "import androidx.compose.ui.graphics.Color",
        "import androidx.compose.ui.unit.Dp",
        "import androidx.compose.ui.unit.dp",
        "",
        "data class Palette(",
    ]
    out += [f"    val {k}: Color," for k in COLOR_KEYS]
    out += [
        "    /** POP：角を丸め、線を太く、ボタンに影、書体はゴシック。 */",
        "    val pop: Boolean = false,",
        "    /** 背景の模様：\"\" なし・\"scan\"（走査線）・\"grid\"（方眼）。 */",
        "    val backdrop: String = \"\",",
        "    /** 見出しの上の警告の帯の太さ。 */",
        "    val hazard: Dp = 4.dp,",
        "    /** 作り：hud・pop・term・braun・soft・window・lcd（枠・時計・見出しの形の種類）。 */",
        "    val style: String = \"hud\",",
        "    /** 角丸の大きさ。 */",
        "    val radius: Dp = 0.dp,",
        "    /** 書体：hud＝Oswald＋Share Tech Mono・sans＝端末のゴシック・mono＝全部 Share Tech Mono。 */",
        "    val font: String = \"hud\",",
        "    /** 影：none・hard（右下 3dp の fg 色）・soft（ぼかした浮き出し）。 */",
        "    val shadow: String = \"none\",",
        "    /** アイコンの台：square・round（角丸 24%）・circle。 */",
        "    val iconShape: String = \"square\",",
        ") {",
        "    fun group(g: Int) = when (g) {",
        "        0 -> accent",
        "        1 -> widget",
        "        else -> launch",
        "    }",
        "}",
        "",
    ]
    for name, skin in data["skins"].items():
        out.append(f"/** {skin['label']}：{skin['summary']} */")
        out.append(f"val {KT_NAMES[name]} = Palette(")
        out += [f"    {k} = Color({kt_color(skin['color'][k])})," for k in COLOR_KEYS]
        out += [
            f"    pop = {str(skin['pop']).lower()},",
            f"    backdrop = \"{skin['backdrop']}\",",
            f"    hazard = {skin['hazard']}.dp,",
            f"    style = \"{skin.get('style', 'hud')}\",",
            f"    radius = {skin.get('radius', 0)}.dp,",
            f"    font = \"{skin.get('font', 'hud')}\",",
            f"    shadow = \"{skin.get('shadow', 'none')}\",",
            f"    iconShape = \"{skin.get('iconShape', 'square')}\",",
            ")",
            "",
        ]
    out += [
        "/** 設定 ui.skin の値（system・" + "・".join(data["skins"]) + "）から配色を決める。 */",
        "fun paletteFor(skin: String, systemDark: Boolean): Palette = when (skin) {",
    ]
    out += [f"    \"{name}\" -> {KT_NAMES[name]}" for name in data["skins"]]
    out += [
        "    else -> if (systemDark) DarkPalette else LightPalette",
        "}",
        "",
    ]
    return "\n".join(out)


def main():
    data = json.loads((SKINS / "skins.json").read_text(encoding="utf-8"))
    files = {SKINS / "theta-skins.css": make_css(data), SKINS / "ThetaSkins.kt": make_kt(data)}
    if "--check" in sys.argv:
        stale = [p.name for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            sys.exit("skins.json と一致しない：" + "、".join(stale) + "（python tools/gen_skins.py を実行）")
        print("ok")
        return
    for p, text in files.items():
        p.write_text(text, encoding="utf-8", newline="\n")
        print("wrote", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
