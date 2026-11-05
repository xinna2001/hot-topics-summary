# HowToGetAlongWithGirls：恋爱教练 Skill、文件记忆与同类选型

收录日期：2026-11-05

最近核实：2026-11-05，Asia/Shanghai

研究状态：**部分核实**。原图明确给出项目名；同名仓库的技能结构、文件和文档差异已核实，但图文没有给出仓库所有者，不能唯一确定作者介绍的是哪一份。未安装技能或运行模型评测。

## 一句话结论

这不是一个新训练的恋爱模型，也不是自动接管聊天的软件，而是一套让现有 AI 按固定流程分析聊天、生成回复草稿、维护对象档案的 **Markdown Skill + 参考知识库**。其可借鉴之处是“任务路由、按需读参考、逐人文件记忆、结构化输出”；所谓兴趣判断与阶段定位仍由宿主大模型推断，不能当作对方真实意愿的测量结果。[S2][S3][S4][S5][S7]

如主要想研究原图展示的轻量结构，可看 `Mayuqi-crypto/HowToGetAlongWithGirls`；如准备进一步选型，建议优先审查 **狗头军师 `shengjidaguai-china/goutoujunshi`**：此次查询为 9,237 stars，明确区分事实/推测/未知，且有可撤销、受同意门禁约束的本地记忆代码。这个建议依据功能与实现边界，不意味着其回答效果已优于其他方案。[S11][S12][S13]

## 原始线索

