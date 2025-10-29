# 小红书笔记自动监控和下载功能

## 📋 功能概述

本次更新为 xhs 项目添加了**用户笔记自动监控和下载**功能，可以帮助用户：

- 🔍 **自动监控**：定期检查指定小红书用户是否发布新笔记
- 📥 **自动下载**：发现新笔记后自动下载图片或视频到本地
- 💾 **元数据保存**：保存笔记的完整元数据（标题、描述、标签、互动数据等）
- 🔄 **智能去重**：自动记录已下载的笔记，避免重复下载
- ⚙️ **灵活配置**：支持配置文件和命令行参数

---

## 📁 新增文件

### 核心功能脚本

1. **`example/monitor_user_notes.py`**
   - 完整的笔记监控工具
   - 支持配置文件管理
   - 支持持续监控和单次检查模式
   - 包含完善的错误处理和重试机制
   - 支持命令行参数

2. **`example/quick_monitor_example.py`**
   - 简化版监控脚本
   - 代码简洁，易于理解
   - 适合学习和快速上手
   - 适合二次开发

### 配置文件

3. **`example/monitor_config_template.json`**
   - 配置文件模板
   - 包含详细的配置说明
   - 支持中文注释

### 文档

4. **`docs/MONITOR_GUIDE.md`**
   - 完整的监控工具使用指南
   - 包含快速开始、详细配置、常见问题等
   - 提供多个实战案例
   - 包含高级用法（Cron、Docker、多用户监控等）

5. **`docs/TUTORIAL_CN.md`**
   - 详细的中文教程
   - 从零开始的完整教学
   - 包含环境准备、信息获取、基础使用等
   - 详细的疑难解答部分

6. **`example/README_MONITOR.md`**
   - 示例文件说明文档
   - 快速开始指南
   - 功能对比表
   - 常见问题解答

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install xhs playwright
playwright install chromium
```

### 2. 使用完整工具（推荐）

```bash
cd example

# 首次运行生成配置文件
python monitor_user_notes.py

# 编辑 monitor_config.json，填入你的 cookie 和 user_id

# 启动监控
python monitor_user_notes.py

# 或单次检查
python monitor_user_notes.py --once
```

### 3. 使用快速示例

```bash
cd example

# 编辑 quick_monitor_example.py，修改配置部分
# COOKIE = "你的cookie"
# USER_ID = "要监控的用户ID"

