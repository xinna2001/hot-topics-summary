# Anywear：Decart 实时虚拟试衣

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：产品与 API 文档已核实；截图中的蚁人效果未实测

## 一句话结论

Anywear 是 Decart 的实时虚拟试衣产品：浏览器采集摄像头视频，再通过视觉模型按衣物参考图或文本改写视频中的穿着。官网明确写“Beta 期间限时免费”；截图中的战衣还原和尺寸变化属于作者展示，未在本轮复现。[S1][S2][S3]

## 原始线索

抖音 @小.Z 的标题为“实测 Anywear 插件｜照片一键生成蚁人战衣。可大可小的设定，AI还原度还不错”，画面是摄像头人物穿战衣。[S0] 没有原视频 ID、地址和发布日期。

本轮读取截图、Decart 产品官网、Chrome 商店页和实时 VTON API 文档。没有启用摄像头、安装扩展或调用付费模型。

## 技术实现

官方 API 给出可复现的接入结构：

1. 浏览器 getUserMedia 获取摄像头流。
2. Decart SDK 将该流连接到实时模型，输出经编辑的远端视频流。
3. 提供服装图和描述性 prompt，用 set() 或 setPrompt() 变更穿着。
4. 参考图最好是单独衣物、干净背景，至少 512×512；真人模特照片可先提取服装。
5. 应用收到 onRemoteStream 后展示结果；录制视频也可通过异步任务接口处理。[S3]

当前文档中 lucy-vton-latest 指向 lucy-vton-3.6；这是查阅时的 API 别名，不证明截图使用该模型。官网产品与 API 属于同厂商，但未取得扩展完整源码，不能指定扩展内部每一步的实现。

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| Chrome 扩展由 Decart.AI, Inc. 提供 | 商店页实际读取 | S2 |
| 衣物拖拽到摄像头画面，实时呈现试穿 | 官方产品说明与 SDK 文档一致 | S1、S3 |
| 产品永远免费 | 不成立于当前官网措辞；官网写 Beta 限时免费 | S1 |
| 战衣尺寸随意变化、每帧细节都准确 | 原视频宣传，本轮未实测 | S0 |
| 40ms 是所有网络下的端到端保证 | 无此证据；本轮未测端到端延迟 | 无 |

## 相关项目与资料

- 产品官网：[anywear.decart.ai](https://anywear.decart.ai/)。
- [官方链接对应的 Chrome 商店扩展](https://chromewebstore.google.com/detail/anywear-live-virtual-try/hijnklblgecbdlhjiofhlhjpndpifejh)；本轮读到版本 2.20，更新时间 2026-10-20。
- [Decart VTON 文档](https://docs.platform.decart.ai/models/realtime/virtual-try-on)，公开 SDK 接入示例可用于理解实现。
- 公开 API 示例不等于模型权重或扩展整体开源；同名 GitHub 项目不是本产品的当然来源。

## 复现路径

**基于产品与 SDK 文档整理，未实机试穿。**

产品体验：从官网打开商店入口，使用电脑 Chrome 安装扩展，在服装网页选择参考图并允许摄像头，检查正面与转身时的衣物、手部遮挡和脸部保持。

自建原型：用 SDK 连接视频流，传服装图与 prompt，展示编辑后的流。服务端签发短期 client token 后给前端使用；不要把永久 API Key 放进前端源码。[S3]

验收至少包含：人物身份保持、衣物颜色与结构、遮挡稳定性、连续动作、实测延迟、停止会话后释放摄像头。模型 fast mode 在当前文档中按标准实时费率的 2 倍计费；产品 Beta 免费和开发 API 计费应分别核对。

## 适用场景与限制

适合服装外观预览、直播换装和视觉特效。生成式穿着预览没有证明真实尺码合身、面料物理或商用质量保证。厚外套、复杂服装、人像遮挡和网络质量会影响效果。版权角色战衣也是作者示例，不代表官方提供该资产。

## 待核实事项

- 原视频链接、战衣参考素材、实际版本与完整效果。
- 本机跨境网络延迟、摄像头表现与 Beta 免费结束条件。
- 扩展是否在此演示中使用其他处理步骤；暂无源码证据。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [画面截图](evidence/05-source.jpg)、[标题截图](evidence/05-caption.jpg) | 未知 | 2026-10-22 | Anywear 名称与蚁人战衣示例 |
| S1 | [产品官网](https://anywear.decart.ai/) | 未标注 | 2026-10-22 | 产品入口、试衣流程、Beta 限时免费 |
| S2 | [Chrome 商店](https://chromewebstore.google.com/detail/anywear-live-virtual-try/hijnklblgecbdlhjiofhlhjpndpifejh) | 更新 2026-10-20 | 2026-10-22 | 发行主体、扩展版本和使用流程 |
| S3 | [官方 VTON 文档 Markdown](https://docs.platform.decart.ai/models/realtime/virtual-try-on.md) | 未标注 | 2026-10-22 | 实时流、参考图、动态更新、token 与 fast mode |

## 更新记录

- 2026-10-22：确认准确厂商和扩展，补入公开 API 流程及限时免费边界。


## 输入溯源

- 首批图片顺序：5。
- 原消息：om_x100b62aa714cd8a0ddbde47e3440ab6。
- 原附件文件名：img_v3_0216n_be4fa325-a17a-4ee1-b288-6d0f670b2a8g.jpg。
- 原图 SHA-256：f9b20de74445e1e28427b62e81a123e7c22afe39bf34343224cf1fc88a963a6d。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