- 用户原短链：[https://v.douyin.com/Bw7Sgs5gzLs/](https://v.douyin.com/Bw7Sgs5gzLs/)。
- 规范图文地址：[https://www.douyin.com/note/7701033373204017650](https://www.douyin.com/note/7701033373204017650)。作品 ID：`7701033373204017650`。
- 标题：找到了个小众项目。标签含 GitHub、恋爱技巧、人工智能、AI、Claude。
- 作者：西兰花费算力。网页显示发布时间 **2026-10-27 01:42:38，Asia/Shanghai**；配图内部另有 01:41 的截图时间，两者不是同一字段，不混用。
- 实际读取范围：网页正文、作者、发布时间，以及 **1 张加载的图文原图**。原图完整视觉读取，明确写出 `HowToGetAlongWithGirls`、Claude 恋爱教练 Skill、聊天分析、回复建议、阶段模型、对象档案、尊重意愿等内容。没有拿到作者自己的安装环境、运行日志或正式效果评测。[S1]
- 访问过程：桌面 HTTP 为 444；已有下载器详情请求为 403；移动分享页只有路由信息。随后隔离 Chrome 正常渲染公开页面，取得正文与图片；未绕过验证码，也未把登录配置或分享页个人信息提交到仓库。

### 原图与仓库的对应关系

GitHub 同名搜索找到两份功能高度相符的公开仓库：`Mayuqi-crypto/HowToGetAlongWithGirls` 与 `Imzl-zl/HowToGetAlongWithGirls`。两份 README 都包含聊天分析、阶段诊断与对象文件记录，前者还包含原图提到的失败场景参考文件。因此本报告以内容更完整的 **Mayuqi-crypto 版本**作为主要研究对象，保留 Imzl-zl 作为同名候选。[S2][S9][S13]

**已确认的是项目名和功能家族，不是唯一 owner/repo。** 图中未出现 GitHub 地址；GitHub API 也未把这两份仓库标为 fork，不能凭同名、星数或创建时间宣布哪份是原作者仓库。

## 技术实现

### 1. 组件是什么

主入口是 `.claude/skills/dating-coach/SKILL.md`：YAML 头部定义 `name: dating-coach` 和触发描述，正文规定角色、输入信息、任务路由、输出和边界。主研究版本在固定 commit 下有 9 份中文参考文档；另有主入口、测试计划及部分基础参考的英文镜像。仓库没有独立模型权重、推理服务、前端应用、聊天抓取或自动发送实现。[S3][S7]

| 组件 | 实际职责 | 实现性质 |
| --- | --- | --- |
| `SKILL.md` | 判断意图、读取相关参考、约束回答结构 | 提示词/工作规程，不是执行程序 |
| `references/chat-analysis.md` | 根据上下文分析阶段、互动信号和下一步，形成回复草稿 | 大模型按文档推理，没有独立分类器 |
| `references/lifecycle.md` | 描述认识到长期相处、结婚的阶段 | 规则知识，不是持久化状态机 |
| `references/profile-template.md` | 按代号组织档案、摘要、时间线和全局索引 | 宿主 Agent 读写 Markdown 文件 |
| 其余参考 | 知识问答、信号、退出决策、自检、失败场景等 | 按需加载的文字知识 |
| `TESTPLAN.md` | 12 个场景与人工/模型评审标准 | 测试计划，不是本轮跑出的成绩 |
| `skill.sh` | 调用 `clawhub publish` 发布技能 | 发布脚本，**不是安装脚本** |

### 2. 输入 → 路由 → 输出

1. **输入。** 用户粘贴聊天文字、提供截图或描述关系背景。截图识别依赖宿主视觉能力；源仓库没有独立 OCR。分析需要先区分当前对象，并补充会影响判断的背景。[S3][S4]
2. **路由。** 聊天分析读取 `chat-analysis.md`，一般知识问答读取 `knowledge-base.md`，阶段建议读取 `lifecycle.md`；对象相关问题再读取档案模板。这个机制是 Agent 按提示选择文件，不是向量数据库检索或专用 RAG 服务。[S3]
3. **推理。** 让宿主模型结合聊天、档案和规则，生成阶段、信号解释、用户可能的问题及下一步。没有公开的训练集、标定概率或独立准确率报告支撑“兴趣几成”。[S3][S4][S7][S8]
4. **输出。** 规程要求先给对象/阶段标签，再给关键原文解释、一个主推回复及少量下一步。输出是给用户审阅的草稿；仓库没有对微信、飞书等平台实际发送消息的工具。[S3][S4][S7]
5. **记录。** 首次建档或文件保存前征得用户同意，再由有文件权限的宿主写入与更新；仅把文档加入模型知识库，不等于获得文件持久化能力。[S3][S5]

### 3. “对象档案系统”其实是什么

参考文档规定项目根目录下的结构：[S5]

```text
profiles/
├── _index.md       # 对象代号、阶段、趋势等总览
├── _template.md    # 新档案模板
└── <代号>.md        # 单对象背景、当前摘要和时间线
```

分析前读取当前对象档案，作答后更新摘要和时间线，再同步总览。**源树并没有随包提供一个数据库、定时任务或写入脚本**；`_template.md` 与 `_index.md` 也需要宿主在同意后创建。跨会话连续性依赖“文件确实写入 + 下轮确实回读”，不是模型天然永久记忆。[S5][S7]

`.gitignore` 排除了 `profiles/`，并排除了 `.claude/commands/`。前者有助于避免默认提交私人档案，后者能解释 README 声称存在、但当前源树实际缺失的 `/coach` 命令文件；Git 忽略规则本身不等于加密或权限隔离。[S7][S14]

### 4. 阶段不是原图概括的五项就结束

原图概括吸引、平淡、暧昧、恋爱、长期相处五项；当前 `lifecycle.md` 实际列出 **1–6 六个阶段**，最后另有走向结婚；“自我建设”是贯穿过程的阶段 0 底座。这是人工设计的沟通框架，并非经本项目实验验证的关系分类标准。[S1][S6]

### 5. 关键判断与证据状态

| 判断 | 证据状态 | 依据 |
| --- | --- | --- |
| 图文确实介绍 HowToGetAlongWithGirls | 已核实 | 原图明示项目名 [S1] |
| 图文一定介绍 Mayuqi-crypto 这份仓库 | 未确认 | 原图无 owner/repo；同名候选不止一份 |
| 这是 Skill 与文本知识库，而非新模型服务 | 已核实到固定源树 | [S3][S7] |
| 可以用对象文件维持连续上下文 | 已核实为规程；宿主运行未测 | [S5] |
| 能准确区分礼貌与好感、量化兴趣 | 作者/转述宣称，效果未核实 | 有规则和输出模板，无标定结果 [S1][S4][S8] |
| 自动读取聊天软件、自动代发 | 源仓库未实现 | [S7] |
| `/coach` 开箱即可用 | 当前文件不支持该保证 | README 有说明，源树无命令入口 [S2][S7] |
| MIT 许可信息完整 | 不完整 | README 写 MIT，但源树无独立 LICENSE，API license 为 null [S2][S7][S13] |

## 相关项目与资料

### 固定版本和一手入口

星数仅为 **2026-11-05 的查询快照**，不表示实际质量；commit 用于固定本轮证据。原短链和规范图文地址是索引中的原始来源，以下 GitHub 项目只作为研究引用，不混进第三列。

| 项目 | Stars | 固定 commit | 许可核验 | 与原素材的关系 |
| --- | ---: | --- | --- | --- |
| [Mayuqi-crypto/HowToGetAlongWithGirls](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls) | 192 | `af0897f4b55897624a19de48374d436906e26461` | README 标注 MIT；无独立 LICENSE | 同名、功能高度相符；主要研究版本，owner 未被原图证实 |
| [Imzl-zl/HowToGetAlongWithGirls](https://github.com/Imzl-zl/HowToGetAlongWithGirls) | 28 | `2440f4b4a523f7abbb45ffb5a4e2139f1be92f79` | README 标注 MIT；源树无独立 LICENSE | 同名较精简候选，不是独立效果验证 |
| [tomwong001/qingsheng-skill](https://github.com/tomwong001/qingsheng-skill) | 196 | `fd762df2e0ce4b8ec68b0087ba7178761045bd1a` | 已有 MIT LICENSE | 相近的 Claude 技能；不是原图项目 |
| [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi) | 9,237 | `6db7354a4002dc7c448a9c87ffdad8132570c9d3` | 已读取 MIT LICENSE | 更广泛的关系沟通/情绪支持 Skill；不是原图项目 |

`powerycy/goutoujunshi` 的 GitHub API 查询当前返回规范仓库 `shengjidaguai-china/goutoujunshi`；报告采用实际返回的名称，不继续把旧路径当成当前 owner。[S13]

### 同功能选型比较

| 维度 | HowToGetAlongWithGirls（主研究版本） | 情圣 qingsheng-skill | 狗头军师 goutoujunshi |
| --- | --- | --- | --- |
| 主体 | 小型 Skill + 分主题参考 | 平台/阶段/快捷模式较丰富的 Skill | 关系知识库 + 实用指南 + 可选记忆代码 |
| 聊天材料 | 用户文字或截图，依赖宿主读取 | 文字/截图；电脑界面读取依赖宿主 computer use | 文字/截图/转述；可接用户已有 ChatLab 数据 |
| 对象记忆 | 项目 `profiles/*.md`，宿主按规程读写 | `~/.qingsheng/` 下用户与目标文件 | `memory_store.py` 本地 SQLite，启用、暂停与撤销流程 |
| 阶段/输出 | 六阶段规程，固定分析结构 | 七阶段标签、短对话与深度模式、对话树草稿 | 更侧重事实、互惠、选择、下一步与停止条件 |
| 不确定性 | 有信息不足先问，但也要求“兴趣几成” | 对事务互动与恋爱信号作区分 | 明确区分事实/推测/未知，禁止把标签当读心 |
| 自动化边界 | 无消息导出或代发实现 | `[发送]` 标签不等于已经代发；真实发送需用户授权 | 不直接解密或导出聊天软件数据库 |
| 本轮效果评测 | 未运行 | 未运行 | 未运行 |

上述差异来自实际读取的主入口和固定文件树，不把上游宣传的私有语料规模、案例质量或模型测试成绩当成已经独立验证的事实。[S3][S7][S10][S11][S12]

**选择建议：**

- 想学习一个小而直观的 Skill 架构：HowToGetAlongWithGirls 足够有参考价值，但需要解决 `/coach` 文档与实际入口不一致、许可文件不完整等缺口。
- 想比较更完整的工程边界：先看狗头军师；其代码有 `CONSENT_REQUIRED` 和 `MEMORY_PAUSED` 门禁以及限量记忆设计，不只是告诉模型“记住”。本轮只审查源码，不保证已安装或端到端正确运行。[S12]
- 想看 Claude 平台差异与快捷交互：情圣是相近候选；入口还包含版本检查命令，加载前需要审查这些副作用，不把参考资料中的命令直接自动执行。[S10]

## 复现路径

### 本轮实际完成的验证

环境为 macOS；使用现有 Python、GitHub CLI 与隔离 Chrome 做资料读取，未常驻部署服务。

- 原图、正文、日期已读取，明确项目名称。
- 固定 4 个仓库的 commit、星数和许可元信息；读取主研究版本的主入口、分析/档案/生命周期/测试计划/发布脚本及文件树，并检查其所有明确的 `references/...` 文件路径。
- **8/8 本地静态资产检查通过**：入口名、9 份中文参考存在、引用路径存在、当前没有模型/服务实现、`coach.md` 缺失、独立 LICENSE 缺失、`skill.sh` 是发布而不是安装脚本、测试计划包含 12 个用例。这里“通过”表示盘点结果与固定源树一致，**包含对缺失资产的确认，不表示上游功能都合格**。详见 [research_snapshot.json](./research_snapshot.json)。
- 没有安装到希儿或其他宿主，没有调用 Claude 做恋爱分析，没有建立真实对象档案，没有执行 `skill.sh`，也没有运行上游 12 场景评测。

### 基于资料整理的最小复现（未实际运行）

1. 选择支持 Skill 与本地文件读写的宿主，在独立实验目录获取固定版本。不要直接把仓库放入现有私人资料目录。[S3][S5]
2. 审查 `.claude/skills/dating-coach/` 后，按所用宿主的技能规范加载 `SKILL.md` 和参考文件。README 没有提供可保证通用的自动安装命令；当前源树也无 `/coach` 命令文件，不把它当作必然存在的入口。[S2][S7]
3. 用自然语言明确请求使用 `dating-coach`，提供**虚构、成年、已脱敏**的对话和背景；不把真实聊天当作首次测试素材。
4. 先验输入不足场景：预期补问关键背景，而不是直接推断对方心意。再验正常聊天场景：预期引用实际原文、区分已知和不确定、生成一条可审阅草稿；不能把“兴趣几成”当成功率。[S3][S4][S8]
5. 如测试持久化，先明确同意保存到实验 `profiles/`；检查实际档案和 `_index.md` 是否出现；另起会话，核对确实回读、对象不混淆、未编造上一轮事件。[S5]
6. 按 `TESTPLAN.md` 的 12 个场景做模型评审，额外记录模型版本、温度、输入、原始输出、评分与失败样本。上游计划要求至少 9 个达标且退出/边界两个关键场景达标；这只是上游验收口径，不是本轮成绩。[S8]

**建议增加的验收点：**明确拒绝不能被解释成“测试”；删除或拒绝保存后不能声称记住；单句短回复不得给确定的心理结论；A/B 对象切换不得串档；回复草稿不得自动发送；输出中的约定时间、经历和事实必须来自输入。

## 适用场景与限制

### 适用

适合做 Skill 架构样本、沟通复盘草稿、缺信息时的追问、档案连续性实验，以及观察“参考知识 + 文件记忆”如何改变通用模型回答。[S3][S5]

### 主要限制

1. **文本规则不是心理测量。** 项目使用兴趣分级、阶段、外貌/条件与部分社交术语，但没有对应模型标定、真实行为研究数据或公开效果报告。把这些看成上游的方法论观点，不推广为可靠结论。[S4][S7][S8]
2. **边界约束存在，但有解释风险。** 主入口写明尊重意愿、不操控和不骚扰；基础分析参考又把某些表达列入“测试”类别。使用时必须以对方明确意愿为准，不能借规则把拒绝改写为可继续推进的信号。[S3][S4]
3. **保存本地 ≠ 全链路离线。** 档案可能在本地，但宿主把聊天/截图发送到哪个模型服务取决于宿主配置；Git 忽略不提供加密、备份隔离或多人权限。真实素材需最小化、去身份化，先确认保存与处理边界。[S5][S14]
4. **没有性能/成本承诺。** 仓库不要求本地 GPU，却仍依赖宿主推理能力；具体费用、延迟、截图读取能力与结果一致性未测，不能把“技能公开可读”理解成“使用模型零成本”。[S3][S7]
5. **文档有漂移。** README 宣称每个技能文件有英文镜像，实际新增的 5 份中文增强参考没有对应 `.en.md`；README 展示 `/coach`，当前源树却没有该入口。[S2][S7]
6. **许可材料不完整。** 两个同名候选 README 都写 MIT，但缺独立 LICENSE，GitHub 未识别许可。归档只描述这一事实，不把它写成已经核验完整的 MIT 授权。[S2][S9][S13]

## 待核实事项

- 原作者介绍的具体仓库 owner/repo、版本和实际加载方式。
- 原作者是否真的演示运行，还是仅介绍功能；当前素材是项目说明图文，不是可复验的运行证据。
- README 中 `/coach` 的命令文件是否存在于未提交的作者环境；`.gitignore` 排除命令目录，公开树不能还原这部分。
- 同名候选的 LICENSE 文件、完整许可声明与最初来源。
- 原项目在具体宿主/模型下的输出准确性、拒绝识别、资料串档、真实文件持久化和隐私行为。
- 两个同类方案的安装、可选 ChatLab/电脑界面读取和端到端模型评测；本轮只完成资料与关键源码检查。

## 来源与证据

以下源码链接固定到本轮读取的 commit；GitHub API 为查询快照，关键元信息保留在 [research_snapshot.json](./research_snapshot.json)。源码日期是本轮所读 revision 日期，不冒充每个文件的初始发布日期。

| 编号 | 来源与链接 | 发布/版本日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [西兰花费算力原图文](https://www.douyin.com/note/7701033373204017650) | 2026-10-27 01:42:38 +08:00 | 2026-11-05 | 作者、日期、项目名和原图宣称；无 owner/repo |
| S2 | [Mayuqi-crypto README](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/README.md) | revision 2026-07-04 | 2026-11-05 | 项目定位、文档宣称、安装说明和 MIT 字样 |
| S3 | [dating-coach 主入口](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.claude/skills/dating-coach/SKILL.md) | revision 2026-07-04 | 2026-11-05 | 路由、结构化输出、档案规程和边界 |
| S4 | [聊天分析方法论](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.claude/skills/dating-coach/references/chat-analysis.md) | revision 2026-07-04 | 2026-11-05 | 模型推理步骤、信号与回复构造，不是效果验证 |
| S5 | [档案模板与持久化规程](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.claude/skills/dating-coach/references/profile-template.md) | revision 2026-07-04 | 2026-11-05 | profiles 文件组织、先同意后写、逐人回读 |
| S6 | [生命周期参考](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.claude/skills/dating-coach/references/lifecycle.md) | revision 2026-07-04 | 2026-11-05 | 六阶段与自我建设底座 |
| S7 | [固定源树 API](https://api.github.com/repos/Mayuqi-crypto/HowToGetAlongWithGirls/git/trees/af0897f4b55897624a19de48374d436906e26461?recursive=1) | revision 2026-07-04 | 2026-11-05 | 文件存在/缺失、9 份中文参考、无模型/服务实现 |
| S8 | [12 场景测试计划](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.claude/skills/dating-coach/TESTPLAN.md)；[发布脚本](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/skill.sh) | revision 2026-07-04 | 2026-11-05 | 测试仅为计划；shell 用于发布而非安装 |
| S9 | [Imzl-zl 同名候选 README](https://github.com/Imzl-zl/HowToGetAlongWithGirls/blob/2440f4b4a523f7abbb45ffb5a4e2139f1be92f79/README.md) | revision 2026-06-29 | 2026-11-05 | 同名、相符功能与候选歧义 |
| S10 | [情圣主入口](https://github.com/tomwong001/qingsheng-skill/blob/fd762df2e0ce4b8ec68b0087ba7178761045bd1a/skill/SKILL.md)；[README](https://github.com/tomwong001/qingsheng-skill/blob/fd762df2e0ce4b8ec68b0087ba7178761045bd1a/README.md) | revision 2026-09-29 | 2026-11-05 | 七阶段、对象文件、快捷模式及宿主能力依赖 |
| S11 | [狗头军师主入口](https://github.com/shengjidaguai-china/goutoujunshi/blob/6db7354a4002dc7c448a9c87ffdad8132570c9d3/SKILL.md)；[MIT LICENSE](https://github.com/shengjidaguai-china/goutoujunshi/blob/6db7354a4002dc7c448a9c87ffdad8132570c9d3/LICENSE) | revision 2026-09-15 | 2026-11-05 | 事实边界、按需知识、ChatLab 和记忆规程、许可文件 |
| S12 | [狗头军师 memory_store.py](https://github.com/shengjidaguai-china/goutoujunshi/blob/6db7354a4002dc7c448a9c87ffdad8132570c9d3/scripts/memory_store.py) | revision 2026-09-15 | 2026-11-05 | SQLite、同意/暂停门禁、记忆大小限制；仅源码检查 |
| S13 | GitHub 仓库 API：[主研究版本](https://api.github.com/repos/Mayuqi-crypto/HowToGetAlongWithGirls)、[同名候选](https://api.github.com/repos/Imzl-zl/HowToGetAlongWithGirls)、[情圣](https://api.github.com/repos/tomwong001/qingsheng-skill)、[狗头军师](https://api.github.com/repos/shengjidaguai-china/goutoujunshi) | 实时查询；摘要已归档 | 2026-11-05 | 名称、星数、创建/提交日期、license 元信息 |
| S14 | [.gitignore](https://github.com/Mayuqi-crypto/HowToGetAlongWithGirls/blob/af0897f4b55897624a19de48374d436906e26461/.gitignore) | revision 2026-07-04 | 2026-11-05 | profiles 与 commands 目录排除规则 |

## 更新记录

- 2026-11-05：首次收录；读取抖音正文与1张原图，研究两个同名候选、情圣与狗头军师，固定源码证据，记录 `/coach`、英文镜像和 LICENSE 的缺口。完成静态资产检查，未安装或进行模型实测。