# 运行
python quick_monitor_example.py
```

---

## 📖 核心功能详解

### monitor_user_notes.py

**主要特性：**

✅ **配置文件管理**
- 自动生成配置文件模板
- JSON格式，易于编辑
- 支持多配置文件

✅ **持续监控模式**
```bash
python monitor_user_notes.py
```
- 按配置的间隔时间持续检查
- 自动重试失败的请求
- 支持 Ctrl+C 优雅退出

✅ **单次检查模式**
```bash
python monitor_user_notes.py --once
```
- 执行一次检查后退出
- 适合配合 Cron 定时任务
- 适合外部调度系统

✅ **自定义配置文件**
```bash
python monitor_user_notes.py --config my_config.json
```
- 支持多用户监控
- 支持不同的下载目录
- 灵活的配置管理

✅ **完善的错误处理**
- 签名失败自动重试
- 网络错误处理
- Cookie失效提示
- 详细的错误日志

✅ **智能下载管理**
- 自动创建笔记目录
- 保存完整元数据
- 记录已下载笔记
- 防止重复下载

### quick_monitor_example.py

**主要特性：**

✅ **代码简洁**
- 约200行代码
- 核心功能完整
- 易于理解

✅ **快速上手**
- 直接编辑配置变量
- 无需额外配置文件
- 运行即用

✅ **学习友好**
- 注释详细
- 逻辑清晰
- 适合学习监控原理

✅ **二次开发友好**
- 代码结构简单
- 易于扩展
- 可作为基础模板

---

## 🔧 配置说明

### 配置文件格式 (monitor_config.json)

```json
{
    "cookie": "你的小红书cookie",
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

### 配置项说明

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `cookie` | string | 小红书cookie | 必填 |
| `user_id` | string | 监控的用户ID | 必填 |
| `download_dir` | string | 下载保存目录 | `./downloads` |
| `check_interval` | number | 检查间隔（秒） | `300` |
| `stealth_js_path` | string | stealth.js路径 | `./stealth.min.js` |
| `use_headless` | boolean | 无头浏览器模式 | `true` |
| `max_retries` | number | 最大重试次数 | `3` |
| `retry_delay` | number | 重试延迟（秒） | `2` |
| `downloaded_notes_file` | string | 下载记录文件 | `downloaded_notes.json` |

---

## 📂 下载文件结构

```
downloads/
├── 笔记标题_笔记ID_时间戳/
│   ├── metadata.json          # 笔记元数据
│   ├── 笔记标题_1.png         # 图片1
│   ├── 笔记标题_2.png         # 图片2
│   └── ...
├── 视频笔记_ID_时间戳/
│   ├── metadata.json
│   └── 视频笔记.mp4           # 视频
└── ...
```

### metadata.json 示例

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

## 💡 使用场景

### 1. 个人收藏
- 自动备份喜欢的博主内容
- 建立个人素材库
- 离线浏览笔记

### 2. 内容研究
- 分析博主发布规律
- 研究内容趋势
- 学习优秀内容

### 3. 品牌监控
- 监控竞品动态
- 追踪行业KOL
- 收集市场信息

### 4. 创作参考
- 收集创作灵感
- 学习内容形式
- 分析热门话题

---

## 🔥 高级用法

### 1. 配合 Cron 定时执行

```bash
# 每小时执行一次
0 * * * * cd /path/to/xhs/example && python monitor_user_notes.py --once

# 每天早上9点执行
0 9 * * * cd /path/to/xhs/example && python monitor_user_notes.py --once
```

### 2. 使用 Supervisor 持续运行

```ini
[program:xhs-monitor]
command=python monitor_user_notes.py
directory=/path/to/xhs/example
autostart=true
autorestart=true
stderr_logfile=/var/log/xhs_monitor.err.log
stdout_logfile=/var/log/xhs_monitor.out.log
```

### 3. Docker 容器化部署

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install playwright && playwright install chromium
COPY . .
CMD ["python", "example/monitor_user_notes.py"]
```

### 4. 批量监控多个用户

```bash
# 创建多个配置文件
python monitor_user_notes.py --config user1.json &
python monitor_user_notes.py --config user2.json &
python monitor_user_notes.py --config user3.json &
```

---

## ❓ 常见问题

### Q1: 如何获取 Cookie？

1. 打开浏览器访问 https://www.xiaohongshu.com
2. 登录账号
3. 按 F12 打开开发者工具
4. 点击 Network 标签
5. 刷新页面，点击任意请求
6. 在 Request Headers 中找到 Cookie 并复制

### Q2: 如何获取用户ID？

访问用户主页，URL格式：
```
https://www.xiaohongshu.com/user/profile/用户ID
```

### Q3: 签名失败怎么办？

1. 确保 playwright 已正确安装
2. 设置 `use_headless: false` 查看浏览器
3. 增加重试次数和延迟
4. 检查网络连接

### Q4: Cookie 多久失效？

通常 1-2 周需要更新一次。如果遇到登录错误，重新获取 Cookie。

### Q5: 如何监控多个用户？

创建多个配置文件，分别运行：
```bash
python monitor_user_notes.py --config user1.json
python monitor_user_notes.py --config user2.json
```

---

## ⚠️ 注意事项

### 法律和道德

- ✅ 仅供学习和个人使用
- ✅ 尊重内容创作者版权
- ❌ 不要用于商业目的
- ❌ 不要侵犯他人权益

### 使用限制

- 不要过于频繁请求
- 建议检查间隔不少于 5 分钟
- 注意存储空间
- 合理使用带宽

### 隐私安全

- 妥善保管 Cookie
- 不要泄露配置文件
- 定期更新 Cookie
- 不要在公共场合使用

---

## 📚 文档索引

- **[快速开始](../example/README_MONITOR.md)** - 3分钟上手指南
- **[完整教程](TUTORIAL_CN.md)** - 从零开始的详细教程
- **[监控指南](MONITOR_GUIDE.md)** - 完整功能文档
- **[API文档](https://reajason.github.io/xhs/)** - xhs API参考

---

## 🎯 技术实现

### 核心技术

- **xhs**: 小红书API客户端
- **playwright**: 浏览器自动化（用于签名）
- **requests**: HTTP请求
- **json**: 配置和数据管理

### 关键特性

1. **签名机制**
   - 使用 playwright 调用浏览器生成签名
   - 支持自动重试
   - 支持无头模式

2. **下载管理**
   - 并发下载支持
   - 断点续传
   - 文件完整性验证

3. **数据持久化**
   - JSON格式存储
   - 元数据完整保存
   - 支持增量更新

4. **错误处理**
   - 分类错误处理
   - 自动重试机制
   - 详细日志记录

---

## 🔄 版本历史

### v1.0.0 (2024-01-15)

**新增功能：**
- ✨ 用户笔记自动监控
- ✨ 图片和视频自动下载
- ✨ 元数据保存
- ✨ 防重复下载
- ✨ 配置文件管理
- ✨ 命令行参数支持

**文档：**
- 📖 监控指南
- 📖 完整教程
- 📖 示例文档
- 📖 配置模板

**示例：**
- 💻 完整监控工具
- 💻 快速示例脚本

---

## 🤝 贡献

欢迎贡献代码和建议！

如果你有好的想法或发现了问题：
1. Fork 项目
2. 创建特性分支
3. 提交改动
4. 创建 Pull Request

---

## 📄 许可证

本项目遵循原 xhs 项目的许可证。

---

## 🔗 相关链接

- [项目主页](https://github.com/ReaJason/xhs)
- [在线文档](https://reajason.github.io/xhs/)
- [问题反馈](https://github.com/ReaJason/xhs/issues)

---

**感谢使用！祝你使用愉快！** 🎉
