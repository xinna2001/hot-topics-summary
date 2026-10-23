# 原素材与核实记录

查阅：2026-10-23，Asia/Shanghai。原作品 ID：7698725807199441387。

## 可见作者评论

原页面的一条作者回复：

> 点插件，添加插件，输入dsh-market搞完之后，设置，里面搞一个dsh-web-all和dsh-boot-animation就好了

读取方式：在已有浏览器能力中打开公开作品页，读取可见评论；未发送评论、关注或私信。该回复没有获取到可长期引用的独立评论 URL，引用作品页面作为来源。

## 媒体核验

| 文件 | 来源 | 实际字节数 | 解码规格 | SHA-256 |
| --- | --- | --- | --- | --- |
| 原抖音 1080p 录像 | 平台浏览器详情响应的播放地址 | 5,995,997 | H.264 / AAC，1920×1080，15.58s | `6a8d8e3eeb76f0f56c94d0eada5add6745be41c7f530ba0e5a0cc4e4c2bda1c5` |
| deepseek-cyberpunk-intro.mp4 | NativeDog1/dsh-boot-animation，commit 24c711296cb4af2618fef4f65e81346a660fc67b | 1,856,280 | H.264 / AAC，1280×720，7.05s | `beabf5956e0b467e9f06f467b3f5b7a682abb6555c1b16aee1c27f7e5b334a58` |
| whale-fantasy-loop.mp4 | dsh-web 商店副本，commit 9c1523417f76ea36516db80e831953c1f1062007 | 6,630,589 | H.264，无音轨，1664×856，25.458333s | `db8a022ac3bf877efb764ca4962e79c9b32cc07fa4be2cbc8ac98d4df0310e4d` |

原录像下载返回 HTTP 200，字节数与详情 `data_size` 一致，MD5 与详情 `file_hash` 一致。上游 MP4 字节数与 GitHub tree 中 size 一致。以上 SHA-256 只用于记录本次读取的文件，不表示三份文件彼此一致。

视觉检查范围：原录像 0–15 秒每秒一帧；片头与循环背景的多个关键帧。原录像中 2–7 秒与赛博朋克片头的线框、彩色角色及字标对应；8–15 秒与背景的线框网格、横向扫描光、代码雨及眨眼对应。没有以视觉比对推断原视频的具体生成模型。

## 实际运行范围

原视频读取与上游素材 ffprobe 通过。独立 HTML 演示的浏览器结果见 [demo/verification.json](demo/verification.json)，包括视频解码、跳转、循环设置、画面贴合、Esc 跳过、本地 Blob 视频选择及片头结束切换。未安装第三方 DSH 插件，也未在用户正式应用中部署。

正式仓库仅保留研究文字、示例代码与验证摘要；播放 URL 为固定 commit 的公开素材地址，没有纳入平台 Cookie、浏览器原始详情、临时签名下载地址或下载的 MP4。
