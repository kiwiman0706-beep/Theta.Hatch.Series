"""移行の進み具合を、各リポジトリの最新のブランチを見て確かめる（Hatch 移行ボードの「Claude が確認」）。

    python tools/check_progress.py [作業用フォルダ] [リポジトリ一覧.json] > progress.json

リポジトリ一覧は GitHub のリポジトリの正式な名前（full_name）の JSON 配列。GitHub は大文字・小文字を区別せず、
改名後も古い名前から転送するので、改名できたかはこの一覧の名前と比べる（Claude は list_repos の結果を渡す）。

catalog/apps.json の各アプリについて、次を ok / ng / unknown で返す：
  rename   新しいリポジトリ名で GitHub に届くか（改名が要るアプリだけ）
  claudemd CLAUDE.md か AGENTS.md に Theta.Hatch.Series への参照があるか
  appid    applicationId が新しいアプリ ID か
  signing  ワークフローが共通の Secret 名（ANDROID_KEYSTORE_B64）を使うか
  update   ハブ（Home・KidsHome）は更新ハブがあるか、ほかはハブに頼む形でインストール権限が無いか（spec §6.1）
  catalog  catalog の current が target と同じか
さらに、各スレッドが書く移行メモ（progress/<id>.md）があれば読み、
  addref・prompt  メモがある＝スレッドが Theta.Hatch.Series を追加して依頼文を受け取った
  plan            メモの「状態」が 作業中・実機確認待ち・完了 なら、計画は OK 済み
  ほかの手順      自動の確認ができていなくても、メモで [x] なら「スレッドは済と報告」と添える
Secret の登録・実機確認は、ここからは見えない（ボード上の自己申告）。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER = "kiwiman0706-beep"
SKIP_DIRS = {".git", "node_modules", "third_party", "build", ".dart_tool"}


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=600)


def renamed(repo, names):
    if names is None:
        return None
    return f"{OWNER}/{repo}" in names


def fetch_latest(repo, work):
    """全ブランチを浅く取り、いちばん新しいコミットのブランチを展開する。"""
    d = work / repo
    if not d.exists():
        d.mkdir(parents=True)
        git("init", "-q", cwd=d)
        git("remote", "add", "origin", f"https://github.com/{OWNER}/{repo}.git", cwd=d)
    if git("fetch", "-q", "--depth", "1", "origin", "+refs/heads/*:refs/remotes/origin/*", cwd=d).returncode != 0:
        return None, None
    best = git("for-each-ref", "--sort=-committerdate", "--format=%(refname:short)", "refs/remotes/origin", cwd=d).stdout.split()
    if not best:
        return None, None
    git("checkout", "-q", "--force", best[0], cwd=d)
    return d, best[0].removeprefix("origin/")


def files(d, pattern):
    for p in d.rglob(pattern):
        if not SKIP_DIRS.intersection(p.parts) and p.is_file():
            yield p


def grep(d, patterns, regex):
    rx = re.compile(regex)
    for pat in patterns:
        for p in files(d, pat):
            try:
                if rx.search(p.read_text(encoding="utf-8", errors="ignore")):
                    return p.relative_to(d).as_posix()
            except OSError:
                pass
    return None


def read_memo(app_id):
    p = ROOT / "progress" / f"{app_id}.md"
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    state = re.search(r"状態[：:]\s*(.+)", text)
    done = set(re.findall(r"^- \[[xX]\]\s*([a-z]+)", text, re.M))
    updated = re.search(r"更新[：:]\s*(\S+)", text)
    return {"state": state.group(1).strip() if state else "", "done": done, "updated": updated.group(1) if updated else ""}


def apply_memo(out, memo, app_id):
    if memo is None:
        return out
    where = f"progress/{app_id}.md"
    out["addref"] = {"s": "ok", "d": f"移行メモあり（{where}）"}
    out["prompt"] = {"s": "ok", "d": "スレッドが移行メモを作成"}
    # テンプレートのまま（「計画中 ／ 計画OK待ち ／ …」）なら、まだ書いていない扱い
    filled = "／" not in memo["state"]
    approved = filled and any(w in memo["state"] for w in ("作業中", "実機確認待ち", "完了", "公開"))
    out["plan"] = {"s": "ok" if approved else "", "d": f"状態：{memo['state'] or '—'}（{memo['updated'] or '日付なし'}）"}
    for key in memo["done"]:
        c = out.get(key)
        if c and c["s"] != "ok":
            c["d"] += "（スレッドは済と報告）"
    return out


def check_app(a, work, names):
    cur, tgt = a["current"], a["target"]
    out = {}
    if cur["repo"] != tgt["repo"]:
        r = renamed(tgt["repo"], names)
        out["rename"] = {"s": "ok" if r else "unknown" if r is None else "ng",
                         "d": f"{tgt['repo']} になっている" if r else "一覧が無く確認できず" if r is None else f"まだ {cur['repo']}"}
    d, branch = fetch_latest(cur["repo"], work)
    if d is None:
        d, branch = fetch_latest(tgt["repo"], work)
    if d is None:
        return out | {"_branch": None}
    hit = grep(d, ["CLAUDE.md", "AGENTS.md"], r"Theta\.Hatch\.Series")
    out["claudemd"] = {"s": "ok" if hit else "ng", "d": f"{hit} に参照あり" if hit else "参照なし"}
    if "android" in a.get("platforms", []):
        pkg = re.escape(tgt["packageName"])
        hit = grep(d, ["build.gradle", "build.gradle.kts"], r"applicationId\s*=?\s*[\"']" + pkg + r"[\"']")
        out["appid"] = {"s": "ok" if hit else "ng", "d": "新しい ID" if hit else f"まだ {cur.get('packageName') or '別の ID'}"}
        hit = grep(d, ["*.yml", "*.yaml"], r"ANDROID_KEYSTORE_B64")
        out["signing"] = {"s": "ok" if hit else "ng", "d": "共通の Secret 名を使用" if hit else "共通の Secret 名を使っていない"}
        if a.get("updateHub"):
            hit = grep(d, ["*.java", "*.kt"], r"app\.thetahatch\.action\.UPDATE")
            out["update"] = {"s": "ok" if hit else "ng", "d": "更新ハブあり" if hit else "更新ハブはまだ（spec §6.1）"}
        else:
            asks = grep(d, ["*.java", "*.kt", "*.dart"], r"app\.thetahatch\.action\.UPDATE")
            perm = grep(d, ["AndroidManifest.xml"], r"REQUEST_INSTALL_PACKAGES")
            ok = asks and not perm
            out["update"] = {"s": "ok" if ok else "ng",
                             "d": "ハブに頼む形" if ok else "インストール権限が残っている" if perm else "ハブに頼む形はまだ"}
    same = cur["repo"] == tgt["repo"] and ("android" not in a.get("platforms", []) or cur.get("packageName") == tgt.get("packageName"))
    out["catalog"] = {"s": "ok" if same else "ng", "d": "一覧は新しい名前" if same else "一覧はまだ古い名前"}
    out["_branch"] = branch
    return out


def main():
    work = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".work"
    names = set(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))) if len(sys.argv) > 2 else None
    work.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((ROOT / "catalog" / "apps.json").read_text(encoding="utf-8"))
    result = {a["id"]: apply_memo(check_app(a, work, names), read_memo(a["id"]), a["id"]) for a in catalog["apps"] if a["id"] != "desk"}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
