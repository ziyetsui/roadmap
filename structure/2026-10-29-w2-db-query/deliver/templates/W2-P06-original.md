# W2-P06 测试 MySQL db 支持

> 作者原输入。_raw/chats/w2.md 第73–78行；变量/旧路径/错误保留。

目前 mysql 已经得到支持，在 ./w2/db_query/fixtures/test.rest 中添加 MySQL db 支持的测试用例，然后运行测试。如果后端测试 ok，那么打开后端和前端，使用 playwright 测试前端，确保 MySQL db 的基本功能：

- 添加 新的数据库 interview_db（url 为 mysql://root@localhost:3306/interview_db）
- 生成 sql，查询 interview_db，并显示结果
- 自然语言生成 MySQL sql，查询 interview_db，并显示结果
