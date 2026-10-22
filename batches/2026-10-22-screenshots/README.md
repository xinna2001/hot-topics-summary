# 首批 9 张截图：热点信息 Skill 实际测试

日期：2026-10-22（Asia/Shanghai）

已完成「读取截图 → 识别线索 → 查找一手资料 → 分析实现 → 写入详细页 → 更新三列索引」流程。9 张用户提供的真实截图按输入顺序收录为 9 个热点，不是虚构测试条目。

## 本批内容

| 图片 | 详细报告 | 核实结果 |
| --- | --- | --- |
| 01 | [Codex 开源维护者计划](../../topics/2026-10-22-codex-open-source/README.md) | 官方活动已定位；资格和权益来自官方索引摘要，全文访问 403，不能保证任意项目获批 |
| 02 | [Piik 屏幕共享](../../topics/2026-10-22-piik-screen-sharing/README.md) | 找到准确仓库，确认 WebRTC P2P、可选 SFU 和自部署；未实机开房间 |
| 03 | [MJ＋可灵视频](../../topics/2026-10-22-midjourney-kling-video/README.md) | 作者回复确认工具组合，可灵公开流程已读取；原参数和完整效果未知 |
| 04 | [dsh 免费与聚合渠道](../../topics/2026-10-22-dsh-free-model/README.md) | 源码实际统计 75 个提供商：68 API Key、2 OAuth、2 ADC、3 本地免认证；不是 75 家无条件免费 |
| 05 | [Anywear 实时试衣](../../topics/2026-10-22-anywear-realtime-vton/README.md) | 找到 Decart 产品、Chrome 扩展和 VTON API；官网写 Beta 限时免费 |
| 06 | [Algora 悬赏机制](../../topics/2026-10-22-algora-bounties/README.md) | 官方仓库确认 Issue/PR、认领和付款链路；未接单、未取得收入 |
| 07 | [AI 控制 Blender](../../topics/2026-10-22-ai-blender/README.md) | 官方 Python API 与社区 MCP 链路可核实；社区方案不代表原作者确实使用 |
| 08 | [AstrBot 微信与人格](../../topics/2026-10-22-astrbot-wechat/README.md) | 当前微信适配器和 persona 源码已读取；扫码有手机版本及 ClawBot 前提 |
| 09 | [BeefTV 视频工作台](../../topics/2026-10-22-beeftv/README.md) | React/Go/Wails、本地工作区、工作流源码已确认；当前许可分为新增 Source Available 与历史 MIT |

## 实际执行的验证

- 9 张原图均成功读取；每张对应一篇报告，记录原消息 ID、文件名与 SHA-256。
- 已核对 6 个 GitHub 项目的固定 commit、README、相关源码和许可信息。
- 已实际读取 Anywear 官网/商店/API、可灵官方指南和接入文档、Blender 官方 Python API。
- 已对 dsh 提供商 JSON 做实际计数与认证类型统计。
- 首页和 CSV 保持「名称 / 详细信息 / 原始链接」三列，9 行顺序与输入一致。
- 已检查所有详细页中的本地证据链接和截图溯源信息。
- 9 条完全相同输入再次执行 upsert 均返回 changed:false；报告、索引和目录数据哈希保持不变。
- catalog.py check 与提交前差异检查通过。

## 实测边界与缺口

本次验证的是截图研究和入库流程。未安装这 9 个线索涉及的软件，未调用生成模型，未扫码登录微信，未申请 Pro、接悬赏或执行付款。详细页中的软件复现步骤均注明“基于资料整理，未实际运行”；dsh 注册表统计除外，已实际运行。

原抖音链接：**0/9 确认**。本轮按作者、项目名和标题检索，没有找到能可靠匹配这些截图的原帖。首页第三列保持“截图提供，原链接待补”。Piik 的关联 B站介绍放在详细页资料区，未冒充截图原视频。

OpenAI 申请页和 Midjourney 参考页本机直读返回 HTTP 403，只使用明确标注的官方搜索索引摘要。Algora 旧文档地址返回招聘页面或 404，已改读当前官方仓库中的流程文档。

技术相关裁剪图随报告保存；手机状态栏、无关聊天与完整原附件不进入仓库。

[返回三列热点索引](../../README.md) · [机器可读验证结果](verification.json) · [输入溯源清单](provenance.json)
