# Piik：P2P 屏幕共享与自部署

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：项目与实现已核实；原帖及端到端体验待核实

## 一句话结论

Piik 是可自部署的屏幕共享工具：房主共享屏幕，观众在浏览器观看，媒体优先走 WebRTC P2P；自建站点可以启用 SFU 转发兜底。它的低延迟和连接成功率依赖实际网络，不能仅凭演示保证。[S1][S2]

## 原始线索

抖音 @索亚加德的“第159集｜开源屏幕共享项目”展示 GitHub 仓库名 Piik。[S0] 截图没有视频 ID、分享链接或发布日期。

本轮实际读取了截图、项目 README、路由设计和传输源码，以及一个关联的 B站项目介绍页。后者由页面列出的 TNTcraft 研发参与，内容指向同一仓库，但并非用户截图中 @索亚加德的原视频。[S4] 没有下载或完整观看视频。

## 技术实现

1. 浏览器或 Piik App 采集屏幕、窗口、标签页、摄像头及可用音频。
2. Go 服务管理房间、邀请凭据、会话与持久数据；浏览器 UI 使用 TypeScript。
3. WebRTC 通过 ICE/STUN 建立媒体路径，优先 P2P。当前设计支持受控的观众转发图，而不是假设房主向所有观众各传一份。
4. 可用的自建站点启用 SFU 后，路由控制器能回退到服务器转发；公开演示站和 App 公网邀请保持纯 P2P。
5. 共享期间浏览器页面或 App 需保持运行。[S1][S2][S3]

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| 一位房主、最多 20 位观众 | 当前 README 与项目介绍页一致 | S1、S4 |
| P2P 优先、可选 SFU、受限网络可能失败 | 项目文档已核实 | S1、S2 |
| Go 传输层使用 Pion WebRTC 与 LiveKit 相关媒体组件 | 源码静态核实 | S3 |
| 房间数据保存在 SQLite | README 已核实 | S1 |
| 所有平台都已经成熟、任何网络都低延迟 | 无此证据；项目仍说明 macOS/Linux 需更多实机测试 | S1 |

## 相关项目与资料

- 官方仓库：[TNTcraftHIM/Piik](https://github.com/TNTcraftHIM/Piik)。
- 核实 commit：bd59e7f798835dec3f2964a9d3688096df45c37d。
- 自有代码 MIT，第三方组件仍保留各自许可。[S1]
- 官网 [piik.tv](https://piik.tv/)；浏览器演示 [demo.piik.tv](https://demo.piik.tv/)。
- 关键源码入口：internal/server/signal、internal/server/room、internal/server/route、internal/media/forwarding；浏览器在 src/client。[S2][S3]

## 复现路径

**基于当前资料整理，未安装 App、未开房间实测。**

1. 使用在线演示或选择适合操作系统的官方 App。
2. 房主选择采集源并创建房间；另一设备打开邀请链接。
3. 验证画面、声音和停止共享行为；以连接拓扑和实际播放为依据。
4. 需要网络兜底时，按仓库自部署文档配置 Go 服务、HTTPS、STUN 与可选 SFU。

成功标准是两台设备收到可用画面和所选音频；低延迟应另测首帧时间、卡顿与端到端延迟。Web 采集通常需要 HTTPS 或 localhost。

## 适用场景与限制

适合小范围游戏、绘画、演示和共同观看。纯 P2P 对 NAT、防火墙和出口网络敏感；自部署增加服务器、TLS、STUN 和转发带宽成本。远程键鼠功能需要 App 且由房主授权，不能从普通浏览器观看自动推出远控能力。

## 待核实事项

- @索亚加德原视频链接及展示时的项目版本。
- 本机 macOS 采集、跨运营商网络、音频兼容性与延迟实测。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [截图证据](evidence/02-source.jpg) | 未知 | 2026-10-22 | Piik 名称与屏幕共享主题 |
| S1 | [固定版本中文 README](https://github.com/TNTcraftHIM/Piik/blob/bd59e7f798835dec3f2964a9d3688096df45c37d/README.zh-CN.md) | 版本截至 2026-10-21 | 2026-10-22 | 功能、上手、SQLite、许可及平台限制 |
| S2 | [路由设计](https://github.com/TNTcraftHIM/Piik/blob/bd59e7f798835dec3f2964a9d3688096df45c37d/docs/standards/routing-transport.md) | 同上 | 2026-10-22 | P2P 图、SFU 与容量约束 |
| S3 | [媒体传输源码](https://github.com/TNTcraftHIM/Piik/blob/bd59e7f798835dec3f2964a9d3688096df45c37d/internal/media/forwarding/transport.go) | 同上 | 2026-10-22 | Pion WebRTC 与媒体发送 |
| S4 | [关联 B站介绍页](https://www.bilibili.com/video/BV1weYR65Ed5/) | 页面显示 2026-09-12 | 2026-10-22 | 同项目介绍、下载与仓库链接；只读页面，未观看视频 |

## 更新记录

- 2026-10-22：收录截图，定位准确仓库并核实当前 P2P/SFU 实现。


## 输入溯源

- 首批图片顺序：2。
- 原消息：om_x100b62aa71b9a0acdd0986cfb6d7951。
- 原附件文件名：img_v3_0216n_70c94d44-5610-4f78-901c-282e15cd9b7g.jpg。
- 原图 SHA-256：80d9933ac2b513aae7129654b693b879a1f4b5e54f7e78ad834fb7079c9ca3fa。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
