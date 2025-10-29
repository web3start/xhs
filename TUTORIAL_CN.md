# 小红书笔记监控完整教程
 
## 目录
- [项目介绍](#项目介绍)
- [环境准备](#环境准备)
- [获取必要信息](#获取必要信息)
- [基础使用](#基础使用)
- [监控功能详解](#监控功能详解)
- [实战案例](#实战案例)
- [疑难解答](#疑难解答)
 
---
 
## 项目介绍
 
### 什么是xhs？
 
`xhs` 是一个用于小红书数据爬取的Python工具包，可以：
 
- 📝 获取笔记详细信息
- 👤 获取用户信息
- 🔍 搜索笔记和用户
- 📥 下载图片和视频
- 💬 获取评论信息
- ⭐ 点赞、收藏、关注等互动操作
 
### 监控功能介绍
 
基于xhs包，我们开发了自动监控工具，可以：
 
1. **定时检查**：按设定的时间间隔检查用户是否发布新笔记
2. **自动下载**：发现新笔记后自动下载图片/视频到本地
3. **元数据保存**：保存笔记标题、描述、标签、互动数据等信息
4. **智能去重**：自动记录已下载的笔记，避免重复下载
5. **持续运行**：可以作为后台服务持续运行
 
---
 
## 环境准备
 
### 1. 系统要求
 
- Python 3.7 或更高版本
- 支持 Windows、macOS、Linux
 
### 2. 安装Python包
 
```bash
# 方式一：从PyPI安装（推荐）
pip install xhs
# 方式二：从源码安装（开发版）
git clone https://github.com/ReaJason/xhs.git
cd xhs
pip install -e .
```
 
### 3. 安装Playwright
 
Playwright用于生成请求签名：
 
```bash
pip install playwright
playwright install chromium
```
 
如果下载失败，可以使用国内镜像：
 
```bash
# 设置环境变量
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
# 然后安装
playwright install chromium
```
 
### 4. 验证安装
 
```bash
python -c "import xhs; print('xhs安装成功')"
python -c "from playwright.sync_api import sync_playwright; print('playwright安装成功')"
```
 
---
 
## 获取必要信息
 
### 步骤1：获取Cookie
 
Cookie是访问小红书的凭证，需要从浏览器中获取。
 
#### 方法一：Chrome浏览器
 
1. 打开Chrome浏览器
2. 访问 https://www.xiaohongshu.com
3. 登录你的小红书账号
4. 按 `F12` 打开开发者工具
5. 点击顶部的 `Network`（网络）标签
6. 按 `F5` 刷新页面
7. 在左侧列表中点击任意请求（通常点击第一个）
8. 在右侧找到 `Request Headers`（请求标头）
9. 向下滚动找到 `Cookie` 字段
10. 右键点击Cookie值，选择 `Copy value`（复制值）
 
#### 方法二：Firefox浏览器
 
1. 打开Firefox浏览器
2. 访问 https://www.xiaohongshu.com
3. 登录你的小红书账号
4. 按 `F12` 打开开发者工具
5. 点击 `网络` 标签
6. 刷新页面
7. 点击任意请求
8. 在右侧 `标头` 中找到 `Cookie`
9. 复制完整的Cookie值
 
#### Cookie示例
 
Cookie类似这样（很长的一串）：
 
```
a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043; webId=ba57f42593b9e55840a289fa0b755374; gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy; ...
```
 
**重要提示：**
- Cookie包含你的登录信息，请妥善保管
- 不要在公开场合分享你的Cookie
- Cookie会过期，需要定期更新
 
### 步骤2：获取用户ID
 
用户ID是用户的唯一标识。
 
#### 获取方法
 
1. 访问你想监控的用户主页
2. 查看浏览器地址栏的URL
3. URL格式为：`https://www.xiaohongshu.com/user/profile/用户ID`
 
**示例：**
 
```
URL: https://www.xiaohongshu.com/user/profile/5b3f8c8e0000000001000a1b
                                                   └──────┬──────┘
                                                       用户ID
```
 
用户ID就是：`5b3f8c8e0000000001000a1b`
 
#### 其他获取方式
 
**从分享链接：**
1. 在小红书App中打开用户主页
2. 点击右上角分享
3. 复制链接
4. 在浏览器中打开链接
5. 从URL中提取用户ID
 
### 步骤3：（可选）下载stealth.js
 
stealth.js可以防止被检测为自动化工具。
 
**下载地址：**
https://github.com/requireCool/stealth.min.js/blob/main/stealth.min.js
 
下载后放在项目目录下。
 
**注意：** 即使不下载此文件，程序也能正常运行，只是可能更容易被检测。
 
---
 
## 基础使用
 
### 方式一：使用完整监控工具（推荐）
 
#### 1. 进入示例目录
 
```bash
cd example
```
 
#### 2. 首次运行生成配置文件
 
```bash
python monitor_user_notes.py
```
 
会自动生成 `monitor_config.json` 文件：
 
```json
{
    "cookie": "your_cookie_here",
    "user_id": "target_user_id_here",
    "download_dir": "./downloads",
    "check_interval": 300,
    "stealth_js_path": "./stealth.min.js",
    "use_headless": true,
    "max_retries": 3,
    "retry_delay": 2,
    "downloaded_notes_file": "downloaded_notes.json"
}
```
 
#### 3. 编辑配置文件
 
用文本编辑器打开 `monitor_config.json`，修改：
 
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
 
**配置说明：**
 
| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| cookie | 你的小红书cookie | 必填 |
| user_id | 要监控的用户ID | 必填 |
| download_dir | 下载保存目录 | ./downloads |
| check_interval | 检查间隔（秒） | 300 (5分钟) |
| stealth_js_path | stealth.js路径 | ./stealth.min.js |
| use_headless | 是否无头模式 | true |
| max_retries | 最大重试次数 | 3 |
| retry_delay | 重试延迟（秒） | 2 |
#### 4. 启动监控
 
```bash
python monitor_user_notes.py
```
 
**输出示例：**
 
```
==============================================================
🚀 小红书笔记监控器启动
==============================================================
配置文件: monitor_config.json
监控用户: 5b3f8c8e0000000001000a1b
检查间隔: 300 秒
下载目录: ./downloads
已下载笔记数: 0
==============================================================
✅ 小红书客户端初始化成功
==============================================================
🔍 检查新笔记 - 2024-01-15 10:30:00
==============================================================
📋 正在获取用户 5b3f8c8e0000000001000a1b 的笔记列表...
   已获取 30 条笔记...
✅ 共获取 30 条笔记
🎉 发现 3 条新笔记！
[1/3] 
📥 开始下载笔记: 6505318c000000001f03c5a6
   标题: 冬日穿搭分享
   类型: normal
   正在下载 3 张图片...
   ✅ 图片 1/3 已保存
   ✅ 图片 2/3 已保存
   ✅ 图片 3/3 已保存
✅ 笔记 6505318c000000001f03c5a6 下载完成
[2/3] 
...
✅ 成功下载 3/3 条新笔记
⏰ 下次检查时间: 2024-01-15 10:35:00
💤 等待 300 秒...
```
 
#### 5. 停止监控
 
按 `Ctrl+C` 停止程序。
 
### 方式二：使用快速示例
 
如果你想快速上手或学习代码，可以使用简化版：
 
#### 1. 编辑快速示例文件
 
打开 `example/quick_monitor_example.py`，找到配置部分：
 
```python
# ============ 在这里修改配置 ============
# 1. 你的小红书cookie（必填）
COOKIE = "your_cookie_here"
# 2. 要监控的用户ID（必填）
USER_ID = "target_user_id_here"
# 3. 下载保存目录（可选）
DOWNLOAD_DIR = "./downloads"
# 4. 检查间隔秒数（可选，建议不少于300秒）
CHECK_INTERVAL = 300  # 5分钟
# ========================================
```
 
修改为你的实际值：
 
```python
COOKIE = "a1=187d2defea8dz1fg..."
USER_ID = "5b3f8c8e0000000001000a1b"
DOWNLOAD_DIR = "./downloads"
CHECK_INTERVAL = 300
```
 
#### 2. 运行
 
```bash
cd example
python quick_monitor_example.py
```
 
### 方式三：编写自己的脚本
 
你也可以基于xhs包编写自己的监控脚本：
 
```python
from xhs import XhsClient
from playwright.sync_api import sync_playwright
# 定义签名函数
def sign(uri, data=None, a1="", web_session=""):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.xiaohongshu.com")
        # ... 签名逻辑
        return {"x-s": "...", "x-t": "..."}
# 初始化客户端
client = XhsClient(cookie="你的cookie", sign=sign)
# 获取用户笔记
result = client.get_user_notes(user_id="用户ID")
notes = result.get("notes", [])
# 遍历笔记
for note in notes:
    note_id = note.get("note_id")
    # 获取笔记详情
    detail = client.get_note_by_id(note_id, note.get("xsec_token"))
    # 处理笔记...
```
 
---
 
## 监控功能详解
 
### 配置文件详解
 
#### cookie
 
**说明：** 你的小红书登录凭证
 
**获取方法：** 见上文"获取必要信息"部分
 
**示例：**
```json
"cookie": "a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043; webId=ba57f42593b9e55840a289fa0b755374; ..."
```
 
**注意事项：**
- Cookie会过期，通常1-2周需要更新一次
- 如果遇到登录错误，首先尝试更新Cookie
- 不同账号的Cookie不同
 
#### user_id
 
**说明：** 要监控的用户的唯一标识
 
**获取方法：** 从用户主页URL获取
 
**示例：**
```json
"user_id": "5b3f8c8e0000000001000a1b"
```
 
**注意事项：**
- 用户ID是固定的，不会变化
- 可以监控任何公开账号
- 私密账号需要你已关注才能获取笔记
 
#### download_dir
 
**说明：** 笔记下载保存的目录
 
**默认值：** `"./downloads"`
 
**示例：**
```json
"download_dir": "/Users/username/Downloads/xhs_notes"
```
 
**目录结构：**
```
downloads/
├── 笔记标题1_笔记ID1_时间戳/
│   ├── metadata.json
│   ├── 笔记标题1_1.png
│   └── 笔记标题1_2.png
├── 笔记标题2_笔记ID2_时间戳/
│   ├── metadata.json
│   └── 笔记标题2.mp4
└── ...
```
 
#### check_interval
 
**说明：** 检查新笔记的时间间隔（秒）
 
**默认值：** `300` (5分钟)
 
**建议值：**
- 日常监控：300-600秒（5-10分钟）
- 重要监控：180-300秒（3-5分钟）
- 不建议低于60秒，容易被限制
 
**示例：**
```json
"check_interval": 300
```
 
#### use_headless
 
**说明：** 是否使用无头浏览器模式
 
**默认值：** `true`
 
**说明：**
- `true`: 后台运行，不显示浏览器窗口（推荐）
- `false`: 显示浏览器窗口，可以看到签名过程
 
**何时设为false：**
- 调试签名问题时
- 想了解签名过程时
- 签名经常失败时
 
**示例：**
```json
"use_headless": true
```
 
#### max_retries
 
**说明：** 请求失败时的最大重试次数
 
**默认值：** `3`
 
**建议值：** 2-5
 
**示例：**
```json
"max_retries": 3
```
 
#### retry_delay
 
**说明：** 重试之间的延迟时间（秒）
 
**默认值：** `2`
 
**建议值：** 1-5
 
**示例：**
```json
"retry_delay": 2
```
 
### 下载的文件说明
 
#### metadata.json
 
每个笔记都会保存一个metadata.json文件，包含：
 
```json
{
    "note_id": "6505318c000000001f03c5a6",
    "title": "冬日穿搭分享",
    "desc": "今天分享一套简约的冬日穿搭...",
    "type": "normal",
    "user": {
        "user_id": "5b3f8c8e0000000001000a1b",
        "nickname": "时尚博主",
        "avatar": "https://..."
    },
    "tags": [
        {"name": "穿搭", "type": "topic"},
        {"name": "冬日", "type": "topic"}
    ],
    "interact_info": {
        "liked_count": "1234",
        "collected_count": "567",
        "comment_count": "89",
        "share_count": "12"
    },
    "download_time": "2024-01-15T10:30:00.123456",
    "xsec_token": "..."
}
```
 
**用途：**
- 记录笔记的详细信息
- 用于数据分析
- 便于搜索和管理
- 可导入数据库
 
#### 图片文件
 
- 格式：PNG
- 命名：`笔记标题_序号.png`
- 按原图质量保存
 
#### 视频文件
 
- 格式：MP4
- 命名：`笔记标题.mp4`
- 原始清晰度
 
### 已下载笔记记录
 
#### downloaded_notes.json
 
记录已下载的笔记，避免重复下载：
 
```json
{
    "note_ids": [
        "6505318c000000001f03c5a6",
        "6505318d000000001f03c5b7",
        "6505318e000000001f03c5c8"
    ],
    "notes_metadata": {
        "6505318c000000001f03c5a6": {
            "title": "冬日穿搭分享",
            "download_time": "2024-01-15T10:30:00.123456",
            "download_path": "./downloads/冬日穿搭分享_6505318c000000001f03c5a6_20240115_103000",
            "type": "normal"
        },
        ...
    }
}
```
 
**重要说明：**
- 删除此文件会重新下载所有笔记
- 可以手动编辑跳过某些笔记
- 定期备份此文件
 
---
 
## 实战案例
 
### 案例1：监控时尚博主的每日穿搭
 
**需求：** 每天早上9点检查博主是否发布新穿搭
 
**配置：**
```json
{
    "cookie": "你的cookie",
    "user_id": "博主的user_id",
    "download_dir": "./fashion_daily",
    "check_interval": 3600,
    "use_headless": true,
    "max_retries": 3,
    "retry_delay": 2,
    "downloaded_notes_file": "fashion_downloaded.json"
}
```
 
**运行方式：**
 
使用Cron定时任务：
```bash
# 编辑crontab
crontab -e
# 添加任务：每天早上9点执行
0 9 * * * cd /path/to/xhs/example && python monitor_user_notes.py --once --config fashion_config.json
```
 
### 案例2：监控多个美食博主
 
**需求：** 同时监控5个美食博主，发现新笔记就下载
 
**方案：** 创建多个配置文件，用进程管理工具运行
 
**步骤：**
 
1. 创建配置文件：
   - `food_blogger1.json`
   - `food_blogger2.json`
   - `food_blogger3.json`
   - `food_blogger4.json`
   - `food_blogger5.json`
 
2. 创建启动脚本 `start_multi_monitor.sh`：
 
```bash
#!/bin/bash
# 后台运行多个监控实例
python monitor_user_notes.py --config food_blogger1.json > logs/blogger1.log 2>&1 &
python monitor_user_notes.py --config food_blogger2.json > logs/blogger2.log 2>&1 &
python monitor_user_notes.py --config food_blogger3.json > logs/blogger3.log 2>&1 &
python monitor_user_notes.py --config food_blogger4.json > logs/blogger4.log 2>&1 &
python monitor_user_notes.py --config food_blogger5.json > logs/blogger5.log 2>&1 &
echo "所有监控已启动"
```
 
3. 创建停止脚本 `stop_multi_monitor.sh`：
 
```bash
#!/bin/bash
# 停止所有监控进程
pkill -f "monitor_user_notes.py"
echo "所有监控已停止"
```
 
4. 运行：
 
```bash
chmod +x start_multi_monitor.sh
chmod +x stop_multi_monitor.sh
./start_multi_monitor.sh
```
 
### 案例3：构建个人笔记数据库
 
**需求：** 定期备份喜欢的博主的所有笔记，用于个人收藏
 
**方案：** 使用单次检查模式 + 数据库存储
 
**代码示例：**
 
```python
import sqlite3
import json
from monitor_user_notes import NoteMonitor
# 初始化数据库
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    note_id TEXT PRIMARY KEY,
    title TEXT,
    desc TEXT,
    type TEXT,
    user_id TEXT,
    nickname TEXT,
    liked_count INTEGER,
    collected_count INTEGER,
    comment_count INTEGER,
    download_time TEXT,
    file_path TEXT
)
''')
# 运行监控
monitor = NoteMonitor('config.json')
monitor.run_once()
# 将下载的笔记信息存入数据库
with open('downloaded_notes.json', 'r') as f:
    data = json.load(f)
for note_id, metadata in data['notes_metadata'].items():
    cursor.execute('''
    INSERT OR REPLACE INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        note_id,
        metadata.get('title'),
        # ... 其他字段
    ))
conn.commit()
conn.close()
```
 
### 案例4：实时通知新笔记
 
**需求：** 博主发布新笔记时，立即发送微信/邮件通知
 
**方案：** 在监控脚本中添加通知功能
 
**修改 monitor_user_notes.py：**
 
在 `check_new_notes` 方法中添加：
 
```python
def send_notification(self, new_notes):
    """发送通知"""
    message = f"发现 {len(new_notes)} 条新笔记！\n\n"
    
    for note in new_notes[:5]:  # 只显示前5条
        message += f"- {note.get('display_title', '无标题')}\n"
    
    # 方式1：发送邮件
    self.send_email(message)
    
    # 方式2：发送到Server酱（微信通知）
    self.send_serverchan(message)
    
    # 方式3：发送到Telegram
    self.send_telegram(message)
def send_email(self, message):
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText(message)
    msg['Subject'] = '小红书新笔记通知'
    msg['From'] = 'your@email.com'
    msg['To'] = 'to@email.com'
    
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('your@email.com', 'password')
    smtp.send_message(msg)
    smtp.quit()
def send_serverchan(self, message):
    import requests
    
    sckey = "你的ServerChan密钥"
    url = f"https://sctapi.ftqq.com/{sckey}.send"
    
    requests.post(url, data={
        "title": "小红书新笔记",
        "desp": message
    })
```
 
然后在 `check_new_notes` 中调用：
 
```python
if new_notes:
    print(f"\n🎉 发现 {len(new_notes)} 条新笔记！")
    self.send_notification(new_notes)  # 发送通知
    # ... 下载笔记
```
 
---
 
## 疑难解答
 
### 问题1：签名失败
 
**错误信息：**
```
window._webmsxyw is not a function
```
 
**可能原因：**
1. Playwright未正确安装
2. 网页加载太慢
3. 网站更新了签名机制
 
**解决方法：**
 
**方法1：** 增加等待时间
```python
# 在 sign 函数中
sleep(3)  # 从1秒增加到3秒
```
 
**方法2：** 使用可见浏览器调试
```json
{
    "use_headless": false
}
```
 
**方法3：** 重新安装Playwright
```bash
pip uninstall playwright
pip install playwright
playwright install chromium
```
 
**方法4：** 检查网络连接
```bash
ping www.xiaohongshu.com
```
 
### 问题2：Cookie失效
 
**错误信息：**
```
需要登录
未授权访问
```
 
**解决方法：**
 
1. 重新获取Cookie
2. 确保Cookie完整（包含a1、webId等）
3. 检查是否被账号被限制
 
**预防措施：**
- 定期更新Cookie（建议每周一次）
- 不要在多个设备同时使用同一账号
- 避免频繁请求
 
### 问题3：下载失败
 
**错误信息：**
```
下载文件失败
网络错误
```
 
**可能原因：**
1. 网络不稳定
2. CDN访问受限
3. 文件已被删除
 
**解决方法：**
 
**方法1：** 使用代理
```python
xhs_client = XhsClient(
    cookie=cookie,
    sign=sign,
    proxies={
        'http': 'http://proxy:port',
        'https': 'http://proxy:port'
    }
)
```
 
**方法2：** 增加重试
```json
{
    "max_retries": 5,
    "retry_delay": 5
}
```
 
**方法3：** 检查网络
```bash
curl -I https://sns-img-qc.xhscdn.com
```
 
### 问题4：内存占用过高
 
**现象：** 长时间运行后内存占用越来越高
 
**原因：** 浏览器实例未正确关闭
 
**解决方法：**
 
确保在sign函数中关闭浏览器：
 
```python
def sign(self, uri, data=None, a1="", web_session=""):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            # ... 签名逻辑
            return result
        finally:
            browser.close()  # 确保关闭
```
 
### 问题5：磁盘空间不足
 
**原因：** 下载的视频文件占用大量空间
 
**解决方法：**
 
**方法1：** 定期清理
```bash
# 删除30天前的笔记
find ./downloads -type d -mtime +30 -exec rm -rf {} \;
```
 
**方法2：** 只下载图片
```python
# 修改代码，跳过视频
if note_type == "video":
    print("跳过视频笔记")
    return
```
 
**方法3：** 使用压缩
```bash
# 压缩下载的图片
find ./downloads -name "*.png" -exec convert {} -quality 85 {} \;
```
 
### 问题6：被检测为机器人
 
**错误信息：**
```
需要验证
滑动验证
```
 
**原因：** 请求频率过高或行为异常
 
**解决方法：**
 
1. 降低检查频率
```json
{
    "check_interval": 600  # 增加到10分钟
}
```
 
2. 使用stealth.js
```json
{
    "stealth_js_path": "./stealth.min.js"
}
```
 
3. 添加随机延迟
```python
import random
time.sleep(random.uniform(1, 3))
```
 
4. 使用住宅代理IP
 
5. 等待一段时间（24小时）后重试
 
### 问题7：找不到用户笔记
 
**错误信息：**
```
用户笔记为空
未找到笔记
```
 
**可能原因：**
1. 用户ID错误
2. 用户设置了隐私
3. 用户未发布笔记
 
**解决方法：**
 
1. 验证用户ID
```python
user_info = client.get_user_info(user_id)
print(user_info)
```
 
2. 检查用户主页是否可访问
 
3. 确认是否需要关注后才能看
 
### 问题8：程序意外退出
 
**原因分析：**
- 异常未捕获
- 系统资源不足
- 网络长时间断开
 
**解决方法：**
 
使用进程守护工具：
 
**Linux - systemd：**
 
创建 `/etc/systemd/system/xhs-monitor.service`：
 
```ini
[Unit]
Description=XHS Note Monitor
After=network.target
[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/xhs/example
ExecStart=/usr/bin/python3 monitor_user_notes.py
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
```
 
启动：
```bash
sudo systemctl enable xhs-monitor
sudo systemctl start xhs-monitor
sudo systemctl status xhs-monitor
```
 
**Linux - Supervisor：**
 
```ini
[program:xhs-monitor]
command=python monitor_user_notes.py
directory=/path/to/xhs/example
autostart=true
autorestart=true
```
 
**Windows - NSSM：**
 
```bash
nssm install xhs-monitor "C:\Python\python.exe" "C:\path\to\monitor_user_notes.py"
nssm start xhs-monitor
```
 
---
 
## 高级技巧
 
### 1. 性能优化
 
**并发下载：**
 
```python
from concurrent.futures import ThreadPoolExecutor
def download_notes_concurrent(self, notes):
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(self.download_note, notes)
```
 
**缓存机制：**
 
```python
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_note_cached(self, note_id):
    return self.xhs_client.get_note_by_id(note_id)
```
 
### 2. 数据分析
 
**统计笔记数据：**
 
```python
import pandas as pd
import json
# 读取元数据
with open('downloaded_notes.json', 'r') as f:
    data = json.load(f)
# 转换为DataFrame
df = pd.DataFrame(data['notes_metadata'].values())
# 分析
print(df['type'].value_counts())  # 笔记类型分布
print(df.groupby('type').size())  # 按类型统计
```
 
### 3. 云端部署
 
**部署到云服务器：**
 
```bash
# 1. 连接服务器
ssh user@your-server.com
# 2. 安装依赖
pip install xhs playwright
playwright install chromium
# 3. 上传代码
scp -r xhs user@your-server.com:~/
# 4. 后台运行
nohup python monitor_user_notes.py > monitor.log 2>&1 &
```
 
### 4. 自动化运维
 
**日志监控：**
 
```python
import logging
logging.basicConfig(
    filename='monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("开始监控")
```
 
**错误告警：**
 
```python
def alert_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            send_alert(f"错误: {e}")
            raise
    return wrapper
```
 
---
 
## 总结
 
通过本教程，你应该能够：
 
✅ 理解xhs项目的基本原理  
✅ 成功配置和运行笔记监控工具  
✅ 解决常见问题  
✅ 根据需求定制功能  
 
**下一步建议：**
 
1. 阅读[API文档](https://reajason.github.io/xhs/)了解更多功能
2. 查看[源代码](https://github.com/ReaJason/xhs)学习实现细节
3. 加入社区讨论和交流经验
 
**注意事项：**
 
⚠️ 请遵守法律法规和网站使用条款  
⚠️ 合理控制请求频率  
⚠️ 尊重内容创作者版权  
⚠️ 仅供学习和个人使用  
 
祝使用愉快！🎉
