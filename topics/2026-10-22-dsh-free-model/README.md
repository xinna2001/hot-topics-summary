# dsh-our-free-model：75 提供商聚合与免费渠道

收录日期：2026-10-22

最近核实：2026-10-22（Asia/Shanghai）

研究状态：源码清单已核实；额度、免费路由和实际调用未实测

## 一句话结论

截图指向 dsh-our-free-model。当前源码的注册表确实有 75 个提供商，但其中 68 个使用 API Key、2 个 OAuth、2 个 ADC、3 个免认证本地服务。这个数字不能解释为“75 家平台都免费、不限量且无需账号”。[S1][S2]

## 原始线索

抖音 @Ai大模型小橘子展示仓库名 dsh-our-free-model，并宣称“75家大模型平台全打包”“把75家大模型平台的免费额度全打包了”。[S0] 没有分享链接、视频 ID 或发布日期。

本轮读取官方仓库 README、package.json、提供商注册表和聚合代码，实际执行了 JSON 计数与认证类型分类；没有安装插件或向任何模型发起真实生成请求。

## 技术实现

插件把多条模型来源接入 DeepSeek Harness 的模型选择器，并提供兼容模型接口的本地转发能力。

1. 免费渠道部分从上游获取模型清单；“免费不限量”属于仓库宣称，上游是否实际放行仍取决于网络、认证和当时规则。
2. 聚合部分由 src/providers/registry.json 定义提供商 ID、基础地址、认证方式、协议和默认模型。
3. 用户设置中的 Key、地址覆盖与发现结果被转换成 provider/model 模型条目。
4. src/aggregate.js 的 authUsable 明确要求 apiKey 类型具备非空 Key；OAuth 和 ADC 提供商在该聚合路径中直接判为不可用。
5. 兼容协议、流式响应处理与路由降级负责把不同上游接进同一宿主。[S1][S2][S3]

| 源码统计 | 本轮实际结果 |
| --- | --- |
| 提供商对象总数 / 唯一 ID | 75 / 75 |
| apiKey | 68 |
| oauth | 2 |
| adc | 2 |
| none | 3 |
| local=true | 3 |

上述统计来自固定 commit 的 JSON，不代表实时可调用数、免费数或账号剩余额度。聚合源码的一处注释仍写 76 providers，与实际 JSON 75 不同；这里以可机器核验的数据文件为准。[S2][S3]

## 相关项目与资料

- 仓库：[Ebony-Vinyl/dsh-our-free-model](https://github.com/Ebony-Vinyl/dsh-our-free-model)；早期搜索记录可能显示旧 owner，本轮以 GitHub 当前名称为准。
- 核实 commit：482500f79ecbf92f581e1d2e98f170701a743083。
- package.json 显示版本 2.5.9、MIT、Node 版本要求 ^22.19.0 或 >=24.0.0。[S4]
- README 另列匿名免费渠道、需要登录的账号渠道以及桌面专属渠道；各自要求不能合并为一句“无登录”。[S1]
- src/providers/registry.json 和 src/aggregate.js 是理解“75 家”最直接的入口。

## 复现路径

**清单统计已实际运行；插件和模型调用未运行。**

要复核本次事实，下载固定版本注册表后用 Python 标准库统计：

```python
import json
from collections import Counter

providers = json.load(open("registry.json", encoding="utf-8"))
print(len(providers), len({p["id"] for p in providers}))
print(Counter(p["auth"]["kind"] for p in providers))
print(sum(bool(p.get("local")) for p in providers))
```

本轮输出：75、75；apiKey=68、oauth=2、adc=2、none=3；local=3。

进一步测试应选一个明确允许此接入方式的渠道，使用自己的授权，记录模型、响应状态、延迟与真实用量。列表探测和模型名称出现，不等于生成已成功或费用为零。

## 适用场景与限制

适合研究模型聚合、协议兼容、动态目录和失败降级。提供商有试用额度并不代表该额度由插件统一发放；本地 Ollama/LM Studio/llama.cpp 也仍需要模型与算力。上游 Key、登录、地区政策及数据使用规则要逐渠道核对。仓库自己的 MIT 许可不替代上游服务条款。

## 待核实事项

- 原抖音链接及宣传时的插件版本。
- 各上游当时的免费政策、实际成功模型数、数据记录政策与计费。
- 桌面专属或账号渠道的授权要求；本轮没有尝试破解、借用或绕过这些要求。

## 来源与证据

| 编号 | 来源与链接 | 发布日期 | 查阅日期 | 支持的结论 |
| --- | --- | --- | --- | --- |
| S0 | [截图证据](evidence/04-source.jpg) | 未知 | 2026-10-22 | 项目名与“75 家免费额度”宣称 |
| S1 | [固定版本 README](https://github.com/Ebony-Vinyl/dsh-our-free-model/blob/482500f79ecbf92f581e1d2e98f170701a743083/README.md) | 版本截至 2026-10-22 | 2026-10-22 | 插件、各类渠道及免费口径 |
| S2 | [提供商注册表](https://github.com/Ebony-Vinyl/dsh-our-free-model/blob/482500f79ecbf92f581e1d2e98f170701a743083/src/providers/registry.json) | 同上 | 2026-10-22 | 75 条记录与认证分类，本轮已实际统计 |
| S3 | [聚合源码](https://github.com/Ebony-Vinyl/dsh-our-free-model/blob/482500f79ecbf92f581e1d2e98f170701a743083/src/aggregate.js#L162) | 同上 | 2026-10-22 | 认证可用性和目录生成 |
| S4 | [package.json](https://github.com/Ebony-Vinyl/dsh-our-free-model/blob/482500f79ecbf92f581e1d2e98f170701a743083/package.json) | 同上 | 2026-10-22 | 版本、许可与运行依赖 |

## 更新记录

- 2026-10-22：定位项目，实测注册表统计，拆分免费宣传和实际认证要求。


## 输入溯源

- 首批图片顺序：4。
- 原消息：om_x100b62aa71b124a0de0331f9b5c3bf4。
- 原附件文件名：img_v3_0216n_f38eed6c-bad3-414b-baf3-2b339265d47g.jpg。
- 原图 SHA-256：57f3dcdacd363432c1cf4b619eb44c973c291076e6e52755bcc65cd241c87115。
- 保存的是技术相关裁剪图；完整原图仍在本机附件目录。
- 本轮没有还原出可确认的原抖音链接。
