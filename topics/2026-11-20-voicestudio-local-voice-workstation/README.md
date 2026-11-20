# VoiceStudio：本地 AI 声音工作室、模型授权与 Palash 的小城创业

收录日期：2026-11-20
最近核实：2026-11-20（Asia/Shanghai）
研究状态：**部分核实**——项目身份、当前规模、主要源码入口和许可已核对；音质、性能、完整离线执行及历史榜首未实测/独立验证。

## 一句话结论

VoiceStudio 的价值是把声音克隆、语音设计、转写、视频翻译配音和有声书制作整合成**本地优先、可换引擎的工作室**，不是 Palash 独自训练了一个覆盖所有任务的新语音模型。可以不购买语音 API、不注册账号使用免费本地版，但 **“免费软件”不等于“默认模型可商用”，“本地优先”不等于“任何模式都不联网”，“646”不等于“每个引擎及所有转写/翻译都支持646种语言”**。[S3-S12,S23]

## 原始线索

- 用户原短链：https://v.douyin.com/saen9p66nv4/ 。确认对应 https://www.douyin.com/note/7709876715334067816 。
- 实际类型是**抖音图文，四张图片**，不是已观看的技术演示视频。发布者「每天认识一个Github用户」；页面发布时间 **2026-11-19 21:39:19（北京时间）**；标题「印度的一座小城，走出11万星的开源大神」。已通过浏览器读取展开后的正文，下载并查看四张原图拼图；未听背景音乐，也没有执行项目演示。[S1]
- 图1为 Palash 的 GitHub 个人页；图2显示 VoiceStudio 约114k Star/12.7k Fork；图3是另一条社交帖子截图；图4是项目首页/榜首徽标。截图中的另一条帖子没有可确认的独立 URL，不作为独立证据。
- 主要宣称：在阿加尔塔拉创业、招不到资深工程师就做三个月/12人训练营；2026-04-09建仓；七个多月超过11万Star；本地免费克隆/配音/转写/有声书；646语言；MCP接入编程助手；2026-09-28全球热门第一。

## 身份、时间与规模核验

| 说法 | 核验结果 | 证据状态 |
| --- | --- | --- |
| 原项目为 debpalash/VoiceStudio，作者 Palash Debnath | GitHub 身份、README 核心成员表与原图一致；Shimul Debnath（velixio）被列为核心成员 | 已核实 [S2,S3] |
| 2026-04-09 创建仓库 | API `created_at=2026-04-09T21:40:26Z`；这是UTC日期，北京时间为**4月10日05:40:26** | 已核实，需保留时区 [S2] |
| 目前11万多Star、1.2万多Fork | 本次API快照 **115,144 Star、12,810 Fork**；观察时间 2026-11-20T22:17:41+08:00。原图约114k与当天量级相符，但本次快照不能倒推11月19日精确计数 | 当前数字已核实；历史精确计数未核实 [S1,S2] |
| 2026-09-28 GitHub全球热门第一 | 原图有榜首徽标；未获取对应日期的 GitHub 榜单独立存档，Trendshift页面本次HTTP403 | 仍是原材料宣称，不把今天徽标当历史证据 [S1] |
| 在 Agartala 建 Yupcha、200条招聘评论、三个月12名额训练营 | 作者2026-07-07文章确实自述这些细节；Yupcha官网确有AI面试产品 | 已核对作者自述；评论数、人数和入职结果无独立审计 [S13] |
| 全部功能免费、所有场景都不用账号 | 免费AGPL本地版无需账号；Pro为另一个闭源付费构建，需账号；README把Cloud标为尚未发布的early access | 已核实边界，不能混称 [S3,S11] |

## 技术实现

### 1. 桌面、后端、模型的分工

当前源码以 **Electron + React** 实现桌面/网页界面，Python/FastAPI作为本地后端，工作流经本地API调用模型与FFmpeg。检索固定commit的`package.json`、`electron/package.json`、`backend/main.py`确认这一层次。作者7月文章仍写Tauri，那是历史架构；当前隐私文档明确提示Tauri外壳已移除，不能用旧文章描述现版本。[S3,S11,S14,S24]

`model_catalogue.py`从`backend/config/models.yaml`读取模型目录，按HF仓库/模型ID管理下载与缓存；`tts_backend.py`定义统一TTS接口并为不同引擎提供适配器，另有ASR接口与引擎。默认合成来自 **Han Zhu及合作者的k2-fsa/OmniVoice**，而不是Palash研发的底层模型。[S6,S7,S23]

