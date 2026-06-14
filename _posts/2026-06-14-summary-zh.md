---
layout: default
title: "Horizon Summary: 2026-06-14 (ZH)"
date: 2026-06-14
lang: zh
---

> 从 15 条内容中筛选出 3 条重要资讯。

---

1. [GLM 5.2 作为完全开放的前沿模型发布](#item-1) ⭐️ 9.0/10
2. [本田思域信息娱乐系统因 AOSP 测试密钥被攻破](#item-2) ⭐️ 8.0/10
3. [人口普查局禁止噪声注入以保护数据隐私](#item-3) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GLM 5.2 作为完全开放的前沿模型发布](https://twitter.com/jietang/status/2065784751345287314) ⭐️ 9.0/10

Z.ai（原智谱 AI）发布了 GLM 5.2，这是一个完全开放的前沿模型，拥有 100 万 token 的上下文窗口，自 2026 年 6 月 13 日起对所有 GLM Coding Plan 用户开放。 此次发布对抗了美国对前沿 AI 模型日益严格的限制，提供了一个全球可访问、开放权重的替代方案，促进了科学开放和竞争。 GLM 5.2 拥有 100 万 token 的上下文窗口、两个新的思考努力级别，并支持工具、推理、结构化输出和温度控制。尽管在某些平台上模型权重被列为封闭，但公告强调其完全开放性。

hackernews · aloknnikhil · 6月13日 16:18 · [社区讨论](https://news.ycombinator.com/item?id=48518684)

**背景**: 前沿模型是最先进的通用 AI 模型，通常需要数亿美元的训练成本。Z.ai 是一家中国 AI 公司，前身为智谱 AI，其 GLM 系列是领先的开源语言模型家族。美国政府近期限制了对某些前沿模型的访问，引发了关于 AI 开放性的讨论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.z.ai/devpack/latest-model">How to Switch Models - Overview - Z.AI DEVELOPER DOCUMENT</a></li>
<li><a href="https://www.buildfastwithai.com/blogs/glm-5-2-review-2026">GLM-5.2 Review 2026: Z.ai's 1M-Context AI Model</a></li>
<li><a href="https://en.wikipedia.org/wiki/Z.ai">Z.ai - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区普遍庆祝此次发布，用户赞扬中国 AI 实验室的开放性，同时批评美国的审查制度。一些人指出 GLM 5.2 可能落后前沿约六个月，但其开放性和低推理成本可能颠覆专有模型提供商。

**标签**: `#AI`, `#open-source`, `#GLM`, `#frontier models`, `#geopolitics`

---

<a id="item-2"></a>
## [本田思域信息娱乐系统因 AOSP 测试密钥被攻破](https://juniperspring.org/posts/honda-evil-valet/) ⭐️ 8.0/10

一名安全研究人员发现，本田思域的信息娱乐系统使用公开的 AOSP 测试密钥签名固件更新，攻击者可通过特制 USB 驱动器实现任意代码执行，且无需 root 权限。 该漏洞揭示了汽车信息娱乐系统普遍存在的安全缺陷，拥有物理接触权限的攻击者可能借此控制车辆电子设备，包括麦克风、摄像头和 GPS。 该漏洞影响运行 Android 4.2.2 的第十代本田思域（2016-2021 款），其更新包使用默认的 AOSP 测试密钥签名，攻击者可通过前 USB 端口刷入自定义固件。

hackernews · librick · 6月14日 00:49 · [社区讨论](https://news.ycombinator.com/item?id=48523080)

**背景**: AOSP（安卓开源项目）为开发提供了默认测试密钥，但生产设备应替换为自定义发布密钥。本田未进行此操作，导致系统存在漏洞。攻击需要物理接触 USB 端口，但无需 root 权限。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/wfairclough/android_aosp_keys">The platform keys that are used as test keys for the AOSP build</a></li>
<li><a href="https://aospinsider.com/courses/aosp-course-1/43-platform-keys-release-keys/">Platform Keys & Release Keys - AOSP Foundations | AOSPInsider</a></li>
<li><a href="https://news.ycombinator.com/item?id=36052753">Show HN: Honda Civic Infotainment Reverse-Engineering | Hacker News</a></li>

</ul>
</details>

**社区讨论**: 评论者就威胁模型展开辩论，有人认为物理接触本就意味着完全沦陷，另一些人则指出这对汽车安全的广泛影响以及车载传感器被用于监视的可能性。少数人称赞系统的开放性允许车主自定义。

**标签**: `#automotive security`, `#embedded systems`, `#vulnerability research`, `#reverse engineering`, `#infotainment`

---

<a id="item-3"></a>
## [人口普查局禁止噪声注入以保护数据隐私](https://desfontain.es/blog/banning-noise.html) ⭐️ 8.0/10

美国人口普查局根据商务部新的行政命令，禁止在其统计产品中使用噪声注入这种统计披露限制方法。 此举移除了一项关键的普查数据隐私保护措施，可能导致个人身份被重新识别，并削弱公众对政府数据收集的信任。 该禁令适用于所有统计产品，包括经济分析局的产品，该局已改用聚合和四舍五入方法。噪声注入通过向数据添加随机噪声来防止个人信息的泄露。

hackernews · nl · 6月13日 13:54 · [社区讨论](https://news.ycombinator.com/item?id=48517377)

**背景**: 噪声注入是一种通过向数据添加微小随机变化来保护隐私的技术，使识别个人变得更加困难。差分隐私是一种更正式的框架，人口普查局在 2020 年人口普查中使用了该技术。该禁令引发了对敏感普查数据安全性的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.bea.gov/help/faq/1490">Why didn’t BEA use noise infusion as its statistical disclosure limitation method in its June 10, 2026, news release on “New Foreign Direct Investment in the United States, 2025’’? | U.S. Bureau of Economic Analysis (BEA)</a></li>
<li><a href="https://www.census.gov/programs-surveys/decennial-census/decade/2020/planning-management/process/disclosure-avoidance/differential-privacy.html">Understanding Differential Privacy</a></li>
<li><a href="https://www.ncsl.org/technology-and-communication/differential-privacy-for-census-data-explained">Differential Privacy for Census Data Explained</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了强烈担忧：一位前人口普查员担心信任丧失和数据被滥用，另一位认为破坏数据收集基础设施是一个错误。还有评论者强调差分隐私对于防止诈骗和欺诈至关重要，并指出聚合数据仍可被重构以识别个人。

**标签**: `#privacy`, `#census`, `#differential privacy`, `#data policy`, `#government`

---