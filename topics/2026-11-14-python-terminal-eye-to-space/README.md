# 眼睛到爱心星空：Python 字符画与终端动画

收录日期：2026-11-14

最近核实：2026-11-14，Asia/Shanghai

研究状态：**部分核实**。原视频、启动命令和相似代码的技术路径已核实；原作者工程、所用 AI 工具及实际运行效果未核实。

## 一句话结论

这是把“眼睛睁开 → 进入瞳孔 → 粉色爱心和星空”画成字符并在终端连续刷新的视觉作品。**可行的实现重点是字符渲染、场景时间轴和终端输出，不是必须调用某个新 AI 模型。**搜到了高度近似的公开 Python 实现，但不能将它直接认作视频作者的原工程；它也没有已识别的许可证。[S1][S2]

## 原始线索

- 用户原短链：[抖音分享](https://v.douyin.com/DreQzf0md9E/)。
- 规范作品：[7707535886544209290](https://www.douyin.com/video/7707535886544209290)。
- 原标题：`你的眼里藏着什么#vibecoding #Python #终端动画 #程序员浪漫`。
- 作者：**肮**；平台详情发布时间：**2026-11-13 14:15:42 +08:00**。[S1]
- 实际读取：作品正文、公开详情、完整下载的 **30.100 秒 / 7,402,602 字节 / 1920×1080 H.264** 视频；查看约 0.15 秒启动画面及 0.5、1.5……29.5 秒共 30 个全时段采样画面。**没有逐帧检查，也没有完整听音或语音转写。**
- 0.15 秒可读到 Windows PowerShell 5.1，以及 `python eye_to_space.py`。脚本正文、依赖列表和 AI 编写过程没有展示。[S1]
- 检索不把网页中的推荐视频、评论求代码或分享文本中的 `8.99`、口令、`06/30` 当作技术版本、收费信息或正式发布时间。

### 画面证据

| 原视频时间点 | 实际看到的内容 | 能确认 / 不能确认 |
| --- | --- | --- |
| 约 0.15 秒 | Windows PowerShell 中启动 `eye_to_space.py` | 确认 Python 启动命令；不能确认具体源码和依赖 |
| 0.5–2.5 秒采样 | 字符眼睛从闭合到睁开 | 确认字符画视觉和开眼变化；不据此测量眨眼速度 |
| 3.5–8.5 秒采样 | 虹膜、瞳孔逐步占据更大画面 | 确认向瞳孔推进的视觉过渡；不确认是否使用真实三维模型 |
| 9.5–14.5 秒采样 | 眼睛局部退出画面，星点和粉色爱心显现 | 确认过渡后的图案；不推定所用粒子引擎 |
| 15.5–29.5 秒采样 | 粉色字符爱心、移动/闪烁的星点 | 确认后半段星空爱心效果；不把屏幕录像当作性能测试 |

## 技术实现

### 1. 可核实的参照实现：`eye_to_space3.py`

代码搜索命中 `kolk42254-code/ai-ml-goal` 的 `Projects_by_AI/Eye_animation/eye_to_space2.py` 和 `eye_to_space3.py`。固定版本为：

`54ad9aa5a40ee2c797beb869136d392e88d5d309`

版本提交时间是 2026-10-28 17:50:25 UTC，早于本次作品发布时间。README 把它列为 AI 工具制作的练习项目，文件注释说形状/时间轴参考视频，但**未找到指向本次抖音作品的出处链**。日期、名字及相似视觉都不能单独确立作者归属。[S2]

尤其需要分清：

- `eye_to_space2.py`：**NumPy + Pillow + Tkinter 窗口**版本；从终端启动不等于在终端内绘制。
- `eye_to_space3.py`：**Python + NumPy 的终端内绘制**版本，包含 ANSI 控制序列、字符映射和星空场景；与本次画面的技术形态更接近。
- 两个文件的说明/默认时间轴约 **14.25 秒**，原视频为 **30.1 秒**，文件名也不完全一致。这些差异尚未解释，不能宣称“找到原作者同款源码”。[S1][S2]

### 2. 输入与场景计算

以下是**已读候选代码的实现**，不是对原视频内部实现的断言：

1. **字符网格与比例**：`configure()` 根据列数、行数、字形高宽比建立坐标，`Scene` 对每个字符格做 2×2 超采样，避免眼球和爱心被终端的长方形字格拉扁。候选默认 150×44 格，允许调整至最多 320×100 格。[S2：109–120、576–604 行]
2. **眼睑、视线和推进**：`openness()`、`gaze()`、`zoom()` 分别决定开闭程度、眼球移动和视角缩放；`zoom()` 使用对数尺度插值后取指数。虹膜纤维、睫毛、皮肤光照与瞳孔遮罩由数值计算产生，而不是加载一个已经核实的照片资产。[S2：270–368、605–768 行]
3. **瞳孔作为场景窗口**：`Scene.paint()` 用瞳孔遮罩把眼球与 `Scene.space()` 混合，星云来自多尺度噪声，粉色爱心通过边界距离、渐变色和两段脉冲式心跳形成。[S2：736–803 行]
4. **星点与纵深**：`StarField` 保存 x/y/深度，按 x/深度、y/深度投影；随深度循环产生穿行效果，同时改变亮度、拖尾和字符。这是可在二维终端输出中营造纵深的计算方法，不要求终端提供三维 GPU 引擎。[S2：493–565 行]
5. **字符与颜色**：`Scene.frame()` 计算亮度 `0.2126R + 0.7152G + 0.0722B`，映射到按覆盖面积排序的字符；`Letters.line_for()` 将睫毛、虹膜和拖尾方向映射到 `- / | \`，并分别计算字符前景和暗背景。[S2：806–896 行]

### 3. 终端输出与调度

- `Terminal` 进入备用屏幕、隐藏光标、关闭自动换行；退出时尝试恢复状态。Windows 分支通过 `SetConsoleMode` 启用 VT 处理，并设置 UTF-8 输出。[S2：1080–1173 行]
- `Painter.paint()` 对比上一帧，仅输出变化的字符/颜色；通过 `ESC[row;colH` 定位，用 `38;2` / `48;2` 设置 RGB 前景/背景，也提供 256 色降级。代码还发送同步更新序列，但**终端是否支持该扩展需要实机确认**。[S2：1202–1290 行]
- `Frames` 用进程池预计算，并以代码、网格和比例为键存 `.npz` 缓存。注释说“全部预计算”，但 `can_start()` 实际允许在预估生产速度足够时提前播放，不能机械地概括为必定等全部帧完成才开始。[S2：904–1074 行]
- `play()` 使用 `time.perf_counter()` 和帧节拍调度，并在窗口变化时重新准备画面。目标 FPS=30 是代码设置，**不是本轮实测成绩**；“流畅、凉快、下一次瞬间启动”等注释不视为性能证据。[S2：1307–1413 行]
- 微软官方说明确认 VT 光标和颜色控制序列的语义，但不同控制台/终端的实际调色板和扩展支持可能不同，不能仅因运行 PowerShell 就保证所有 RGB 或防闪烁功能生效。[S6]

| 关键判断 | 证据状态 | 依据 |
| --- | --- | --- |
| 原视频用 Python 命令启动字符动画 | 已核实 | S1，约 0.15 秒 |
| 画面包含眼睛推进、爱心和星空 | 已核实 | S1，全时段采样 |
| 候选终端版本可用 NumPy 场景计算 + ANSI 输出实现这种构图 | 源码已核实，运行未核实 | S2，`Scene` / `StarField` / `Painter` |
| 原作者使用的就是上述 GitHub 文件 | **待核实** | 没有原作者/作品到仓库的出处链，且时间轴存在差异 |
| 原作者用特定 Agent、模型或提示词生成 | **未证实** | `#vibecoding` 标签不是工具、模型或生成过程证据 |
| 必须用实时图像生成模型才能得到这种动画 | 不成立为必要条件 | S2 提供无需模型调用的可行计算路径；不推定原作者路径 |
| 任意电脑上都能稳定 30 FPS | **未证实** | 没有设备、终端、网格和负载下的实测 |

## 相关项目与资料

先比较用途，再看 Star 数。以下为 **2026-11-14 查询快照**，不是排名或原作者依赖证明；所有项目本轮均未安装运行。

| 项目 | Star 快照 | 固定版本 / 许可证 | 用途与交付结果 | 与本素材的关系及门槛 |
| --- | ---: | --- | --- | --- |
| [ai-ml-goal / Eye_animation](https://github.com/kolk42254-code/ai-ml-goal/tree/54ad9aa5a40ee2c797beb869136d392e88d5d309/Projects_by_AI/Eye_animation) | 1 | `54ad9aa5a40e…`；**未发现许可证** | 具体眼睛→星空→爱心场景；终端版和窗口版分开 | 构图高度近似，但归属未核实；终端版需 NumPy、可用 TTY；不能直接按 MIT/Apache 项目复制发布 |
| [asciimatics](https://github.com/peterbrittain/asciimatics) | 4,309 | `bf0cea87b5043…`；Apache-2.0；最新 GitHub Release `1.15.0`（2023-10-25） | 跨平台场景、Effect、字符图像渲染、星点和交互；输出终端动画/TUI | 更适合自己做完整场景和复用星空等组件；Python ≥3.8，依赖 Pillow/pyfiglet/wcwidth，Windows 还涉及 pywin32；眼睛推进仍需编写 |
| [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects) | 4,303 | `3eac3eded0b9…`；MIT；最新 GitHub Release `release-0.15.0`（2026-05-10） | 字符运动路径、颜色/符号场景、内置转场；输出终端文字特效 | 更适合 Logo、文字/字符聚散和转场；当前 main 核心要求 Python ≥3.9.2、无第三方核心依赖；不是现成眼睛/星空作品 |
| [video2chars](https://github.com/ryan4yin/video2chars) | 229 | `a3092cc0b2bd…`；MIT；源码版本 `0.7.0` | 输入已有视频，逐帧映射字符并**导出 MP4** | 如果目标是“成片转字符风格”更直接；当前入口不是实时终端播放器，也不会凭空生成眼睛场景；Python ≥3.9，依赖较旧的 NumPy/Pillow/MoviePy 区间 |

### 源码核对与选型

- **asciimatics**：`effects.py::Print` 将 Renderer 的文本/颜色绘制到指定位置，`Stars` 明确实现随机闪烁星点；`renderers/images.py::ImageFile` 读取图像/动画帧、灰度化、按字符密度映射，并补偿字格比例。`ColourImageFile` 的调色板限制不可忽略。它能减少场景编排代码，但没有证据表明原作者用了它。[S3]
- **TTE**：`engine/motion.py` 提供 Path/Waypoint/Motion，`engine/animation.py` 提供 Frame/Scene/Animation，`engine/terminal.py` 处理画布、光标生命周期和帧率；`effect_expand.py` / `effect_rings.py` 是可参考的内置效果。**README 明示 main 正向 0.16.0 开发，PyPI 最新发布为 0.15.0；不能把 main 所有新增特性当作 `pip install` 稳定版已提供。**[S4]
- **video2chars**：`converter.py::get_chars_frame()` 对视频帧逐像素取灰度/颜色，用 Pillow 画等宽字符，`generate_chars_video()` 建立 MoviePy 视频并保留音频；CLI 最终调用 `write_videofile()`。中文 README 的旧 shell 演示不代表当前 0.7.0 的默认输出是实时终端。[S5]

**建议**：追求自己的同类浪漫动画，优先“独立场景设计 + NumPy/ANSI”，或用 asciimatics 做较易维护的完整场景；文字聚散/片头选 TTE；已有素材转成字符成片选 video2chars。高度近似候选只作来源调查和技术参照，不因“像原片”就直接搬进正式产品。

## 复现路径

**基于源码与文档整理，未实际运行。**本轮只执行媒体获取/探测、静态源码阅读和收录检查，没有安装动画依赖，没有启动候选脚本或进行 FPS 测试。

### A. 独立实现一个最小同类作品

这条路线不依赖拿到原作者未公开的工程，也不直接复制无许可证候选：

1. 准备 Python、等宽字体和支持 VT 的真实终端。先从约 100×30 或 120×40 格、15–20 FPS 起步；这些是建议起点，不是实测最优值。
2. 用椭圆/曲线遮罩定义眼白、虹膜、瞳孔与上下眼睑；建立“开眼 → 推进瞳孔 → 爱心星空”的自有时间轴。
3. 以 NumPy 数组计算颜色/亮度，或先用简化字符轮廓完成构图。星点保存位置、闪烁相位和可选深度；爱心用自定义轮廓/数学曲线填充，并随时间做轻微缩放。
4. 对每帧建立 `(字符, 前景色, 背景色)` 网格，按字格高宽比修正坐标，必要时用 256 色或 ASCII-only 降级。
5. 一次性/按变化区域输出，避免对每个字符单独 `print()`，也避免每帧调用系统 `cls`/`clear`。用单调时钟控制阶段和帧率，迟到时丢弃过时帧。
6. 使用 `try/finally` 恢复光标、色彩和终端输入模式；检测窗口变小/改变时重排画面。可用 `shutil.get_terminal_size()` 读取尺寸，但它会受 `COLUMNS`/`LINES` 和非 TTY fallback 影响。[S7]

伪代码结构（不是已运行程序）：

```text
初始化字符网格、时间轴、星点、终端状态
循环直到结束或退出：
    t = 单调时钟 - 起点
    计算眼睑/瞳孔缩放/爱心/星点
    合成场景颜色 → 亮度/方向映射字符
    输出变化的字符与颜色
    等待下一个节拍，跳过过期节拍
finally：恢复终端状态
```

### B. 基于已授权开源库复用组件

- **asciimatics**：在隔离 Python 环境中按所选 release 安装，先验证 README 的 `Screen.wrapper` 和 `Stars` 小场景，再增加自定义 Renderer/Effect。它不是安装后自动得到原片。
- **TTE**：先决定使用稳定 release 还是固定 main commit，按该版本文档做简单文字效果，再增加字符路径/场景。不要在未核对版本时照搬开发分支特性。
- **video2chars**：先准备自己有使用权的眼睛/爱心视频，按固定版本依赖区间配置环境，执行转换后检查生成 MP4；不能把此结果称为“实时终端程序复现”。
- **近似候选代码**：先取得复制/分发所需授权并审查执行入口。`eye_to_space3.py` 默认会起 worker、写入/清理临时缓存和修改终端模式；`eye_to_space2.py` 还会创建 Tkinter 窗口。不要将它们混为同一执行路径。

### 验收建议

- 三阶段在同一终端视口内按预期出现，不滚屏、不出现大量残留字符；
- 眼睛、瞳孔、爱心比例正常，缩放过程不跳变；
- 星点闪烁和爱心轻微变化可辨识，缩小窗口后可恢复；
- 正常结束、Q/Esc、Ctrl+C、异常退出均恢复光标和输入；
- 在**同一设备、终端、字格尺寸、FPS 设置**下分别记录首轮生成、缓存启动和播放帧耗时，再讨论流畅程度。

## 适用场景与限制

- 适合编程艺术、教学、节日告白、终端展示和短视频创意素材；核心工作是美术构图与时间轴，不应宣传成新的大模型能力。
- 字符格分辨率有限：字更密会增加计算量、输出字节和终端重绘压力。预计算可降低播放期计算量，但会增加首次等待和内存/磁盘占用。[S2]
- 字体、字格比例、颜色模式、终端扩展和远程连接都会影响效果；不能仅凭屏幕录像保证跨平台一致。[S2][S3][S6]
- `#vibecoding`、README 里的“AI-made”及代码注释都不提供实际提示词、AI 工具、人工修改量或生成耗时证据。[S1][S2]
- 公开可读不等于授予复制/再发布许可。近似候选的完整未截断树中未发现许可证文件，仓库 API 也返回 `license: null`；这里只链接和分析，不打包或再发布它的代码。
- 原视频属于创作展示，下载仅用于本次核实；不发布原视频、音轨、完整页面或任何登录态。

## 待核实事项

1. 视频作者“肮”与 `kolk42254-code/ai-ml-goal` 是否存在关系，`eye_to_space.py` 是否对应候选某个版本。
2. 作者原工程、依赖、源资产、许可证及可公开复用范围。
3. 原作品的 30.1 秒与候选 14.25 秒时间轴差异的原因。
4. 所用 AI 工具、模型、提示词、生成/修改流程与耗时。
5. 实际运行稳定性、首轮/缓存启动、设备负载、不同终端的颜色与防闪烁支持。

## 来源与证据

固定源码链接均指向本轮实际下载读取的 commit；相邻 [research_snapshot.json](research_snapshot.json) 记录公开元信息、文件 SHA-256 和核实范围，不含媒体、源码正文或登录凭据。

| 编号 | 来源与链接 | 发布/版本日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [肮：你的眼里藏着什么](https://www.douyin.com/video/7707535886544209290)，[用户短链](https://v.douyin.com/DreQzf0md9E/) | 2026-11-13 14:15:42 +08:00，平台详情 | 2026-11-14 | 作者/标题/发布时间、启动命令、眼睛与爱心星空的视觉展示 |
| S2 | [近似终端版 eye_to_space3.py](https://github.com/kolk42254-code/ai-ml-goal/blob/54ad9aa5a40ee2c797beb869136d392e88d5d309/Projects_by_AI/Eye_animation/eye_to_space3.py)，[窗口版 eye_to_space2.py](https://github.com/kolk42254-code/ai-ml-goal/blob/54ad9aa5a40ee2c797beb869136d392e88d5d309/Projects_by_AI/Eye_animation/eye_to_space2.py)，[README](https://github.com/kolk42254-code/ai-ml-goal/blob/54ad9aa5a40ee2c797beb869136d392e88d5d309/README.md) | 固定提交 2026-10-28；不代表这些文件的首次发布日期 | 2026-11-14 | 候选场景、字符映射、ANSI 输出、预计算/缓存、窗口版差异；不证明原作者归属 |
| S3 | [asciimatics README](https://github.com/peterbrittain/asciimatics/blob/bf0cea87b50439e40a5c7b708d64da4195314a60/README.rst)，[effects.py](https://github.com/peterbrittain/asciimatics/blob/bf0cea87b50439e40a5c7b708d64da4195314a60/asciimatics/effects.py)，[images.py](https://github.com/peterbrittain/asciimatics/blob/bf0cea87b50439e40a5c7b708d64da4195314a60/asciimatics/renderers/images.py)，[依赖](https://github.com/peterbrittain/asciimatics/blob/bf0cea87b50439e40a5c7b708d64da4195314a60/pyproject.toml)，[许可证](https://github.com/peterbrittain/asciimatics/blob/bf0cea87b50439e40a5c7b708d64da4195314a60/LICENSE)，[1.15.0 Release](https://github.com/peterbrittain/asciimatics/releases/tag/1.15.0) | 固定提交 2026-07-04；Release 2023-10-25 | 2026-11-14 | 场景/Effect、图像到字符、星点、依赖与 Apache-2.0 |
| S4 | [TTE README](https://github.com/ChrisBuilds/terminaltexteffects/blob/3eac3eded0b9bca2e2a878102ebb9e7b2d8c9d25/README.md)，[engine 源码](https://github.com/ChrisBuilds/terminaltexteffects/tree/3eac3eded0b9bca2e2a878102ebb9e7b2d8c9d25/terminaltexteffects/engine)，[依赖](https://github.com/ChrisBuilds/terminaltexteffects/blob/3eac3eded0b9bca2e2a878102ebb9e7b2d8c9d25/pyproject.toml)，[许可证](https://github.com/ChrisBuilds/terminaltexteffects/blob/3eac3eded0b9bca2e2a878102ebb9e7b2d8c9d25/LICENSE)，[0.15.0 Release](https://github.com/ChrisBuilds/terminaltexteffects/releases/tag/release-0.15.0) | 固定提交 2026-11-02；Release 2026-05-10 | 2026-11-14 | 运动/颜色场景、终端输出、main 与 release 边界、MIT |
| S5 | [video2chars 转换器](https://github.com/ryan4yin/video2chars/blob/a3092cc0b2bd4311359e5f630dda0e36ad271be0/video2chars/converter.py)，[CLI](https://github.com/ryan4yin/video2chars/blob/a3092cc0b2bd4311359e5f630dda0e36ad271be0/video2chars/__init__.py)，[依赖](https://github.com/ryan4yin/video2chars/blob/a3092cc0b2bd4311359e5f630dda0e36ad271be0/pyproject.toml)，[中文说明](https://github.com/ryan4yin/video2chars/blob/a3092cc0b2bd4311359e5f630dda0e36ad271be0/doc/README-zh-cn.md)，[许可证](https://github.com/ryan4yin/video2chars/blob/a3092cc0b2bd4311359e5f630dda0e36ad271be0/LICENSE) | 固定提交 2024-02-08，源码版本 0.7.0 | 2026-11-14 | 视频转字符 MP4、灰度映射、音轨保留、依赖区间及 MIT |
| S6 | [Microsoft：Console Virtual Terminal Sequences](https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences) | 页面修订日期未单独核实 | 2026-11-14 | VT 处理开关、光标定位、RGB/256 色序列和控制台兼容边界 |
| S7 | [Python：shutil.get_terminal_size](https://docs.python.org/3/library/shutil.html#shutil.get_terminal_size) | 官方动态文档；非软件发布公告 | 2026-11-14 | 字符列/行读取、环境变量和 fallback 的影响 |

## 更新记录

- 2026-11-14：首次收录；核实原视频和公开近似实现，比较三个通用开源方案，保留归属、许可和未运行边界。