### 2. 声音克隆与语音设计

输入是有权使用的参考声音、目标文本及语言/风格参数。OmniVoice将参考声音编码成可复用的voice-clone prompt，再结合文本进行生成；这是参考条件驱动的zero-shot克隆，**不等于每新增一个人都训练/微调一套模型**。上游README将其描述为diffusion language model式架构；声线设计则由支持此功能的引擎处理描述/属性。具体支持以所选引擎为准，预设音色型引擎并不都支持克隆。[S6,S7,S23]

VoiceStudio指南建议5–15秒干净语音，接受较长片段但处理策略各异；默认OmniVoice对长参考取信息量较高的15秒窗口、适配20秒约束，VoxCPM2另有30秒策略。未在本次实测相似度或跨语言口音一致性。[S6,S7]

### 3. 视频翻译配音

不是简单“视频丢给一个模型”：[S8]

1. 本地视频或指定URL导入，FFmpeg抽取**16kHz单声道ASR轨**，另抽**44.1kHz双声道高质量轨**供人声/背景分离；Demucs为可选阶段，失败可能降级。
2. ASR获得文字与时间戳，按配置做分段/说话人处理；说话人分离可能依赖pyannote等单独组件与HF授权，不能假定开箱即用。
3. 选择翻译器。Argos和NLLB是本地路径；Google/DeepL/其他在线API不是本地。Cinematic流程增加LLM反思与改写，`translator.py`的默认兼容端点为OpenAI，也可配置本机Ollama等；若未配置/不可达会回退字面译文并带错误标记。
4. 各片段按声线合成，`dub_generate.py`按缓存/参数/语言处理生成，再依据策略做时长匹配、保音高拉伸或Smart Fit及轨道拼接。
5. 输出配音轨、字幕与合成视频。**时长匹配不是嘴唇形状重绘，不能把它宣传成已验证lip-sync。**字幕内容、人物身份、语义和配音溢出仍需验收。

### 4. 有声书与长文本

`audiobook.py`提供规划与渲染接口，导入文本/Markdown/EPUB/PDF，按章节及`[voice:NAME]`等标记生成；章节与片段级content-addressed缓存支持续跑/局部重渲染。`longform_render.py`生成FFmpeg concat及FFMETADATA章节信息，合成含章节标记的M4B等格式；不是把整本书一次塞进TTS。文档存在这些流程，本次没有导入或朗读书稿。[S9]

### 5. API与MCP

后端挂载 `/mcp/`，编程助手可以使用`generate_speech`、`clone_voice`、`design_voice`、`transcribe`等工具；`generate_speech`转向本地`/generate`，返回audio_id、音频时长和生成时间等字段。文档提供Claude Code/Cursor/Codex配置。[S10]

特别要注意：默认`resources`模式可能把WAV base64回到**Agent上下文**。即使合成在本机，如果Agent随后将上下文交给云端LLM，数据仍可能外流。可配置`OMNIVOICE_MCP_OUTPUT_MODE=files`和明确共享的`OMNIVOICE_MCP_BASE_PATH`，返回文件路径/音频URL而不是大段音频；这减少上下文负担，并不自动证明所有Agent后续调用都离线。[S10；外流判断为基于返回合同的条件推论]

### 关键源码索引（固定快照）

研究commit：`17a70e1368d8b823a670fed822a2ece6894e5bc5`（提交时间2026-11-20T13:52:28Z）。该main快照`package.json`为**0.5.9-beta.7**；稳定release元数据为**v0.5.8，2026-11-12发布**。下述源码结论不自动等于稳定安装包行为。[S17,S24]

