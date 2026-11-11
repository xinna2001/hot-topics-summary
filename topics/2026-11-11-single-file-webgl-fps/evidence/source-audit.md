# 源码核对与证据边界

核实日期：2026-11-11，Asia/Shanghai。

本记录只发布技术说明与必要证据，不附最初参考 HTML、完整应用源码、个人聊天信息或开发机位置。代码内函数名用于定位原样本，不证明作者身份。

## 1. 两个样本的身份

| 样本 | 文件/产物 | 字节数 | SHA-256 |
| --- | --- | ---: | --- |
| 参考 | `几猫国产3A大作_V1.html` | 1,425,707 | `9e55b5200b088adaf8e1152da04efc0d3b25e236e6baf2dee96f81e23e084966` |
| Demo | `断电协议_BLACKOUT.html` | 598,178 | `a705ac8a3329aae190be895a74094d3278404b7e27889a4fcfee180d2c3ed5fd` |

参考作品包含 Three.js r180，代码多处带 `SALTLINE` 标识。公开来源、作者与应用代码许可证均未确认，不能据此推断由谁或哪个模型制作。Demo 锁定 `three: 0.180.0`，其交付前验证文件中的哈希与本次读取的产物一致。

## 2. 源码读取方法

参考 HTML 的脚本是合并/压缩形式。为了定位函数，使用 esbuild **只做格式展开**，不在 Node 中执行用户脚本；格式化副本只作临时研究材料，不提交。以下位置使用“原始函数名或入口”，而不把格式化行号伪装成原文件行号。

随后在隔离 Chrome 中实际运行原 HTML。截取游戏画面时确认 `game.state === "playing"`，高级渲染有效；换弹图由实际武器换弹状态产生。未以尚在淡入的介绍画面作质量对照。

## 3. 参考作品关键入口

| 入口/标识 | 核对内容 |
| --- | --- |
| `QC` | 构造上下文并依次初始化 render、mats、physics、props、input、level、backdrop、ground、fx、audio、player、combat、weapon、enemies、hud、game |
| `Hg` / `jy` / `qy` | 渲染器、高级后处理、替换阴影采样逻辑；`qy` 在实际初始化中调用，不是只有未用的 shader 字符串 |
| `Gg` | GPU 材质生成；将 albedo、normal、ORM 分别接到颜色/法线/粗糙度/金属度/AO 输入 |
| `d3` / `moveCapsule` | 对盒形障碍进行水平圆截面推出，修正墙内速度；台阶、地面吸附与头顶碰撞 |
| `Mt` / `x_` | 角色移动、加减速、蹲姿、跳跃容错、步态、落地与镜头反馈 |
| `dm` / `ma` | 第一人称枪械控制器与弹簧积分 |
| `Vv` 及 `dm` 内姿态构造 | 手指参数与握持形态；食指顶点姿态混合；左手和弹匣的关键帧配合 |
| `u_` | Web Audio 音频图、panner、卷积器与游戏事件响应 |

### 已读到的角色参数

- 行走/冲刺/蹲姿/ADS 基础速度：3.8 / 6.4 / 1.9 / 2.4。
- 地面加速度 34、减速度 26、空中加速度 9。
- 离地容错 0.12 秒、跳跃缓冲 0.13 秒。
- 站立高度 1.8 米；碰撞求解中的台阶阈值约 0.42 米。
- `moveCapsule` 水平子步数随位移/半径增加，每子步最多进行 3 轮重叠推出。
- 其导航网格有路径搜索；不能将它误写成动态刚体或任意网格碰撞。

### 已读到的武器机制

- 基础弹匣 30 发，720 RPM。
- 弹簧状态包含位置、速度、刚度和阻尼，不是单一插值参数。
- 通道 `kZ / kP / kY / kR / swY / swP / jY / jP / bump` 分别参与后坐、摆动、跳跃落地和阶段冲击。
- 普通/空仓换弹时长约 2.10 / 2.72 秒。
- 左手轨迹用位置插值和四元数 slerp，弹匣在指定阶段随手移动。
- `weapon:reload` 阶段包括 `start / magout / magin / bolt / done`，音效订阅对应阶段。
- 枪栓、扳机食指、抛壳、热量/枪口烟、连射扩散和视角扰动都有独立逻辑。
- 射击时钟递减后使用循环补发，并通过累加 `60 / RPM` 保留余量；单更新补发上限为 3。

### 材质与渲染

运行时 high 配置确认了 4× MSAA、4096 阴影贴图、24 步体积散射、AO、平面反射、Bloom 和运动模糊。代码存在运行失败降级路径，所以本报告同时记录了实际 `advanced: true / softShadows: true`，没有仅凭功能名称断言开启。

