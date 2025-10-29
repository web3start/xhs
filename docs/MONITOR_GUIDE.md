# 小红书用户笔记监控和自动下载指南

## 目录
- [功能介绍](#功能介绍)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [使用方法](#使用方法)
- [常见问题](#常见问题)
- [高级用法](#高级用法)

---

## 功能介绍

这个工具可以帮助你：

✅ **自动监控**：定期检查指定小红书用户是否发布了新笔记  
✅ **智能下载**：自动下载新笔记的图片或视频到本地  
✅ **元数据保存**：保存笔记的标题、描述、标签、互动数据等信息  
✅ **防重复下载**：自动记录已下载的笔记，避免重复下载  
✅ **友好组织**：按笔记标题和ID创建独立文件夹存储  

---

## 快速开始

### 1. 安装依赖

```bash
# 安装xhs包
pip install -e .

# 或者从PyPI安装
pip install xhs

# 安装playwright（用于签名）
pip install playwright
playwright install chromium
```

### 2. 获取Cookie

#### 方法一：从浏览器获取（推荐）

1. 打开浏览器，访问 https://www.xiaohongshu.com
2. 登录你的小红书账号
3. 按 `F12` 打开开发者工具
4. 点击 `Network`（网络）标签
5. 刷新页面，随便点击一个请求
6. 在右侧找到 `Request Headers`（请求头）
7. 找到 `Cookie` 字段，复制完整的cookie值

#### 方法二：使用登录脚本

```python
# 参考 example/login_qrcode.py
python example/login_qrcode.py
```

### 3. 获取要监控的用户ID

1. 访问你想监控的用户主页
2. URL格式为：`https://www.xiaohongshu.com/user/profile/用户ID`
3. 复制URL中的用户ID

例如：`https://www.xiaohongshu.com/user/profile/5b3f8c8e0000000001000a1b`  
用户ID就是：`5b3f8c8e0000000001000a1b`

### 4. 首次运行

```bash
cd example
python monitor_user_notes.py
```

首次运行会自动创建 `monitor_config.json` 配置文件模板。

### 5. 编辑配置文件

打开 `monitor_config.json`，填入你的信息：

```json
{
    "cookie": "你的cookie",
    "user_id": "要监控的用户ID",
    "download_dir": "./downloads",
    "check_interval": 300,
    "stealth_js_path": "./stealth.min.js",
    "use_headless": true,
    "max_retries": 3,
    "retry_delay": 2,
    "downloaded_notes_file": "downloaded_notes.json"
}
```

### 6. 开始监控

```bash
python monitor_user_notes.py
```

---

## 详细配置

### 配置文件说明 (monitor_config.json)

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `cookie` | 字符串 | 你的小红书cookie | `"your_cookie_here"` |
| `user_id` | 字符串 | 要监控的用户ID | `"target_user_id_here"` |
| `download_dir` | 字符串 | 下载文件保存目录 | `"./downloads"` |
| `check_interval` | 整数 | 检查新笔记的间隔（秒） | `300` (5分钟) |
| `stealth_js_path` | 字符串 | stealth.js文件路径 | `"./stealth.min.js"` |
| `use_headless` | 布尔值 | 是否使用无头浏览器 | `true` |
| `max_retries` | 整数 | 失败重试次数 | `3` |
| `retry_delay` | 整数 | 重试延迟（秒） | `2` |
| `downloaded_notes_file` | 字符串 | 已下载笔记记录文件 | `"downloaded_notes.json"` |

### 关于 stealth.js

`stealth.js` 文件用于防止被网站检测为自动化工具。你可以：

1. 从这里下载：https://github.com/requireCool/stealth.min.js
2. 或者不使用（代码会自动跳过）

---

## 使用方法

### 基本使用

#### 持续监控模式（推荐）

```bash
python monitor_user_notes.py
```

程序会每隔指定时间（默认5分钟）检查一次是否有新笔记。

#### 单次检查模式

```bash
python monitor_user_notes.py --once
```

只执行一次检查，然后退出。适合配合cron或其他调度工具使用。

#### 使用自定义配置文件

```bash
python monitor_user_notes.py --config my_config.json
```

### 下载的文件结构

```
downloads/
├── 笔记标题_笔记ID_时间戳/
│   ├── metadata.json          # 笔记元数据
│   ├── 笔记标题_1.png         # 图片1（如果是图文）
│   ├── 笔记标题_2.png         # 图片2
│   └── ...
├── 另一篇笔记_ID_时间戳/
│   ├── metadata.json
│   └── 笔记标题.mp4           # 视频（如果是视频笔记）
└── ...
```

### metadata.json 内容示例

```json
{
    "note_id": "6505318c000000001f03c5a6",
    "title": "笔记标题",
    "desc": "笔记描述内容...",
    "type": "normal",
    "user": {
        "user_id": "...",
        "nickname": "...",
        "avatar": "..."
    },
    "tags": [
        {"name": "标签1"},
        {"name": "标签2"}
    ],
    "interact_info": {
        "liked_count": "123",
        "collected_count": "45",
        "comment_count": "67",
        "share_count": "8"
    },
    "download_time": "2024-01-15T10:30:00.000000",
    "xsec_token": "..."
}
```

---

## 常见问题

### Q1: 签名失败怎么办？

**问题**：出现 `window._webmsxyw is not a function` 错误

**解决方案**：
1. 设置 `use_headless: false` 查看浏览器状态
2. 增加 `retry_delay` 延迟时间
3. 确保playwright已正确安装：`playwright install chromium`
4. 尝试更新cookie

### Q2: Cookie失效怎么办？

**现象**：请求失败，返回登录相关错误

**解决方案**：
1. 重新从浏览器获取cookie
2. 确保cookie包含 `a1`、`webId` 等关键字段
3. 使用登录脚本重新登录获取cookie

### Q3: 下载速度慢怎么办？

**原因**：为避免被限制，程序会在请求间加入延迟

**解决方案**：
- 这是正常的，请耐心等待
- 不建议过度降低延迟时间，可能导致IP被封

### Q4: 如何监控多个用户？

**方法一**：创建多个配置文件
```bash
python monitor_user_notes.py --config user1_config.json
python monitor_user_notes.py --config user2_config.json
```

**方法二**：使用进程管理工具（如supervisord）同时运行多个实例

### Q5: 出现验证码怎么办？

**原因**：请求频率过高或IP被标记

**解决方案**：
1. 增加 `check_interval` 间隔时间
2. 使用代理IP
3. 等待一段时间后重试

### Q6: 如何只下载新笔记？

程序会自动记录已下载的笔记ID到 `downloaded_notes.json` 文件中，只会下载新笔记。

如果想重新下载所有笔记，删除 `downloaded_notes.json` 文件即可。

---

## 高级用法

### 1. 配合Cron定时执行（Linux/Mac）

```bash
# 编辑crontab
crontab -e

# 每小时执行一次检查
0 * * * * cd /path/to/xhs/example && python monitor_user_notes.py --once

# 每天早上9点执行检查
0 9 * * * cd /path/to/xhs/example && python monitor_user_notes.py --once
```

### 2. 配合Windows计划任务

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每小时）
4. 操作选择"启动程序"
5. 程序/脚本填写：`python`
6. 添加参数：`monitor_user_notes.py --once`
7. 起始于：脚本所在目录

### 3. 使用Supervisor持续运行（Linux）

创建 `/etc/supervisor/conf.d/xhs_monitor.conf`：

```ini
[program:xhs_monitor]
command=python /path/to/xhs/example/monitor_user_notes.py
directory=/path/to/xhs/example
autostart=true
autorestart=true
stderr_logfile=/var/log/xhs_monitor.err.log
stdout_logfile=/var/log/xhs_monitor.out.log
user=your_username
```

启动：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start xhs_monitor
```

### 4. 使用Docker运行

创建 `Dockerfile`：

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install playwright && playwright install chromium

COPY . .

CMD ["python", "example/monitor_user_notes.py"]
```

构建和运行：
```bash
docker build -t xhs-monitor .
docker run -v $(pwd)/downloads:/app/downloads -v $(pwd)/monitor_config.json:/app/example/monitor_config.json xhs-monitor
```

### 5. 添加通知功能

可以修改代码添加通知，例如：

```python
# 在 check_new_notes 方法中添加
if new_notes:
    # 发送邮件通知
    send_email(f"发现 {len(new_notes)} 条新笔记")
    
    # 或发送微信/Telegram通知
    send_wechat_notification(f"发现 {len(new_notes)} 条新笔记")
```

### 6. 批量监控多用户

创建 `multi_user_monitor.py`：

```python
import json
from monitor_user_notes import NoteMonitor
import time

# 加载多用户配置
with open('users.json', 'r') as f:
    users = json.load(f)

# users.json格式：
# [
#     {"user_id": "xxx", "name": "用户1"},
#     {"user_id": "yyy", "name": "用户2"}
# ]

cookie = "your_cookie_here"

for user in users:
    print(f"检查用户: {user['name']}")
    
    # 为每个用户创建独立配置
    config = {
        "cookie": cookie,
        "user_id": user["user_id"],
        "download_dir": f"./downloads/{user['name']}",
        "downloaded_notes_file": f"downloaded_{user['user_id']}.json"
    }
    
    # 保存临时配置
    config_file = f"config_{user['user_id']}.json"
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    # 执行监控
    monitor = NoteMonitor(config_file)
    monitor.run_once()
    
    time.sleep(10)  # 用户间隔延迟
```

---

## API参考

### XhsClient 主要方法

```python
from xhs import XhsClient

# 初始化客户端
client = XhsClient(cookie="your_cookie", sign=sign_function)

# 获取用户笔记列表（简要信息）
notes = client.get_user_notes(user_id="xxx", cursor="")
# 返回: {"notes": [...], "cursor": "xxx", "has_more": true}

# 获取笔记详细信息
note = client.get_note_by_id(note_id="xxx", xsec_token="xxx")
# 返回: 完整笔记信息字典

# 获取用户信息
user_info = client.get_user_info(user_id="xxx")

# 搜索笔记
results = client.get_note_by_keyword(keyword="旅行")
```

### 辅助函数

```python
from xhs import help

# 从笔记中提取图片URL
img_urls = help.get_imgs_url_from_note(note)

# 从笔记中提取视频URL
video_url = help.get_video_url_from_note(note)

# 下载文件
help.download_file(url="http://...", filename="output.jpg")

# 清理文件名中的非法字符
clean_name = help.get_valid_path_name("标题/包含:非法*字符")
```

---

## 注意事项

⚠️ **法律和道德**
- 本工具仅供学习和个人使用
- 请尊重内容创作者的版权
- 不要用于商业目的或侵犯他人权益
- 遵守小红书的使用条款

⚠️ **使用限制**
- 不要频繁请求，避免IP被封
- 建议检查间隔不少于5分钟
- 使用合理的重试策略
- 注意存储空间，视频文件较大

⚠️ **隐私安全**
- 妥善保管cookie，不要泄露
- 定期更新cookie
- 不要在公共场合使用
- 配置文件不要提交到代码仓库

---

## 更新日志

### v1.0.0 (2024-01-15)
- ✨ 初始版本发布
- ✅ 支持用户笔记监控
- ✅ 支持图片和视频自动下载
- ✅ 支持元数据保存
- ✅ 支持防重复下载

---

## 贡献指南

欢迎提交Issue和Pull Request！

如果你有好的想法或发现了bug，请：
1. Fork这个项目
2. 创建你的特性分支
3. 提交你的改动
4. 推送到分支
5. 创建Pull Request

---

## 许可证

本项目遵循原项目的许可证。

---

## 联系方式

- 项目主页：https://github.com/ReaJason/xhs
- 文档：https://reajason.github.io/xhs/

---

**祝使用愉快！如有问题，欢迎提Issue！** 🎉
