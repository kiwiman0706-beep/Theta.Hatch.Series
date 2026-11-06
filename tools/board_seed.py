"""Hatch 移行ボード（tracker/migration-board.html）に入れるデータを作る。

    python tools/board_seed.py seed  [progress.json] > ops.json   … 初回：アプリと全体の作業を作る（done は空）
    python tools/board_seed.py check  progress.json  > ops.json   … 確認結果（checks）と meta/run だけを更新

出力は Claude の ArtifactData batch にそのまま渡す操作の配列。利用者が付けた「済」（done）は check では触らない。
"""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID_STEPS = ["secret", "rename", "addref", "prompt", "plan", "claudemd", "appid", "signing", "update", "device", "catalog"]
OTHER_STEPS = ["rename", "addref", "prompt", "plan", "claudemd", "catalog"]
CONCEPT_STEPS = ["addref", "prompt", "claudemd"]

GLOBAL = [
    ("key", "me", "署名鍵を手元に用意する",
     "Meishi の theta-hatch-release.jks と keystore-password.txt。見つからなければ新しく作る（secrets/README.md）。"),
    ("gh", "me", "GitHub CLI を入れてログイン",
     "winget install GitHub.cli → gh auth login。Secret をまとめて配るのに使う。"),
    ("rename", "me", "リポジトリ名を変える（Meishi・Book・Chirashi）",
     "GitHub の各リポジトリの Settings → Repository name。MeishiApp→Theta.Meishi.Hatch、dsbooks→Theta.Book.Hatch、THETA.Chirashi.Hatch→Theta.Chirashi.Hatch。"),
    ("secrets", "me", "Secret を全リポジトリに配る",
     "tools\\sync-secrets.ps1 -Keystore <鍵ファイル>。配る先は tools/repos.txt（改名後の名前）。"),
    ("google", "me", "Google Cloud に新しいアプリ ID を登録",
     "docs/APP_IDS.md の Android アプリ。Android 用 OAuth クライアント＋共通の SHA-1。古い ID の登録は移行が終わるまで残す。"),
    ("music-public", "me", "Theta.Music.Hatch を公開にする", "非公開だとアプリ内の自動更新が Release を読めない。"),
    ("book-branch", "me", "Book の本線ブランチを決める",
     "claude/vigilant-…（1.0.0・デスクトップ版あり）と ccr-fbd7…（0.8.7-preview）に分かれている。"),
    ("suite", "me", "Theta.Hatch.Suite をアーカイブ", "このリポジトリと内容が重複。Settings → Archive this repository。"),
    ("desk", "me", "DeskHatch を Theta.Desk.Hatch にするか決める", "シリーズに入れるならリポジトリ名・appId を揃える。"),
    ("series-public", "me", "Theta.Hatch.Series を公開にするか決める",
     "鍵の値は入っていない。公開にすると各スレッドがリポジトリを追加しなくても読め、Home が catalog を読める。"),
    ("update-hub", "me", "Home・KidsHome のスレッドに「ハブ」（更新・共通設定）を頼む",
     "docs/PROMPT_UPDATE_HUB.md を送る。全アプリの更新をこの 2 つでまとめて行い、ほかのアプリからインストール権限を外す（spec §6.1）。"),
    ("synology-spec", "claude", "Synology 接続の共通仕様を書く",
     "DS1825+・Tailscale・Secure SignIn（確認コード＋デバイストークン）。Book・Home・Music で別々の接続をまとめる。"),
    ("nas-vault", "claude", "Vault の置き場所に NAS を加える",
     "Google ドライブ・Tailscale 経由の NAS・両方。spec/THETA_VAULT_SPEC.md に追記。"),
]


def steps_for(a):
    if a.get("status") in ("concept", "design", "prototype"):
        steps = CONCEPT_STEPS
    elif "android" in a.get("platforms", []):
        steps = ANDROID_STEPS
    else:
        steps = OTHER_STEPS
    if a["current"]["repo"] == a["target"]["repo"]:
        steps = [s for s in steps if s != "rename"]
    return list(steps)


def checks_for(progress, app_id):
    p = progress.get(app_id, {})
    return {k: v for k, v in p.items() if not k.startswith("_")}


def main():
    mode = sys.argv[1]
    progress = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else {}
    catalog = json.loads((ROOT / "catalog" / "apps.json").read_text(encoding="utf-8"))
    today = datetime.date.today().isoformat()
    ops = []
    apps = [a for a in catalog["apps"] if a["id"] != "desk"]
    for i, a in enumerate(apps):
        path = f"apps/{a['id']}"
        if mode == "seed":
            remark = a.get("remark", "")
            ops.append({"op": "set", "path": path, "data": {
                "name": a["name"].replace("Theta ", "").replace(" Hatch", ""),
                "order": i + 1,
                "kind": "concept" if a.get("status") in ("concept", "design", "prototype") else "app",
                "repoNow": a["current"]["repo"], "repoTarget": a["target"]["repo"],
                "idNow": a["current"].get("packageName") or "",
                "idTarget": a["target"].get("packageName") or a["target"].get("appId") or "",
                "thread": a.get("thread", ""), "remark": remark,
                "applies": steps_for(a), "done": {}, "doneAt": {},
                "checks": checks_for(progress, a["id"]),
            }})
        else:
            ops.append({"op": "update", "path": path, "data": {"checks": checks_for(progress, a["id"]), "idNow": a["current"].get("packageName") or "", "repoNow": a["current"]["repo"]}})
    if mode == "seed":
        for i, (gid, who, title, detail) in enumerate(GLOBAL):
            ops.append({"op": "set", "path": f"global/{gid}", "data": {"order": i + 1, "who": who, "title": title, "detail": detail, "done": False}})
    ok = sum(1 for a in progress.values() for k, v in a.items() if not k.startswith("_") and v["s"] == "ok")
    ops.append({"op": "set", "path": "meta/run", "data": {"checkedAt": today, "summary": f"GitHub の最新ブランチを確認（できている項目 {ok}）"}})
    json.dump(ops, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
