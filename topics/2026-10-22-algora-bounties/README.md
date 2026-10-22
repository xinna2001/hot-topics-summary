# Algora：GitHub Issue 悬赏与贡献者付款

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：平台机制与源码已核实；具体可接单、收益和付款资格未核实

## 一句话结论

GitHub Issue 悬赏确有相应平台。Algora 用 GitHub App 关联 Issue、PR 和奖励，用支付处理器完成付款。AI 可以辅助实现代码，但提交 PR、通过测试或合并，都不能单独证明悬赏已到账。[S1][S2]

## 原始线索

抖音 @Sayumi 的图文展示一段聊天，提到“修好一个bug拿几十到几百美元”“Algora”“AI刷出来的提交”“竞争很凶”。[S0] 这些是截图聊天内容和作者说法，不构成真实接单、收入或付款凭证。没有原帖链接。

本轮读取 Algora 官方仓库 README、悬赏流程文档和相关源码，没有登录接单、发 Issue/PR、声称悬赏或执行支付。

## 技术实现

1. 项目组织安装 GitHub App，建立 Issue/PR 与平台项目的关联。
2. 悬赏和参与尝试存储为 bounty、attempt、claim 等记录。
3. GitHub 事件及平台任务同步请求，追踪认领悬赏的 PR。
4. 维护者确认方案后通过 Reward 链接进入结算。
5. 支付完成后，机器人在 Issue 里发布收款确认。[S1][S2][S3]

当前仓库使用 Elixir/Phoenix 相关模块组织 Web 平台、GitHub 集成、后台任务和支付流程。公开 README 明确列出 web app、GitHub app 与 payment processor 三部分；当前首页侧重开源工程师招聘，不能把旧的“纯悬赏市场”介绍当作完整现状。[S1]

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| 平台有 GitHub Issue/PR 悬赏和付款机制 | 官方 README、文档与源码核实 | S1、S2、S3 |
| 满意方案可以 Reward，付款后有机器人确认 | 官方流程文档核实 | S2 |
| 每个 bug 都值几十到几百美元、可自动赚钱 | 截图宣称，没有通用保证 | S0 |
| AI 生成的提交会被接受 | 依具体项目政策和人工评审决定，本轮未接单 | 无 |

旧 cal.algora.io/bounties/workflow 路径在本轮实际返回招聘页面；docs.algora.io/bounties/workflow 返回 404。为避免错用旧链接，本报告采用当前官方仓库内流程文档。

## 相关项目与资料

- 官方仓库：[algora-io/algora](https://github.com/algora-io/algora)。
- 核实 commit：74a49d7728400152f5d640ac8d461e6664b7c2eb；AGPL-3.0。
- 主要实现：lib/algora/bounties/bounties.ex、lib/algora/bounties/jobs、lib/algora_web，以及 GitHub/支付集成配置。
- [官方平台](https://algora.io/)当前可核实为工程师招聘、合同和悬赏相关服务，不是“AI 零成本被动收入”承诺。

## 复现路径

**平台工作机制已静态核实；未尝试接单或付款。**

1. 选择仍然开放、需求明确的真实悬赏；阅读维护者的范围、认领和 AI 使用政策。
2. 本地复现问题、准备修复、执行项目要求的检查。
3. 提交可审查的 PR，说明修改与验证；如项目要求，按当时流程关联悬赏。
4. 维护者验收后按平台流程奖励，贡献者完成自己所需的收款资料。
5. 以平台付款状态、Issue 确认和真实收款记录核对到账。

成功标准是修复被认可、奖励明确且实际支付。预计报酬应扣除模型调用、开发时间和可能的手续费；本轮没有测算某个真实订单。

## 适用场景与限制

适合已经具备代码阅读、复现与交付能力的开发者参与开源贡献。悬赏不是竞标必胜，也不是任何 PR 自动付费；多个贡献者、项目政策和付款资格都可能影响结果。使用 AI 的声明及验收要求应按维护者明确规则处理。

## 待核实事项

- 原帖地址及截图聊天是否为真实交互。
- 当前开放悬赏、项目认领规则、付款渠道、支持地区与具体手续费。
- 截图所说收益、竞争强度和额度成本对应哪一单，暂无证据。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [截图中的机制描述](evidence/06-source.jpg) | 未知 | 2026-10-22 | Algora 线索与收益说法 |
| S1 | [固定版本 README](https://github.com/algora-io/algora/blob/74a49d7728400152f5d640ac8d461e6664b7c2eb/README.md) | commit 查于本轮 | 2026-10-22 | Web、GitHub App、支付处理器与当前定位 |
| S2 | [创建与奖励悬赏流程](https://github.com/algora-io/algora/blob/74a49d7728400152f5d640ac8d461e6664b7c2eb/priv/content/docs/bounties/in-your-own-repos.md) | 同上 | 2026-10-22 | PR 跟踪、Reward 和支付确认 |
| S3 | [悬赏与 claim 源码](https://github.com/algora-io/algora/blob/74a49d7728400152f5d640ac8d461e6664b7c2eb/lib/algora/bounties/bounties.ex) | 同上 | 2026-10-22 | 悬赏记录、认领与关联方案 |

## 更新记录

- 2026-10-22：从截图定位平台；改用当前仓库文档，明确奖励与到账的不同状态。


## 输入溯源

- 首批图片顺序：6。
- 原消息：om_x100b62aa714898b4ddd28c616e4c1e0。
- 原附件文件名：img_v3_0216n_ada039f5-a40a-4ed3-9c74-414aeb661adg.jpg。
- 原图 SHA-256：fff82282ccc2fbe6229936957d65014bf9c0e7de5a1489494e9199712d5e47e0。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
