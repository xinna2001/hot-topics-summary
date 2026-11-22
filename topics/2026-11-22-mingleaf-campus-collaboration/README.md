# Mingleaf：3D 校园组队、项目协作与成果沉淀

收录日期：2026-11-22

最近核实：2026-11-22，Asia/Shanghai

研究状态：部分核实；作者与原站已确认，公开前端构建代码已拆读，原始工程及后端源码未找到。

## 一句话结论

这不是“又一个聊天软件”，而是把认识队友、组队、推进项目、留下成果放在同一套校园工作空间里：3D 场景负责低压力接触和功能入口，真正的协作由任务、成果版本、决策记录与周报承接。**官网公开的前端代码可以研究，但本次没有拿到能独立部署的完整源码工程。** [S1–S8]

## 原始线索

- 用户分享：[抖音短链](https://v.douyin.com/Rkdz8DNmmK8/)。
- 规范地址：[图文作品 7710680127528504616](https://www.douyin.com/note/7710680127528504616)；作者 **JAY1023**；发布时间 **2026-11-22 01:37:03（北京时间）**。
- 实际读取范围：完整作品说明、五张公开配图、公开 HTML 结构化数据中的作者入口评论；没有把图文误当成视频，也没有宣称观看视频或听取配乐。
- 作者评论 `7710679805130457890` 原文：“🌿 体验入口 主链接：mingleaf-vhixy8if5qk.qoder.zone 备用：demo.jay23.cn”。评论中的作者 UID 与作品作者 UID 一致。浏览器评论面板提示登录，但公开页面的服务端数据已经含有这条评论；没有绕过登录门槛。
- 已打开的作者入口：[Qoder 主站](https://mingleaf-vhixy8if5qk.qoder.zone/)和[备用站](https://demo.jay23.cn/)，均返回 HTTP 200，标题均为“Mingleaf · 和合拍的人，做点有意思的事”。主站 HTML 的 `og:url` 也指向备用站。
- 作者宣称：快捷问候、咖啡制作与配方收集、任务/里程碑/白板/签到、在线文档版本管理、项目记忆和周报；参加阿里天池 Qoder 高校创造力大赛及“1万+ 浏览”。参赛状态、浏览量和社交效果没有独立核验。 [S1–S3]

### 五张配图能支持什么

1. 3D 校园与室内空间总览。
2. 角色附近的快捷问候入口。
3. 咖啡台及制作界面。
4. 讨论室电脑上的协作工作台、白板便签。
5. 名为 `scidraw-journal-club-zh` 的文档/图表画面。

第五张配图只证明作者展示了这类内容，不足以确认该文档的来源、自动生成方式或第三方项目集成关系；没有把它另认成 Mingleaf 的开源仓库。

## 技术实现

### 1. 公开代码拿到了什么

网站 HTML 直接引用入口 JS 和 React 分包；入口的 Vite 依赖映射进一步给出场景、角色、咖啡、项目工作台、成果库等模块的公开地址。本次只读取这些明确引用的资源及与分析有关的后续依赖，保存 URL、大小与 SHA-256 到 [research_snapshot.json](research_snapshot.json)。没有扫描私有文件、尝试读取服务器目录或调用项目数据的写接口。 [S2–S8]

| 层级 | 本次结果 | 能否据此完整复刻 |
| --- | --- | --- |
| 官网 HTML、CSS、浏览器 JS 构建产物 | 已获取并拆读相关模块 | 可以研究已发布的前端逻辑，但不是完整原始工程 |
| 原始 React/TypeScript 文件、构建配置和依赖锁 | 未取得 | 不能恢复成作者原项目或断言精确依赖范围 |
| Source map | 入口、Scene、FilePage、TeamDashboard 四个对应 `.map` 均 404；所读入口未见 `sourceMappingURL` | 仅此有限检查，不能断言全站没有任何 map |
| 后端、数据库、迁移、部署配置 | 未取得 | 不能用前端文件部署完整服务 |
| 开源许可证与作者仓库关联 | 未找到可确认的原项目仓库或授权文件 | 公开可下载不等于允许复制、改名商用或再分发 |

备用站资源带 `764d2fdbedc0a4c9a8b53a832903d52e1e8860dd` 路径前缀。本次只把它当作部署资源标识，**没有认定为 Git commit**。两个站的入口 JS 不同，因此没有假定它们是完全相同版本。

### 2. 3D 是入口，业务工作台是主体

- 入口代码具有 `__vite__mapDeps`，React 厂商包内版本字符串为 **19.3.1**；Three.js 包暴露 `REVISION: "175"`，场景依赖包含 `react-three-fiber` 和 `react-three-drei`。这是已发布构建内的证据，不是已拿到 `package.json`。 [S3–S5]
- `SceneCanvas` 使用正交相机、按设备选择的 DPR/阴影/抗锯齿设置，以及桌面/移动交互；源码能读到校园、讨论室、工位、咖啡区域和电脑纹理等构造逻辑。
- 场景设施打开普通 React 功能面板；项目房间加载 `RoomTools`，再加载 `ProjectWorkspace` 和成果库。空间负责“在哪儿做什么”，数据并非只存在于地图里。
- WebGL 不可用或加载失败时有 `SceneFallback`，提供设施/工作台入口。这是代码中的降级路径，未做低端设备或 WebGL 故障实测。

### 3. “走近再说话”如何实现

`Scene` 维护本地位置和远端角色位置，按 X/Z 平面距离筛选附近角色，阈值为 **3.6 场景单位**，不是现实米数。它发送/接收 `avatar:move`、`avatar:say`、`avatar:left`、`avatar:appearance` 和 `room:joined` 等事件；收到问候后，气泡约 **7 秒**清除。`SceneCanvas` 有“你好呀”“一起学习吗？”“来杯咖啡？”等预设问候。 [S4–S5]

**值得借鉴：**把开口成本降为“靠近＋一句短问候”，而不是强迫用户进入视频会议或立即建立好友关系。该设计能否真正减轻社交压力仍需用户研究，不能由代码证明。

### 4. 不要被 `/ws` 字符串误导

主站入口中虽然构造了 `/ws` URL，但当前所读的实际实时客户端走的是 **HTTP 持续拉取与事件提交**：

- 随机客户端路径 `/realtime/clients/<id>`，带 `channel` 与可选 `project` 参数。
- GET 拉取事件并递归开始下一次拉取；POST 提交事件；关闭时 DELETE 客户端。
- 角色移动发送端按约 **160ms**定时窗口合并待发送状态；失败重试从 **1 秒**指数增长，最多 **15 秒**。
- 项目快照还结合事件触发刷新与 **20 秒**定时刷新，团队/项目列表有 **60 秒**刷新兜底。 [S3–S4]

因此本次不能写成“已确认 WebSocket 同步”。GET 是否由服务器长时间挂起、实际负载和延迟如何，需要后端或网络实测；这里只确认前端采用长轮询风格的 HTTP 客户端逻辑。

### 5. 文档协作不是已确认的 CRDT 编辑器

`ArtifactLibrary` 的文本文档编辑以版本为单位保存，携带 `baseVersionId`。发生 `version_conflict` 时读取当前版本，比较 **基准 / 我的修改 / 对方修改**：不同位置自动合并，同处修改显示冲突选择，再由用户保存。`merge3` 是按行差分和三方合并的纯函数模块。 [S6–S7]

- 差分使用 LCS 动态规划；两侧行数乘积超过 **4,000,000** 时，退化为全删/全加的粗差分。
- 相同修改可合并；冲突有“我的/对方”等选择，不是悄悄用最后一次写入覆盖。
- 成果还具有修改提议、采纳/拒绝/撤回、版本对比、回收站等前端流程。
- 本次没有证据把文本文档流程写成 Yjs/CRDT 或实时逐字共同编辑；Word 等其他预览/编辑依赖未完整审查，不扩大结论。

**实际小范围验证：**完整读过 `merge3` 后，仅运行该无外部依赖的纯函数模块，验证了四类样例：不同位置修改合并、同一行冲突及双方选择、相同插入不重复、按行差分计数，全部通过。没有运行整站、后端、上传、注册或多用户编辑验收。

### 6. “干活—收尾”的数据闭环

| 功能 | 读到的具体实现 | 证据状态 |
| --- | --- | --- |
| 任务看板 | `todo / in_progress / in_review / done`，另有列表与日历视图 | 前端代码已核实 |
| 里程碑、白板、签到 | 项目级资源、便签和签到读取/写入的客户端方法及界面 | 前端流程已核实，服务端未验收 |
| 文档、文件成果 | task↔artifact 关联、版本内容、修改提议和回收站 | 前端流程已核实 |
| 项目记忆 | 决策标题、背景、结论、影响范围；任务/成果/里程碑等时间线事件 | 前端流程已核实 |
| 周报 | 先 GET 预览，再显式 POST 发布到项目频道 | 前端流程已核实，未发布 |
| AI 摘要 | 存在 `/projects/<id>/ai-summary` 及 `ai-reports` 调用 | 仅确认入口，模型与摘要质量未知 |
| 咖啡制作 | 制作、成绩保存、端杯与饮用的客户端流程 | 前端流程已核实，未实际制作 |

主站 API 基址直接指向 **`https://demo.jay23.cn/api/v1`**。所以即使复制主站静态资源，业务仍然依赖备用域名的服务器，不能当成离线应用。某些咖啡留言还有本地存储降级逻辑，不能把本地成功显示当成跨用户同步成功。 [S3、S8]

## 相关项目与资料

GitHub 本次检索 `Mingleaf`、`Mingleaf 3D`、`jay23`：只出现无法与作者对应的同名/近名结果，未找到可信原项目；这不是“GitHub 上绝对不存在”的证明。原站已由作者评论确认，不需要拿相似项目替代它。

以下只比较可借鉴的方向，不认定作者使用了这些项目，也没有安装或测试它们。星数均为 **2026-11-22 查询快照**，不代表质量排名。

| 项目 | 快照、范围与许可证 | 与 Mingleaf 的关系 |
| --- | --- | --- |
| [WorkAdventure](https://github.com/workadventure/workadventure) | 5,948 stars；`master`，`621f2bf29b36e1aa3aacb2e4a64299356f2cf412`。README 描述虚拟世界及靠近触发视频聊天；`play/LICENSE.txt`、`back/LICENSE.txt` 明写 AGPLv3 加 Commons Clause，另提示混合组件和商业版 | 更接近“空间社交”；不是校园任务/成果完整闭环的直接替身。不能按普通无商业限制的 AGPL 项目理解，收费服务等用途须核对附加条款 |
| [Plane](https://github.com/makeplane/plane) | 62,936 stars；`preview`，`da21a8ff8b4b0a1d7bfcca72eb184a13233bb143`；README 与 LICENSE.txt 确认 AGPLv3。文档描述工作项、周期、模块、视图、Pages 和分析 | 更接近“项目推进与文档”；没有在本次资料里确认 Mingleaf 式 3D 校园与咖啡社交。较高星数不是整套需求更匹配的证据 |

## 复现路径

### 已实际执行

1. 跟随抖音短链，读取作品正文、五张图片和作者公开入口评论。
2. 打开作者两个官网，读取 HTML/CSS 和被页面明确引用的 JS；按哈希留存证据索引。
3. 用独立、未登录的浏览器打开备用站首页，确认登录页及“一键进入演示”按钮可见；**没有点击该按钮、注册账号或进行项目写入**。
4. 仅执行已审读的纯 `merge3` 模块，四类样例通过。

### 如要学习前端，可按此顺序读

`index → SceneCanvas / Scene → RoomTools → ProjectWorkspace → ArtifactLibrary → merge3`

报告末尾链接和快照给出本次读到的真实发布文件。它们可被作者更新或下线；重取时应重新核对哈希和站点版本。**没有原始工程和后端，不能给出作者项目的 `npm install / npm run dev` 完整复现命令。**

### 如要自己实现同类产品（设计建议，未实现）

1. 先做普通网页的团队、项目、任务、成果版本和决策台账。
2. 让 3D 场景只承担导航和在线状态；同一功能同时保留普通网页入口。
3. 先做明确的版本冲突控制，不急着把“有在线文档”升级为复杂实时协同。
4. 再加入低压力问候与可选轻互动；不让咖啡等小游戏阻塞工作。
5. 收尾时把成果、负责人、状态、重要决策和下一步交接串起来。

验收要分别验证业务记录保存/回读、多账号同步、版本冲突、断线恢复、场景降级与权限控制；地图能显示不是业务验收通过。本轮没有实现或执行这套方案。

## 适用场景与限制

- 适合校园小组、读书会、短期共创与需要保留过程记忆的轻团队。
- 最值得借鉴的不是“把办公画成游戏”，而是**空间入口与业务台账分离、低压力接触、版本冲突不丢内容、成果和决策留痕**。
- 多人并发性能、权限的服务端执行、备份/恢复、真实数据隔离、移动设备帧率没有实测。
- 图文有演示效果，前端有相应流程，不等于所有后台功能已稳定可用。
- 未识别到 Mingleaf 项目的开源许可。只公开研究结论、文件定位与校验摘要，不在本仓库整包镜像作者代码、图片或品牌素材。

## 待核实事项

1. 作者是否愿意公开原始工程、后端、数据库迁移及部署说明，是否有 GitHub/Gitee 等正式仓库。
2. Mingleaf 代码与 3D/字体/文档素材的许可范围。
3. 两个站的版本关系；备用资源目录前缀的具体含义。
4. HTTP 实时拉取的服务器等待机制、负载和多用户一致性。
5. AI 摘要背后的模型、数据发送范围和真实效果。
6. 文档/Word/上传预览各自的协作模式、权限与大文件边界。
7. 作者参赛及浏览量宣称，校园真实使用效果。

## 来源与证据

以下官网构建文件为 **2026-11-22 实际读取**的发布资源，不是永久 Git commit 链接；校验摘要见同目录快照。

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S1 | [JAY1023 抖音图文及公开作者评论](https://www.douyin.com/note/7710680127528504616) | 2026-11-22 | 2026-11-22 | 作者、说明、五张图片、两个官网入口 |
| S2 | [Mingleaf Qoder 主站](https://mingleaf-vhixy8if5qk.qoder.zone/)；[备用站](https://demo.jay23.cn/) | 未知 | 2026-11-22 | 真实站点身份、HTML 引用、公开登录页 |
| S3 | [入口 index-Boyh8TLa.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/index-Boyh8TLa.js)；[React 厂商包](https://mingleaf-vhixy8if5qk.qoder.zone/assets/react-vendor-B8ms0qdQ.js) | 未知 | 2026-11-22 | API、HTTP 实时客户端、React 版本、局部降级 |
| S4 | [Scene-C9NNscCf.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/Scene-C9NNscCf.js) | 未知 | 2026-11-22 | 邻近距离、气泡时间、事件与项目刷新 |
| S5 | [SceneCanvas-CsyqYyL9.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/SceneCanvas-CsyqYyL9.js)；[Three.js 厂商包](https://mingleaf-vhixy8if5qk.qoder.zone/assets/three-CH9DKzjz.js) | 未知 | 2026-11-22 | 3D 场景、问候、显示与降级设置 |
| S6 | [ArtifactLibrary-qMcidO6C.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/ArtifactLibrary-qMcidO6C.js) | 未知 | 2026-11-22 | 基准版本、冲突处理、成果版本与修改提议 |
| S7 | [merge3-CYUgnbT3.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/merge3-CYUgnbT3.js) | 未知 | 2026-11-22 | 按行差分/三方合并及小范围函数验证 |
| S8 | [RoomTools-DaWk4PrI.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/RoomTools-DaWk4PrI.js)；[ProjectWorkspace-CC_MRYFn.js](https://mingleaf-vhixy8if5qk.qoder.zone/assets/ProjectWorkspace-CC_MRYFn.js) | 未知 | 2026-11-22 | 项目、看板、决策、白板、签到、周报 |
| S9 | [WorkAdventure 固定版本 README](https://github.com/workadventure/workadventure/blob/621f2bf29b36e1aa3aacb2e4a64299356f2cf412/README.md)；[前端许可](https://github.com/workadventure/workadventure/blob/621f2bf29b36e1aa3aacb2e4a64299356f2cf412/play/LICENSE.txt)；[后端许可](https://github.com/workadventure/workadventure/blob/621f2bf29b36e1aa3aacb2e4a64299356f2cf412/back/LICENSE.txt) | 未单独核定 | 2026-11-22 | 相似空间社交方向、商业附加限制 |
| S10 | [Plane 固定版本 README](https://github.com/makeplane/plane/blob/da21a8ff8b4b0a1d7bfcca72eb184a13233bb143/README.md)；[LICENSE.txt](https://github.com/makeplane/plane/blob/da21a8ff8b4b0a1d7bfcca72eb184a13233bb143/LICENSE.txt) | 未单独核定 | 2026-11-22 | 项目协作方向和 AGPLv3 许可 |

## 更新记录

- 2026-11-22：首次收录；由作者公开评论定位官网，完成发布前端拆读、限定 source map 检查和四类纯函数样例验证。未取得原始工程或后端，未做整站业务验收。
