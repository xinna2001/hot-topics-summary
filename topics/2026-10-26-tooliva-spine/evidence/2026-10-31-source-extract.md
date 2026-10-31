# Spine 制作关联线索与当前资料核实

查阅日期：2026-10-31，Asia/Shanghai。

## 本轮新输入

- 短链：https://v.douyin.com/pv8XkhA5D7I/
- 跳转确认规范链接：https://www.douyin.com/video/7702771710579199241
- 分享文本作者：开发工程师彭飞。截断标题：「用 AI，把角色创意变成 Spine 动画 有了角...」。
- 完整正文、确切发布时间、媒体和产品名称未取得。同作者和相似标题不足以证明是 Tooliva，作为待核实关联线索归入既有 Spine 专题。
- 短链抓取 HTTP 200；PC 网页仅含应用通用数据。原生详情接口未返回 aweme_detail；移动分享页没有作品数据；独立 Chrome 浏览器上下文显示「视频数据加载中」，捕获的详情为 0、视频地址为 0。未下载视频或读取字幕。

## 当前 Tooliva 官方资料

- https://toolivaai.com/ai-studio/spine-workbench 实际跳转到 AI Studio 内的 Spine 工作台。
- 工作台引导原文：「模板决定部件结构和已有动画。点击一个模板，右侧会显示它的动画效果。」
- 当前界面选中「黑铠巨刃斗士」，显示「动作 7」「部件 44」；封面和动画仍在加载，因此只记录文字，未确认图像播放。
- https://toolivaai.com/zh/tutorials/spine-workbench-guide 全文重新读取，仍说明形象候选、部件生成、对照校准、变换/镜像/Warp、分割修正、返工/武器款式及多皮肤导出；教程包的说明是共享 JSON、Atlas 与各皮肤 PNG。
- https://toolivaai.com/zh/blog/seo-ai-sprite-cutting-vs-spine-parts 区分完整动作帧与角色部件，明确切片不等于骨骼绑定或工程；页面日期 2026-10-17。
- 本轮没有创建资源、上传角色、调用生成、支付或导出，也未运行引擎。

## 本轮同类代码调查

- GenielabsOpenSource/spine-animation-ai，核实 commit `702b71689cac826efee942ee4564fef9560d6ef8`；GitHub 采样 616 stars。
- LICENSE 实文为 PolyForm Noncommercial 1.0.0；README 说明商业使用需单独许可。不因仓库可访问就称其为 MIT 或无限制可商用。
- `scripts/position_parts.py` 使用 SIFT、FLANN 和 `estimateAffinePartial2D(..., method=cv2.RANSAC)` 求相似变换，匹配失败时使用多尺度模板匹配；`compute_z_order` 对重叠区颜色比较所得分数排序，没有按 README 所称拓扑排序实现。
- `scripts/build_spine_json.py` 读取骨骼/slots/附件/动作配置，内置六种动作，写 `skeleton.spine=4.2.0` 并转换时间轴格式；未在运行时验证它的输出。
- `scripts/split_character.py` 调用 Gemini 生成拆分图集，后续用连通区域分割；已有部件时可以不使用此步骤。
- `reskin-app` 面向已有 Spine rig 换皮肤，文档要求 Gemini 与 SAM-3 服务；当前 pipeline 另有 atlas/exploded 合成路径。本轮读取源码和说明，未运行此项目。
- God Mode AI 当前官网继续宣称单图分层、自动骨骼绑定，导出 skeleton JSON、Atlas、PNG，支持 Spine 3.5–4.2；未做生成或同图效果对比。

## 输出与许可复核

Spine 官方 Import、JSON format 与 Runtimes License 已重新读取。骨骼 JSON/图集可走数据导入，不等于原生 .spine 工程；官方运行时仍有独立许可合同。实际导出文件、动画质量与引擎版本匹配需要单独验证。

这里保存读取范围和公开信息，不保存 cookie、账号页面或短期媒体地址。
