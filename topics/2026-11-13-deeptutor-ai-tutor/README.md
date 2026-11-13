# DeepTutor：知识库、交互式教材与自适应学习助手

收录日期：2026-11-13
最近核实：2026-11-13，Asia/Shanghai
研究状态：**部分核实**——原片、项目归属、官方文档和指定源码已读取；未安装应用，未验证教学效果。

## 一句话结论

视频对应 **HKUDS/DeepTutor**：它把自己的教材知识库、带引用的问答与出题、可交互的书籍、学习路径和可检查的记忆放到同一个学习工作区。其价值是把学习流程连起来，而不是发现了一个可以保证“所有题都会、所有学生都能教好”的新模型。**“AI 家教界最高的山”是视频作者的评价，不是已验证的行业排名。**[S1–S3]

## 原始线索

- 用户原短链：[https://v.douyin.com/YCY4n6Enh74/](https://v.douyin.com/YCY4n6Enh74/)。分享文本中的 `5.15`、`02/12` 等字符不作为发布日期。
- 规范原作品：[https://www.douyin.com/video/7707504463086814683](https://www.douyin.com/video/7707504463086814683)。作品 ID：`7707504463086814683`。
- 作者：**企鹅加德**；标题/简介：`ai家教界最高的山 #ai #学习 #家教 #开源 #vibecoding`；平台详情时间戳对应 **2026-11-13 12:13:45 +08:00**，网页显示到分钟为 12:13。[S1]
- 实际读取：网页正文、平台作品详情、完整下载的 **40.833333 秒**视频；抽样查看实际媒体时间 `0/4/8/12/16/20/24/28/32/36/40` 秒的画面。**没有逐句听音或执行语音转写，不称为完整视听审查。**画面内印刷的 `TC 00:xx` 是卡片设计文字，不作为媒体时间码。
- 视频主要是仓库介绍和动画卡片：第 40 秒明确写出 **`HKUDS / DeepTutor · Apache-2.0`**；早段的 DeepTutor Logo、官方域名、仓库描述与中文 README 对应。这里的项目归属已确认，不是仅凭标题猜到的相似项目。[S1–S3]
- 卡片介绍了资料整合、问答/出题、交互式教材、学习路线、数学/语言辅助、论文梳理；多张卡片注明“示意”或基于 README 的用法。**动画里的进度百分比和顺畅流程不是实机性能/学习效果测量。**

### 视频画面与核实范围

| 媒体时间 | 画面说法/内容 | 本轮判断 |
| --- | --- | --- |
| 0–4 秒抽样 | DeepTutor 仓库与开源介绍 | 项目归属已核；不是独立排名证据 |
| 8、12 秒 | 教材、论文、PDF 整理成资料库 | 有官方文档和 RAG 源码；扫描件/复杂版式效果未实测 |
| 16 秒 | 一问一答、自动练习题 | 出题 pipeline 存在；题目正确性未实测 |
| 20 秒 | 图表与可交互的书 | Book / interactive HTML 实现存在；本轮未生成课件 |
| 24、28 秒 | 学习路线、动态重排 | 有 Mastery Path、评估和修订工具；未验证真实学生学习收益 |
| 32、36 秒 | 公式拆解、论文知识体系 | 有 Solve/Visualize/Research 等工作流；示意图不证明数学/科研结论可靠 |
| 40 秒 | HKUDS/DeepTutor 与“非常好使” | 仓库与许可证已核；使用体验属于作者评价 |

## 技术实现

### 1. 工作区外壳：Python 后端 + Next.js 前端，而非一个独立“万能模型”

本轮固定读取 `main` 的 commit **`60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db`**；最新正式 Release 为 **v1.7.2**，发布时间 **2026-11-06 08:42:06 UTC**。后端 `deeptutor/api/main.py` 构造 FastAPI 应用；`web/package.json` 声明 Next.js `^16.2.3`、React `^19.0.0`，是依赖范围，不代表本轮运行过该精确解析版本。`pyproject.toml` 要求 Python `>=3.11,<3.15`，CLI 入口为 `deeptutor_cli.main:main`。[S2–S4]

用户按学科/项目建立 workspace：Home 用于对话、任务与笔记，Learning 包含 Book/Mastery Path/Reading/Practice，Resources 保存历史、题库、知识中心；模型、嵌入、搜索、语音等服务由 Settings 配置。普通聊天、解题、研究、出题等模式共用学习上下文，不能把早期版本的“两个固定循环”描述直接套到现在所有功能。[S2–S3]

### 2. 教材知识库：解析与检索是分开的，可选择不同 RAG 引擎

典型链路为：**上传材料 → 按选定解析器提取内容 → 建立指定知识库/索引版本 → 检索相关来源 → 把来源提供给对话或学习工作流**。[S2、S5]

`rag_tool.py:15–51` 先校验查询和 `kb_name`，默认经过用户知识库访问解析，再调用 `RAGService.search`；`services/rag/service.py` 根据知识库绑定选择 pipeline。当前 README 区分 LlamaIndex 默认混合检索、PageIndex 页级推理检索、GraphRAG/LightRAG 图检索及若干外部知识库连接。**每个知识库绑定一个引擎，不是每次问答同时跑遍所有引擎。**[S2、S5]

PDF 也不是“直接扔进去就必定准确”：解析器、图片描述、embedding 服务以及索引配置都会影响结果。官方提供 `deeptutor kb eval`，评估检索排名指标；它不等于验证生成答案的事实正确性或学生的学习提升。[S2]

### 3. 出题与交互教材：生成内容和生成代码都要验证

- `agents/question/pipeline.py` 包含 `_explore`、`_plan`、`_quiz_one` 与 quiz payload 解析/修复等阶段；这是可检查的出题工程，不是只往聊天提示词里写一句“请当家教”。[S6]
- `VisualizePipeline` 分离 AnalysisAgent、CodeGeneratorAgent、ReviewAgent，对应分析、代码生成、按错误修复等方法。[S7]
- `book/blocks/interactive.py` 调用上述 pipeline，指定 `render_mode="html"`，生成 HTML 文档并做本地 `validate_visualization`；失败抛出 `GenerationFailure`。**此 Book HTML 分支不跑 HTML 修复 pass**，不能把 Visualize 的修复能力泛化成所有交互块都会自动修好。文件说明前端以隔离 iframe 呈现；iframe 不是对所有生成脚本的安全审计证明。[S7–S8]

Book 的官方功能包括章节提纲审核、文字/测验/卡片/图表/代码/交互 HTML 等类型化块，以及各章 Page Chat。视频的“能拖的图、能读进去的书”有实现基础，但某个具体图表能否正确交互仍需实际生成、操作和检查。[S2、S8]

### 4. 学习路径：LLM 辅导 + 可持久化的判题/掌握度状态

Mastery Path 在聊天 loop 上增加 `mastery_quiz`、`mastery_grade`、`mastery_assess`、`mastery_revise` 等工具。出题、答案、知识点、来源证据与进度绑定；`mastery_grade` 把判题结果同步到题库，区分 quiz 过关与定性目标的 assessment gate，并在返回值给出 `mastery`、`threshold`、`mastered`、`next`。[S9]

**具体算分不是神秘的“读懂大脑”模型。**`learning/mastery.py:15–39` 的当前策略是最近最多五次作答的加权正确率，权重为 `0.5/0.7/0.85/0.95/1.0`；只积累一次证据时分数上限 `0.5`、两次时 `0.8`，防止偶然答对就被认定掌握。文件明确将 IRT/BKT 等更复杂模型作为可以替换的策略，不能说它已实现这类模型。[S10]

`LearningService.grade_interaction_semantic` 同时有 exact verdict 与语义评估路径：**判题并非全部由确定性代码完成**。来源不充分/不确定时可以保持 `ungraded`，不应产生负面掌握度证据。`mastery` 数值是应用的状态估计，不能当作正式考试能力或认知能力的测量。[S9–S10]

### 5. 持久化、记忆与隐私

- 当前存储文档列出 SQLite 对话/题库/练习数据库、settings、工作区生成内容、用户目录和系统目录。README 的 L1/L2/L3 记忆是可阅读的 trace/facts/synthesis 分层；这些是个性化上下文，不是额外训练一个个人模型。[S2、S11]
- **自托管 ≠ 资料绝不出机器。**原始文件/学习状态可以落在自己的部署中；选用远程 LLM、embedding、云解析或搜索服务时，相关内容仍可能发送给服务商。必须按模型、解析器、RAG 引擎分别确认数据流；不把视频末段“资料留在自己机器上”扩写为无条件离线保证。[S2、S11]
- 代码执行有单独 sandbox 后端选择：runner sidecar、Linux bwrap、管理员显式开启的 restricted subprocess，否则 `exec` 关闭；普通用户执行需要系统级隔离。**不能为了方便安装而默默放开生成代码执行。**本轮只读了配置与文档，未审计全部 sandbox 或多用户权限路径。[S12]

### 关键判断汇总

| 关键判断 | 证据状态 | 依据 |
| --- | --- | --- |
| 原视频对应 HKUDS/DeepTutor | 已核实 | 第40秒明确 owner/repo；官方 README/Logo/域名匹配 |
| Python/FastAPI + Next.js/React，Apache-2.0 | 已核实（源码/许可） | S2–S4；不是运行验收 |
| RAG、出题、交互 HTML、掌握度状态确有实现 | 已核实（实现存在） | S5–S10；未测输出正确率 |
| “最高的山”“非常好使” | 作者评价 | 无统一榜单、测试条件或实测对照支持 |
| 卡片中的即时路线重排与百分比代表真实学习提升 | 未核实 | 视频为动画说明；源码状态机制不等于教育效果 |
| 自托管可以无条件保证全程不外发资料 | 不成立的泛化 | 配置远程服务会产生外部调用；需逐项确认 |

## 相关项目与资料

### 同类选型，而不是单看 Star

以下是 **2026-11-13 查阅快照**，不是完整的 AI 教育市场排名。按关键词检索并实际读取这三个项目，没有发现它们共同参与的统一“家教效果第一”评测；高 Star 只说明关注度。

| 项目 | 当次 Stars / 固定 revision | 路线 | 更适合的需求与边界 |
| --- | --- | --- | --- |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | 58,717 / `60fb3bdf…` | 知识库、工具调用、学习工作区与持久状态 | 想把教材问答、出题、阅读、交互教材连起来；配置/解析/部署门槛较高；Apache-2.0 |
| [JushBJJ/Mr.-Ranedeer-AI-Tutor](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor) | 29,536 / `ea29bcf1…` | 可配置深度、苏格拉底式交流等的家教提示词 | 快速试教学风格，不需要完整应用；README 明确 **DISCONTINUED**；固定树未见许可证文件，不能当作有明确商用再分发许可 [S13] |
| [Nutlope/llamatutor](https://github.com/Nutlope/llamatutor) | 2,054 / `e29ac566…` | Next.js + 搜索材料 + 流式教学聊天 | 想学习简洁 Web 家教实现；Exa/Together 等服务需单独配置；固定树未见许可证文件 [S14] |

LlamaTutor 有一个值得注意的“宣传/源码漂移”：README 仍写 Llama 3.1 70B，当前 `app/api/getChat/route.ts:36–40` 实际指定 **`Qwen/Qwen2.5-7B-Instruct-Turbo`**；`getSources` 用 Exa 获取最多9个来源，每个请求文本上限10,000字符。选择项目不能直接照 README 的模型名推断现在线上运行什么，本轮未访问其线上聊天进行确认。[S14]

**建议：**有自己的教材并想长期积累学习记录，可把 DeepTutor 列为优先试验候选；只想验证苏格拉底式辅导是否适合自己，先试提示词路线更省事；要做小型产品原型，LlamaTutor 的搜索→材料→聊天结构更容易理解。这里不是授权安装/购买/部署其中任何一个产品。

### 官方论文

已读取 [DeepTutor: Towards Agentic Personalized Tutoring](https://arxiv.org/abs/2604.26962) 的摘要与版本历史：v1 于 **2026-04-10** 提交，当前页面为 **2026-07-09 的 v3**。摘要介绍 TutorBench、五个大学课程领域、带学习者档案的学生模拟器以及人类对齐/消融研究，并报告个性化指标平均提升10.8%、五种骨干模型上的通用推理指标提升29.4%。[S15]

这些数字是**作者论文摘要中的实验报告**；本轮没阅读全文表格、没核对基线与统计条件、没重跑，也不是独立实测。大学课程的模拟学习者评估不能直接证明高中课程提分、儿童适用性或“行业最强”。本轮将其用于溯源研究方向，不当作选型胜负的决定性证据。

## 复现路径

**状态：基于实际读取的官方资料整理，未实际安装、启动或调用模型。**本轮下载/抽查的是用户原视频；不是 DeepTutor 的运行验收。

### 推荐最小试验：一份自己的材料 + 可回溯答案 + 一次学习闭环

1. 选择有权使用的、版式清晰的 5–20 页 PDF，手工准备10个问题及对应页码/标准答案；不要先上传未授权教材、内部文件或真实儿童信息。
2. 在独立环境安装固定发布族，避免直接跟随 `dev` 或把 bare `deeptutor` 误认为全量 Web 应用。官方支持 Python 3.11–3.14；PyPI Web 路线要求 Node.js 20.9+。下例是待执行步骤，模型、解析器与数据外发边界应先确认：

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install 'deeptutor[full]==1.7.2'
   deeptutor init
   deeptutor doctor --online
   deeptutor start
   ```

   v1.7.2 README 的默认 Web 入口为 `http://127.0.0.1:3782`，以实际终端输出为准；`doctor --online` 会探测已配置服务，仍不等于业务验收。[S2–S4]
3. 在 Knowledge Center 新建知识库，确认解析后的文字、公式与页码，再等待索引完成。先采用一种 RAG 引擎，不同时叠加多个复杂配置。[S2、S5]
4. 要求解释一页内容并指向来源，再用不同表述追问；记录10题的来源命中、正确性、无法回答时是否诚实保留缺口。教师/学习者检查是必要的，检索指标只是辅助。
5. 从同一材料生成几道题，故意提交一次错误答案、一次正确答案，确认答案、判题、错因、题库记录、掌握度状态相互一致；重启后查看是否持久化。若语义评分不确定，应允许 `ungraded`，不强行判错。[S9–S11]
6. 再生成一个简单的交互内容，例如拖动参数观察函数曲线；检查数值、坐标、交互与隔离。**生成出来≠正确可教**，不要直接拿给学生使用。[S7–S8、S12]
7. 只有以上闭环通过，再考虑更大教材、扫描件、多学科、语音或 IM。分别记录 LLM/embedding/解析/搜索的请求费用与延迟，不宣称开源即无成本。[S2]

### 验收标准

- 引用回到确实支持答案的材料，而非只挂一个文档名。
- 出题的题干、选项、标准答案和解释一致；材料外的内容有清楚标识。
- 判题与学习状态可读回，错误不被吞掉，重启不丢记录，不确定答案不被错误记成失败。
- 交互课件不仅能显示，还能实际操作且数学结果正确。
- 所有选用服务的数据流、成本、权限和代码执行隔离可解释。

上述项目本轮**均未实测**；本次完成的是资料研究与归档。

## 适用场景与限制

- 适合有明确材料与学习目标的个人/课程研究、科研阅读和自托管试验。与普通聊天相比，工程价值在于来源与学习状态的连接。[S2、S5、S9]
- 长 PDF、扫描图片、复杂公式、表格会受解析和检索能力限制；OCR/多模态解析与 embedding 可能增加成本。教材索引正确也不能保证模型推导正确。[S2]
- 当前掌握度是规则/评估驱动的应用估计，不是临床或教育测量，也未证明固定百分比能预测考试成绩。[S9–S10]
- 软件 Apache-2.0 不授予教材、论文、模型权重或 API 的额外使用权；提示词/代码公开但未见许可证的对照项目不能自动视为任意可再分发。[S4、S13–S14]
- 语义评分、生成代码、外部知识库、多用户/代理授权均需要专项验证；本轮未做安全审计或生产上线。

## 待核实事项

1. 视频未提供实际用户的完整操作、模型配置、任务耗时、费用、失败率；顺畅动画不能替代这些证据。
2. 教材解析、生成题正确率、数学动画准确性和动态学习路线对真实学生的效果均未实测。
3. 论文只读摘要/版本记录，尚未核查完整实验设置、人类样本规模、基线和统计分析；未找到可据此验证视频“最高的山”措辞的统一排名。
4. 本轮固定读取的是 `main@60fb3bdf…` 与 v1.7.2 发布信息，不能把它们说成视频作者实际安装的准确版本；代码树、Release 与 README 版本各自留有出处。
5. 自托管、多用户隔离和外部服务的数据流，需要结合真正部署配置重新验收；此报告不提供“绝不外发”保证。

## 来源与证据

查阅日期均为 **2026-11-13（Asia/Shanghai）**。GitHub 源码链接固定到读取的 commit，方便后续区分版本漂移；视频原链不携带分享追踪参数。旁边的 [research_snapshot.json](research_snapshot.json) 保存仓库元数据、媒体摘要、读取路径与文件哈希，不含登录态、个人信息或视频大文件。

| 编号 | 来源与链接 | 发布/版本时间 | 支持的结论 |
| --- | --- | --- | --- |
| S1 | [企鹅加德原视频](https://www.douyin.com/video/7707504463086814683)、[原短链](https://v.douyin.com/YCY4n6Enh74/) | 2026-11-13 12:13:45 +08:00 | 原始宣称、owner/repo、第40秒归档卡、示意演示范围 |
| S2 | [DeepTutor 英文 README](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/README.md) | 固定 main commit；发布列表至v1.7.2 | 功能、配置、安装、记忆、RAG引擎与限制 |
| S3 | [中文 README](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/assets/README/README_CN.md)、[v1.7.2 Release](https://github.com/HKUDS/DeepTutor/releases/tag/v1.7.2) | Release：2026-11-06 08:42:06 UTC | 视频与仓库匹配、当前正式发布版本 |
| S4 | [Python配置](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/pyproject.toml)、[Web依赖](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/web/package.json)、[FastAPI入口](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/api/main.py)、[LICENSE](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/LICENSE) | 固定 commit `60fb3bdf…` | 架构、依赖范围、CLI入口、Apache-2.0 |
| S5 | [RAG工具](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/tools/rag_tool.py#L15-L51)、[RAG服务](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/services/rag/service.py) | 同上 | 显式知识库、访问检查、绑定pipeline与检索 |
| S6 | [出题pipeline](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/agents/question/pipeline.py) | 同上 | explore/plan/quiz生成与结构修复 |
| S7 | [VisualizePipeline](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/agents/visualize/pipeline.py) | 同上 | 分析、生成代码、按错误修复方法 |
| S8 | [Book交互块](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/book/blocks/interactive.py) | 同上 | HTML生成、本地校验、失败处理与iframe说明 |
| S9 | [Mastery工具](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/capabilities/mastery/tools.py)、[Mastery loop](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/capabilities/mastery/loop.py) | 同上 | quiz/assessment gate、题库同步、学习状态 |
| S10 | [掌握度规则](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/learning/mastery.py#L15-L39)、[学习服务语义判题](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/learning/service.py#L3148-L3290) | 同上 | 最近作答加权、证据上限、exact/semantic判题边界 |
| S11 | [Local Data Persistence](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/docs-for-dev/DATA_STORAGE.md) | 同上 | SQLite、settings、工作区与账户存储；不等于全程离线 |
| S12 | [Sandbox配置](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/services/sandbox/config.py) | 同上 | 后端选择、执行关闭条件与隔离等级 |
| S13 | [Mr. Ranedeer README](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor/blob/ea29bcf196d28e70eb31100d00b108ebbacceb96/README.md)、[v2.7提示词](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor/blob/ea29bcf196d28e70eb31100d00b108ebbacceb96/Mr_Ranedeer.txt) | 固定 commit；README标记DISCONTINUED | 提示词路线、个性化教学参数；许可未确认 |
| S14 | [LlamaTutor README](https://github.com/Nutlope/llamatutor/blob/e29ac56679d60140b451466b2b17151cb000d88a/README.md)、[聊天API](https://github.com/Nutlope/llamatutor/blob/e29ac56679d60140b451466b2b17151cb000d88a/app/api/getChat/route.ts)、[搜索API](https://github.com/Nutlope/llamatutor/blob/e29ac56679d60140b451466b2b17151cb000d88a/app/api/getSources/route.ts) | 固定 commit `e29ac566…` | 简单Web辅导结构、Exa来源、README/当前Qwen模型漂移 |
| S15 | [DeepTutor论文摘要与历史](https://arxiv.org/abs/2604.26962) | v1：2026-04-10；v3：2026-07-09 | 作者的TutorBench研究与实验宣称；本轮未复现 |

## 更新记录

- 2026-11-13：首次收录；原短链/视频归属核实，固定v1.7.2发布信息与main源码，对比两种不同家教路线，明确动画示意、效果未实测和自托管数据流边界。
