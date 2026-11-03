# 分课逐字稿

每课独立MD与SRT。中文本地MLX Whisper large-v3-turbo自动识别，语音活动检测后映射回原视频时间；不是人工逐字校订。

高压缩/循环疑似段做短窗重识别，原始首次结果和重试结果留在edit/_raw/transcripts/。剩余低置信词在MD用【转写待核】标注；未静默删真实讲话。术语以原视频画面和代码核对。media-inventory.json记录源路径、时长、流、大小与SHA-256。

- [01-Claude Code 简介](01-Claude Code 简介.md) · [SRT](01-Claude Code 简介.srt)
- [02-Claude Code 的架构设计](02-Claude Code 的架构设计.md) · [SRT](02-Claude Code 的架构设计.srt)
- [03-Claude Code 的常用功能](03-Claude Code 的常用功能.md) · [SRT](03-Claude Code 的常用功能.srt)
- [04-用 Claude Code 为数据库查询工具增加 MySQL 的支持](04-用 Claude Code 为数据库查询工具增加 MySQL 的支持.md) · [SRT](04-用 Claude Code 为数据库查询工具增加 MySQL 的支持.srt)
- [05-用 Claude Code 构建一个语音 App](05-用 Claude Code 构建一个语音 App.md) · [SRT](05-用 Claude Code 构建一个语音 App.srt)
- [06-语音 App 的代码实现](06-语音 App 的代码实现.md) · [SRT](06-语音 App 的代码实现.srt)
- [07-本章小结](07-本章小结.md) · [SRT](07-本章小结.srt)

第4讲归数据库查询工具，已并入对应手册；这里仍保留原w3七讲逐字稿完整清单，RaFlow主线使用其余六讲。