材料生成器确实产出颜色、法线、ORM，并在材质实例中连接对应 map。雾的体积光阶段沿视线采样并查询阴影；天空云层仍有程序化近似，不宣称完整物理天气模拟。

## 4. Demo 关键入口与实际简化

这些位置属于核实当天的原开发工程，工程本身未复制进本条目：

| 原工程位置 | 核实内容 |
| --- | --- |
| `src/main.js`，`state / player` | 集中状态；menu/playing/paused/won/dead |
| `src/main.js`，`shoot` | 每次开火将冷却置为 0.11 秒；hitscan；一个后坐标量 |
| `src/main.js`，`blocked / updatePlayer` | 直接水平位移、X/Z 分轴 AABB 阻挡；未检查障碍底部是否高于头顶；无自动上台阶 |
| `src/main.js`，`updateCamera` | 相机与整枪姿态插值；正弦换弹姿势与弹匣隐藏窗口 |
| `src/main.js`，`frame` | 变 dt 主循环，上限 0.05 秒；没有固定步长物理累加器 |
| `src/world.js`，`surfaceTexture / environment` | 512×512 Canvas 噪声表面与程序环境贴图；PMREM 预过滤 |
| `src/world.js`，`reflectionShader` | Reflector 结果叠加噪声积水遮罩、微小扰动和简单模糊 |
| `src/world.js`，后处理构造 | RenderPass → UnrealBloomPass → OutputPass → FXAA |
| `src/models.js`，`createWeapon` | 主要使用圆角盒体、圆柱和简单玻璃/准星；没有手指/左手换弹轨迹 |
| `src/audio.js` | 共享输出、振荡器与噪声合成，没有参考作品的空间与混响图 |
| `scripts/build.mjs` | esbuild bundle/minify/IIFE，嵌入 HTML |

### 射击时钟缺陷的最小源码摘录

Demo 的真实语句：

```javascript
state.shootCooldown = Math.max(0, state.shootCooldown - delta);
if (state.fire) shoot();
```

而每次 `shoot()` 成功开火后执行：

```javascript
state.shootCooldown = 0.11;
```

这会丢弃本次越过零点的余量。结果不是“低帧率一定更难玩”的泛泛判断，而是探针中真实出现了 6 秒 52/45/40 发的变化。参考作品采用累加间隔的时钟，结果为 72/73/73 发；两者设计射速本身不同。

### 悬空梁缺陷的最小源码摘录

Demo 在水平阻挡检查中有：

```javascript
if (player.position.y >= box.max.y + 0.04) continue;
```

之后进行 X/Z 范围重叠判断，但没有对应的“`box.min.y` 高于人物头部则排除”检查。故高处障碍在平面投影上仍可能充当墙。此项已用梁底 3 米的夹具复现，不只是代码猜测。

## 5. 受控探针方法

- 浏览器：隔离 Chrome；窗口 1440×900；DPR 1。
- 真实游戏画面在修改测试状态前采集。
- 参考作品停止自己的 animation loop；直接调用真实 `moveCapsule`、`player.update`、`weapon.update`。
- Demo 捕获实际帧回调，驱动真实游戏循环；关闭无关渲染成本并替换测试碰撞体。
- 测试夹具为 0.20 米矮台阶与梁底 3 米的悬空盒体。两者均使用相同障碍尺寸，不把不同场景中的任意物件当成同一试验。
- 射击测试给足弹药并隔离伤害/任务干扰；分别以 60/30/20 Hz 模拟六秒。
- 原始文件保持不变。结果见 [quality-gap-probes.json](quality-gap-probes.json)。

此方法验证逻辑行为与时间步敏感性，**不验证真实鼠标延迟、音频听感、整关体验或跨设备稳定帧率**。保存的实时 FPS/绘制快照只用于记录当时状态。

## 6. 上游版本核对

Three.js `r180` annotated tag 指向 commit：

`0af9729d0c143a86a1d725d6e2c3ad83301f3f34`

标签记录时间：2025-09-03。已读取 MIT 许可。以下安装文件与该官方固定版本逐字节比较一致：

- `src/renderers/WebGLRenderer.js`
- `examples/jsm/objects/Reflector.js`
- `examples/jsm/postprocessing/EffectComposer.js`
- `examples/jsm/postprocessing/UnrealBloomPass.js`
- `examples/jsm/postprocessing/OutputPass.js`
- `src/extras/PMREMGenerator.js`

上游许可证只说明上游库许可，不替代参考游戏应用代码与素材授权。
