# 小红书笔记监控器 - 快速开始

## 简介

这个工具可以自动监控指定小红书用户的新笔记，并自动下载到本地。

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 包
pip install -r ../requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 2. 配置

首次运行会自动创建配置文件模板：

```bash
python monitor_user_notes.py
```

然后编辑 `monitor_config.json`：

```json
{
  "cookie": "你的小红书 Cookie",
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

#### 如何获取 Cookie:

1. 打开浏览器，登录小红书网页版 (https://www.xiaohongshu.com)
2. 按 F12 打开开发者工具
3. 切换到 "Network" (网络) 标签
4. 刷新页面或点击任意链接
5. 找到任意请求，在 "Request Headers" 中找到 "Cookie" 
6. 复制整个 Cookie 值

#### 如何获取 user_id:

访问用户主页，URL 格式为:
```
https://www.xiaohongshu.com/user/profile/[用户ID]
```

例如: `https://www.xiaohongshu.com/user/profile/5657d81c7c5bb814405de598`

用户ID就是: `5657d81c7c5bb814405de598`

### 3. 运行

#### 持续监控模式（推荐）

```bash
python monitor_user_notes.py
```

程序会按配置的间隔持续检查新笔记。

#### 单次检查模式

```bash
python monitor_user_notes.py --once
```

只检查一次，然后退出。适合测试配置。

#### 使用自定义配置文件

```bash
python monitor_user_notes.py --config my_config.json
```

### 4. 停止监控

在持续监控模式下，按 `Ctrl+C` 停止。

## 故障排查

### 如果程序卡住不动

1. **运行诊断工具**
   ```bash
   python test_sign.py
   ```

2. **查看详细故障排查指南**
   ```bash
   cat MONITOR_TROUBLESHOOTING.md
   ```
   或在浏览器中打开该文件。

### 常见问题

**Q: 提示 "签名失败"**
```
A: 
1. 确保已安装 Playwright: pip install playwright
2. 安装浏览器: playwright install chromium
3. 检查网络连接
4. 运行 test_sign.py 诊断
```

**Q: 提示 "Cookie 无效"**
```
A:
1. Cookie 可能已过期，重新获取
2. 确保 Cookie 完整（包含 a1, web_session 等）
3. 确保已登录小红书网页版
```

**Q: 找不到新笔记**
```
A:
1. 确认 user_id 正确
2. 确认该用户确实发布了新笔记
3. 检查 downloaded_notes.json，看是否已记录为已下载
```

**Q: 下载失败**
```
A:
1. 检查网络连接
2. 检查磁盘空间
3. 确认 download_dir 目录有写权限
```

## 高级用法

### 监控多个用户

创建多个配置文件，分别运行：

```bash
# 终端 1
python monitor_user_notes.py --config user1_config.json

# 终端 2  
python monitor_user_notes.py --config user2_config.json
```

### 后台运行（Linux/Mac）

```bash
nohup python monitor_user_notes.py > monitor.log 2>&1 &
```

查看日志:
```bash
tail -f monitor.log
```

停止:
```bash
ps aux | grep monitor_user_notes
kill [PID]
```

### 定时任务（cron）

如果不想持续运行，可以用 cron 定时执行单次检查：

```bash
# 编辑 crontab
crontab -e

# 添加一行（每 5 分钟执行一次）
*/5 * * * * cd /path/to/example && python monitor_user_notes.py --once >> monitor.log 2>&1
```

## 配置优化

### 减少资源占用

```json
{
  "use_headless": true,       // 使用无头模式
  "check_interval": 600,      // 增加检查间隔到 10 分钟
  "max_retries": 2            // 减少重试次数
}
```

### 提高成功率

```json
{
  "use_headless": false,      // 调试时关闭无头模式
  "max_retries": 5,           // 增加重试次数
  "retry_delay": 5            // 增加重试延迟
}
```

### 使用 stealth.js（推荐）

下载 stealth.js 避免被检测：

```bash
wget https://cdn.jsdelivr.net/npm/puppeteer-extra-plugin-stealth@latest/stealth.min.js
```

然后在配置中指定路径：
```json
{
  "stealth_js_path": "./stealth.min.js"
}
```

## 输出说明

### 下载的文件结构

```
downloads/
└── 笔记标题_笔记ID_时间戳/
    ├── metadata.json          # 笔记元数据
    ├── 笔记标题_1.png         # 图片 1
    ├── 笔记标题_2.png         # 图片 2
    └── ...
```

或（视频笔记）：
```
downloads/
└── 笔记标题_笔记ID_时间戳/
    ├── metadata.json          # 笔记元数据
    └── 笔记标题.mp4           # 视频文件
```

### metadata.json 内容

```json
{
  "note_id": "笔记ID",
  "title": "笔记标题",
  "desc": "笔记描述",
  "type": "normal/video",
  "user": {
    "user_id": "用户ID",
    "nickname": "用户昵称",
    ...
  },
  "tags": ["标签1", "标签2"],
  "interact_info": {
    "liked_count": "点赞数",
    "collected_count": "收藏数",
    "comment_count": "评论数",
    ...
  },
  "download_time": "2025-01-29T12:00:00",
  "xsec_token": "..."
}
```

## 最佳实践

1. **定期更新 Cookie** - 建议每周更新一次
2. **合理设置检查间隔** - 避免频繁请求，建议 ≥ 5 分钟
3. **定期备份** - 定期备份 `downloaded_notes.json` 避免重复下载
4. **监控日志** - 定期查看日志，及时发现问题
5. **网络稳定** - 确保网络连接稳定，避免下载中断

## 获取帮助

- 遇到问题先运行: `python test_sign.py`
- 查看故障排查指南: `MONITOR_TROUBLESHOOTING.md`
- 查看示例代码: `monitor_user_notes.py`

## 注意事项

⚠️ **重要提示:**

1. 本工具仅供学习和个人使用
2. 请遵守小红书的服务条款
3. 不要频繁请求，避免对服务器造成压力
4. 下载的内容仅供个人使用，请勿传播
5. Cookie 包含敏感信息，请妥善保管

## 许可

本工具遵循项目主仓库的许可协议。
