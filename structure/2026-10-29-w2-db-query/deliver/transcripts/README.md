# 分课逐字稿

每课独立MD与SRT。中文本地MLX Whisper large-v3-turbo自动识别，语音活动检测后映射回原视频时间；不是人工逐字校订。

高压缩/循环疑似段做短窗重识别，原始首次结果和重试结果留在edit/_raw/transcripts/。剩余低置信词在MD用【转写待核】标注；未静默删真实讲话。术语以原视频画面和代码核对。media-inventory.json记录源路径、时长、流、大小与SHA-256。

- [01-快速上手 Cursor](01-快速上手 Cursor.md) · [SRT](01-快速上手 Cursor.srt)
- [02-如何使用 Cursor 的 Rules](02-如何使用 Cursor 的 Rules.md) · [SRT](02-如何使用 Cursor 的 Rules.srt)
- [03-Spec Kit 实践](03-Spec Kit 实践.md) · [SRT](03-Spec Kit 实践.srt)
- [04-设计一个数据库查询工具](04-设计一个数据库查询工具.md) · [SRT](04-设计一个数据库查询工具.srt)
- [05-实现数据库查询工具](05-实现数据库查询工具.md) · [SRT](05-实现数据库查询工具.srt)
- [w3-04-用 Claude Code 为数据库查询工具增加 MySQL 的支持](w3-04-用 Claude Code 为数据库查询工具增加 MySQL 的支持.md) · [SRT](w3-04-用 Claude Code 为数据库查询工具增加 MySQL 的支持.srt)

w3-04为同一数据库项目的MySQL扩展；其他5讲沿用w2原编号。
