# W2-P05 添加 MySQL db 支持

> 作者原输入。_raw/chats/w2.md 第69–71行；变量/旧路径/错误保留。

参考 ./w2/db_query/backend 中的 PostgreSQL 实现，实现 MySQL 的 metadata 提取和查询支持，同时自然语言生成 sql 也支持 MySQL。目前我本地有一个 todo_db 数据库，使用 `mysql -u root todo_db -e "SELECT * FROM todos;"` 可以查询到数据。
