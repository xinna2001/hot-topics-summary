# AI 控制 Blender：Python 与 MCP 三维创作

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：可行实现与社区集成已核实；原作者实际工具未知

## 一句话结论

自然语言控制 Blender 可以通过“LLM 生成 Python → Blender 执行 → 读取场景和截图反馈”实现。社区 MCP for Blender 已公开这条链路；截图没有点名插件，所以它是经核实的实现选项，不能直接当作原作者使用的工具。[S1][S2]

## 原始线索

截图来自抖音 @西兰花费算力（半晴PRO），展示“半晴Pro”关于 AI 写 Blender 脚本、摆物体、布置镜头、回到软件检查修改的文章。内嵌文字显示 26-10-17 13:40，但原抖音帖子地址和绝对发布日期仍未获取。[S0]

本轮读取 Blender 官方 Python API、社区集成 README、server.py 和 addon.py。没有启动 Blender、安装插件或生成三维资产。

## 技术实现

Blender 官方 Python API 可以访问场景、网格、材质和操作；bpy.data、bpy.context、bpy.ops 是主要入口。[S1]

一个已公开的 MCP 方案是：

1. MCP 客户端把用户需求交给 LLM，调用场景信息、代码执行与视图工具。
2. Python MCP 服务使用 socket 把结构化命令发送到 Blender 插件。
3. 插件把命令排入由 Blender 主线程处理的队列，通过 bpy 完成建模、材质和相机操作。
4. 获取场景概要、截图或渲染图，模型根据实际输出继续修正。
5. 保存可编辑 .blend 文件与最终渲染结果。[S2][S3][S4]

| 关键判断 | 证据状态 | 来源 |
| --- | --- | --- |
| Blender 能通过 Python 编辑场景数据 | 官方 API 已核实 | S1 |
| MCP 服务与 Blender 插件双组件、默认 socket 端口 9876 | 当前 README 与源码静态核实 | S2、S3、S4 |
| 场景/视图反馈可以支撑迭代 | 社区集成功能与工具函数已核实 | S2、S3 |
| 截图作者必然使用该插件或 Claude | 未知，截图未点名 | S0 |
| 任何人都能一次生成生产级三维资产 | 宣传愿景，未得到质量保证 | S0 |

## 相关项目与资料

- 官方：[Blender Python API](https://docs.blender.org/api/current/info_quickstart.html)。
- 社区：[ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender)，原名 blender-mcp；查阅时的新 PyPI 包名为 mcp-for-blender。
- 核实 commit：5a3618fccb2d982d0dd61e7a1879912c3100073b，社区集成 MIT；它不是 Blender Foundation 的官方插件。
- 关键入口：src/blender_mcp/server.py 与 addon.py；模型接入可选择兼容的 MCP 客户端。

## 复现路径

**基于资料整理，未运行 Blender。**

1. 选择匹配的 Blender、Python 和 MCP 客户端版本，固定插件版本。
2. 阅读安装配置后安装插件与服务，保持 socket 仅供本机访问。
3. 从“创建一个立方体、材质、地面、相机和一盏灯”的简单场景开始。
4. 获取场景信息和渲染预览，核对对象数量、变换、颜色与相机位置。
5. 保存 .blend，重新打开并确认资产可继续编辑；再验证动画或导出。

成功标准应是可编辑资产和正确场景状态，不能只看聊天里声称已经完成。该集成具备 Python 执行能力，当前版本提供可选 safe mode；实际执行应在测试场景内进行，防止误改已有工程。[S2]

## 适用场景与限制

适合程序化场景、产品展示、简单动画、资产批量处理和创意预演。拓扑、绑定、UV、光照、美术一致性和游戏引擎约束仍需专业验收。Python API 的上下文与线程限制会造成失败；外部资产和 AI 3D 服务的收费与许可不因 Blender 免费而消失。

## 待核实事项

- 原文章/抖音链接、作者实际插件与模型。
- 本机 Blender 版本、插件兼容性、场景质量与动画实测。
- “机器人训练所需仿真素材”需要的物理与标注质量，截图未给验证方案。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [文章截图](evidence/07-source.jpg) | 内嵌文字 2026-10-17；原帖日期待核 | 2026-10-22 | AI 脚本控制三维软件的线索 |
| S1 | [Blender Python API](https://docs.blender.org/api/current/info_quickstart.html) | 当前文档 | 2026-10-22 | Python 数据与操作能力 |
| S2 | [社区集成 README](https://github.com/ahujasid/mcp-for-blender/blob/5a3618fccb2d982d0dd61e7a1879912c3100073b/README.md) | 版本截至 2026-10-20 | 2026-10-22 | 包名、依赖、双组件与边界 |
| S3 | [MCP 服务源码](https://github.com/ahujasid/mcp-for-blender/blob/5a3618fccb2d982d0dd61e7a1879912c3100073b/src/blender_mcp/server.py) | 同上 | 2026-10-22 | socket、场景工具、代码与视图反馈 |
| S4 | [Blender 插件源码](https://github.com/ahujasid/mcp-for-blender/blob/5a3618fccb2d982d0dd61e7a1879912c3100073b/addon.py) | 同上 | 2026-10-22 | 主线程队列与场景命令 |

## 更新记录

- 2026-10-22：收录三维创作思路，给出公开可行方案，标明与原作者工具的证据差距。


## 输入溯源

- 首批图片顺序：7。
- 原消息：om_x100b62aa714430a4dfb7ad7aef8400a。
- 原附件文件名：img_v3_0216n_83d2cbd1-0981-4f95-ac98-332a920a4c8g.jpg。
- 原图 SHA-256：8e9dce1b842ff2650a4231466ab177c7d4f87caf14d7379c50d0907a034be148。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
