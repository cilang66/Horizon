"""知识提炼引擎 - 从 Horizon 日报中提取新知识，增量更新到知识库

每日流程:
  1. 读取当天 Horizon 生成的日报（重要条目）
  2. 让 AI 判断每条内容是否值得入库
  3. 提取结构化知识
  4. 写入 _inbox 目录
"""
import json, os, sys, re
from pathlib import Path
from datetime import datetime, timezone
from openai import AsyncOpenAI
import asyncio

KB = Path(r"H:/家人/hp/hp/feishu-wiki")
INBOX = KB / "_inbox"
HORIZON_SUMMARY_DIR = Path(r"F:/claudeClode/zhishiku/Horizon/data/summaries")
CHANGELOG = KB / "CHANGELOG.md"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 知识库主题分类
TOPICS = [
    "提示词工程（prompt engineering、提示词写法、优化技巧）",
    "AI图像生成（Stable Diffusion、ComfyUI、Midjourney、Gemini绘图、文生图、图生图）",
    "AI视频生成（Sora、Runway、Seedance、文生视频、图生视频）",
    "AI短剧制作（剧本创作、分镜脚本、角色设定、AI动画制作流程）",
    "AIGC工具教程（ComfyUI工作流、模型下载、工具使用）",
    "行业资讯（公司动态、政策法规、市场趋势）",
]

def get_latest_summary(days=1):
    """获取最近的日报摘要文件"""
    summaries = sorted(HORIZON_SUMMARY_DIR.glob("*.md"))
    if not summaries:
        print("[Warning] No summary files found")
        return None
    return summaries[-1]  # 最新的

def parse_important_items(summary_text):
    """解析日报，提取重要条目"""
    items = []
    current = {}
    for line in summary_text.split("\n"):
        if line.startswith("## "):
            if current:
                items.append(current)
            current = {"title": line[3:].strip(), "content": ""}
        elif line.startswith("- **["):
            # 可能是一条新闻项
            if current and current.get("title"):
                items.append(current)
            current = {"title": line, "content": ""}
        elif current:
            current["content"] += line + "\n"

    if current:
        items.append(current)

    return items

async def extract_knowledge(client, title, content, existing_topics):
    """让 AI 判断一条内容是否值得入库并提取知识"""
    prompt = f"""你是一个AI短剧知识库管理员。请判断下面这条信息是否与 AI短剧制作、AI图像/视频生成、提示词工程相关，如果是，提取为结构化知识。

## 现有知识库目录摘要
{existing_topics[:2000]}

## 信息标题
{title[:200]}

## 信息内容
{content[:2000]}

请按以下JSON格式回复（不要其他文字）：
{{
  "relevant": true/false,
  "topic": "所属主题（从以下选择：提示词工程/AI图像生成/AI视频生成/AI短剧制作/AIGC工具教程/行业资讯）",
  "knowledge_type": "new_tool|new_technique|tutorial|update|news",
  "title": "知识条目标题（中文，简洁）",
  "summary": "核心知识点（100字以内）",
  "key_points": ["要点1", "要点2", "要点3"],
  "related_links": [],
  "action": "add_to_inbox" 或 "skip"
}}
"""

    try:
        resp = await client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[{"role": "system", "content": "你是AI短剧知识库管理员，擅长从技术资讯中提取可复用的知识。"},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=1000,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"[Error] AI call failed: {e}")
        return {"relevant": False, "action": "skip"}

def save_to_inbox(knowledge):
    """将提取的知识写入 _inbox"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[<>:"/\\|?*]', '-', knowledge["title"])[:50]
    filename = f"[{date_str}]{safe_title}.md"
    filepath = INBOX / filename

    lines = [
        f"---",
        f"date: {date_str}",
        f"topic: {knowledge.get('topic', '未分类')}",
        f"type: {knowledge.get('knowledge_type', 'unknown')}",
        f"status: draft",
        f"---",
        f"",
        f"# {knowledge['title']}",
        f"",
        f"## 摘要",
        f"{knowledge.get('summary', '')}",
        f"",
        f"## 要点",
    ]
    for pt in knowledge.get("key_points", []):
        lines.append(f"- {pt}")
    lines.append("")
    if knowledge.get("related_links"):
        lines.append("## 参考链接")
        for link in knowledge["related_links"]:
            lines.append(f"- {link}")

    filepath.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [Inbox] {filename}")
    return filepath

async def main():
    print("=" * 50)
    print("AI短剧知识提炼引擎")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    if not DEEPSEEK_API_KEY:
        print("[Error] 请设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)

    client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

    # 1. 读取最新日报
    summary_file = get_latest_summary()
    if not summary_file:
        print("[Info] 没有找到日报文件，等待 Horizon 首次运行")
        return

    print(f"\n[1] 读取日报: {summary_file.name}")
    summary_text = summary_file.read_text(encoding="utf-8")

    # 2. 提取重要条目
    items = parse_important_items(summary_text)
    print(f"[2] 发现 {len(items)} 个条目")

    # 3. 读取现有知识库目录结构
    existing_topics = ""
    if (KB / "INDEX.md").exists():
        existing_topics = (KB / "INDEX.md").read_text(encoding="utf-8")

    # 4. AI 逐条分析
    print(f"[3] AI 知识提取中...")
    inbox_count = 0
    for i, item in enumerate(items):
        print(f"  [{i+1}/{len(items)}] {item['title'][:50]}", end="")
        knowledge = await extract_knowledge(client, item["title"], item["content"], existing_topics)
        if knowledge.get("relevant") and knowledge.get("action") == "add_to_inbox":
            save_to_inbox(knowledge)
            inbox_count += 1
            print(f" -> relevant ({knowledge.get('topic', '?')})")
        else:
            print(" -> skip")

        # 控制并发
        if i % 5 == 4:
            await asyncio.sleep(1)

    print(f"\n[4] 完成！{inbox_count} 条新知识写入 _inbox/")

    # 5. 更新 CHANGELOG
    log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d')}\n"
    log_entry += f"- Horizon日报提炼: {inbox_count} 条新增到 _inbox\n"
    if CHANGELOG.exists():
        existing = CHANGELOG.read_text(encoding="utf-8")
        CHANGELOG.write_text(log_entry + existing, encoding="utf-8")
    else:
        CHANGELOG.write_text(f"# 知识库变更日志\n\n{log_entry}", encoding="utf-8")

    print(f"[5] CHANGELOG 已更新")

if __name__ == "__main__":
    asyncio.run(main())
