# 2026-10-26 抖音原文读取摘要

- 原始短链：https://v.douyin.com/nEw2vrdzTTk/
- 规范原文：https://www.douyin.com/note/7700688501772469157
- 作品 ID：7700688501772469157。
- 标题：微信聊天ai机器人；作者：柚子。
- 页面 createTime：1792956266，换算为 2026-10-26 03:24:26（Asia/Shanghai）。
- 公开网页读取 HTTP 200；已有下载器详情 API 返回 HTTP 403。实际从公开网页的数据与图片读取内容，没有取得教程视频。
- 图文类型：awemeType=68；images 数量 4；video.duration=0。
- 四张图片均已读取；这里只保留技术裁剪及内容摘要，完整聊天图片不提交。

## 原文正文

微信聊天ai机器人 借助开源网站github上的AstrBot项目，使用docker工具在本地接入DeepSeek，实现微信聊天机器人。
质疑痞老板，
理解痞老板，
成为痞老板。
#ai开发软件 #微信自动化  #deepseek大肥鱼

## 图片内容及证据边界

1. AstrBotDevs/AstrBot 仓库页面；可见 v4.29.3 和 Python 3.12+ 徽章。只能确认页面展示，不能确认容器实际运行版本。
2. Docker Desktop 列表中 wechatbot、wechat-friend 两个项目显示运行状态。列表没有展开，镜像与端口显示为横线；不能据此还原 Compose 或确认每个项目的软件。
3. 微信聊天图片含“双开测试”“小乖，现在能回复吗？”与机器人回复；随后机器人索取称呼。属于效果截图，未证明实例隔离或跨会话记忆。
4. 微信聊天询问 token 消耗与上下文上限；回复称“我这儿看不到具体数字，一般十万 token 这个量级”，后又称看不到自己的配置。这不是模型元数据或容量测量。

## 归档裁剪

- [仓库、项目标识与版本徽章](2026-10-26-repository.jpg)：从第 1 张图片裁剪并拼接，排除无关浏览器信息和页面底部签名资源地址。
- [Docker 项目列表](2026-10-26-docker-projects.jpg)：从第 2 张图片裁剪，只保留用于判断项目运行状态的列表。

## 文件校验

原始图片 hash 用于追溯本轮实际读取文件，不代表已经公开归档完整图片。

| 文件 | SHA-256 |
| --- | --- |
| source-01.webp | 784548c067bd95ad21e7874ff2b62257d0eed28cbebceed65f1aa12542511569 |
| source-02.webp | 48f0364dd8b4a177c7a8b102127dcd46564587f19a1164223ee7d2c674cf6ac6 |
| source-03.webp | 2c116d942cdc7af91a2a9578e32cae6273000f57b705169e1b946d2ed66dbad5 |
| source-04.webp | 4eeb668a5aca54ce976c5de498cc80d37d931073bdad4032f33f27f484fb3937 |
| 2026-10-26-docker-projects.jpg | 93d07cd89364287ee587984e09a400b31e796189e6ab027ff02c5a4379a389bc |
| 2026-10-26-repository.jpg | e5e02468101a340f2d5d86eee6a0cfb2409db73fc64052c2664efb72dd0b4620 |
