"""知识库目录重整脚本 - 将现有文件归类到结构化目录"""
import shutil, re, os
from pathlib import Path

KB = Path(r"H:/家人/hp/hp/feishu-wiki")

# 分类映射规则：关键词 -> (目标目录, 重命名规则)
RULES = [
    # 01-提示词工程
    (["提示词怎么写", "提示词输出格式", "提示词反推", "提示词优化"],
     "01-提示词工程/基础教程"),
    (["进阶优化技巧", "微表情提示词"],
     "01-提示词工程"),
    (["提示词"],
     "01-提示词工程"),

    # 02-图像生成
    (["Gemini 绘图提示词工程师"],
     "02-图像生成/Gemini绘图"),
    (["Gemini三视图", "Gemini 9宫格", "Ai生成多角色", "gemini仿写", "复刻视频", "空拍提示词", "让AI复刻"],
     "02-图像生成/Gemini绘图"),
    (["Gpt-image2", "image2", "Image2", "角色设定"],
     "02-图像生成/Image2角色设定"),
    (["风格参考", "吉卜力", "十二花神"],
     "02-图像生成/风格参考"),

    # 03-视频生成
    (["Seedance2", "种子"],
     "03-视频生成/Seedance2"),
    (["运镜", "镜头运镜", "电影级专业运镜"],
     "03-视频生成/运镜技巧"),
    (["分镜成片工作流"],
     "03-视频生成"),

    # 04-短剧制作
    (["修仙故事", "剧本", "分镜", "人物设定", "制作交付包"],
     "04-短剧制作/修仙故事"),
    (["短剧剧本格式规范"],
     "04-短剧制作"),
    (["故事板提示词"],
     "04-短剧制作"),

    # 05-工具教程
    (["Yt-dlp", "豆包", "Ai Studio", "Google Ai Studio", "9宫格分镜图", "25宫格"],
     "05-工具教程"),
    (["DeepSeek", "GTP5"],
     "05-工具教程"),
    (["大模型提示词优化助手"],
     "05-工具教程"),

    # 宠物拟人Vlong -> 视频生成
    (["宠物拟人"],
     "03-视频生成"),

    # 默认 -> 待分类
    ([], "_inbox/待分类"),
]

def classify(filename, content=""):
    """根据文件名和内容确定目标目录"""
    text = filename + " " + content[:200]
    for keywords, target in RULES:
        if not keywords:
            continue
        for kw in keywords:
            if kw in text:
                return target
    return "_inbox/待分类"

def extract_title(filepath):
    """从md文件提取标题"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("# "):
                return first_line[2:].strip()
    except:
        pass
    return filepath.stem

def restructure():
    # 收集首页下所有子目录的文件
    home = KB / "首页"
    if not home.exists():
        print("[Error] 首页目录不存在!")
        return

    moved_count = 0
    # 递归遍历首页下的所有文件
    for filepath in sorted(home.rglob("*.md")):
        if filepath.name == "首页.md":
            continue

        title = extract_title(filepath)
        target_dir = classify(filepath.stem, title)

        dest_dir = KB / target_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 文件名：用标题或原文件名
        safe_name = re.sub(r'[<>:"/\\|?*]', '-', title or filepath.stem)
        if not safe_name:
            safe_name = filepath.stem
        dest_file = dest_dir / f"{safe_name}.md"

        # 避免覆盖
        counter = 1
        while dest_file.exists():
            dest_file = dest_dir / f"{safe_name}_{counter}.md"
            counter += 1

        shutil.copy2(filepath, dest_file)
        print(f"  {filepath.relative_to(KB)}")
        print(f"    -> {dest_file.relative_to(KB)}")
        moved_count += 1

    print(f"\n共整理 {moved_count} 个文件")

    # 对完成的任务：将分类为空的关键词、或者没有匹配的放入 _inbox/待分类
    # 检查是否有文件还在首页目录
    remaining = list(home.rglob("*.md"))
    remaining = [f for f in remaining if f.name != "首页.md"]
    if remaining:
        print(f"\n⚠ 还有 {len(remaining)} 个文件仍在首页目录下（未被规则覆盖）")
        for f in remaining:
            print(f"  {f.relative_to(KB)}")

def generate_index():
    """生成 INDEX.md 目录索引"""
    lines = ["# AI短剧知识库索引\n", f"更新日期: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n"]

    # 按目录遍历
    for dirpath in sorted(KB.iterdir()):
        if not dirpath.is_dir() or dirpath.name.startswith("_"):
            continue
        if dirpath.name == "首页":
            continue

        md_files = sorted(dirpath.rglob("*.md"))
        # 排除 INDEX.md 自身
        md_files = [f for f in md_files if f.name != "INDEX.md"]

        if not md_files:
            continue

        # 显示中文目录名
        dir_cn = dirpath.name[3:] if re.match(r"\d{2}-", dirpath.name) else dirpath.name
        lines.append(f"\n## {dir_cn}\n")

        for mf in md_files:
            rel = mf.relative_to(KB)
            indent = "  " * (len(rel.parents) - 2)  # simple indent
            # count lines
            try:
                with open(mf, "r", encoding="utf-8") as f:
                    line_count = len(f.readlines())
            except:
                line_count = 0
            lines.append(f"{indent}- [{mf.stem}]({rel}) ({line_count}行)")

    (KB / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nINDEX.md 已生成 ({sum(1 for l in lines if l.startswith('- ['))} 条记录)")

if __name__ == "__main__":
    print("=" * 40)
    print("知识库目录重整")
    print("=" * 40)
    restructure()
    print("\n" + "=" * 40)
    print("生成索引")
    print("=" * 40)
    generate_index()
