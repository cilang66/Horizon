"""知识库迭代入口 - 串联 Horizon 日报 → 知识提炼 → 知识库更新"""
import subprocess, sys, os
from pathlib import Path
from datetime import datetime

HORIZON_DIR = Path(r"F:/claudeClode/zhishiku/Horizon")
KB_DIR = Path(r"H:/家人/hp/hp/feishu-wiki")
SCRIPTS = {
    "restructure": HORIZON_DIR / "kb_restructure.py",
    "refiner": HORIZON_DIR / "kb_refiner.py",
}

def run_step(name, cmd, cwd=None):
    print(f"\n{'='*50}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}")
    print(f"{'='*50}")
    r = subprocess.run(cmd, cwd=cwd or HORIZON_DIR, capture_output=False, text=True)
    if r.returncode != 0:
        print(f"[Error] {name} 失败 (exit code {r.returncode})")
        return False
    print(f"[Done] {name} 完成")
    return True

def main():
    print("=" * 60)
    print("  AI短剧知识库迭代系统")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 模式选择
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "restructure"):
        # 第一步：重整目录结构（首次运行 / 按月整理）
        run_step("知识库目录重整", ["python", str(SCRIPTS["restructure"])])
        # 生成 INDEX.md
        run_step("生成知识库索引", [
            "python", "-c",
            f"import sys; sys.path.insert(0, r'{HORIZON_DIR}'); from kb_restructure import generate_index; generate_index()"
        ])

    if mode in ("all", "refine"):
        # 第二步：从 Horizon 日报提炼新知识
        env = os.environ.copy()
        env["DEEPSEEK_API_KEY"] = env.get("DEEPSEEK_API_KEY", "")
        run_step("AI知识提炼", ["python", str(SCRIPTS["refiner"])])

    if mode in ("all", "stats"):
        # 第三步：统计知识库状态
        print(f"\n{'='*50}")
        print("知识库统计")
        print(f"{'='*50}")
        md_files = list(KB_DIR.rglob("*.md"))
        total = len(md_files)
        total_size = sum(f.stat().st_size for f in md_files)
        inbox_files = list((KB_DIR / "_inbox").rglob("*.md")) if (KB_DIR / "_inbox").exists() else []
        print(f"  总文件数: {total} (含 {len(inbox_files)} 个待审核)")
        print(f"  总大小: {total_size/1024:.0f} KB")
        # 按目录统计
        for d in sorted(KB_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                count = len(list(d.rglob("*.md")))
                if count > 0:
                    print(f"    {d.name}: {count} 个文件")

    print(f"\n{'='*60}")
    print("  迭代完成!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
