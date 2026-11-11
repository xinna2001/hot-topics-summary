# Petalwake：Claude Fable 5.2 制作的 3D 扫帚飞行游戏

收录日期：2026-11-11

最近核实：2026-11-11，Asia/Shanghai

研究状态：**原游戏与公开源码已定位，静态核验通过；开发成本和运行表现仍未独立验证。**

## 一句话结论

原视频对应的游戏是 **Petalwake**，源码为 [jjcm/petalwake](https://github.com/jjcm/petalwake)。不是相似项目代替：仓库画面中的女巫、花海、海岛与原片匹配，源码还包含原片的风之种子提示、`The Sisters` 和 `The Open Hand` 地点。它是 JavaScript + Three.js r187 / WebGL2 浏览器游戏，已公开源码和处理后资产，MIT 许可。作者 README 称用 Claude Code + Fable 5.2，结合参考视频及多轮试玩反馈制作；这项制作过程陈述并非本次独立计时或模型日志验证。[S1,S7–S13]

## 原始线索

- 用户原分享：[抖音短链](https://v.douyin.com/AwzPvnN73AU/)；[原作品](https://www.douyin.com/video/7706789737599634714)，作品 ID `7706789737599634714`。
- 抖音发布者：为了即将到来的时刻；发布时间：2026-11-11 14:00:19 +08:00。
- 首轮读取完整简介、详情与页面正文，下载 96.943 秒、1020×576 视频，检查 0/4/8/16/24/32/40/44/48/56/64/72/80/88/94 秒关键帧。未逐帧检查、未做全视频转写、未试玩。
- 原帖称约四小时及后续提示、视频生成器引导视觉方向、200 美元月套餐消耗约 20%；00:04 字幕称网页可玩，00:48 称工程开源、1060 能运行。这些原始说法保留；现在已经找到工程与对应网页，但耗时、额度和 1060 性能依然未实测。
- 原帖署名 `@pwnies`。源码作者由仓库及 LICENSE 标为 Jacob Miller / `jjcm`；未完成 X 署名账号的独立身份绑定，不把 GitHub 的同名 `Pwnies` 账号误认为本项目。

### 对应关系核验

| 核验点 | 原视频线索 | 对应仓库/网页证据 |
| --- | --- | --- |
| 画面 | 小女巫、粉色花海、海岛、悬崖、扫帚尾迹 | 已读取 `screenshots/meadow_wake.jpg`；角色与画面特征匹配 [S8] |
| 收集提示 | 00:44 的首个风之种子提示 | `src/main.js:308` 有相同完整提示字符串 [S9] |
| 地名 | HUD 显示 `THE SISTERS` | `src/main.js:392` 返回 `The Sisters`；第一版网页源码也有相同地点 [S9,S14] |
| 地点 | 后段有 `The Open Hand` 与海岸石手线索 | `tools/places/west_layout.py:320` 定义 `open_hand` / `The Open Hand` [S10] |
| 第一版归属 | 花海飞行、无明确城镇送货展示 | README 保留第一版试玩；第一版网页的 `index.html` 与 `src/main.js` 两个文件和第一版 GitHub commit **字节完全一致** [S7,S14] |

这些证据共同支持它是原片对应游戏，而非仅标题相似。当前主分支已经加入后续玩法；没有把当前版本当成视频录制版本逐字节核验。

## 源码、试玩与版本

- **源码主仓库：** [jjcm/petalwake](https://github.com/jjcm/petalwake)。创建于 2026-11-10，默认分支 `main`。
- **第一版试玩：** [petalwake.non.io](https://petalwake.non.io/)，更接近原视频的花海、海面飞行内容。
- **第一版源码快照：** [8b773736f40388e88218a82ff9ed69608592acd6](https://github.com/jjcm/petalwake/tree/8b773736f40388e88218a82ff9ed69608592acd6)。此 revision 在城镇更新之前，网页入口和主 JS 已读回一致。
- **第二版试玩：** [petalwake.non.io/v2](https://petalwake.non.io/v2)，增加城镇、送货、降落地点、隐藏地点和海岸生态。
- **本次核验主分支快照：** [25443cef0eba802052d9ef24c94ba3c4157b6f2e](https://github.com/jjcm/petalwake/tree/25443cef0eba802052d9ef24c94ba3c4157b6f2e)。commit 说明为新增城镇等功能，提交时间 2026-11-10 22:39:30 UTC。
- LICENSE：MIT，版权行标明 Jacob Miller。`package.json` 为 `1.0.0`，`three` 固定 `0.187.0`；这个 package 版本不等于“视频就是 v1.0.0”的独立证明。[S11]

两个试玩网页已读取标题与内容；第一版入口及主 JS 均返回 HTTP 200。**没有运行渲染或操纵角色，不宣称试玩通过。**

## 技术实现

### 模型、素材和游戏运行时

README 的制作说明称使用 Claude Code / Fable 5.2，从短简报和参考片段开始，再根据试玩备注调整；城镇等内容在下一天追加。代码、shader、地形烘焙和资产管线由模型编写的说法来自作者自述，不把 commit 的模型共同作者署名当成全部代码来源的独立证明。[S7]

运行时由 **Three.js r187 + 原生 JavaScript + 自定义 GLSL** 实现。`index.html:12–13` 的 import map 指向仓库自带的 `vendor/three`，`index.html:60` 加载 `src/main.js`；不需要在运行时把每一帧发送给大模型。[S7,S9,S11]

素材不是全部“模型写几何代码”生成的。README 说明角色、树石、部分地点素材及材质通过 fal / Meshy 生成并由 Blender 脚本加工，建筑由 Python / Blender 脚本建模。仓库包含处理后的 `assets/`，约 250 MB 的原始 `art/` 不在仓库中；这些生成服务的费用未披露。[S7]

### 关键代码入口

| 模块 | 真实源码入口 | 已核验的实现范围 |
| --- | --- | --- |
| 入口与 HUD | `index.html`、`src/main.js` | Three.js import map、场景初始化、种子收集与 HUD 提示；不是视频播放器 |
| 飞行 | `src/player/flight.js` | `Flight` 与速度/转向/地形约束相关逻辑；未执行手感测试 |
| 花海 | `src/world/meadow.js` | GPU 实例几何与自定义草/花 shader，质量档、网格池；不是原先泛化建议里的 `InstancedMesh` 直接套用 |
| 尾涡 | `src/fx/vortex.js` | 256 个轨迹截面，双向旋转涡核；CPU 采样粒子作用、GPU 绘制地表响应场 |
| 草花/水面响应 | `src/fx/wake.js`、`src/fx/strip.js` | 滚动尾迹场与累计花瓣损失图，供材质读取 |
| 海面 | `src/world/water.js` | 自定义 `Water`，Gerstner 波、反射/折射、岸边效果；**不是** Three.js 官方 addon `Water.js` 原样接入 |
| 地形 | `src/world/terrain.js`、`tools/terrain/bake.py` | README 说明为离线烘焙高度场与 CDLOD；已读取运行时源码，未运行烘焙 |
| 后处理 | `src/core/pipeline.js` | 原项目帧管线；README 描述 HDR、抗锯齿、运动模糊、bloom 等，未测 GPU 开销 |
| 声音 | `src/audio/audio.js` | 浏览器合成声音的源文件；未播放或检查听感 |

`meadow.js:447–508` 使用实例几何数量、草/花 `ShaderMaterial`、池化网格和质量档；`vortex.js:1–25` 明确双涡轨迹及 CPU/GPU 两条消费路径；`main.js:298–309` 更新种子计数并触发提示。以上是实际读取源码得到的判断。[S9,S12,S13]

这次源代码定位把首轮报告的“三维运行库候选”收敛为具体 Three.js 游戏实现，但不因此认定物理准确性、性能或全部玩法质量已经验证。

## 相关项目与资料

| 资料/工具 | 与本案例关系 | 证据状态 |
| --- | --- | --- |
| Petalwake | 本次找到的实际游戏工程 | 截图、特征文字、网页主 JS 与固定 revision 交叉核验 |
| Claude Fable 5.2 | 作者在 README 点名的编程模型 | 型号真实，官方发布日期 2026-11-09；作者调用日志未取得 [S2–S3,S7] |
| Claude Code | 作者 README 写明的开发工具 | 制作说明已读；未取得完整开发会话 [S4,S7] |
| Three.js | 实际运行库 | 原工程 import map、package 与运行时源码已核实 |
| fal、Meshy、Blender | 作者描述的素材生成与处理链路 | README / 目录可见；未重新生成资产、未使用任何服务凭据 |
| OhMyGame | 仍可参考的相关游戏工作室 | 没有证据表明作者用了它；[既有专题](../2026-10-30-ohmygame-ai-game-studio/README.md) 另行记录 |

## 复现路径

**状态：启动入口与源文件已静态检查，未在本次运行原项目；以下按仓库说明整理。**

### 直接运行已有工程

1. 获取主分支源码，或固定到上面的第一版 revision。项目带有处理后资源和 `vendor/three`；普通试玩不需要先重新调用素材生成模型。
2. 在仓库根目录使用 Python 3 启动自带静态服务器：

   ```bash
   python3 tools/serve.py
   ```

3. 在复现者自己的浏览器打开脚本显示的服务入口；需要通过 HTTP 提供模块，不能只双击 `index.html`。**这不是提供给飞书用户访问的线上交付地址；线上试玩请用上面的真实公网链接。**
4. 建议先用桌面 Chrome 和 WebGL2，按 README 可加 `?q=low` 降低花海密度。作者只声明在 Chrome 开发检查，不能推成所有浏览器/手机都已兼容。
5. 控制：W/S 俯冲/爬升，A/D 倾斜转向，Shift 加速，Space 减速，C 切换镜头，M 静音。第二版还有降落、送货、翻转和日志等操作，详见对应版本 README。

`tools/serve.py` 只使用 Python 标准库；包含默认本机绑定的静态服务及受约束的截图保存入口，已读取但没有执行。仓库 `.gitattributes` 没有 Git LFS filter，不额外假设必须安装 Git LFS。[S11]

### 重建或重新生成资产

运行已提交资产和重新生成资产是不同合同。地形重烘焙需要工具依赖；城镇建模需要 Blender，生成新美术可能需要 `FAL_KEY` / `MESHY_API_KEY` 并产生费用。README 指明原始 `art/` 不随仓库分发，不能承诺拿到仓库就能完全重演每一步生成过程。[S7]

### 建议验收

确认资源无 404、能够起飞转向/升降、种子只计一次、花海和海面响应持续更新；在注明设备、浏览器、分辨率和质量档下测帧时间。第一版/第二版分别验收，不把读到 HTML 或下载 JS 当成游戏运行通过。

## 成本口径

原抖音“约四小时、200 美元月套餐用了 20%”仍属于发布者陈述，未取得额度周期、账单和 token 日志。`200 × 20% = 40` 不是实际开发费用证据。作者 README 说首日制作、下一日追加功能，也不能用于核对原片四小时的计时范围。[S1,S7]

Fable 5.2 官方标准 API 价格为输入每百万 tokens 8 美元、输出 40 美元，订阅额度与按量计费不能混算。当前 200 美元/月 Ultra 有全模型周额度和独立 Fable 周额度；不能据此替发布者确定具体账号及 20% 分母。参考视频、fal/Meshy、已有资产、人力与托管费用仍有缺口。[S2,S6]

## 适用场景与限制

- 已经找到的是完整可阅读的游戏工程，不只是 Skill、教程或概念视频；适合研究浏览器飞行、花海实例化、尾迹响应和 AI 资产管线。
- README 顶部作者明确提醒代码没有经过其逐行阅读；源码公开不等于安全、性能或维护质量已经审查。此轮仅做定位和关键静态核验，不是代码审计。
- 第一版 README 写首次加载约 48 MB，第二版写约 95 MB。这些是作者说明，本次没有完整加载所有资源测量；不能据此承诺 1060 帧率或移动端运行。
- LICENSE 和代码已读；字体与生成资产的来源另有说明，不把 MIT 当成所有外部服务、素材的无条件授权。
- 本次没有安装游戏、启动服务器、调用付费模型或重生成美术，也没有向外部服务发送本机凭据。

## 待核实事项

1. 抖音 `@pwnies` 对应 X 原帖的精确链接与署名绑定；当前游戏归属不依赖同名 GitHub 账号推断。
2. 原视频录制的是哪个历史构建，以及性能、碰撞/收集和各设备表现；第一版入口与主 JS 已核对，但没有按全量工程做视频版本一致性证明。
3. 完整原始提示和开发会话，参考视频生成器的名称及制作费用。
4. 四小时计时范围、20% 额度的分母，以及实际模型/素材账单。

**已解决的缺口：** 正式名称 Petalwake、对应源码、许可证、真实公网试玩入口、第一版与第二版区分及实际运行库。

## 来源与证据

| 编号 | 来源与链接 | 版本/日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [抖音原片](https://www.douyin.com/video/7706789737599634714) | 2026-11-11 | 2026-11-11 | 原始宣称、15 个时间点画面及特征文字 |
| S2 | [Fable 5.2 官方型号页](https://platform.claude.com/docs/en/models/fable-5-2/overview) | 2026-11-09 发布 | 2026-11-11 | 型号、API 价格与规格 |
| S3 | [Anthropic 发布公告](https://www.anthropic.com/claude-fable-and-mythos-5-2) | 2026-11-09 | 2026-11-11 | 发布日期与用途定位 |
| S4 | [Claude Code 官方概览](https://code.claude.com/docs/en/overview) | 持续更新 | 2026-11-11 | 编程 Agent 与游戏运行时的层次区别 |
| S6 | [Ultra 官方说明](https://support.claude.com/en/articles/17728952-what-is-the-ultra-plan) | 持续更新 | 2026-11-11 | 200 美元订阅与额度周期 |
| S7 | [Petalwake README](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/README.md) | 固定主分支 commit `25443cef…` | 2026-11-11 | 游戏名称、版本入口、制作自述、素材、操作与运行说明 |
| S8 | [仓库花海截图](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/screenshots/meadow_wake.jpg) | 同一 commit | 2026-11-11 | 已下载视觉核对，角色与环境对应 |
| S9 | [主入口源码](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/src/main.js) | 同一 commit；308、392 行 | 2026-11-11 | 风之种子提示、The Sisters、初始化调用 |
| S10 | [The Open Hand 地点定义](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/tools/places/west_layout.py#L320) | 同一 commit | 2026-11-11 | 原片地名和海岸石手线索 |
| S11 | [LICENSE](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/LICENSE)、[package](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/package.json)、[index](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/index.html)、[serve.py](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/tools/serve.py) | 同一 commit | 2026-11-11 | MIT、Three.js 固定版本、模块路径、启动入口 |
| S12 | [花海源码](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/src/world/meadow.js#L447) | 同一 commit | 2026-11-11 | 实例几何、shader 与网格池 |
| S13 | [尾涡](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/src/fx/vortex.js)、[海面](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/src/world/water.js) | 同一 commit | 2026-11-11 | 原项目自定义效果源码，不是泛化候选 |
| S14 | [第一版源码](https://github.com/jjcm/petalwake/tree/8b773736f40388e88218a82ff9ed69608592acd6)、[第一版公网页面](https://petalwake.non.io/)、[第二版公网页面](https://petalwake.non.io/v2) | 第一版固定 commit `8b773736…` | 2026-11-11 | 网页内容可读；第一版 index/main 两文件与 GitHub 字节一致，未试玩 |

附 [结构化研究快照](research_snapshot.json)，保留原始观察、版本与静态核验结果，不公开登录态或全量原视频。

## 更新记录

- 2026-11-11 首轮：读取抖音原片，核对 Fable 5.2 与成本口径；当时原工程/试玩尚未定位，三维运行库只列为候选。
- 2026-11-11 源码追查：根据 `The Open Hand` 找到 `jjcm/petalwake`，用截图、种子提示与 `The Sisters` 交叉核对；确认源码/MIT/试玩，并将第一版 index/main 与固定 GitHub commit 逐文件比对一致。以实际实现替换初轮泛化候选，仍不宣称运行测试或开发账单已经验证。
