# 西安交大校园网自动登录器
### 简介
西安交大校园网自动登录器，python3实现。现在适合在linux下使用，后续考虑适配windows。
### 使用方法

1. 克隆项目

``` sh
cd ~
git clone 
cd AutoLogin_XJTU
vim config.json
```

2. 编辑配置文件config.json

```json
{
  "username": "your netid",
  "password": "your password"
}
```

3. 设置crontab定时执行

```sh
sudo crontan -e
```

在最底下添加

```sh
*/10 * * * * /usr/bin/python3 /home/your home/AutoLogin_XJTU/AutoLogin_XJTU
```

意思是每个小时执行一次登录脚本，然后重启cron服务

```sh
sudo service cron restart
```

