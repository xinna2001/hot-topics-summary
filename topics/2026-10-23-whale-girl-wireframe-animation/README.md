# 鲸鱼娘线框显影：DSH 片头与动态视频背景

收录日期：2026-10-23

最近核实：2026-10-23，Asia/Shanghai

研究状态：核心播放机制已核实；画面与公开素材视觉吻合；原视频制作模型与工程未公开确认。

## 一句话结论

这段「蓝色线框描出少女，再上色、扫描、眨眼」的效果已有可用素材：DSH 片头插件播放预制 MP4，进入聊天页后由皮肤中心循环播放另一段人物视频，半透明界面叠在上面。人物显影本身已经做进视频，接入程序主要完成播放、切换与界面合成。[S1–S5]

已提供一个[独立 HTML 演示](demo/index.html)，实际验证了片头播放、背景循环、进度拖动、切换和个人视频选择。下载这个 HTML 后在浏览器打开即可试看；上游素材由固定版本网址提供，需要联网。GitHub 文件页显示源码，不会直接执行 HTML。

## 原始线索

- 原短链：[https://v.douyin.com/v2JCN3Z_L_c/](https://v.douyin.com/v2JCN3Z_L_c/)
- 核实后的作品：[7698725807199441387](https://www.douyin.com/video/7698725807199441387)
- 作者：星⭐海鲸🐳梦；作品标题：「人老了就是心酸 省一块钱的tokens，手搓了三个小时」，标签包括 `wallpaper壁纸`、`deepseek`、`鲸鱼娘`、`AI`。
- 发布日期：2026-10-20 20:28:05，Asia/Shanghai；来自详情接口时间戳，与页面显示的 20:28 一致。
- 实际读取范围：作品详情、页面可见评论；完整下载 15.58 秒视频，按 0–15 秒每秒提取并检查一帧。未做完整音轨转写，技术结论来自画面、作者评论及公开源码。
- 下载核验：HTTP 200；文件 5,995,997 字节，与接口 `data_size` 一致；MD5 与接口 `file_hash` 一致。ffprobe：H.264 / AAC，1920×1080，15.58 秒。
- 作者可见评论的安装线索：「点插件，添加插件，输入dsh-market搞完之后，设置，里面搞一个dsh-web-all和dsh-boot-animation就好了」。这是作者关于组合插件的说明；不能把评论中的简称自动当成当前版本的唯一安装包名。[S1]

### 画面拆解

| 原视频时间 | 实际可见内容 | 对应调查结果 |
| --- | --- | --- |
| 0–1 秒 | 载入窗口，随后短暂出现人物与聊天界面 | 应用启动与界面准备 |
| 2–3 秒 | 蓝色轮廓、头发线条和面部网格逐步出现 | 与 `deepseek-cyberpunk-intro.mp4` 的显影阶段视觉吻合 |
| 4–7 秒 | 彩色少女、DeepSeek 字标、眼睛和数据效果 | 与同一片头的后半段视觉吻合 |
| 8–15 秒 | 回到半透明聊天页，背景再次线框化、扫描、上色、眨眼 | 与 `whale-fantasy-loop.mp4` 中的动画阶段视觉吻合 |

这是对翻拍屏幕与公开视频关键帧的视觉比对；原抖音是拍屏录像，两者不是相同的二进制文件。[S1、S3、S5]

## 技术实现

### 1. 片头：把人物动画作为视频覆盖在应用上

`NativeDog1/dsh-boot-animation` 的 `BootOverlay` 是视频播放器。`src/client/ui.ts` 创建 `<video>`，设置 `muted`、`autoPlay`、`playsInline`，指定片段 URL 后调用 `load()` 与 `play()`；播放结束关闭浮层，也提供跳过与错误处理。[S2]

内置片头之一 `media/deepseek-cyberpunk-intro.mp4` 包含线框人物转成彩色人物的完整效果。实际下载核验：1,856,280 字节，1280×720，H.264 / AAC，7.05 秒。线框、上色、眨眼和字标属于素材内容，播放器源码负责将它显示出来。[S3]

插件额外用 CSS 做浮层交接：0.4.4 的进入阶段为淡入、虚化到清晰；退出阶段为淡出、模糊和轻微缩放。`src/client/styles.ts` 与 `ui.ts` 中的交接时长分别为 460ms 和 500ms。这些 CSS 是视频与应用的过渡，与视频内部的人物线框显影分属两个层次。[S2]

### 2. 聊天背景：循环视频，再叠界面

皮肤 `whale-fantasy`，中文名「鲸鱼娘 · 未至之境」，在 `skin.json` 中明确声明：

```json
{
  "backgroundMedia": {
    "dark": { "type": "video", "src": "assets/whale-fantasy-loop.mp4" }
  }
}
```

这段视频的源码位置是 `zhu1090093659/dsh-skins/skins/whale-fantasy/`；本次也核对了 `dsh-web` 商店发行副本。实际下载该副本核验：6,630,589 字节，1664×856，H.264，无音轨，25.458333 秒。[S4、S5]

皮肤中心 `src/client/runtime/decoration-layers.ts` 的 `buildBackgroundMedia()` 在 `type: video` 时创建原生 `<video>`，设置 `muted=true`、`loop=true`、`autoplay=true`、`playsInline=true`，用 `object-fit:cover` 铺满背景；清单中的 `scrim` 则作为遮罩层。[S6]

`skin.css` 重映射主题颜色，`patches.css` 将面板、输入卡和边框调成半透明 HUD 风格。人物视频在底层，界面在上层，因而看起来像「少女在整个程序里被渲染出来」。这个背景皮肤本身是清单、CSS 和视频资产；其 README 明确说明没有 hooks，也没有人物实时生成脚本。[S4]

### 3. 给自己的软件接入时的最小结构

```html
<!-- 背景层：人物、线框、扫描和眨眼均来自视频内容 -->
<video class="background" src="your-character-loop.mp4"
       autoplay muted loop playsinline></video>
<!-- 交互层 -->
<main class="app">你的界面</main>
```

```css
.background {
  position: fixed; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover; pointer-events: none;
}
.app { position: relative; }
.panel { background: rgba(10,16,32,.55); border: 1px solid #1e3a6b; }
```

启动阶段另放一个视频浮层，`ended` 或用户跳过后进入工作界面。素材采用浏览器可解码的 H.264 MP4；有音轨时静音播放，处理 `play()` 被拒后的点击播放入口。MDN 官方指南与实际源码都支持这条自动播放处理方式。[S2、S6、S7]

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| 作者提及 `dsh-web-all` 和 `dsh-boot-animation` | 作者评论，实际读取 | S1 |
| 片头使用原生 video，人物显影已在 MP4 内 | 源码与素材核实 | S2、S3 |
| 持续人物背景来自 video 类型皮肤 | 清单、源码与素材核实 | S4–S6 |
| 原抖音与两段素材对应 | 关键帧视觉吻合；非文件哈希一致证明 | S1、S3、S5 |
| 接入播放不需要每次调用模型生成画面 | 对本次已核实播放路径的结论 | S2、S6 |
| 原作者用了哪个图生视频模型、3D 软件或提示词 | 未核实 | 公开素材不足以推断 |

## 相关项目与资料

| 项目 | 核实时版本 / commit | 许可证及关键入口 | 与原素材的关系 |
| --- | --- | --- | --- |
| [NativeDog1/dsh-boot-animation](https://github.com/NativeDog1/dsh-boot-animation) | 0.4.4；`24c711296cb4af2618fef4f65e81346a660fc67b` | BSD-3-Clause；`src/client/ui.ts`、`styles.ts`、`media/deepseek-cyberpunk-intro.mp4` | 作者点名的片头插件，内置动画视觉吻合 |
| [zhu1090093659/dsh-skins](https://github.com/zhu1090093659/dsh-skins) | 核对 `aaa972c5d8bb97eec1bf6662a64e90324f32c057`；`whale-fantasy` 1.0.0 | 引擎 BSD-3-Clause；此皮肤及视频按其单独 LICENSE 为 CC BY-NC-SA 4.0；`skins/whale-fantasy/`、`src/client/runtime/decoration-layers.ts` | 对应动态背景的资产与播放器 |
| [zhu1090093659/dsh-web](https://github.com/zhu1090093659/dsh-web) | `9c1523417f76ea36516db80e831953c1f1062007` | 主仓库 Apache-2.0；特定皮肤资产遵循自己的许可证；`packages/dsh-web-all/README.md` | 作者提及的插件聚合生态，包含皮肤中心和商店发行素材 |

`dsh-boot-animation` 的 GitHub 元信息显示 `NOASSERTION`，但实际读取 LICENSE 和 package.json 均为 BSD-3-Clause；许可证结论以实际文件为依据。其 LICENSE 还明确说明内置视频按同一条款发行。`whale-fantasy` 的视频则有单独的非商业、署名、相同方式共享要求，不能用引擎的许可证替代。[S2、S4]

## 复现路径

### 已实际运行：独立浏览器示例

本仓库 [demo/index.html](demo/index.html) 只使用 HTML、CSS 和本页 JavaScript，引用固定 commit 的两段公开视频。它没有模型接口、npm 安装步骤或外部 JavaScript 依赖。

1. 下载 `demo/index.html`，在 Chrome / Edge 等浏览器打开，保持能访问 GitHub 的网络。
2. 片头自动静音播放；拖动时间轴观察约 1–2 秒的线框阶段。
3. 播完后进入循环背景与示例界面。也可点「查看循环背景」或在片头按 Esc。
4. 用「暂停」、时间轴和「铺满 / 完整显示」观察效果。
5. 「试用自己的视频」用本地 Blob URL 播放，不上传所选文件。

本机 Chromium 实测：两段视频解码、进度跳转、背景循环标记、画面贴合切换、Esc 跳过、本地文件播放、片头结束自动切背景均通过；没有页面 JavaScript 错误。详细结果见 [demo/verification.json](demo/verification.json)。这验证的是独立浏览器示例；没有安装或运行整套 DSH 插件。

### 基于一手说明整理，未实际运行：在 DSH 里使用

已有 DSH 环境时，可以使用对应插件 README 的明确包名：

```sh
dsh plugin --profile web add github:NativeDog1/dsh-boot-animation
dsh plugin --profile web add @linxin666/dsh-client-ui-skin-center
```

第一条是片头，第二条是皮肤中心。若需要作者评论所述的聚合套件，`dsh-web-all` README 的命令为 `dsh plugin --profile web add @linxin666/dsh-web-all@latest`，其中已经包含皮肤中心；选择聚合路径时不要再为同一功能重复安装独立包。[S2、S4、S8]

按对应版本说明重启 DSH，在片头片库选择「DeepSeek 赛博朋克片头」；在创意工坊安装 `whale-fantasy` 后到皮肤中心应用「鲸鱼娘 · 未至之境」。当前皮肤清单明确为暗色风格。安装兼容性应核对自己运行的 DSH 版本；这里没有对用户现有客户端做安装或重启。[S2、S4]

### 如果要换成自己的角色

推荐先准备属于自己或已获使用授权的角色动画，再复用上面的播放器结构：片头 5–8 秒，背景做可循环版本。程序负责展示视频；制作素材时才需要美术或生成工具。

「角色图 → 霓虹线稿 / 网格层 → 扫描遮罩逐步切到彩色图 → 眼睛与头发动效 → 输出 MP4」是一条可设计的制作路线，但**不是已经查明的原作者工程**。网格画面本身不能证明有真实 3D 拓扑。如果希望角色随鼠标、语音或情绪即时变化，则需要额外的实时模型与动画系统，现有 MP4 播放器只能播放提前做好的画面。

## 适用场景与限制

- 适合应用启动片头、AI 工作台动态背景、主题皮肤、个人桌面视觉效果；实际覆盖范围是应用窗口。
- 播放已制作好的动画无需逐次消耗模型 tokens，主要成本是视频解码与合成；这不代表制作素材、AI 对话或其他插件操作没有费用。
- 眨眼与线框显影跟随视频时间，不能直接拿聊天情绪驱动。背景动画也可能影响文字阅读，需要面板遮罩或背景开关。
- `object-fit: cover` 会裁边；`contain` 会留边。重复播放平滑与否取决于素材剪辑，不是加上 `loop` 就一定无缝。
- 背景 README 宣称经过裁黑边、降规格与首尾交叉淡入处理；本次核对了发行视频的规格，没有重新运行其素材烘焙脚本或复测 README 中的画质指标。[S4]
- 演示引用上游网址，网络不可用时可选本地视频；视频和皮肤的具体许可不同，商用自有产品应准备可商用的素材。

## 待核实事项

1. 原作者制作人物视频时使用的模型、提示词、角色原图和可编辑工程；插件只能证明如何播放，不能追溯如何生成每一帧。
2. 拍屏电脑上的准确插件版本与全部皮肤设置。公开片头和循环视频的画面吻合，但没有取得作者机器的完整配置。
3. 在用户目标应用中的正式接入方式、目标系统与性能。本次交付包含研究与可试看的独立示例，未在用户生产应用中部署。

## 来源与证据

所有下列资料均于 2026-10-23 实际读取。页面评论可能随平台变化；关键原文与媒体验证记录见 [evidence.md](evidence.md)。

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [原抖音作品与可见评论](https://www.douyin.com/video/7698725807199441387) | 2026-10-20 | 2026-10-23 | 实际画面、作者插件线索、视频详情 |
| S2 | [片头 README](https://github.com/NativeDog1/dsh-boot-animation/blob/24c711296cb4af2618fef4f65e81346a660fc67b/README.md)、[ui.ts](https://github.com/NativeDog1/dsh-boot-animation/blob/24c711296cb4af2618fef4f65e81346a660fc67b/src/client/ui.ts)、[styles.ts](https://github.com/NativeDog1/dsh-boot-animation/blob/24c711296cb4af2618fef4f65e81346a660fc67b/src/client/styles.ts)、[LICENSE](https://github.com/NativeDog1/dsh-boot-animation/blob/24c711296cb4af2618fef4f65e81346a660fc67b/LICENSE) | 核对 commit 日期 2026-10-21 | 2026-10-23 | video 播放、CSS 交接、安装方式、许可证 |
| S3 | [DeepSeek 赛博朋克片头 MP4](https://github.com/NativeDog1/dsh-boot-animation/blob/24c711296cb4af2618fef4f65e81346a660fc67b/media/deepseek-cyberpunk-intro.mp4) | 素材最初发布日期未核实 | 2026-10-23 | 线框到人物已在视频内；规格与画面 |
| S4 | [whale-fantasy 清单](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/skins/whale-fantasy/skin.json)、[中文说明](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/skins/whale-fantasy/README.zh.md)、[许可证](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/skins/whale-fantasy/LICENSE) | 首发日期未核实 | 2026-10-23 | 视频背景、纯资产皮肤、非商业许可 |
| S5 | [商店发行循环 MP4](https://github.com/zhu1090093659/dsh-web/blob/9c1523417f76ea36516db80e831953c1f1062007/market/dist/assets/skins/whale-fantasy/assets/whale-fantasy-loop.mp4) | 素材最初发布日期未核实 | 2026-10-23 | 循环视频规格、与拍屏背景视觉吻合 |
| S6 | [皮肤中心 decoration-layers.ts](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/src/client/runtime/decoration-layers.ts)、[skin-controller.ts](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/src/client/runtime/skin-controller.ts) | 文件初次发布日期未核实 | 2026-10-23 | 创建循环 video、挂载背景与样式 |
| S7 | [MDN：Autoplay guide for media and Web Audio APIs](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay) | 页面首次发布日期未核实 | 2026-10-23 | 静音视频自动播放与拒绝处理 |
| S8 | [dsh-web-all README](https://github.com/zhu1090093659/dsh-web/blob/9c1523417f76ea36516db80e831953c1f1062007/packages/dsh-web-all/README.md)、[皮肤中心 README](https://github.com/zhu1090093659/dsh-skins/blob/aaa972c5d8bb97eec1bf6662a64e90324f32c057/README.md) | 文档初次发布日期未核实 | 2026-10-23 | 当前包名、聚合包与皮肤中心的关系 |

## 更新记录

- 2026-10-23：首次收录；读取原视频与作者评论，核对两段公开素材及播放器源码；新增并实测独立 HTML 演示。
