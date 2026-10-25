# Pixelle-Video：AI 全自动短视频引擎

收录日期：2026-10-25

最近核实：2026-10-25，Asia/Shanghai

研究状态：**部分核实**。Pixelle-Video 的公开仓库、许可证、版本和核心实现已核实；它与用户原抖音视频的对应关系仍待核实。以下技术分析以实际读取的项目源码为依据。

## 一句话结论

Pixelle-Video 把主题/现成文案、分镜规划、逐段配音、AI 图片或视频、字幕画面和 FFmpeg 合成组织成一条自动成片流水线。它适合模板化科普、知识解说和图文口播，也能接入已有素材；效果、费用与时长仍取决于接入的模型和工作流。[S1][S4][S5][S7]

## 原始线索

- 用户提供：[抖音原分享短链](https://v.douyin.com/PR-x_TmHfUg/)。
- 分享文本：`3.02 复制打开抖音，看看【爱科技AI的作品】阿里开源了 AI 短视频引擎 写脚本一小时、找素材...`。
- 作者与标题：来自分享文本，尚未由作品详情独立验证；视频发布日期未知，分享文本末尾 `06/04` 不作为发布日期。
- 原短链跳转到 `iesdouyin.com/share/video/7699893581566216810/`；规范链接为 [视频 7699893581566216810](https://www.douyin.com/video/7699893581566216810)。不归档跳转 URL 的用户/设备/分享追踪参数。
- 实际读取范围：用户分享文本、短链跳转、移动/桌面网页壳。网页未返回可用的作品详情；桌面页面数据中的作品对象为 `null`。本机已接入的抖音下载器执行 1 条任务，结果为成功 0、失败 1，无可读视频或字幕。**未观看原视频，未进行原视频转写或关键帧验证。**
- 主要宣称：从分享文本看，是“阿里开源 AI 短视频引擎”、减少写脚本及找素材的人工时间；具体项目名、演示用时、画质与成本尚未从原视频验证。
- 检索“阿里 / 开源 / AI 短视频引擎”得到 **Pixelle-Video** 候选。[S16] 同时直接读取官方仓库，核实其确有相应能力；关键词匹配不能证明它就是原作者演示的项目。

## 技术实现

```mermaid
flowchart LR
    A[主题或固定文案] --> B[旁白与分镜]
    B --> C[逐段 TTS 与音频时长]
    C --> D[生成图片/视频或跳过媒体]
    D --> E[HTML 字幕画面]
    E --> F[FFmpeg 分镜合成]
    F --> G[拼接与 BGM]
    G --> H[成片与任务记录]
```

### 1. 输入与文案：主题生成和固定文案两条路径

标准流水线 `StandardPipeline` 在 `generate_content` 中根据 `mode` 分流：`generate` 调用 LLM 由主题生成旁白；`fixed` 对已有脚本按段落、行或句子切分，此时 `n_scenes` 不决定实际分镜数。标题可直接提供；未提供时仍可能调用 LLM，因此固定文案并不等于所有文本模型调用都被关闭。[S4]

LLM 采用可配置的 OpenAI 兼容接口，配置包含 `base_url`、`model` 与 `api_key`，官方示例列出通义、OpenAI、DeepSeek 和 Ollama。产品不是只能调用某一个厂商的模型。[S1][S11]

### 2. 视觉规划：模板决定需要生成什么

标准流水线依据模板前缀决定路线：

| 模板类型 | 处理 | 使用含义 |
| --- | --- | --- |
| `static_*.html` | 跳过画面提示词与媒体生成 | 可先验证文字、配音与成片链路 |
| `image_*.html` | 生成每段旁白对应的图片提示词与图片 | 适合图文解说、知识卡片 |
| `video_*.html` | 生成视频片段，并做模板合成 | 动态画面依赖视频模型能力 |

模板是程序实际读取的 HTML 文件，尺寸和参数由模板元信息决定。标准流水线中的“帧”通常指一个分镜段，不能理解成视频编码中每一帧都重新请求 AI。[S4][S5][S8]

### 3. 配音先行：用音频时长约束画面

`FrameProcessor` 对每个分镜先生成 TTS、探测音频时长，再生成媒体、合成字幕画面、制作视频段。对于动态视频，会把音频时长传给媒体服务作为目标时长；后续合成服务也包含裁切、变速或补帧处理。这个设计帮助同步旁白与画面，但不能据此保证所有模型原生输出都精确等长。[S5][S7]

TTS 有 `local` 与 `comfyui` 两种模式。`local` 分支实际调用 `edge_tts` 库访问微软在线服务；这里的 local 指调用封装在本机执行，**不代表离线推理**。ComfyUI 工作流可以接 Index-TTS 等方案，具体声音克隆和本地运行条件以所选模型/工作流为准。[S6][S12]

### 4. 模型执行：ComfyUI、RunningHub 和直连 API

`MediaService` 将媒体生成接到可替换的后端：

- `selfhost/...`：通过 ComfyKit 执行自部署 ComfyUI 工作流。
- `runninghub/...`：通过 ComfyKit 调用 RunningHub 云端工作流。
- `api/...`：分流到直连媒体服务；当前 README 和配置列出 DashScope、OpenAI、ARK、Kling 等供应商。[S1][S9][S11]

工作流按 `image_`、`video_`、`tts_` 文件前缀发现。自定义 ComfyUI 工作流需要先单独跑通，绑定动态参数节点并导出为 API 格式；官方 FAQ 给出 `$prompt.text!` / `$prompt.value!` 参数绑定约定。[S12]

### 5. 字幕画面和最终视频

`HTMLFrameGenerator` 用 Playwright Chromium 打开临时 HTML，填入标题、旁白和媒体路径并截图。随后视频服务通过 `ffmpeg-python` 调用 FFmpeg，为图片或动态视频添加配音、拼接分镜，并按配置混入 BGM。成片以及分镜、任务元数据保存到本地。[S5][S7][S8]

因此标准模板字幕主要来自旁白文本的画面渲染；不能直接等同于完整的逐词字幕编辑器或任意时间线剪辑系统。若需要这种能力，应单独评估具体模板与其他剪辑方案。[S5][S8]

### 6. 自动化接口与并发

除了 Streamlit WebUI，项目有 Python 入口 `PixelleVideoCore`、同步接口 `POST /api/video/generate/sync`、异步接口 `POST /api/video/generate/async`，以及任务查询接口 `GET /api/tasks/{task_id}`。可把它接入外部 Agent 或批量脚本。[S10]

标准流水线仅在检测到 RunningHub 工作流、且配置的并发数大于 1 时，以 `asyncio.Semaphore` 和 `gather` 并行处理分镜，并按原顺序合成。该实现没有提供“所有后端都自动并行”的保证。API 的任务状态存储在进程内存，完成的视频与分镜元数据另有文件落盘；部署重启后的在途任务恢复需要额外设计。[S4][S10]

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| 主题到旁白、媒体、配音、模板和成片的自动链路存在 | 已核实：源码与 README 一致 | S1、S4、S5、S7 |
| 固定文案可跳过旁白创作，静态模板可跳过媒体生成 | 已核实：实际分支 | S4 |
| 当前实现支持 ComfyUI / RunningHub / `api/` 后端 | 已核实：配置与服务分流 | S9、S11 |
| Edge-TTS 的 local 分支需要网络 | 已核实：调用实现与 FAQ | S6、S12 |
| 声音克隆、数字人口播、动作迁移等扩展 | 作者宣称：README 与目录有相关入口，本次未逐项运行 | S1 |
| 零剪辑经验、几分钟即可完成、0 元方案 | 作者宣称；缺本次独立测量，费用仍有硬件和服务条件 | S1 |
| 原抖音视频展示的项目就是 Pixelle-Video | 待核实：仅关键词匹配候选 | 原分享文本、S16 |

## 相关项目与资料

### 官方项目、版本与资料冲突

- 当前规范仓库：[ATH-MaaS/Pixelle-Video](https://github.com/ATH-MaaS/Pixelle-Video)。2026-10-25 通过 GitHub API 查询旧地址 `AIDC-AI/Pixelle-Video`，实际返回的新 `full_name` 为 `ATH-MaaS/Pixelle-Video`。README、源码版权及 NOTICE 仍使用 AIDC-AI 名称；这能证明仓库历史标识，当前组织信息不足以独立证明团队组织归属变更的细节。[S1][S2]
- 本次源码快照：`848b054e4fae40dabc62ec58e960b573e83793ac`，commit 时间为 **2026-06-14**。提交说明涉及延迟初始化媒体 API 客户端和空 LLM 返回内容处理。[S2]
- 包声明版本：`0.2.0`，Python 要求为 **>=3.11**。[S3]
- 最新发布包：`v0.1.15`，发布于 **2026-01-27**，Windows ZIP 约 398.6 MB。Releases 的 latest 包和 main 源码版本不相同；不能假设旧整合包包含 6 月直连 API 功能。[S2]
- 主项目许可证：**Apache-2.0**，以实际 LICENSE、pyproject 与源码版权头为依据。[S3] FAQ 末尾写 MIT，与许可证文件冲突，应视为文档残留。[S12]
- 安装文档写 Python 3.10+，与 pyproject 的 3.11+ 冲突；复现以 **3.11+** 为准。[S3][S12]
- 原子工作流封装：[ComfyKit](https://github.com/puke3615/ComfyKit)，项目直接依赖并调用；README 把 [Pixelle-MCP](https://github.com/ATH-MaaS/Pixelle-MCP) 列为参考项目。Pixelle-Video 已有自身 Web/API，不需要先安装 Pixelle-MCP 才能使用。[S1][S9][S15]
- README 的“系列工作”列出 FilmAgent、Anim-Director、ComfyUI-Copilot 等论文；本次没有发现其作为标准流水线运行所必需的证据，不把这些论文的多 Agent / MCTS 机制套用到 Pixelle-Video。[S1][S4]

### 同类方案比较

以下热度为 **2026-10-25 GitHub API 快照**，后续会变化。功能比较来自实际读取各项目 README，尚未做统一条件的生成质量或性能测试。

| 项目 | Stars / 许可证 | 已读取资料支持的定位 | 如何选择 |
| --- | --- | --- | --- |
| [Pixelle-Video](https://github.com/ATH-MaaS/Pixelle-Video) | 29,359 / Apache-2.0 | HTML 模板 + ComfyUI/RunningHub/直连媒体 API 的自动短视频 | 想复用 ComfyUI 工作流或控制卡片风格时重点评估 |
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 134,908 / MIT | 主题到脚本、配音、素材、字幕和成片；支持本地素材、Pexels/Pixabay/Coverr，也声明支持 AI 图像/视频 | 更高热度的直接同类；有库存素材和批量成片需求时优先对照 |
| [NarratoAI](https://github.com/linyqh/NarratoAI) | 11,526 / MIT | 已有影视/短剧素材的视频理解、解说、混剪、配音、字幕与剪映草稿导出 | 已有长视频、需要解说与混剪时评估 |

**选型判断**：高 Stars 不代表画面质量更好；Pixelle-Video 在工作流替换和模板布局上有具体价值，MoneyPrinterTurbo 有更高社区热度且覆盖同类主题成片链路，NarratoAI 更偏已有影视素材。三者应围绕同一脚本、素材预算、TTS 和输出画幅做实际比较。[S1][S13][S14]

## 复现路径

**状态：基于官方资料和源码整理，未实际安装 Pixelle-Video，未调用其模型或生成成片。** 本次完成的是网页/仓库读取、源码静态核实和目录一致性检查。抖音下载尝试不属于项目复现成功。

### 1. 环境与入口

需要 Python 3.11+、uv、FFmpeg；HTML 模板渲染还需要 Playwright 的 Chromium。首次安装通常有依赖和浏览器下载。已阅读 `pyproject.toml`、`start_web.sh`、Dockerfile 和 Docker 启动脚本；下面采用明确步骤，避免直接执行含目录自动清理逻辑的 Docker 一键脚本。[S3][S8][S12]

```bash
git clone https://github.com/ATH-MaaS/Pixelle-Video.git
cd Pixelle-Video
git checkout 848b054e4fae40dabc62ec58e960b573e83793ac
uv sync
uv run playwright install chromium
ffmpeg -version
uv run streamlit run web/app.py
```

预期 WebUI 为 `http://localhost:8501`。Linux 还可能需要 Chromium 系统依赖和中文字体，Dockerfile 中已有参考。上述命令是复现建议，本次未执行。[S1][S8][S12]

### 2. 先用静态模板做最小检查

1. 先配置可用的 LLM；即使使用固定旁白，标题等步骤也可能使用它。
2. 输入 3 段简短固定文案，选择固定文案模式和 `1080x1920/static_default.html`。
3. 选择可用 TTS。用 Edge-TTS 可以减少自部署工作量，但仍需要网络。
4. 生成一条无 BGM 视频，检查中文字体、每段旁白、字幕布局、画幅和可播放性。
5. 在 `output/` 找到成片与分镜/任务记录；用 `ffprobe` 检查存在视频和音频流、时长为正，人工确认没有空画面、字幕越界及明显截断。[S4][S5][S6][S7]

这一步主要检查编排、配音和渲染，不代表 AI 生图或视频模型已经跑通。

### 3. 再验证 AI 图片/视频路线

选择 `image_` 模板与对应 `selfhost/`、`runninghub/` 或 `api/` 工作流。只填写实际使用后端的配置；先把单张图片或单段视频生成跑通，再扩展到 3 个分镜。按实际模型能力配置尺寸、画幅、时长；不要把“支持某厂商 API”直接理解成所有模型名都已适配。[S1][S4][S9][S11]

自部署路线需要另行运行 ComfyUI、安装对应节点和模型权重。文档的“6GB+ 显存建议”不是所有 Flux / Wan / TTS 工作流的通用硬件保证；资源应按具体模型和输出参数评估。[S12]

### 4. 接入批量自动化

API 入口为 `uv run python api/app.py`；提交异步生成后保存 `task_id`，查询 `/api/tasks/{task_id}`，成功后读取返回的成片 URL。先验证单条成功和一条故意无效配置的错误返回，再评估限流、预算、排队、持久化与重启恢复。标准流水线的 RunningHub 并发配置必须匹配账号能力。[S4][S10]

## 适用场景与限制

- **适用**：科普、读书摘要、知识卡片、图文解说、模板化口播，以及已有 ComfyUI 工作流的内容批量编排。[S1][S4]
- **动态画面与角色一致性**：由所选模型、参考图和提示词决定；未发现标准流水线内可据以承诺跨镜头角色一致性的独立保障。连续剧情漫剧应另做测试。[S4][S5]
- **费用**：Apache-2.0 软件本身可免费使用；云端 LLM、图片、视频、RunningHub 等按服务规则计费。自部署依然有硬件、电力与模型许可条件。没有本次实测单条价格或耗时。[S1][S3][S11]
- **离线**：本地 Ollama + 本地 ComfyUI 只覆盖部分组件；默认 Edge-TTS 是在线服务。完整离线需要另外选用、配置并实测本地 TTS。[S6][S11][S12]
- **稳定性**：有 TTS 重试、网页渲染浏览器重建和分镜进度，但 API 在途任务处于内存；服务重启、长任务与并发额度不能仅凭“一键”宣传判断生产可用。[S4][S8][S10]
- **版本与资料**：main、Windows latest 包、FAQ 与安装说明存在时间或内容差异；本报告以固定 commit 的代码与 LICENSE 为准。[S2][S3][S12]

## 待核实事项

1. 原视频的完整标题、发布时间、语音与画面；以及是否明确展示 Pixelle-Video 名称/仓库地址。当前只确认短链对应的视频 ID。
2. 分享文本中的“阿里开源”具体组织归属；当前仓库规范地址和 AIDC-AI 版权标识已记录，原作者的说法尚未独立验证。
3. 原视频展示的写脚本/找素材用时、成片速度、成本与质量，缺完整视频和独立测试。
4. 不同后端、数字人口播、动作迁移、声音克隆的实际可用性及硬件/费用条件。
5. 未实际运行安装或成片链路；后续复现应以一次静态模板和一次 AI 图片模板作为最小验收。

## 来源与证据

除另注日期外，均于 **2026-10-25** 实际读取。源码链接固定到本次核实 commit，避免后续 main 漂移。

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [Pixelle-Video README](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/README.md) | 本快照 2026-06-14；功能更新另列 | 2026-10-25 | 功能范围、配置、示例、参考项目、作者宣传 |
| S2 | [原仓库 API](https://api.github.com/repos/AIDC-AI/Pixelle-Video)、[固定 commit](https://github.com/ATH-MaaS/Pixelle-Video/commit/848b054e4fae40dabc62ec58e960b573e83793ac)、[v0.1.15 发布](https://github.com/ATH-MaaS/Pixelle-Video/releases/tag/v0.1.15) | commit 2026-06-14；发布 2026-01-27 | 2026-10-25 | 规范仓库、Stars、源码/整合包版本差异 |
| S3 | [pyproject.toml](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pyproject.toml)、[LICENSE](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/LICENSE)、[NOTICE](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/NOTICE) | 本快照 2026-06-14 | 2026-10-25 | Python 3.11+、依赖、0.2.0、Apache-2.0、版权标识 |
| S4 | [standard.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/pipelines/standard.py)、[linear.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/pipelines/linear.py) | 本快照 2026-06-14 | 2026-10-25 | 模式、模板分流、RunningHub 并发、最终合成、元数据 |
| S5 | [frame_processor.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/services/frame_processor.py) | 本快照 2026-06-14 | 2026-10-25 | TTS → 媒体 → 字幕画面 → 视频段、时长传递 |
| S6 | [tts_service.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/services/tts_service.py)、[tts_util.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/utils/tts_util.py) | 本快照 2026-06-14 | 2026-10-25 | local Edge-TTS 真实调用、网络依赖、重试 |
| S7 | [video.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/services/video.py) | 本快照 2026-06-14 | 2026-10-25 | FFmpeg、音画时长处理、拼接与 BGM |
| S8 | [frame_html.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/services/frame_html.py) | 本快照 2026-06-14 | 2026-10-25 | HTML 参数、Playwright Chromium 与截图渲染 |
| S9 | [media.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/services/media.py)、[service.py](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/pixelle_video/service.py) | 本快照 2026-06-14 | 2026-10-25 | ComfyKit、工作流发现、API 分流、Python 服务 |
| S10 | [API 入口](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/api/app.py)、[视频接口](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/api/routers/video.py)、[任务管理](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/api/tasks/manager.py) | 本快照 2026-06-14 | 2026-10-25 | 同步/异步/任务查询、内存任务状态 |
| S11 | [配置示例](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/config.example.yaml) | 本快照 2026-06-14 | 2026-10-25 | LLM、媒体服务商、默认工作流、默认模板 |
| S12 | [FAQ](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/docs/FAQ_CN.md)、[安装文档](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/docs/zh/getting-started/installation.md)、[Dockerfile](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/Dockerfile)、[启动脚本](https://github.com/ATH-MaaS/Pixelle-Video/blob/848b054e4fae40dabc62ec58e960b573e83793ac/docker-start.sh) | 本快照 2026-06-14 | 2026-10-25 | 工作流接入、Edge-TTS 网络条件、环境与文档冲突 |
| S13 | [MoneyPrinterTurbo README](https://github.com/harry0703/MoneyPrinterTurbo/blob/82bb4a7502704559575f4e3d002b9dcb31d4ed6a/README.md)、[LICENSE](https://github.com/harry0703/MoneyPrinterTurbo/blob/82bb4a7502704559575f4e3d002b9dcb31d4ed6a/LICENSE)、[仓库 API](https://api.github.com/repos/harry0703/MoneyPrinterTurbo) | 本次 main 快照；创建日期不作为功能发布日期 | 2026-10-25 | 同类主题成片、素材源、热度与 MIT |
| S14 | [NarratoAI README](https://github.com/linyqh/NarratoAI/blob/29a11b6cdf61b69ba90321fc5babc160e0ca2657/README.md)、[LICENSE](https://github.com/linyqh/NarratoAI/blob/29a11b6cdf61b69ba90321fc5babc160e0ca2657/LICENSE)、[仓库 API](https://api.github.com/repos/linyqh/NarratoAI) | 本次 main 快照 | 2026-10-25 | 影视解说、混剪、草稿导出、热度与 MIT |
| S15 | [ComfyKit README](https://github.com/puke3615/ComfyKit/blob/2468c197e63c9ce719ae2d7b25d6c79942ed634c/README.md)、[Pixelle-MCP README](https://github.com/ATH-MaaS/Pixelle-MCP/blob/b30e749655a91c5d8896f029ba83572aebf2d9a5/README.md) | 各自固定 commit | 2026-10-25 | 工作流封装与同生态参考项目 |
| S16 | [检索候选线索：掘金文章](https://juejin.cn/post/7635139412649426994) | 未核实 | 2026-10-25 | 仅实际读取搜索摘要，用于定位候选；未读取全文，不作实现或团队归属一手证据 |

仓库本地与线上交付检查另记录在 [研究快照](evidence/research-snapshot.json)。该快照不含 Cookie、API Key、原页面用户标识或分享追踪参数。

## 更新记录

- 2026-10-25：恢复话题中的抖音输入；新增 Pixelle-Video 候选研究，核实固定源码、许可证、安装要求与版本差异；比较 MoneyPrinterTurbo 和 NarratoAI；明确保留原视频读取与项目对应关系缺口，复现未实际运行。
