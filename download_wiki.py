"""Download all wiki pages from feishu wiki to local markdown files."""
import subprocess, json, os, sys, re
from pathlib import Path

WIKI_URL = "https://my.feishu.cn/wiki/T5dswzVlyiknChk1wl4cWF2hn8g"
OUTPUT_DIR = "feishu-wiki"
LARK_CLI = r"C:\Users\24384\AppData\Roaming\npm\lark-cli.cmd"

def run(cmd):
    cmd[0] = LARK_CLI
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=False, encoding="utf-8", env=env)
    if r.returncode != 0:
        err = r.stderr[:300] if r.stderr else r.stdout[:300]
        print(f"  WARN: {' '.join(cmd[:4])}... failed: {err}")
        return None
    if not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return r.stdout

def sanitize(name):
    name = re.sub(r'[<>:"/\\|?*]', '-', name).strip()
    return name or "untitled"

def fetch_and_save(token, title, path_parts, indent=""):
    sname = sanitize(title) if title else "untitled"
    fname = f"{sname}.md"
    fpath = Path(OUTPUT_DIR, *path_parts, fname)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    print(f"{indent}[Doc] {title or token} -> {fpath}")

    result = run(["lark-cli", "docs", "+fetch", "--doc", token, "--doc-format", "markdown", "--format", "pretty", "--as", "user"])
    if result is None:
        fpath.write_text(f"# {title}\n\n*Failed to fetch content*", encoding="utf-8")
        return

    content = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2)
    md = f"# {title}\n\n{content}" if title else content
    fpath.write_text(md, encoding="utf-8")

def list_children(space_id, parent_token=None, seen=None):
    if seen is None:
        seen = set()
    cmd = ["lark-cli", "wiki", "+node-list", "--space-id", space_id, "--as", "user"]
    if parent_token:
        cmd.extend(["--parent-node-token", parent_token])
    data = run(cmd)
    if not data or not data.get("ok"):
        return []
    return data.get("data", {}).get("nodes", [])

def process_node(node, space_id, path_parts, seen, indent=""):
    nt = node.get("node_token")
    if nt in seen:
        return
    seen.add(nt)

    title = node.get("title", "").strip()
    ot = node.get("obj_token")
    has_child = node.get("has_child", False)

    if ot:
        fetch_and_save(ot, title or nt, path_parts, indent)

    if has_child:
        children = list_children(space_id, nt, seen)
        for child in children:
            child_path = path_parts + [sanitize(title or nt)]
            process_node(child, space_id, child_path, seen, indent + "  ")

def get_root_info(url):
    data = run(["lark-cli", "wiki", "+node-get", "--node-token", url, "--as", "user"])
    if data and data.get("ok"):
        return data["data"]
    return None

def main():
    root = get_root_info(WIKI_URL)
    if not root:
        print("Failed to get root wiki node!")
        sys.exit(1)

    space_id = root["space_id"]
    root_token = root["node_token"]
    root_title = root.get("title", "首页").strip()

    print(f"[Wiki] {root_title}  (space: {space_id})")
    print()

    seen = set()
    fetch_and_save(root["obj_token"], root_title, [], "")
    nodes = list_children(space_id, root_token, seen)
    for node in nodes:
        process_node(node, space_id, [sanitize(root_title)], seen)

    print(f"\n[Done] All pages saved to '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()
