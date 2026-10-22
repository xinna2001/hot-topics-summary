# AstrBot：微信 AI 聊天与人格配置

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：框架与当前个人微信路径已核实；截图人格和模型未复现

## 一句话结论

截图作者明确推荐 AstrBot。当前框架具有多平台适配、大模型调用和人格设置，官方仓库还给出扫码登录个人微信的路径；“大肥鱼”的具体性格、模型和主动行为无法从截图聊天可靠还原。[S0][S1][S2]

## 原始线索

抖音评论中，作者 @溺水回复“电脑下 astrbot，填api然后扫码设置微信bot就行了”，并说可以自己设置人格。上方聊天显示“大肥鱼 AI”及“v4pro”，但这只是显示名称和对话文本，不能据此确认底层模型、额度读取或机器人转账。[S0]

本轮读取截图、AstrBot README、个人微信接入文档、客户端源码与 persona 管理源码，没有安装框架、扫码登录或发送微信消息。

## 技术实现

1. 平台适配器接收文本和媒体，把平台消息转成框架事件。
2. 会话上下文和 persona system_prompt 交给已配置的模型 Provider。
3. 模型回复及工具/插件输出经过消息链发送回平台。
4. 人格由配置、历史和模型行为共同影响，不是固定保证能复现某段语气。[S1][S3][S4]

当前官方个人微信文档说明：v4.22.0 引入 weixin_oc 适配器，使用扫码登录与长轮询；文档称基于微信官方 openclaw-weixin 接口，要求手机微信具有 ClawBot 插件并达到指定版本。[S2] 这与旧教程常见的 Gewechat 路径不同，应以当前版本为准。

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| 作者推荐 AstrBot 并允许设置人格 | 截图作者回复 | S0 |
| 框架支持 persona、模型和消息平台适配 | README 与 persona 源码静态核实 | S1、S4 |
| 当前个人微信路径有二维码登录、长轮询及版本要求 | 官方项目文档与客户端已读取 | S2、S3 |
| “大肥鱼”真能往 API 账户充值、自己赚钱或情绪化 | 截图对白，不能当作行为证据 | S0 |
| 随意填一个 API 就可接入任意版本微信 | 过度简化；模型配置和微信前提均需满足 | S1、S2 |

## 相关项目与资料

- 官方仓库：[AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot)。
- 核实 commit：0cd42bd4dd216d8810da4e3f5fb2e381d3c6817e；AGPL-3.0。
- 当前 README 显示 Python 3.12+；实际安装仍按选定版本的文档。
- docs/zh/platform/weixin_oc.md、astrbot/core/platform/sources/weixin_oc/、astrbot/core/persona_mgr.py 是理解该功能的入口。
- 微信个人号、微信公众号、企业微信是不同适配器，不能混用配置。

## 复现路径

**基于项目文档整理，未扫码或调用模型。**

1. 在本地测试环境安装选定版本 AstrBot，先用 WebUI 确认模型 Provider 可正常回复。
2. 配置一个简单 persona，明确名字、语气和回复长度；同一问题多次验证效果。
3. 满足当前个人微信适配器的手机版本与 ClawBot 前提后，用账号本人扫码并确认登录。
4. 文档要求登录成功后保存配置；再从微信发送一条测试消息，检查正常回复与日志。
5. 若测试图片、文件或语音，按当前消息类型支持表逐项验收。

成功标准是消息实际收发、人格配置按预期生效、重启后会话/登录态表现符合要求。API 余额和外部付款需要单独、真实的工具能力与授权，聊天文本不能证明已实现。

## 适用场景与限制

适合个人聊天助手、知识问答和消息平台自动化。人格提示影响输出但不会保证持续记忆、主动消息或某种情感；这些需要额外功能与检验。截图里的 v4pro 未能确认对应哪一家模型，不能据此推荐不明 API 渠道。

## 待核实事项

- 原视频地址、完整 persona、模型 ID、记忆和主动消息插件。
- 用户设备是否具备文档所需的微信 ClawBot 入口。
- 原截图所用版本；本报告说明的是核实时的当前实现。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [作者配置回复](evidence/08-source.jpg) | 只显示相对时间 | 2026-10-22 | AstrBot 名称和扫码线索 |
| S1 | [固定版本 README](https://github.com/AstrBotDevs/AstrBot/blob/0cd42bd4dd216d8810da4e3f5fb2e381d3c6817e/README_zh.md) | 版本截至 2026-10-22 | 2026-10-22 | persona、模型、多平台和依赖 |
| S2 | [个人微信接入文档](https://github.com/AstrBotDevs/AstrBot/blob/0cd42bd4dd216d8810da4e3f5fb2e381d3c6817e/docs/zh/platform/weixin_oc.md) | v4.22.0 起 | 2026-10-22 | 手机版本、ClawBot、扫码与长轮询 |
| S3 | [个人微信客户端源码](https://github.com/AstrBotDevs/AstrBot/blob/0cd42bd4dd216d8810da4e3f5fb2e381d3c6817e/astrbot/core/platform/sources/weixin_oc/weixin_oc_client.py) | 同上 | 2026-10-22 | API 请求、登录态与媒体处理 |
| S4 | [人格管理源码](https://github.com/AstrBotDevs/AstrBot/blob/0cd42bd4dd216d8810da4e3f5fb2e381d3c6817e/astrbot/core/persona_mgr.py) | 同上 | 2026-10-22 | persona 的 system_prompt 配置 |

## 更新记录

- 2026-10-22：确认框架名，并补充当前扫码路径的真实前提与旧教程差异。


## 输入溯源

- 首批图片顺序：8。
- 原消息：om_x100b62aa714048a4c0f82a50d0fe709。
- 原附件文件名：img_v3_0216n_87571ce5-ff59-404d-8c5f-6a7894b9a90g.jpg。
- 原图 SHA-256：7839f4c88060d17b08cb819e64a51db16cd5a793fb059115eead8d5cd74a9c91。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
