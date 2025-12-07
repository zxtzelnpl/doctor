### 地址
https://tutorial.helloflask.com/ready/

### 常用PSQL命令
\l: 列出所有数据库。
\c <数据库名>: 切换到指定的数据库。
\dt: 查看当前数据库中的所有表。
\d <表名>: 查看某个表的结构（列、数据类型、索引等）。
\encoding: 显示当前数据库的字符集编码。
\q: 退出 psql 命令行。 
\du 命令来查看当前数据库中的所有用户

#### 
```
<!-- 创建数据库新用户 -->
CREATE USER dbuser WITH PASSWORD '123456';

<!-- 创建数据库 -->
CREATE DATABASE exampledb OWNER dbuser;

<!-- 为用户分配数据库权限 -->
GRANT ALL PRIVILEGES ON DATABASE exampledb TO dbuser;
```
 


### 命令
#### 激活
```bash
$ source .venv/bin/activate  # Linux 或 macOS
.venv\Scripts\activate  # Windows
```

#### 退出
```bash
$ deactivate
```
