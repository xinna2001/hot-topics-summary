# GitHub 轻小说文库：资源库、阅读器与 EPUB 工具选型

收录日期：2026-11-07

最近核实：2026-11-07，Asia/Shanghai

研究状态：项目资料与关键源码已核实；用户所指具体仓库未唯一确定；未运行上游应用或抓取书籍。

## 一句话结论

GitHub 上的“轻小说文库”至少包括三种不同东西：**现成 EPUB/TXT 文件集合、连接文库网站的阅读器、把网页整理成 EPUB 的工具**。找现成目录可看 CyberCommy 的分年库和 `LightNovel_Collection`；研究自动化文库架构可看 `mojimoon/wenku8`；研究安卓阅读与离线书架可比较 MewX 与 LightNovelReader。它们不是同一个项目，也不能因代码开源就推定书籍内容获准用于公开再分发或训练。[S1][S6][S7][S8][S9]

## 原始线索

- 用户原话：`热点信息汇总:github轻小说文库`。
- 用户未提供具体 GitHub 地址、视频、截图、作者或项目名称；因此本条按“关键词专题”研究，**不宣称已找出某条原视频的唯一对应仓库**。
- 首页第三列保留“用户关键词的可复查检索入口（非原帖）”，这是根据输入构造的 GitHub 搜索地址，**不是用户提供的原始链接**。候选项目仅作为本报告研究对象，不冒充原素材来源。
- 实际读取：9 个 GitHub 仓库的 API 元信息、固定提交的递归文件树；可取得的 README；关键生成、数据源接口、构建配置和许可证文件。对网页型项目另做公开首页 HTTP 检查。
- 原材料没有功能、热度或性能宣称。此处 Star 是查询当时的累计快照，不是近期涨星、GitHub Trending 或“正在爆火”的证据。
- 本轮没有下载书籍 EPUB/TXT 正文文件，没有运行下载器、安装 APK、提交上游 Issue、配置抓取账户或部署文库服务。

## 相关项目与资料

### 1. 现成资源库：最接近“GitHub 上放了一套轻小说文库”