| 入口 | 实际核对内容 |
| --- | --- |
| [tts_backend.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/tts_backend.py#L1869) | 默认OmniVoice适配器；统一接口与每引擎语言约束 |
| [model_catalogue.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/model_catalogue.py#L19) | YAML模型目录、ID与HF缓存识别 |
| [dub_pipeline.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/dub_pipeline.py#L1636) | 导入、抽音轨、分离与素材缓存 |
| [dub_generate.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/dub_generate.py#L529) | 分段生成、重渲染、时长策略与水印路径 |
| [translator.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/translator.py) | 字面译文→反思→改写；OpenAI兼容端点和降级 |
| [audiobook.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/audiobook.py) / [longform_render.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/longform_render.py) | 章节规划、缓存和FFmpeg封装 |
| [mcp_server.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/mcp_server.py#L924) | MCP工具→本地HTTP API；文件/base64返回合同 |
| [profiles.py](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/profiles.py#L1271) | 录音/声明授权记录，非生物身份验证 |

## 三个容易误读的边界

### 646不是全流程覆盖保证

`docs/languages.md`明确说**该目录描述OmniVoice模型**，本次计数得到646行。其他TTS有各自语言集，并有“不支持则拒绝”的校验。ASR指南列出Whisper、Parakeet等不同集合，Uyghur示例甚至明确“OmniVoice可合成，但Whisper不可转写”，翻译器又是第三套集合。原图“视频配音支持646种语言”及MCP文档`transcribe`表中的646不能直接用来证明实际转写/翻译能力，更不能代表646种语言均有相同克隆音质。[S6,S10]

### 本地优先不等于永远不联网

| 模式/功能 | 处理边界 |
| --- | --- |
| 免费开源本地引擎 | 核心音频、文本和项目由本地后端处理；无需VoiceStudio账号/API订阅 |
| 首次模型/依赖下载、更新检查 | 需要访问分发服务器；模型准备完成前不是即刻可离线 |
| 远程后端 | 整个后端与项目运行在另一台机器；“自己的GPU”也已越过当前电脑边界 |
| 在线翻译、OpenAI兼容ASR、Cinematic云端LLM | 文本/音频按选中功能发往相应端点；本机端点才可能仍在本机 |
| 免费版分析/自动错误报告 | 固定commit隐私文档描述独立opt-in；不是上传音频/正文的合同，但本次未抓包验证 |
| Pro/Cloud/网页预览 | Pro有账号/许可/设备与用量元数据；**官网说明Pro桌面用量元数据自动发送、无关闭开关**，不能套用免费版opt-in说明；网页TTS预览和Cloud是独立服务 |

上述免费版和Pro应分别看开源仓库文档与官网2026-11-04隐私政策。Pro关于文本/音频仍留本地的承诺不能推导“没有任何外发数据”。作者8月文章也专门解释local-first边界；本次该文章Markdown只收到前1360/5585字节，读取其关于默认loopback与可选remote的开头，不声称已读全文。[S11,S12,S15]

### 软件许可、权重许可、声音同意是三件事

- **应用代码：AGPL-3.0-only。**允许遵循AGPL的商业及内部使用，并非“公司使用就必须付费”。修改版通过网络向他人提供时有对应源码义务；闭源嵌入等另行商业许可需按实际架构审查。本报告不是法律清关。[S4]
- **默认OmniVoice代码：Apache-2.0；预训练权重：CC-BY-NC。**上游模型卡明确因训练数据约束非商用，未在该段明确CC版本；tokenizer还有Boson Higgs Audio 2/Meta Llama社区条款、归属声明及额外商用条件。购买VoiceStudio Pro/商业代码许可**不会覆盖这些第三方权重/组件**。F5-TTS同样是MIT代码、预训练权重CC-BY-NC，不是天然的商用替代方案。[S4,S5,S20]
- **声音/录音与书稿：需授权。**官方使用政策禁止误导性冒充、诈骗等；应用有授权声明/录音留存和AudioSeal合成水印路径，但声明记录不是实际持有人生物验证，也不保证杜绝滥用。水印依赖可用性和配置，文档明确加载失败时可能继续无隐形水印。用途政策与模型许可限制不要写成“AGPL本身附加了用途禁止条款”。[S5,S11,S16]

## 相关项目与同类比较

本次先查GitHub的高Star声音克隆/视频配音候选，再读下面各仓库固定快照README及代码许可证。**这是功能与许可范围的静态对比，不是音质/速度/易用性实测排名。**没有在这组候选中找到Star高于VoiceStudio且覆盖完全相同全链路的替代物，也不能据此宣称全GitHub唯一或最好。

| 项目 | 本次Star | 代码许可 | 与本线索的关系/更适合的方向 |
| --- | ---: | --- | --- |
| VoiceStudio | 115,144 | AGPL-3.0-only | 多引擎声音工作室、配音、有声书、API/MCP整合；模型授权与模式选择仍需单独审查 |
| [Voicebox](https://github.com/jamiepine/voicebox) | 60,973 | MIT | 同类本地声音工作室，README列8个TTS引擎/23语言、听写、故事编辑器、REST/MCP，当前为Tauri；是否覆盖同等视频译配音未在本次确认 [S18] |
| [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | 64,140 | MIT | 少样本微调、中文/粤语/英日韩克隆和训练数据工具更贴近定制音色；不是独立全流程视频翻译工作室；VoiceStudio可接其外部API服务 [S6,S19] |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | 15,629 | MIT | Flow Matching TTS与推理/训练研究；预训练权重非商用；不是整套桌面工作室 [S20] |
| [pyVideoTrans](https://github.com/jianchang512/pyvideotrans) | 19,783 | GPL-3.0 | 更聚焦ASR→字幕翻译→多人配音→视频合成与逐阶段人工校对；支持本地及在线API，不能默认全离线 [S21] |
| [ebook2audiobook](https://github.com/DrewThomasson/ebook2audiobook) | 20,589 | Apache-2.0 | 更聚焦电子书输入、章节/元数据及多种有声输出；1696语言是项目目录宣称，不等于全部模型支持克隆或商用 [S22] |
| [OmniVoice](https://github.com/k2-fsa/OmniVoice) | 16,731 | Apache-2.0代码 | **底层上游，不是竞争工作室**；模型与推理API支持600+语言、参考条件克隆/设计，权重另受CC-BY-NC约束 [S5,S23] |

各项目精确commit和证据哈希见同目录`research_snapshot.json`。除了已在VoiceStudio引擎文档列明的适配关系，不把这些相似项目说成Palash实际用过的组件。

**选型建议：**非商用、个人本地试用可将VoiceStudio当整合工作台候选；主要任务是视频交付先与pyVideoTrans对比；主要任务是批量章节有声书对比ebook2audiobook；追求中文定制训练对比GPT-SoVITS。给客户做商用或训练数据生产时，先审查确切权重版本/组件、声音及文本权利，再做质量评测；Star不是生产验收。

## 复现路径

**本次未安装VoiceStudio、未拉起后端、未下载模型权重、未执行克隆/配音/有声书/Agent工具调用。**实际执行的是素材读取、静态源码/许可研究及本仓库目录校验。下列步骤供独立测试，不表示已通过。[S3,S6,S9,S10,S24]

1. 优先用官方v0.5.8 release按系统选安装包；比较稳定版与本文main快照时分别记录版本。macOS当前README区分Apple Silicon本地路径和Intel Mac远程后端有限支持；不要把“Mac支持”理解为Intel本地推理保证。
2. 源码复现须先审查安装入口。本次读取`prepare-dev.mjs`确认`bun run dev`会执行依赖安装和本地API设置，不只是启动已有程序；Node **22.12.0+**检查来自实际代码，Bun锁定声明为1.4.2，Python项目要求**>=3.11**。`setup-api.mjs`还调用Python setup流程，本次未对完整安装器做安全审计，不建议直接curl管道执行或绕过系统签名保护。
3. 在独立可写目录取固定源码，确认环境/磁盘与许可证后才执行：

```bash
git clone https://github.com/debpalash/VoiceStudio.git
cd VoiceStudio
git checkout 17a70e1368d8b823a670fed822a2ece6894e5bc5
# 先检查 package.json、scripts/prepare-dev.mjs、scripts/setup-api.mjs及所调用安装脚本
# 独立环境满足Node/Bun/Python依赖后再按官方指引运行：
bun run dev
```

4. 先只装一个所需TTS和一个所需ASR，若需要离线翻译再预下载适用Argos/NLLB包；确认所有实际选中的模型及组件可用于本次用途。首次下载可能较大；“CPU能跑”仅是作者兼容宣称，不是本机速度保证。
5. 用本人或明确授权的5–15秒干净样本与两句无敏感文本测试克隆。核对声线、字词、不漏读、文件格式、采样率、可播放性；记录实际语言、设备、引擎、参数和实时率。
6. 再用有权使用的短视频，人工校对ASR、译文、说话人和时间轴，检查合成MP4/字幕无错位、无缺段；同时检查每个处理端点是否符合本地要求。断网测试应在模型/依赖齐全后进行，结合网络记录，不仅看“任务成功”。
7. 用两章自有文本测试有声书规划、M4B章节、局部重渲染和断点续跑；结果逐章听检，检查章节数、时长及正文覆盖。
8. Agent需先确认后端健康与本机端点，再按官方文档连接`http://127.0.0.1:3900/mcp/`（以实际端口为准）。配置文件返回模式与明确目录后调用；验证返回ID与实际音频一致、越界路径拒绝、不得未经授权把音频/文字放进云端Agent上下文。

## 适用场景与限制

适合个人原型、授权声线实验、小规模本地工作台、需要统一API/MCP的音频流程；不是自动替代专业配音、内容权利审查或生产质检。困难语言/跨语言声线、情绪及口音一致性、长文本稳定性、显存/CPU耗时、FFmpeg封装、模型兼容依赖和硬件分层仍要测试。专业的生产判断至少要同时满足：**质量合格、权限合法、数据路径符合约束、吞吐与成本可接受**。

作者关于“小城缺经验→项目制训练→团队建设”的经历有明确本人文章支持，是值得记录的经营方法；200评论/12名额不是本报告独立核验的量化经营成绩。[S13]

## 待核实事项

- 2026-09-28 GitHub榜首及2026-11-19精确Star/Fork历史快照；Trendshift本次拒绝访问，不绕过。
- 各引擎646目录之外的实际语言覆盖、每语种克隆质量、ASR/翻译完整覆盖及对齐效果。
- 稳定v0.5.8安装包与main beta快照是否逐项一致、实际签名/硬件兼容性与完全离线网络行为。
- Pro闭源版未检查源码/抓包；本报告只引用官网明确的Pro账号及自动元数据说明，不用免费版代码替它背书。
- 每一目标模型版本与依赖二进制的完整商用/分发清关、voice-consent核实和真实滥用防护有效性；未替用户部署或授权。
- 作者local-first文章仅部分读取；训练营经营数字仍主要来自本人自述。

## 来源与证据

全部于2026-11-20实际查阅；固定commit文件日期指研究快照，不假定文档首发时间。动态官网与计数后续会变。

| 编号 | 一手来源与链接 | 发布/版本时间 | 支持的结论 |
| --- | --- | --- | --- |
| S1 | [原抖音图文](https://www.douyin.com/note/7709876715334067816)；[原短链](https://v.douyin.com/saen9p66nv4/) | 2026-11-19 21:39:19 +08:00 | 展开正文、四图、平台发布者与原宣称；不是实测视频 |
| S2 | [GitHub仓库API](https://api.github.com/repos/debpalash/VoiceStudio) | 2026-11-20T22:17:41+08:00快照 | 仓库身份、建仓时间、当前Star/Fork |
| S3 | [VoiceStudio README](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/README.md) | 17a70e1368d8 | 工作室功能、免费版/Pro/Cloud、核心成员、平台 |
| S4 | [应用许可证](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/LICENSE)；[License Notice](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/LICENSE-NOTICE.md) | 同一快照 | AGPL-3.0-only、商业使用与第三方模型边界 |
| S5 | [OmniVoice模型卡](https://huggingface.co/k2-fsa/OmniVoice/blob/3fc979d1cd72492cd679c5ac2611e0d7ac047ba1/README.md#license)；[tokenizer实际LICENSE](https://huggingface.co/k2-fsa/OmniVoice/blob/3fc979d1cd72492cd679c5ac2611e0d7ac047ba1/audio_tokenizer/LICENSE) | HF 3fc979d1cd72 | 权重CC-BY-NC、代码Apache-2.0及Boson/Llama附加条款 |
| S6 | [引擎指南](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/docs/engines/README.md)；[646行目录](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/docs/languages.md) | 同一快照 | 默认模型、各引擎能力与语言差异 |
| S7 | [TTS适配器](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/tts_backend.py)；[模型目录](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/model_catalogue.py) | 同一快照 | 实际适配/语言校验与目录来源 |
| S8 | [配音导入源码](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/dub_pipeline.py)；[生成源码](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/dub_generate.py)；[翻译引擎](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/translation_engines.py)；[Cinematic](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/translator.py) | 同一快照 | 双音轨、处理流水线、翻译端点与时长策略 |
| S9 | [有声书路由](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/audiobook.py)；[长文渲染器](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/services/longform_render.py) | 同一快照 | 章节、缓存与FFmpeg封装 |
| S10 | [MCP文档](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/docs/mcp.md)；[工具实现](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/mcp_server.py) | 同一快照 | mounted MCP、本地API、音频返回模式 |
| S11 | [免费版隐私文档](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/docs/electron-privacy.md)；[官网隐私政策](https://voicestudio.sh/privacy) | 文档快照；官网标2026-11-04更新 | 免费版opt-in与Pro自动元数据、账号/网络边界 |
| S12 | [Remote GPU文档](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/docs/remote-gpu.md) | 同一快照 | 可选远程后端与项目不在当前电脑 |
| S13 | [Building a Tech Company from Agartala](https://palash.dev/blog/building-from-agartala/)；[Yupcha官网](https://yupcha.com/) | 2026-07-07；官网动态 | 本人自述招聘/训练营/团队及产品存在 |
| S14 | [Why I Built an Open-Source ElevenLabs](https://palash.dev/blog/omnivoice-open-source-elevenlabs/)；[实际读取Markdown](https://palash.dev/blog/omnivoice-open-source-elevenlabs.md) | 2026-07-08，2026-08-13更新 | 创作动机，Tauri是历史写法 |
| S15 | [What Local-First Has to Explain](https://palash.dev/blog/local-first-trust-boundaries/)；[Markdown](https://palash.dev/blog/local-first-trust-boundaries.md) | 2026-08-28 | **仅部分读取**loopback/可选remote开头；全文未取得 |
| S16 | [Acceptable use](https://voicestudio.sh/acceptable-use)；[授权记录源码](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/backend/api/routers/profiles.py) | 政策标2026-11-04更新；代码快照 | 同意责任、冒充/诈骗禁止与能力限制 |
| S17 | [v0.5.8 release](https://github.com/debpalash/VoiceStudio/releases/tag/v0.5.8) | 2026-11-12T08:53:29Z | 仅稳定版发布元数据，未安装 |
| S18 | [Voicebox固定README](https://github.com/jamiepine/voicebox/blob/8af7efe62fab8d33e2a5dfbedabaa45f68a5184f/README.md)；[LICENSE](https://github.com/jamiepine/voicebox/blob/8af7efe62fab8d33e2a5dfbedabaa45f68a5184f/LICENSE) | 2026-11-20查询快照 | 本地工作室同类功能与MIT代码许可 |
| S19 | [GPT-SoVITS固定README](https://github.com/RVC-Boss/GPT-SoVITS/blob/6d51ffceafbf240145619af4c92408a6e54b7924/README.md)；[LICENSE](https://github.com/RVC-Boss/GPT-SoVITS/blob/6d51ffceafbf240145619af4c92408a6e54b7924/LICENSE) | 同日快照 | zero/few-shot、语言与训练工具、MIT |
| S20 | [F5-TTS固定README](https://github.com/SWivid/F5-TTS/blob/600e5fdfbf319f84735557aca80a7aaf60d487e6/README.md)；[LICENSE](https://github.com/SWivid/F5-TTS/blob/600e5fdfbf319f84735557aca80a7aaf60d487e6/LICENSE) | 同日快照 | Flow Matching、MIT代码和NC权重区别 |
| S21 | [pyVideoTrans固定README](https://github.com/jianchang512/pyvideotrans/blob/b2354a552ab472e1a66a8f907749f38db9cad8bc/README.md)；[LICENSE](https://github.com/jianchang512/pyvideotrans/blob/b2354a552ab472e1a66a8f907749f38db9cad8bc/LICENSE) | 同日快照 | 视频翻译链路、本地/在线API、GPL-3.0 |
| S22 | [ebook2audiobook固定README](https://github.com/DrewThomasson/ebook2audiobook/blob/e2e768c24ef507669e1ee920328a0111905656d0/README.md)；[LICENSE](https://github.com/DrewThomasson/ebook2audiobook/blob/e2e768c24ef507669e1ee920328a0111905656d0/LICENSE) | 同日快照 | 章节/多格式输出及目录宣称、Apache-2.0代码 |
| S23 | [OmniVoice上游README](https://github.com/k2-fsa/OmniVoice/blob/4d5ed0f0621507e8aebd4560bde316549e85c553/README.md)；[LICENSE](https://github.com/k2-fsa/OmniVoice/blob/4d5ed0f0621507e8aebd4560bde316549e85c553/LICENSE) | 同日快照 | 底层模型来源、diffusion架构与参考prompt |
| S24 | [package.json](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/package.json)；[Electron包](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/electron/package.json)；[prepare-dev](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/scripts/prepare-dev.mjs)；[Node门槛](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/electron/scripts/node-version.mjs)；[pyproject](https://github.com/debpalash/VoiceStudio/blob/17a70e1368d8b823a670fed822a2ece6894e5bc5/pyproject.toml) | 同一快照 | 当前架构/beta版本、自动安装行为、Node/Python门槛 |

## 更新记录

- 2026-11-20：首次收录；对齐真实图文来源，核对代码/权重许可、当前架构和隐私边界，补充五类替代工具与未实测验收步骤；历史榜首保留待核实。
