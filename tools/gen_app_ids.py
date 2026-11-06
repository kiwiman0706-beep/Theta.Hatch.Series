"""catalog/apps.json から docs/APP_IDS.md（アプリ ID とリポジトリ名の一覧）を作る。

    python tools/gen_app_ids.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    d = json.loads((ROOT / "catalog" / "apps.json").read_text(encoding="utf-8"))
    out = [
        "# アプリ ID とリポジトリ名（決定版）",
        "",
        f"生成ファイル：`python tools/gen_app_ids.py` で `catalog/apps.json` から作る（{d['updated']} 時点）。",
        "各スレッドはこの表の自分の行に合わせる。ID は `app.thetahatch.<名前>`、リポジトリ名は `Theta.<名前>.Hatch`。",
        "",
        "| アプリ | 新しいアプリ ID | 今のアプリ ID | 新しいリポジトリ名 | 今のリポジトリ名 | 変更 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for a in d["apps"]:
        cur, tgt = a["current"], a["target"]
        new_id = tgt.get("packageName") or tgt.get("appId") or "—"
        old_id = cur.get("packageName") or "—"
        changes = []
        if tgt.get("packageName") and cur.get("packageName") and tgt["packageName"] != cur["packageName"]:
            changes.append("ID")
        if tgt["repo"] != cur["repo"]:
            changes.append("リポジトリ名")
        status = {"concept": "（構想中）", "design": "（設計中）", "prototype": "（試作）"}.get(a.get("status", ""), "")
        out.append(f"| {a['name']}{status} | `{new_id}` | `{old_id}` | `{tgt['repo']}` | `{cur['repo']}` | {'・'.join(changes) or 'なし'} |")
    out += [
        "",
        "- Google Cloud の Android 用 OAuth クライアントには「新しいアプリ ID」＋共通の SHA-1 を登録する（`secrets/README.md`）。",
        "- Android 版の無いアプリ（Hitsudan・File・DeskHatch）の ID は、デスクトップ版などを作るときに使う。",
    ]
    (ROOT / "docs" / "APP_IDS.md").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("wrote docs/APP_IDS.md")


if __name__ == "__main__":
    main()