| 项目 | Star 快照 | 实际内容 | 已核实的边界 |
| --- | ---: | --- | --- |
| [CyberCommy/lightnovel-2018to2020](https://github.com/CyberCommy/lightnovel-2018to2020) | 338 | 固定提交的完整文件树包含 **1,014 个 `.epub` 文件**；文件名带书名、作者和日期 | 没有 README 或 LICENSE；提交日期为 2021-05-11；同书不同日期可重复，文件数不等于独立作品数。[S6] |
| [CyberCommy/lightnovel-2025](https://github.com/CyberCommy/lightnovel-2025) | 91 | 固定提交包含 **615 个 `.epub` 文件**；全部文件都是 EPUB | 没有 README 或 LICENSE；提交日期为 2025-12-31；年份是仓库组织方式，不能直接认定每本书的出版年份或完整性。[S6] |
| [luozhiming2020/LightNovel_Collection](https://github.com/luozhiming2020/LightNovel_Collection) | 59 | A–Z 与 `others` 目录；完整文件树含 **9,048 个 TXT、2 个 EPUB**，另有图片和 README | README 自称个人网络收集、限个人用途并建议购买正版；未见 LICENSE 或逐书授权清单；默认分支提交停在 2021-03-19。[S7] |

统计方法：通过 `git/trees/<固定 SHA>?recursive=1` 统计 `type=blob` 的文件扩展名，三个树均返回 `truncated=false`。这里没有读取 EPUB 内部章节，不能据此宣称无缺章、无重复、插图完整或“全网最全”。这些是数据文件集合，**不是爬虫程序、在线阅读平台或 AI 写作系统**。[S6][S7]

### 2. 阅读器：应用源码，不是仓库内自带全套书籍

| 项目 | Star 快照 | 技术与功能 | 许可证与版本 |
| --- | ---: | --- | --- |
| [MewX/light-novel-library_Wenku8_Android](https://github.com/MewX/light-novel-library_Wenku8_Android) | 3,398 | Java/Android；Wenku8 第三方客户端；搜索、书架、分卷缓存、图文阅读与阅读进度。主要工程在 `studio-android/LightNovelLibrary` | GPL-2.0；API 查询的最新非预发布 Release 为 `v1.30`，2026-08-29。[S8] |
| [dmzz-yyhyy/LightNovelReader](https://github.com/dmzz-yyhyy/LightNovelReader) | 2,327 | Kotlin/Jetpack Compose；多数据源、插件接口、离线缓存、多个书架、更新提示、EPUB 导出 | Apache-2.0；最新非预发布 Release 为 `1.2.4`，2026-10-16；本次源码取默认分支 `dev/1.3`，不等于发布包。[S9] |

**MewX 的复现注意点：** README 包含很多早年的说明，例如“暂停维护”“2000 本不到”，不能当作 2026 年现状。当前仓库有新发布记录，同时文件树包含 `studio-android/LightNovelLibrary/api` 子模块和 `api-stub`。已读的 stub 中 `BASE_URL` 为 `Unknown`、部分方法抛出 `UnsupportedOperationException`；它不是可用的线上 API 实现。不能把“看到公开工程”说成“自行编译后即可连上真实文库”。本轮没有申请该 API、读取私有子模块或验证官方发布包的服务可用性。[S8]

**LightNovelReader 的技术价值：** `WebBookDataSource` 把搜索、探索、书本详情、分卷目录和章节正文拆成明确接口；`epub/` 模块独立构建 manifest、spine、nav 和 NCX。这比把网络请求、UI 与 EPUB 拼装全部写在同一脚本里更适合扩展数据源。此处是基于接口结构的工程判断，不是实测阅读性能结论。[S9]

### 3. 生成／文库自动化工具：重点看完整链路，不只比 Star

| 项目 | Star 快照 | 定位与已读入口 | 许可证／主要限制 |
| --- | ---: | --- | --- |
| [mojimoon/wenku8](https://github.com/mojimoon/wenku8) | 234 | 文库聚合与静态站点；`merge.py` 合并书目，`main.py` 生成检索页，`gen_epub.py`/`epub_maker.py` 生成电子书，Actions 批量或按需构建 | MIT 是代码许可；依赖第三方目录、下载来源及访问条件；部署与下载质量未实测。[S1–S5] |
| [lncrawl/lightnovel-crawler](https://github.com/lncrawl/lightnovel-crawler) | 2,690 | 多站点电子书引擎；统一 `Crawler` 接口；CLI、FastAPI 服务、网页书库与阅读流程 | `pyproject.toml` 声明 GPL-3.0-or-later、Python ≥3.9；源码版本与最新 Release 均为 `4.14.0`；本次读的是默认 `dev` 分支。其 README 的“361 个来源／446 个 crawler”等数字只是项目声明，本轮没有逐站验收。[S10] |
| [JeffersonQin/lightnovel_epub](https://github.com/JeffersonQin/lightnovel_epub) | 354 | Python provider 框架；轻之国度、Wenku8 页面转 EPUB；`cli.py`、`provider/wenku8.py`、`lightnovel.py` | **混合许可**：`cli.py`、`lightnovel.py` 为 AGPLv3，其余文件为 MIT；默认分支提交日期为 2023-09-09。README 已注明旧直接下载路径遇到站点限制。[S11] |
| [montaro2017/bili_novel_packer](https://github.com/montaro2017/bili_novel_packer) | 757 | Dart 命令行打包；README 列出哔哩轻小说和 Wenku8；`WenkuNovelSource` 获取书籍与卷章信息，`EpubPacker` 生成包结构 | MIT；`pubspec.yaml` 版本 `0.2.50`、Dart `>=3.11.0 <4.0.0`；README 说明提供 Windows 编译产物，其他系统需自行编译。本次 `/releases/latest` 未返回可用最新正式 Release，不能据此说完全没有 release 或附件。[S12] |

筛掉了关键词检索中的泛用图书合集、NLP 大杂烩和无关仓库：它们可能 Star 更高，但不能因为检索命中就视为同功能方案。**Star 更高的 `lightnovel-crawler` 更偏完整的多源私有书库；`mojimoon/wenku8` 更适合研究单一文库的目录聚合和静态发布；两者不能互相替代所有场景。**[S1][S10]

## 技术实现

### A. `mojimoon/wenku8`：目录合并 → 静态检索 → EPUB 构建

这条链路是本专题最值得复用的工程设计，但应替换为有权使用的内容源。

1. **输入层：** 论坛电子书列表、TXT 来源列表、Wenku8 目录和已生成电子书索引。输入大部分先保存成 CSV/JSON，而不是每次打开网页都直接访问来源。[S1][S2]
2. **书目消歧：** 以文库 `aid` 为主键，结合标题、别名、作者和人工映射，把不同来源合并。同一 `aid` 只保留最新 TXT 记录；无法匹配的项保留为独立待处理记录，避免静默丢失。`merge.py:67–165` 直接体现此流程。[S2]
3. **静态前端：** `main.py:create_data()` 把合并 CSV 与 `epub_index.json` 变成精简 JSON；`create_html()` 将数据替换进模板，输出 `docs/index.html`。浏览器看到的是检索入口，不等于所有书籍正文都嵌在 HTML 里。[S3]
4. **电子书生成：** `gen_epub.py` 提供目录、简介、章节解析与分卷构建入口；`epub_maker.py:create_epub()` 把封面、简介、章节 XHTML、图片、CSS、nav、NCX、OPF 打包。其 `mimetype` 首项使用不压缩存储，最终从临时文件原子替换成 EPUB。**源码存在完整包结构不代表本轮已经通过 epubcheck。**[S4]
5. **异步更新：** Actions 工作流负责构建、写入索引、触发静态站部署；按需请求由 Issue 触发，本质上是把 Issue 当作任务队列，而不是网页内同步等待全书生成。[S5]

```text
目录／来源元信息
        ↓
CSV + aid 主键消歧 + 人工别名
        ↓
merged.csv ──────────→ 模板 + JSON → 静态检索页
        ↓                                  ↑
有权读取的卷章内容 → EPUB 构建 → 版本／分卷索引
```

**发现的文档／实现差异：** README 称请求队列“每小时检查”，但已读 `build_request.yml:10–11` 的 cron 为 `27 7/12 * * *`，即每 12 小时检查一次，另有 `issues: opened` 即时触发。批量工作流 `build_epub.yml:9–10` 则是每 4 小时计划一次。实际执行时刻还受 Actions 调度影响，不能把计划周期当成保证完成的 SLA。配额说明也有 README 与工作流注释不一致的痕迹，本轮没有检查 `build_request.py` 的实际配额逻辑，因此不复述配额数字为已核实规则。[S1][S5]

公开首页 `https://wenku.mojimoon.top` 本轮返回 HTTP 200，HTML 标题为“轻小说文库 EPUB 下载”，收到 1,665,573 字节。**只检查 HTTP HTML，没有实际操作搜索、点击下载或提交生成请求**；不能把首页可访问升级成端到端功能验收。[S13]

### B. 阅读器与生成器的共同模型

- 阅读器把内容建模成“书 → 卷 → 章”，缓存正文、插图和阅读位置；MewX 文档给出 XML 与本地书架存档，LightNovelReader 接口明确分离书本资料、卷目录与章节结果。[S8][S9]
- Python provider 或 Dart source 负责将站点特有的 DOM 转换为统一模型；EPUB builder 再生成资源清单与阅读顺序。JeffersonQin 的 Wenku8 provider 明确按目录表格区分卷、章并按卷筛选；Dart 的 packer 明确写入 mimetype、container、NCX、XHTML 导航和 OPF。[S11][S12]
- `lightnovel-crawler` 进一步增加服务层。已读 `lncrawl/server/app.py:33–52` 建立 FastAPI/OpenAPI，`79–95` 接入 API 与静态资源；并非只有 CLI，也不是原文中某个 GitHub 资源目录的别名。[S10]

| 关键判断 | 证据状态 | 依据 |
| --- | --- | --- |
| CyberCommy 的两份被查仓库是 EPUB 文件集合，不含生成代码 | 已核实 | 完整树与扩展名统计。[S6] |
| `LightNovel_Collection` 以 TXT 文件为主，不是 EPUB 优先工具 | 已核实 | 9,048 TXT／2 EPUB；README 自述。[S7] |
| `mojimoon/wenku8` 有实际 CSV 合并、HTML 输出与 EPUB 构建代码 | 已核实（静态） | `merge.py`、`main.py`、`epub_maker.py`。[S2–S4] |
| 作者说生成文件可通过 epubcheck，且页面首屏快 | 作者宣称，未实测 | README；本轮没有生成或做性能测试。[S1] |
| 本关键词唯一指向 MewX、CyberCommy 或 mojimoon 中某一个 | 未确认 | 用户没有给 owner/repo 或原素材。 |
| 这些项目的正文均可合法公开再分发／用于模型训练 | 未确认 | 缺逐书授权证据，软件许可证不能作为正文授权证明。 |

## 复现路径

**状态：基于资料与静态源码整理，未实际运行上游项目。** 下列是验证路线，不是已经完成的部署或批量采集。

### 1. 复查资源库目录（不读取正文）

- 输入：仓库地址和下表固定 SHA。
- 用 GitHub Git Trees API 取得完整树，确认 `truncated=false`，仅统计文件路径、扩展名和重复命名。
- 预期：2018–2020 库是 1,014 个 EPUB；2025 库是 615 个 EPUB；`LightNovel_Collection` 是 9,048 个 TXT、2 个 EPUB。**这些统计已实际执行。**
- 验收：计数对应固定提交，不把文件数当作品数；若需要正文质量评估，另行选择明确有权使用的样本，检查缺章、编码、图片与重复卷。

### 2. 研究并复现文库静态页

- 固定 `mojimoon/wenku8` 的已查 SHA；先审查依赖、入口和工作流的外部请求／写操作，在隔离目录操作，不启用自动发布工作流。
- 上游 workflow 使用 Python 3.12；依赖见 `requirements.txt`。先用自己的书目或可使用的元信息替代下载地址与原始内容源。
- README 提供 `python main.py none` 的离线路径，含义是跳过抓取、重新合并已有数据并生成页面；此命令**本轮未运行**。
- 预期：得到 `out/merged.csv` 与 `docs/index.html`；同一书目正确合并，不匹配项有保留与原因；浏览器搜索书名、别名、作者均指向同一条目。
- 验收：核对源记录数量、主键唯一性、孤立项与页面链接；这比只看网页成功打开更有意义。

### 3. 验证 EPUB 或阅读器

- 用自己创作的测试文本和自有图片，构造书名、作者、一卷两章、封面等最小样本；**不要直接从未知授权资源库复制正文当测试数据**。
- 对生成器核对 mimetype、container、OPF、manifest、spine、nav/NCX、内部图片路径，再用 epubcheck 和阅读器检查显示；重复生成核对章节顺序、文本保留与插图引用。
- 对 Android 项目先确认发布版本、源码分支和所需 SDK／JDK；LightNovelReader 可优先用自定义测试数据源或已获授权的样本，MewX 必须区分真实 API 与 stub。
- 预期：两章按正确顺序可读、插图无断链、缓存后离线可读、阅读位置可保存。
- **以上生成、编译、离线阅读、插件加载和 epubcheck 均未执行。** 本轮没有为“研究成功”虚构行为测试通过率。

## 适用场景与限制

- **找资源目录：** 先辨认 CyberCommy 的年份分库与 `LightNovel_Collection` 的文本目录，不能默认它们持续更新、覆盖全部轻小说或有商业使用授权。
- **研究书库自动化：** `mojimoon/wenku8` 的元信息落盘、主键消歧、静态发布和异步任务思路有参考价值；实际部署需重新核验来源、访问条件与写权限。
- **Android 多源阅读开发：** LightNovelReader 的插件／API 模块更贴近扩展数据源；MewX 是长期第三方客户端参考，但历史文档和 API 子模块是重要门槛。
- **多站点私人书库：** `lightnovel-crawler` 链路较完整，但默认开发分支、外部模块与服务安全配置均要另行验证，不因高 Star 直接认定更稳定。
- **授权与内容边界：** 三份资源仓库未展示逐书授权清单；收集者的免责声明也不是权利人的授权证明。本报告只收录技术与目录信息，不镜像小说正文。项目的 MIT/GPL/Apache/AGPL 标签是所读代码的许可信息，未证明对应小说和插图可再利用。
- **网站可用性：** 页面结构、登录要求、限流或下架可能变化。遇到访问限制或内容下架应停下核实，不把“调整请求就能拿到”当作授权；本轮没有使用绕过付费、验证码或访问控制的方法。
- **热度与质量：** Star、更新日期、文件数量分别只说明累计关注、记录时间和文件库存；不能推出下载成功率、版权完整性、检索正确率或 EPUB 质量。

## 待核实事项

1. 用户所指的是哪一个具体 GitHub 仓库；若后续补 owner/repo 或原链接，更新本专题，保留本轮关键词来源，不另造重复条目。
2. 三份资源库的独立作品数、卷章完整性、文本／插图质量及逐书权利信息；本轮只统计路径，没有检查正文。
3. mojimoon 首页搜索、生成请求、Release 文件下载、内容一致性与 EPUB 合规；HTTP 200 不代表这些都通过。
4. mojimoon 文档中队列检查周期与配额说明的同步；已记录 cron 差异，但没有为上游提交修复。
5. MewX API 子模块可用性与发布应用真实联网能力；LightNovelReader 开发分支与正式包的插件兼容性。
6. 各生成器当前站点适配、目标平台安装／编译、服务安全配置与真实采集结果；本轮没有开启生产任务。

## 固定版本快照

日期是所查默认分支 head 的 **committer 时间（UTC）**，不是项目首次发布日期。`pushed_at` 可能来自其他分支或 tag，不能与默认分支源码日期混为一谈。API 原始快照与路径统计见 [research_snapshot.json](research_snapshot.json)。

| 仓库 | 所查分支 | 固定 commit | commit 日期（UTC） |
| --- | --- | --- | --- |
| CyberCommy/lightnovel-2018to2020 | master | `279c8c2438b8785b9ec05482be65cbd73a4c0fc5` | 2021-05-11 |
| CyberCommy/lightnovel-2025 | master | `117ae8545c3ec47c26a5dde2621fb6a62bf3319e` | 2025-12-31 |
| luozhiming2020/LightNovel_Collection | master | `65bbecd6643b8689400599dd544461b95f460bdd` | 2021-03-19 |
| mojimoon/wenku8 | main | `4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1` | 2026-11-06 |
| MewX/light-novel-library_Wenku8_Android | master | `7cd6a569ca5fb0c12fbc5c25cc8ddc658531fba0` | 2026-08-29 |
| dmzz-yyhyy/LightNovelReader | dev/1.3 | `49695ccfeab4207adf6ad476b1f48078f7bee2ac` | 2026-10-25 |
| lncrawl/lightnovel-crawler | dev | `59b0382d51927953aa8120c5de62dab23ce3f731` | 2026-08-04 |
| JeffersonQin/lightnovel_epub | master | `05a6aee5a51fb79b1095507edf9242184239c6b9` | 2023-09-09 |
| montaro2017/bili_novel_packer | master | `b75b1fb518fb8ba76623ac8328fafdfd25e065df` | 2026-10-31 |

## 来源与证据

全部技术来源为实际读取的上游仓库／项目页面；没有把搜索摘要、镜像、第三方热度网站当作实现证明。查阅日期均为 2026-11-07。

| 编号 | 一手来源与链接 | 记录日期或发布状态 | 支持的结论 |
| --- | --- | --- | --- |
| S1 | [mojimoon README](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/README.md)；[MIT LICENSE](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/LICENSE) | 固定提交 2026-11-06 | 项目定位、来源、离线路径；作者性能与质量宣称；代码许可。 |
| S2 | [merge.py:67–165](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/merge.py#L67-L165) | 同 S1 | aid 消歧、最新记录、孤立项保留、CSV 输出。 |
| S3 | [main.py:249–326](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/main.py#L249-L326) | 同 S1 | 页面数据和静态 HTML 生成。 |
| S4 | [gen_epub.py](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/gen_epub.py)；[epub_maker.py:183–344](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/epub_maker.py#L183-L344) | 同 S1 | 生成入口、包结构和原子写入；不是 epubcheck 通过证据。 |
| S5 | [build_epub.yml](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/.github/workflows/build_epub.yml)；[build_request.yml](https://github.com/mojimoon/wenku8/blob/4dbbfb22a0e5069fd23077076b8c5eaa1016d8d1/.github/workflows/build_request.yml) | 同 S1 | 定时／Issue 触发、共享并发组、索引写入；队列 cron 差异。 |
| S6 | [2018–2020 文件树](https://api.github.com/repos/CyberCommy/lightnovel-2018to2020/git/trees/279c8c2438b8785b9ec05482be65cbd73a4c0fc5?recursive=1)；[2025 文件树](https://api.github.com/repos/CyberCommy/lightnovel-2025/git/trees/117ae8545c3ec47c26a5dde2621fb6a62bf3319e?recursive=1) | 固定提交 2021-05-11／2025-12-31 | EPUB 文件数量、纯资源库形态、README/LICENSE 缺失。 |
| S7 | [Collection README](https://github.com/luozhiming2020/LightNovel_Collection/blob/65bbecd6643b8689400599dd544461b95f460bdd/README.md)；[完整文件树](https://api.github.com/repos/luozhiming2020/LightNovel_Collection/git/trees/65bbecd6643b8689400599dd544461b95f460bdd?recursive=1) | 固定提交 2021-03-19 | 个人收集声明、目录和文件类型，不是授权证明。 |
| S8 | [MewX README](https://github.com/MewX/light-novel-library_Wenku8_Android/blob/7cd6a569ca5fb0c12fbc5c25cc8ddc658531fba0/README.md)；[API stub](https://github.com/MewX/light-novel-library_Wenku8_Android/blob/7cd6a569ca5fb0c12fbc5c25cc8ddc658531fba0/studio-android/LightNovelLibrary/api-stub/src/main/java/org/mewx/wenku8/api/Wenku8API.java)；[v1.30 发布](https://github.com/MewX/light-novel-library_Wenku8_Android/releases/tag/v1.30) | Release 2026-08-29；固定提交同日 | Java 阅读器、存档设计、历史文档差异、stub 和版本。 |
| S9 | [LightNovelReader README](https://github.com/dmzz-yyhyy/LightNovelReader/blob/49695ccfeab4207adf6ad476b1f48078f7bee2ac/README.md)；[数据源接口](https://github.com/dmzz-yyhyy/LightNovelReader/blob/49695ccfeab4207adf6ad476b1f48078f7bee2ac/api/src/main/kotlin/io/nightfish/lightnovelreader/api/web/WebBookDataSource.kt)；[EPUB builder](https://github.com/dmzz-yyhyy/LightNovelReader/blob/49695ccfeab4207adf6ad476b1f48078f7bee2ac/epub/src/main/kotlin/io/nightfish/potatoepub/builder/EpubBuilder.kt)；[1.2.4 发布](https://github.com/dmzz-yyhyy/LightNovelReader/releases/tag/1.2.4) | 固定提交 2026-10-25；Release 2026-10-16 | Compose、多源／缓存、接口和独立 EPUB 模块。 |
| S10 | [Crawler README](https://github.com/lncrawl/lightnovel-crawler/blob/59b0382d51927953aa8120c5de62dab23ce3f731/README.md)；[pyproject.toml](https://github.com/lncrawl/lightnovel-crawler/blob/59b0382d51927953aa8120c5de62dab23ce3f731/pyproject.toml)；[Crawler 接口](https://github.com/lncrawl/lightnovel-crawler/blob/59b0382d51927953aa8120c5de62dab23ce3f731/lncrawl/core/crawler.py)；[FastAPI 入口](https://github.com/lncrawl/lightnovel-crawler/blob/59b0382d51927953aa8120c5de62dab23ce3f731/lncrawl/server/app.py) | 固定提交 2026-08-04；Release v4.14.0 为 2026-08-03 | 多源引擎、CLI／服务架构、Python 和代码许可；来源数未逐站验收。 |
| S11 | [lightnovel_epub README](https://github.com/JeffersonQin/lightnovel_epub/blob/05a6aee5a51fb79b1095507edf9242184239c6b9/README.md)；[混合 LICENSE](https://github.com/JeffersonQin/lightnovel_epub/blob/05a6aee5a51fb79b1095507edf9242184239c6b9/LICENSE)；[Wenku8 provider](https://github.com/JeffersonQin/lightnovel_epub/blob/05a6aee5a51fb79b1095507edf9242184239c6b9/provider/wenku8.py) | 固定提交 2023-09-09 | provider 适配、卷章解析、明确的分文件许可。 |
| S12 | [bili_novel_packer README](https://github.com/montaro2017/bili_novel_packer/blob/b75b1fb518fb8ba76623ac8328fafdfd25e065df/README.md)；[pubspec.yaml](https://github.com/montaro2017/bili_novel_packer/blob/b75b1fb518fb8ba76623ac8328fafdfd25e065df/pubspec.yaml)；[WenkuNovelSource](https://github.com/montaro2017/bili_novel_packer/blob/b75b1fb518fb8ba76623ac8328fafdfd25e065df/lib/light_novel/wenku_novel/wenku_novel_source.dart)；[EpubPacker](https://github.com/montaro2017/bili_novel_packer/blob/b75b1fb518fb8ba76623ac8328fafdfd25e065df/lib/epub_packer/epub_packer.dart) | 固定提交 2026-10-31 | 支持站点声明、Dart 版本、解析／打包入口。 |
| S13 | [mojimoon 公开首页](https://wenku.mojimoon.top)；本专题 JSON 中的 `homepage_check` | 首页发布日期未确认；检查于 2026-11-07 | HTTP 200、HTML 标题／大小／SHA-256；仅首页响应。 |

## 更新记录

- 2026-11-07：根据用户关键词首次收录；比较 9 个项目，按资源库／阅读器／生成工具分类；固定 SHA、Star、代码许可与统计口径；保留具体项目未唯一确认、行为测试未执行及正文授权缺口。
