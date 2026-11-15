# Small Magic：纯代码场景与 WebGPU 破坏物理的巫师沙盒

收录日期：2026-11-15

最近核实：2026-11-15，Asia/Shanghai

研究状态：部分核实——原作品、官方项目、固定版本源码和许可已读取；未运行游戏、构建或性能测试，制作耗时与模型调用未独立验证。

## 一句话结论

视频对应 **blendi 在 Patch 发布的 [Small Magic](https://patch.gg/games/blendi/small-magic)**。它不是实时让 AI 生成游戏画面，而是 **JavaScript/Three.js 绘制程序化世界，WebGPU 上的 three-avbd 计算可断裂刚体结构，七种法术改变场景状态**。最值得借鉴的是“场景按构件搭建 → 连接承重 → 施法施力 → 断裂坍塌 → 画面与声音反馈”的完整交互链路。[S1–S8]

“零模型、零纹理”应理解为**没有导入的三维模型与场景贴图素材**，不是没有几何体、运行时纹理、UI 图片或第三方音效。完整破坏玩法需要可用的硬件 WebGPU；只支持普通 WebGL 的浏览器可能留下草地与法术，却没有建筑。[S3,S5,S7,S8]

## 原始线索

- 用户分享：[抖音短链](https://v.douyin.com/XAelPajEvmw/)；规范作品：[7708132655045441946](https://www.douyin.com/video/7708132655045441946)。
- 发布者：**最佳故事人**；抖音发布时间：**2026-11-15 07:00:00 +08:00**。原简介称 blendi 用 **fable 5.2** 在一天内制作巫师沙盒，七个法术、约 1800 个可摧毁物理部件、零三维模型与纹理，开源且可玩。[S1]
- 原视频 **54.752653 秒，1280×720，H.264/AAC，19,626,510 字节**。实际读取了完整简介，以及约 2.5、7.5、12.5、17.5、22.5、27.5、32.5、37.5、42.5、47.5、52.5 秒的十一幅采样画面；没有完整连续观看、听音或 ASR。
- 画面依次能看到 Explosion、Singularity、Tornado、Fire、Frost、Growth；左上角一直有七个法术图标。没有据此声称七种法术都已完整试玩。
- 发布者在原作品评论中补了一张链接便签图，显示 `patch.gg/play/blendi/sm...`。实际打开 Patch 的 Discover 后找到完整地址，再核对项目作者、法杖、草地、建筑及七法术说明，定位 **Small Magic**，不是把 `blendi-remade` 的 sprite-sheet-creator、falcraft 或其他同作者项目代替原工程。[S1,S2]
- 官方项目首次上线时间字段为 **2026-11-14T12:11:45.363Z**；本轮读取到公开版 **1.0.4**，发布于 **2026-11-15T05:27:26.307Z**。研究固定源码 commit：
  `70252753137776f81de8dbb0518586300c027f74`。[S2,S3]

## 技术实现

### 1. 输入与主循环：模型负责开发，浏览器负责运行

`src/main.js` 创建 `THREE.WebGLRenderer`、世界、第一人称 Walker、法杖、后处理、火焰、法术和声音。WASD/鼠标控制行走与视角，左键施法，数字 1–7 或滚轮切换；部分法术蓄力后释放，部分持续喷射。[S4,S6]

`tick(dt)` 统一驱动行走、世界状态、破坏物理、法术、火焰、粒子与声音，然后渲染。这条实际运行路径没有调用 Fable 来生成每一帧。“Fable 5.2 / 一天完成”是**抖音发布者的开发过程陈述**，并非运行时技术栈或本轮独立计时结论；没有取得原始开发记录、提示词或模型请求日志。[S1,S4]

依赖文件锁定 `three: 0.186.1`，开发依赖为 `vite: 8.3.5` 和 `playwright-core: ^1.64.1`，不是沿用另一个案例的 Three.js r187。`patch.json` 记录公开版 1.0.4；Vite 将别名 `three-avbd` 指向仓库内的源文件。[S3,S8]

### 2. 程序化画面：没有导入场景素材，不等于没有纹理

- `src/structures.js:plan` 以 Builder 按尺寸摆放石块、木梁、墙面和瓦片，构成 keep、cottage、mill、abbey 四个建筑区域；每个构件是盒状体，连接到接触它的其他构件。[S5]
- `src/ruin.js` 用 `InstancedMesh + BoxGeometry` 显示构件，shader 根据材质、局部坐标和噪声绘制石材、木材、砖瓦等外观。不是把一个完整建筑模型换成“毁坏动画”。[S5]
- `src/meadow/world.js` 组织草地、树、地形与状态图；`src/paint.js` 是程序化画面组件。状态图用 `DataTexture`，符文图集用 `CanvasTexture`。因此若按图形 API 的严格定义，说“完全不用纹理”并不成立；**纹理数据可以由代码生成，而不用美术贴图文件**。[S7]
- 七个 UI 法术徽章是 `public/ui/1.webp` 至 `7.webp`；许可说明和 credits 称用 Nano Banana 2.1 生成，封面也使用图像模型。不能把场景程序化扩大为“所有画面均无图片、所有美术均无模型服务”。[S8]

### 3. 破坏物理：WebGL 画图，WebGPU 计算

`createRuin` 申请 `navigator.gpu`、硬件 adapter 与 device，再创建 three-avbd 的 World。它读取 Builder 的构件与焊接关系，以 `Structure.build` 生成结构，先稳定结构，再按承重赋予连接强度；连接断裂会触发 `world.onBreak` 与碎屑效果。[S5]

物理坐标使用 z 向上，画面世界使用另一套坐标，代码显式转换。WebGPU 求解后的构件姿态被读回，由原 WebGL 渲染器绘制，所以两套 API 各司其职，而不是整款游戏只有 WebGPU 渲染。[S4,S5]

容量不是常量 1800：`MAX = ceil((built.pieces.length + 64) / 256) * 256`，接触、pair、manifold 缓冲按 MAX 预分配，`maxSubsteps = 2`，逐帧读回。**本轮没有执行场景生成，也没有统计可破坏/固定/树木构件的实际数量**，保留“约 1800”为原帖量级陈述；它不是“所有设备稳定跑 1800 刚体”的性能承诺。[S1,S5]

vendored three-avbd 来自 Steven Bobyn，记录上游 commit `cd3ce901557aa9cf4f7ede489fac385971d383ea`，MIT。`VENDOR.md` 还记录一个邻接表排序 kernel 的修改；这属于依赖版本与修改说明，不把文档的确定性或提速描述写成本轮实测。[S8]

**没有 WebGPU 时不是等价降级。** `createRuin` 返回 null，主入口显示 `No buildings here: this browser has no WebGPU`，其余草地与法术仍可构建。硬件加速关闭且识别为软件渲染时，正常路径会停止进一步加载并提醒开启加速。[S4,S5]

### 4. 七法术与共享场景状态

`SPELLS` 数组明确列出 Fire、Frost、Wind、Growth、Explosion、Singularity、Tornado；实际键盘处理也覆盖 Digit1–Digit7，不能被文件开头残留的“1 to 4”注释误导。[S6]

| 法术 | 源码所定义的行为 | 证据与边界 |
| --- | --- | --- |
| Fire | 按住蓄力，松开抛射；命中后点火，火在草地与树间传播 | spells.js、fire.js；采样画面有燃烧 [S6] |
| Frost | 持续喷射，标记冻结地面与湖面，并调用 `fire.quench` 灭火 | spells.js；采样画面有冻结，灭火未单独实测 [S6] |
| Wind | 蓄力后投射阵风，压草、落叶、助燃并作用于构件 | spells.js；该类未完整观测操作过程 [S6] |
| Growth | 调用 `fire.regrow`、世界生长状态与树木状态更新，恢复烧焦/冻结地面 | spells.js；不是确认所有倒塌建筑都自动重建 [S6] |
| Explosion | 持续蓄力触发爆炸；提前松开可取消 | blast.js、spells.js；采样有爆炸 [S6] |
| Singularity | 按住维持黑洞、拉扯构件，松开后关闭与释放 | hole.js、spells.js；采样有吸附与碎块 [S6] |
| Tornado | 召唤并按瞄准位置带动，可与火、冰、水状态交互 | twister.js、spells.js；采样有普通/火龙卷 [S6] |

视觉上再叠加相机震动、视野变化、暗化、冲击波与粒子。它们让“施法有重量”，但不等于这些冲击已按真实流体力学或气象物理模拟。[S4,S6]

### 5. 声音与公开源码的资产缺口

`src/sound.js` 合成程序化声音，仓库另带五条 Kenney 草地脚步录音，标为 CC0。发布版还叠加 **39 条 Sonniss 录音，切成 76 个小文件**，这些文件不在公开仓库。[S8]

作者说明许可允许游戏使用，但不允许把录音作为独立素材再分发；下载原始记录约 830 MB，需另外确认。本轮**没有下载这些音频，也没有调用生成模型**。复现应先使用 `?bare` 或自己的可授权音效，不把录音打包进公开 Skill/仓库。[S8]

### 关键判断与证据状态

| 关键判断 | 状态 | 依据 |
| --- | --- | --- |
| 原视频对应 Small Magic，官方项目位于 Patch | 已核实，链接与画面/功能互证 | 原作品评论便签、Discover、官方游戏页 [S1,S2] |
| 七种法术已实现为独立 dispatch 与处理代码 | 静态源码已核实；七种运行未验收 | `SPELLS` 与各模块 [S6] |
| 程序化场景＋WebGL 渲染＋WebGPU 破坏物理 | 静态源码已核实 | main.js、ruin.js、world.js [S4,S5,S7] |
| 场景无导入模型/贴图，但有程序生成纹理、UI 图片与录音 | 原说法需限定；源码与许可已核实 | DataTexture/CanvasTexture、UI、credits [S7,S8] |
| 约 1800 个可破坏物理部件 | 发布者宣称，数量未测 | 原简介；代码按实际构件动态分配 [S1,S5] |
| 用 Fable 5.2 在一天内开发 | 发布者宣称，模型日志/开发时长未取得 | 原简介 [S1] |
| 代码 MIT，不代表所有美术和音频均 MIT | 许可文件与平台字段已核实 | LICENSE、LICENCE-NOTES、MISSING_ASSETS [S3,S8] |

## 相关项目与资料

先比较应用目标，再比较底层工具；**Small Magic 位于 Patch，不以 GitHub Stars 计量**，不能把 Patch 的 plays、likes、remixes 与 GitHub 星数混算。以下是 2026-11-15 的实际查询快照，不是质量排名或性能排名。

| 项目与关系 | 核实时 Stars / 许可 | 用途与交付结果 | 可执行前置条件及差异 |
| --- | --- | --- | --- |
| **Small Magic**，原工程 | GitHub 不适用；代码 MIT，美术字段 `LicenseRef-Proprietary` | 第一人称七法术与可破坏建筑沙盒 | 官方试玩入口；本地构建需 Node/依赖，完整破坏需硬件 WebGPU [S2–S8] |
| [Petalwake](https://github.com/jjcm/petalwake)，邻近成品案例 | **68**，MIT；commit `25443cef0eba802052d9ef24c94ba3c4157b6f2e` | 扫帚飞行、花海风场、岛屿探索与递送 | 静态 HTTP 服务、桌面 WebGL2；有处理后模型/贴图，不是七法术破坏沙盒，也不是“零美术资产” [S9] |
| [three-avbd](https://github.com/sbobyn/three-avbd)，原工程采用的物理基础 | **161**，MIT；当前 main `f3d8c48cc640b8f29899e43c5655a90cebfbb4d8` | GPU 刚体、接触、关节与可断裂结构，输出模拟机制 | 当前 README 指定 Node 22.18+、pnpm 10.18.0、硬件 WebGPU；0.4 候选源码与已发布包不能混用；不是完整游戏 [S10] |
| [Rapier](https://github.com/dimforge/rapier)，替代物理方案 | **6072**，Apache-2.0；commit `475caa3ff4646fd9a796b67d14116256f4962bc7` | 2D/3D 物理库与多语言示例，可另建同类交互 | 需使用对应语言绑定并自行连接画面、法术、断裂规则。不是换包即复现，也没有本轮效率对照 [S11] |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js)，替代 Web 3D 开发底座 | **26364**，Apache-2.0；commit `c221550275c9072f1c35f19398130dbd9cd4cfb1` | Scene/Engine、相机、几何体与渲染循环，官方 playground | 需自己实现玩法与结构破坏；库使用门槛与开发整个引擎仓库的 Node/npm 要求不同；官方 CDN 不建议用于生产 [S12] |

**如何选：**想拆解可玩交互，优先看 Small Magic；想研究风场、花海和飞行反馈，再看 Petalwake；想先验证一个刚体/断裂机制，看 three-avbd 或 Rapier 的小例子；做通用 Web 3D 项目再比较 Babylon.js。更高 Stars 的库不是原视频游戏的高星“同款”，本轮没有找到并验证一个七法术、程序化画面、同样破坏机制的高星直接替代成品。

另外，Small Magic 的 LICENSE 尾部残留 Rapier/figure 路径说明，但当前已读取的主入口、破坏入口与 Vite 别名实际使用 three-avbd。**不能只看该条 notice 就断言当前破坏求解器是 Rapier**；完整历史及残留说明仍可继续审计。[S4,S5,S8]

## 复现路径

**基于实际读取的源码和文档整理，未实际运行。**本次只读取来源与源码，不安装、不构建、不发布、不修改游戏项目。

1. **直接观察公开版：**打开 [Small Magic 试玩](https://patch.gg/play/blendi/small-magic)。桌面浏览器开启硬件加速，检查是否具备硬件 WebGPU；只有画面出现，不足以确认破坏物理可用。本轮仅取得试玩包装页与 1.0.4 标记，游戏 iframe 域名直取曾 SSL 超时，没有据此宣称试玩成功。
2. **取得源码：**官方公开 clone URL 是 `https://git.patch.gg/blendi/small-magic.git`，不是猜测的 GitHub 同名仓库。先选择独立目录，再取源码并固定本报告 commit。本轮 clone 不支持 partial filter，传输停滞后主动停止；改用公开、无需登录的 repo/tree 和 repo/file API 成功读取选定代码，每个响应都核对 commit，并记录 blob/hash 到相邻快照。
3. **安装前审查：**确认 `package.json`、锁文件、`build.mjs`、`vite.config.mjs`、`tools/serve.mjs` 与许可证。`build.mjs` 执行本地 Vite 构建、生成录音 manifest 并复制许可；构建会重建该新目录内的 dist，不应指向已有项目。
4. **环境：**作者 README 写 Node 20+，但工程锁定 Vite 8.3.5，安装前需按其实际包 engine 约束选择兼容 Node；本轮没有查询安装器 engine 或运行依赖验证，不保证所有 Node 20 小版本都可用。正常构建不需要 Fable/fal API Key；额外复刻 AI 美术或第三方音效另算。

   ```sh
   git clone https://git.patch.gg/blendi/small-magic.git small-magic-review
   cd small-magic-review
   git checkout 70252753137776f81de8dbb0518586300c027f74
   # 完成依赖、脚本、素材许可审查后再执行：
   npm ci
   npm run build
   npm run serve
   # 默认脚本端口： http://127.0.0.1:5495/
   ```

5. **最小验收：**加载成功 → 能走动和切换七法术 → 实际存在建筑/物理对象 → 爆炸或黑洞使连接断裂、构件位姿改变 → 重载可以重建初始状态 → 查看错误与长帧记录。单独验证火→冰灭火、火→风/龙卷风助燃、生长恢复地面；不要把生长当成重建整座建筑。
6. **证据与性能：**源码提供 `window.lab`、`?capture` 和 `tools/gaps.mjs`。后者记录超过 30 ms 的帧间隔、加载与错误，但默认 `--cast` 列表是 **Fire、Wind、Frost、Growth、Fire**，并没有覆盖七种；全面验收需显式补 Explosion、Singularity、Tornado，并记录 adapter、浏览器、分辨率、实际构件数、测试时长与 P99。测试工具存在不是测试已经通过，也不能把 capture 的手动推进速度当真实 FPS。[S4,S13]
7. **音效先走 bare：**以 `?bare` 比较合成声音版本；若需要发布版完整录音，单独核对 Sonniss 授权、下载体积与再分发限制后再决定。不能把相关抓取命令当作本轮自动下载许可。[S8]

## 适用场景与限制

- **适合学习：**有反馈的法术状态机、程序化场景、实例化构件、承重连接与断裂、视觉/声音联动，或一个边界明确的浏览器玩法原型。
- **不代表完整商业游戏：**当前介绍定位自由沙盒，没有“完整关卡、长线成长、多人服务、存档、移动适配全部完备”的证据；不能从一分钟演示推导生产验收。
- **硬件是关键门槛：**WebGL 负责画面，WebGPU 负责结构求解；移动端、关闭加速、不同 adapter/驱动需要分别验收。WebGPU 不可用时核心建筑消失，不能仅按“网页能打开”判成功。
- **许可按层处理：**游戏与物理代码 MIT；UI/封面的平台美术字段是 proprietary，AI 图片的来源说明不自动授予第三方所有商业权利；脚步 CC0 与 Sonniss 自有条款分开。正式复用优先保留代码 notices、替换不明确资产。
- **开发成本未知：**“一天”不是承诺，“用 Fable”不是项目 token 账单，也不能证明所有代码由同一模型一次生成。没有原始请求、订阅用量、人工工时与素材费用，不输出伪精确成本。
- **不自动迁入已有游戏仓库：**本次仅收录与比较；把结构破坏机制接入其他项目属于另一次开发与验收任务。

## 待核实事项

1. 原始 blendi 开发帖、Fable 请求/Agent 记录、一天的时间边界及真实费用；抖音转述不构成独立证据。
2. 1.0.4 的实际构件数、可破坏/固定/树木分项、极端坍塌后的性能和错误；未运行计数或 benchmark。
3. 七法术完整运行与状态组合，以及不同浏览器、GPU、移动端的功能差异。
4. 当前 UI/封面再使用授权、生成服务条款；Sonniss 官方许可原文尚未独立全文读取，这部分现阶段依据项目许可说明，不能扩张其权利。
5. Clone 的稳定可用性与完整依赖构建；README 的 Node 20+ 是否满足锁定 Vite 的精确 engine。
6. LICENSE 的旧 Rapier/figure notice 与当前目录不一致；未全量审计历史及所有 third-party 文件。

## 来源与证据

以下均为本轮实际读取的页面、文件或公开 API；固定版本文件 API 会返回 commit、Git blob 和正文。相邻 `research_snapshot.json` 记录读取成功的路径与 SHA-256，**不发布原视频、完整评论截图、Cookie 或浏览器状态**。

| 编号 | 来源与链接 | 发布日期/版本 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [抖音原作品](https://www.douyin.com/video/7708132655045441946)，简介、采样画面与发布者评论链接便签 | 2026-11-15 07:00 +08 | 2026-11-15 | 原始宣称、视觉演示及 Patch 链接线索 |
| S2 | [Patch Discover](https://patch.gg/discover)、[官方 Small Magic 页](https://patch.gg/games/blendi/small-magic) | 初次上线 2026-11-14；持续更新 | 2026-11-15 | 名称、作者、法术、公开地址与版本更新 |
| S3 | [官方源码浏览器](https://patch.gg/games/blendi/small-magic/source)、[package.json API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=package.json&ref=70252753137776f81de8dbb0518586300c027f74)、[patch.json API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=patch.json&ref=70252753137776f81de8dbb0518586300c027f74) | 固定 commit 7025275；1.0.4 | 2026-11-15 | 开放源码、依赖、版号；试玩包装页未等于游戏运行 |
| S4 | [src/main.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fmain.js&ref=70252753137776f81de8dbb0518586300c027f74) | 同一固定 commit | 2026-11-15 | WebGL 主循环、硬件加速/WebGPU 降级、lab 工具 |
| S5 | [ruin.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fruin.js&ref=70252753137776f81de8dbb0518586300c027f74)、[structures.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fstructures.js&ref=70252753137776f81de8dbb0518586300c027f74)、[physics/structure.ts API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fphysics%2Fstructure.ts&ref=70252753137776f81de8dbb0518586300c027f74) | 同一固定 commit | 2026-11-15 | GPU 求解、构件生成、连接承重与断裂、容量计算 |
| S6 | [spells.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fspells.js&ref=70252753137776f81de8dbb0518586300c027f74)，另读取 fire.js、blast.js、hole.js、twister.js | 同一固定 commit | 2026-11-15 | 七法术 dispatch、环境状态与特效逻辑 |
| S7 | [meadow/world.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fmeadow%2Fworld.js&ref=70252753137776f81de8dbb0518586300c027f74)、[paint.js API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=src%2Fpaint.js&ref=70252753137776f81de8dbb0518586300c027f74) | 同一固定 commit | 2026-11-15 | 程序化画面、运行时 DataTexture/CanvasTexture |
| S8 | [LICENCE-NOTES.md API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=LICENCE-NOTES.md&ref=70252753137776f81de8dbb0518586300c027f74)、[MISSING_ASSETS.md API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=MISSING_ASSETS.md&ref=70252753137776f81de8dbb0518586300c027f74)；另读取 LICENSE、CREDITS、VENDOR、build、vite、serve | 同一固定 commit | 2026-11-15 | 代码与图片/录音权利边界、依赖来历、构建入口 |
| S9 | [Petalwake README](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/README.md)、[LICENSE](https://github.com/jjcm/petalwake/blob/25443cef0eba802052d9ef24c94ba3c4157b6f2e/LICENSE) | 固定 commit 25443ce | 2026-11-15 | 不同成品目标、WebGL2/HTTP、资产与 MIT |
| S10 | [three-avbd README](https://github.com/sbobyn/three-avbd/blob/f3d8c48cc640b8f29899e43c5655a90cebfbb4d8/README.md)；Small Magic 的 vendor LICENSE/VENDOR 已读 | 当前 main；与游戏 vendored 版本不同 | 2026-11-15 | 物理库定位、硬件 WebGPU、候选版与质量边界 |
| S11 | [Rapier README](https://github.com/dimforge/rapier/blob/475caa3ff4646fd9a796b67d14116256f4962bc7/README.md)、[LICENSE](https://github.com/dimforge/rapier/blob/475caa3ff4646fd9a796b67d14116256f4962bc7/LICENSE) | 固定 commit 475caa3 | 2026-11-15 | 替代物理库、多语言绑定、Apache-2.0 |
| S12 | [Babylon.js README](https://github.com/BabylonJS/Babylon.js/blob/c221550275c9072f1c35f19398130dbd9cd4cfb1/README.md)、[license.md](https://github.com/BabylonJS/Babylon.js/blob/c221550275c9072f1c35f19398130dbd9cd4cfb1/license.md) | 固定 commit c221550 | 2026-11-15 | 通用 Web 3D 底座、示例循环、CDN 提醒与 Apache-2.0 |
| S13 | [tools/gaps.mjs API](https://patch.gg/api/v1/projects/blendi/small-magic/repo/file?path=tools%2Fgaps.mjs&ref=70252753137776f81de8dbb0518586300c027f74) | 同一固定 commit | 2026-11-15 | 长帧/错误记录，默认施法列表不覆盖七种 |

## 更新记录

- 2026-11-15：首次收录；从抖音简介、视频采样与链接便签溯源 Small Magic，读取固定源码与许可，比较邻近成品和底层库，明确未运行、数量/成本未测及资产授权边界。
