# Dash fighter / fly：精灵堆叠像素战斗机与“32KB”口径核查

收录日期：2026-11-17

最近核实：2026-11-17，Asia/Shanghai

研究状态：**原项目及可读业务代码已定位；未找到对应 GitHub 开源仓库，32KB 历史版本与开放许可证未核实，未完成试玩验收。**

## 一句话结论

原视频对应 Dash（`@creativedash`）的 **fighter / fly**，入口是 [remix.ui8.ai/fly](https://remix.ui8.ai/fly)，现跳转到 [UI8 Forge 分享页](https://forge.ui8.ai/share/frag_1eb8944c-57b1-42ca-a909-5c2d7e517c24)。已从该公开预览读取战斗机组件与场景、模型、座舱等九个依赖模块，不是用相似仓库冒充原项目。核心画面确实使用自写的软件像素渲染和精灵堆叠，没有发现 Three.js 依赖；但当前是 **fighterv2**，使用 React，并有可选 WebGL 火焰层，不能把“32KB、零引擎”扩写成“整个网页只有32KB、零库、零GPU”。[S1–S4]

## 原始线索

- 用户原分享：[抖音短链](https://v.douyin.com/yc_GihotvsA/)；[规范作品链接](https://www.douyin.com/video/7708679164118830371)，视频 ID `7708679164118830371`。
- 发布者：Enter.AI；平台时间：2026-11-16 16:12:18 +08:00。
- 已读完整详情、简介与页面正文；下载原视频，`ffprobe` 核实 32.933333 秒、9,981,414 bytes、1080×2356 H.264/AAC。查看约 0、3、6、9、12、15、18、21、24、27、30 秒采样画面，并单独放大12秒原帖截图。**未完整听音频、未做ASR或连续全程观看。**
- 简介宣称：32KB代码、纯2D Sprite Stacking、没有传统3D引擎、俯视/追尾/座舱三视角、网页直接飞行；视频底部还列出噪声高度图、HUD、UI8 Forge参数与Remix。
- 约12秒出现 Dash / `@creativedash` 原帖画面，清楚给出 `remix.ui8.ai/fly` 和 `No 3D engine, no polygons, 32 KB of code.`。公开页面标题与描述为 `fighter`，同样写明像素战斗机、堆叠岛屿、三视角和翻滚/推力控制。[S1–S2]
- [二手报道](https://bitcoinversus.tech/2026/11/15/32kb-flight-game-canvas2d-sprite-stacking-pixel-art-jet-2026/)给出[候选 Dash X 原帖](https://x.com/creativedash/status/2122000830895386680)。本机访问 X 遇到 TLS 证书不匹配，未跳过证书检查；因此精确 X 帖子身份仍未独立读取确认，**对应关系主要依靠原片内可读链接与实际项目**，不把二手报道当源码审计。[S6]

### 原片到原工程的对应关系

| 核验点 | 原片证据 | 原项目证据 |
| --- | --- | --- |
| 入口/作者 | 12秒 Dash 截图中的 `remix.ui8.ai/fly` | 该地址返回 `fighter · Forge`，公开 fragment 的 slug 为 `fly` |
| 画面主题 | 灰橙战斗机、像素岛屿、海洋与层叠云 | 描述点名 pixel-art fighter / sprite stacking / stacked islands；`jet-model.ts` 定义灰色机体、橙色强调色与蓝绿座舱调色板 |
| 三镜头 | 0秒俯视、3秒追尾、6秒座舱，后段继续切换 | `view` 参数为 `top/chase/cockpit`，`updateView()` 在三种相机状态之间混合 |
| 交互/堆叠 | 后段层片分离、参数控制、HUD | `spread`、`pixelSize`、`altitude` 等公开 controls；源码 `sliceOrder`、HUD 与控制事件可读 |

这是相同入口和实现特征的交叉核验，不代表已经找到了原视频录制时的历史构建。[S1–S4]

## 源码在哪里、能否获取

### 原作者项目

1. [原入口](https://remix.ui8.ai/fly) / [当前 Forge 分享页](https://forge.ui8.ai/share/frag_1eb8944c-57b1-42ca-a909-5c2d7e517c24)：无需登录即可访问公开分享信息与预览入口，当前组件为 `fighterv2`。
2. 已观察到公开分享数据：`visibility=public`、`linkAccess=remix`、`passwordProtected=false`，匿名 viewer 的 `canRemix=true`。**点 Remix 时仍需登录 Forge**；分享页代码与[官方文档](https://ui8.ai/forge/docs)均说明，未登录者先进入登录页，复制到自己的工作区后是私有未发布项目。[S2,S5]
3. 正规拿工程路径：在自己的 Forge 账号登录 → 打开分享页 → Remix 到自己的工作区 → 通过项目文件编辑器查看 Code/Assets，或按官方已授权 Agent/MCP 的“pull into codebase”能力读取代码、资源和控制参数。文档说明拉取为复制，不改变原项目。本轮**没有登录新服务、创建副本或安装 Forge/MCP，也没有实际验证完整导出**。[S5]
4. 无需账号已读到的部分：公开预览 HTML 引用 `src/main.tsx` 与 `src/components/fighter-jet-eject.tsx`，再沿真实相对 import 读取九个业务模块，均HTTP200。虽然路径后缀为 `.tsx/.ts`，响应实际上是 `text/javascript`，类型已移除且 JSX 被转为 React 调用，**属于可读运行时代码，不等于原始TS工程ZIP**。临时预览签名URL会过期，故不在报告传播；从稳定分享页重新打开预览才是可持续入口。[S3–S4]
5. 有界 GitHub 搜索覆盖原链接、`user:creativedash`、`ui8 remix` 等；截至本次未找到与原片明确对应的源码仓库。这个结论不是“作者没有源码”，也不把同名 GitHub 账号自动绑定为原作者。

**许可证状态：** 分享支持平台内 Remix，不代表已采用 MIT/Apache 或允许把完整代码、美术、声音再公开发布。本轮未取得原项目明确开放许可证，也未取得所有素材的授权说明。因此只发布研究与哈希/路径证据，**不将原工程整包上传到本热点仓库**；正式产品或商业使用前应向作者确认代码与素材授权。

## 技术实现

### 从模型与地图到像素画面

1. **飞机并非视频贴图，也不是polygon mesh。** `src/lib/jet-model.ts:1–7,101–116` 定义34×46像素、13层水平切片。调色板索引以 `(count,index)` 游程编码后写成Base64，`decodeJet()` 用 `atob` 解码到连续 `Uint8Array`，再切分各层。这里的13层是飞机切片数，不是物理精度或地图层数。[S4]
2. **相机/投影由代码自写。** `src/lib/eject/scene.ts:3667–3680` 的 `project()` 将世界坐标变换成相机深度，再用 `1 + vQ * depth` 做透视缩放；`updateView():1038–1112`混合俯视、追尾、座舱位置、缩放与滚转。没有3D引擎不等于没有三维空间数学。[S4]
3. **飞机是切片加遮挡。** `drawJet():4114起` 把切片投影、按相对眼高排序，再画进软件像素缓冲；4181–4215还做体素多采样/层间补缝和切片排序，避免大角度下“散层”。飞行员另用 `voxel-sprite.ts` 的壳体采样、局部深度与描边，不应把v2全部对象都说成最朴素的二维旋转贴图。[S4]
4. **岛屿是程序化高度图。** `buildWorld():642–735` 用固定seed的伪随机数、多尺度value noise叠加、归一化及高度分布决定海平面，分段生成草地、岩石、雪顶和树林；`drawWorld():3683起` 将地面像素作为高度柱，近处优先占据像素并维护深度。代码不需要预制岛屿三角网格，但会分配高度/材料/像素/深度等数组。[S4]
5. **最终主场景走Canvas 2D。** `fighter-jet-eject.tsx:219,250起,389–441` 创建2D context，根据显示尺寸与pixel size动态计算内部分辨率，RAF循环 `step→render→ImageData→putImageData`。不支持把二手报道中的300×250当当前固定分辨率；内部宽高随视口和像素大小变化。[S3–S4]
6. **现代宿主/效果没有消失。** `src/main.tsx` 明确引入 Forge mount、React/ReactDOM 19.2.8。当前组件还导入 `createFlameLayer()`；选择 realistic 火焰、实际有火焰需要绘制时，`flame-layer.ts:148起` 创建WebGL context，用GLSL和覆盖三角形绘制透明火焰层。默认 `flameStyle=pixel`；失败可退回像素火焰。主场景无Three.js，但当前可选模式不是“整个工程没有WebGL/三角形”。[S3–S4]
7. **声音与资源是独立部分。** `sound.ts` 导入多条MP3，并通过fetch/Web Audio加载；公开资源清单包含飞机四视图、飞行员四视图与声音。源码里有模型数据不代表工程没有外部图音资源。本轮未下载音频、美术全量，也未验证播放与来源许可。[S4]

| 关键判断 | 证据状态 | 证据 |
| --- | --- | --- |
| 找到原入口而非相似项目 | 已核实 | 原片12秒URL＋页面slug/描述＋业务源码 |
| 主要画面是自写软件像素渲染/精灵堆叠 | 已核实到所读代码 | jet-model、scene、Canvas 2D输出 |
| 当前整个项目完全零库、零GPU | 不成立于所读v2代码 | React宿主＋可选WebGL火焰；不外推历史版 |
| 原视频对应版本代码准确32KB | 作者/转载宣称，未核实 | 未取得该历史构建和计量口径 |
| 项目达到任何设备流畅飞行 | 未验证 | 没有交互/FPS/设备测试 |
| 原项目可按MIT等自由再分发 | 未取得证据 | 平台Remix权限不是开源许可证 |

### “32KB”应该怎么理解

目前公开分享记录为 revision **44**、publishedRevision **43**，组件 `fighterv2`。公开元信息报告 `sourceByteSize=48,795`；实际HTTP读取的变换后组件正文为 **47,996 bytes**，九个业务依赖正文合计 **326,358 bytes**，本轮读取的十个业务模块共 **374,354 bytes**。这仍**未包括**入口/Forge宿主、React、CSS、图音资源和所有可能资源，不是全站下载量。[S2–S4]

平台另报告项目 `byteSize=3,183,871`、32个assets；这是平台元信息，不是本轮下载全工程后得出的独立总计。公开asset清单大小之和为2,659,352 bytes，且它不包含全部业务源码/宿主，不能强行把不同字段凑成一套文件账。[S2]

平台原始source hash、预览版本查询值和实际变换后响应hash分别保留在[研究快照](research_snapshot.json)。**不把原始源文件与变换后响应哈希不同当成校验失败，也不声称它们字节相同。** 当前预览mount和分享均报告revision44，但未独立核对全量作者文件、历史源码版本与发布43的差异。

结论是：**视频所述32KB历史口径尚待验证，当前可读v2已经不是32KB总工程。** 原始源码、压缩后传输、单一核心文件、全量资源是不同计量对象；不能从本次v2数字反推作者当时造假，也不能拿原帖32KB替代今天的全量体积。

## 相关项目与资料

先比较用途与交付物，再比较星数。SVG sprite打包器虽然更高星，但不是体积感精灵堆叠，已排除。

| 项目 | 本次快照/星数 | 许可证 | 实际用途与同原片的关系 |
| --- | --- | --- | --- |
| Dash fighter / fly | Forge revision44，fighterv2；无确认GitHub仓库 | 未取得明确开放许可证 | 原项目；可读运行代码，平台内Remix需要账号 |
| [loktar00/sprite-stacking](https://github.com/loktar00/sprite-stacking) | `25a6cfdc8b8f142b4cc297dd34bba24841d12213` / 4★ | MIT，已读LICENSE | 浏览器单HTML教程、提示模板和演示；tutorial真实用Canvas层片绘制。适合学方法，不是原飞机。README点明其简单层片法不支持自由bank/roll；不能直接替代原工程的自写投影 |
| [StanislavPetrovV/SpriteStacking](https://github.com/StanislavPetrovV/SpriteStacking) | `1cf2aee5374f47ccb99e963065b62754754ed353` / 38★ | MIT，已读LICENSE | Python/Pygame游戏示例；已读StackedSprite的旋转缓存选图/位置变换/层级更新；不是浏览器座舱飞行 |
| [x3cca/Shader-Stacker](https://github.com/x3cca/Shader-Stacker) | `21d86ab62140b0d08ea217982036e3cb184afed5` / 71★ | MPL-2.0 | Godot4插件，已读SpriteStack._draw；实际用CanvasItem分层纹理绘制，虽然项目名字含Shader，不能直接说当前是自定义shader方案。适合Godot项目，不是零引擎网页原飞机 |

星数是2026-11-17查询快照，不是效果/性能排行榜。以上均未安装或运行；MIT项目再分发需保留通知，MPL项目应按其许可证逐项确认衍生文件义务。本轮仅把它们作为已查阅的一手方法/源码参考。

## 复现路径

**状态：原项目与关键业务代码已静态核实；未实际复现工程、未试玩或测FPS。**

### 获取原工程

- 优先使用上面的原入口和Forge分享页。官方流程为登录自己的账号后Remix，再查看文件，或通过自己授权的Agent拉取到代码仓库。不要新注册账号/使用付费能力，只为完成本轮信息研究。
- 主组件入口是 `src/components/fighter-jet-eject.tsx`，场景是 `src/lib/eject/scene.ts`。要同时拿到模型、座舱、后处理、教程、声音及资源，不能只保存一个组件就承诺独立运行。
- 若仅学习实现，公开预览的网络响应可以读到这些已变换业务模块；必须重新从稳定页面获取临时预览，不硬编码过期签名、不伪造账号访问。
- 项目依赖React和Forge runtime。未取得独立构建说明，不虚构“下载后npm run dev即跑通”；自建宿主或导出后的依赖接入要另做测试。

### 最小验收建议

按源码：Space循环三视角、方向键飞行、Shift推力，F/G翻转循环、右键机炮、M导弹；当前还声明手柄/触摸及撞地弹射。应分别检查视角切换连续性、层片遮挡、HUD一致性、地图seed可重复、像素/realistic火焰退化以及资源请求错误。新增v2战斗/救援功能不能混作原片已有玩法；全部仅为源码推导的验收建议，没有本次通过记录。

### 如果目标只是学会精灵堆叠

先研究MIT的浏览器单HTML示例，弄懂“切片→同轴旋转→分层偏移→遮挡”，再实现世界坐标/相机、透视、俯仰滚转、程序化地图。代码体积小不代表实现没有数学、没有素材处理或不需要CPU预算。不要把教程中的限制抹掉，宣称简单层片blit天然具备自由三视角飞行。

## 适用场景与限制

- 适合研究像素风体积感、程序化岛屿、轻量软件渲染及浏览器交互；不是工程级空气动力学或生产级空战验证。
- 32KB不等于32KB内存，也不等于全网页传输量。噪声高度图、像素缓冲、深度数组和效果会占用额外内存/CPU，未测硬件性能。
- 公开预览支持查看与参数试验；正规Remix、工作区读文件/拉取需要自己的Forge身份。本轮匿名读取未进入其他用户工作区、未调用写操作。
- 这次headless浏览器读到了分享UI，但截图仍在预览加载状态；不以可下载代码/外层页面HTTP200声称已经成功渲染游戏。原片画面只证明演示有展示，不能替代当前环境运行验收。
- 许可证/素材权利未明时不转存完整工程；商业复用和公开发布先确认作者授权。

## 待核实事项

1. 作者宣称32KB的精确历史源文件/发布构建，原始、minify、gzip/brotli或某核心文件的计量范围。
2. 原片录制版本与fighterv2的版本差异；当前share44与published43、不同源hash的关系。
3. 对应GitHub/Git仓库、独立导出包与启动/依赖合同；本轮搜索未发现不等于永远不存在。
4. 原代码开放许可证、飞机/飞行员图片和音频各自授权，以及允许再发布的范围。
5. 当前环境正常加载与三视角/武器/弹射等真实操作、帧率和移动设备兼容性。
6. 候选X原帖精确链接、原帖发布时间；网络TLS错误未绕过。

## 来源与证据

| 编号 | 来源与链接 | 日期/版本 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [Enter.AI原片](https://www.douyin.com/video/7708679164118830371) / [短链](https://v.douyin.com/yc_GihotvsA/) | 2026-11-16 16:12:18 +08:00 | 2026-11-17 | 完整简介、媒体信息、采样帧；12秒原入口与作者截图 |
| S2 | [原入口](https://remix.ui8.ai/fly) / [Forge分享](https://forge.ui8.ai/share/frag_1eb8944c-57b1-42ca-a909-5c2d7e517c24) | fragment `frag_1eb8944c-57b1-42ca-a909-5c2d7e517c24`；share44/published43 | 2026-11-17 | 名称、slug、description、匿名canRemix、组件与资源元信息 |
| S3 | 同一Forge分享页实际请求的预览HTML、`src/main.tsx`与`src/components/fighter-jet-eject.tsx` | preview mount44；临时签名不公开 | 2026-11-17 | React依赖、Canvas输出、控制器与变换后业务组件；响应哈希见快照 |
| S4 | 同一预览实际import的九个`src/lib/`模块 | 版本query与解压正文SHA256见快照 | 2026-11-17 | 飞机13层、噪声地图、自写透视、排序、座舱、可选WebGL和声音引用 |
| S5 | [Forge官方文档](https://ui8.ai/forge/docs) | 持续更新 | 2026-11-17 | 分享权限、Remix登录与私有副本、Code/Assets文件编辑、授权Agent拉取 |
| S6 | [BitcoinVersus.Tech报道](https://bitcoinversus.tech/2026/11/15/32kb-flight-game-canvas2d-sprite-stacking-pixel-art-jet-2026/) | 2026-11-15；二手资料 | 2026-11-17 | 候选X原帖和解释方法；该文也声明未测32KB，不能替代源码证据 |
| S7 | [loktar00 README](https://github.com/loktar00/sprite-stacking/blob/25a6cfdc8b8f142b4cc297dd34bba24841d12213/README.md)、[tutorial](https://github.com/loktar00/sprite-stacking/blob/25a6cfdc8b8f142b4cc297dd34bba24841d12213/demos/tutorial.html)、[LICENSE](https://github.com/loktar00/sprite-stacking/blob/25a6cfdc8b8f142b4cc297dd34bba24841d12213/LICENSE) | 固定commit | 2026-11-17 | 单HTML方法、旋转/层距限制、MIT |
| S8 | [Pygame README](https://github.com/StanislavPetrovV/SpriteStacking/blob/1cf2aee5374f47ccb99e963065b62754754ed353/README.md)、[StackedSprite](https://github.com/StanislavPetrovV/SpriteStacking/blob/1cf2aee5374f47ccb99e963065b62754754ed353/stacked_sprite.py)、[LICENSE](https://github.com/StanislavPetrovV/SpriteStacking/blob/1cf2aee5374f47ccb99e963065b62754754ed353/LICENSE) | 固定commit | 2026-11-17 | Python方案与MIT，不是原飞机 |
| S9 | [Godot README](https://github.com/x3cca/Shader-Stacker/blob/21d86ab62140b0d08ea217982036e3cb184afed5/README.md)、[SpriteStack](https://github.com/x3cca/Shader-Stacker/blob/21d86ab62140b0d08ea217982036e3cb184afed5/addons/ShaderStacker/SpriteStack/SpriteStack.gd)、[LICENSE](https://github.com/x3cca/Shader-Stacker/blob/21d86ab62140b0d08ea217982036e3cb184afed5/LICENSE) | 固定commit，README声明4.0.5 | 2026-11-17 | Godot4 CanvasItem实现及MPL标识，非原网页 |

附[结构化研究快照](research_snapshot.json)：保留身份对应、读取范围、业务模块版本/大小/hash、公开元信息与对比版本；不保存Cookie、临时访问签名或全量原工程。

## 更新记录

- 2026-11-17：首次收录。放大原片链接定位Dash fighter；匿名读取公开v2预览组件及九个业务依赖，核实软件渲染/地图/三视角，区分32KB历史宣称与v2体积、React/可选WebGL及平台Remix/开源许可；未运行游戏。
