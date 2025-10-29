# 小红书笔记监控示例

## 📁 文件说明

### 1. `monitor_user_notes.py` - 完整监控工具（推荐）

**功能最完整的监控脚本**，包含：
- ✅ 配置文件管理
- ✅ 命令行参数支持
- ✅ 失败重试机制
- ✅ 详细日志输出
- ✅ 灵活的配置选项

**使用方法：**

```bash
# 1. 首次运行，生成配置文件
python monitor_user_notes.py

# 2. 编辑 monitor_config.json，填入你的信息

# 3. 持续监控模式
python monitor_user_notes.py

# 4. 单次检查模式
python monitor_user_notes.py --once

# 5. 使用自定义配置文件
python monitor_user_notes.py --config my_config.json
```

---

### 2. `quick_monitor_example.py` - 快速入门示例

**简化版监控脚本**，代码简洁易懂，适合：
- 🎓 学习和理解监控原理
- 🚀 快速开始使用
- 🔧 基于此进行二次开发

**使用方法：**

```bash
# 1. 编辑文件，修改以下变量：
#    - COOKIE: 你的cookie
#    - USER_ID: 要监控的用户ID
#    - DOWNLOAD_DIR: 下载目录
#    - CHECK_INTERVAL: 检查间隔

# 2. 直接运行
python quick_monitor_example.py
```

---

### 3. 其他示例文件

| 文件 | 说明 |
|------|------|
| `basic_usage.py` | 基本API使用示例 |
| `basic_sign_usage.py` | 签名功能示例 |
| `basic_sign_server.py` | 签名服务器示例 |
| `login_qrcode.py` | 二维码登录示例 |
| `login_phone.py` | 手机号登录示例 |
| `login_qrcode_from_creator.py` | 创作者平台登录示例 |

---

## 🚀 快速开始（3分钟上手）

### 第一步：安装依赖

```bash
# 安装xhs包
pip install xhs

# 安装playwright
pip install playwright
playwright install chromium
```

### 第二步：获取Cookie

1. 打开浏览器访问 https://www.xiaohongshu.com
2. 登录你的账号
3. 按 `F12` 打开开发者工具
4. 点击 `Network` 标签
5. 刷新页面，点击任意请求
6. 在右侧找到 `Request Headers` → `Cookie`，复制完整内容

### 第三步：获取用户ID

访问要监控的用户主页，URL格式：
```
https://www.xiaohongshu.com/user/profile/5b3f8c8e0000000001000a1b
                                         └──────┬──────┘
                                            这就是用户ID
```

### 第四步：运行监控

**方式一：使用完整工具（推荐）**

```bash
python monitor_user_notes.py
# 首次运行会生成配置文件，编辑后再次运行
```

**方式二：使用快速示例**

```bash
# 编辑 quick_monitor_example.py，修改：
COOKIE = "你的cookie"
USER_ID = "要监控的用户ID"

# 运行
python quick_monitor_example.py
```

---

## 📖 详细文档

完整的使用指南和高级功能请查看：
- **[监控指南](../docs/MONITOR_GUIDE.md)** - 详细的监控工具文档
- **[项目文档](https://reajason.github.io/xhs/)** - API文档和更多示例

---

## 💡 功能对比

| 功能 | monitor_user_notes.py | quick_monitor_example.py |
|------|----------------------|-------------------------|
| 配置文件管理 | ✅ | ❌ |
| 命令行参数 | ✅ | ❌ |
| 失败重试 | ✅ | ⚠️ 简单重试 |
| 详细日志 | ✅ | ⚠️ 基础日志 |
| 代码复杂度 | 较高 | 简单 |
| 适合场景 | 生产使用 | 学习和开发 |

---

## 📂 下载文件结构

运行后会创建以下结构：

```
downloads/
├── 笔记标题_笔记ID_时间戳/
│   ├── metadata.json          # 笔记元数据
│   ├── 笔记标题_1.png         # 图片（图文笔记）
│   ├── 笔记标题_2.png
│   └── ...
├── 视频笔记标题_ID_时间戳/
│   ├── metadata.json
│   └── 视频笔记标题.mp4       # 视频（视频笔记）
└── ...

monitor_config.json            # 配置文件（完整工具）
downloaded_notes.json          # 已下载记录（完整工具）
downloaded_notes.json          # 已下载记录（快速示例）
```

---

## ❓ 常见问题

### Q: 签名失败怎么办？

```
错误: window._webmsxyw is not a function
```

**解决方法：**
1. 确保已安装playwright: `playwright install chromium`
2. 尝试设置 `use_headless: false` 查看浏览器
3. 增加重试次数和延迟时间
4. 检查网络连接

### Q: Cookie失效了？

**解决方法：**
重新从浏览器获取cookie并更新配置

### Q: 如何监控多个用户？

**方法一：** 创建多个配置文件分别运行
```bash
python monitor_user_notes.py --config user1.json
python monitor_user_notes.py --config user2.json
```

**方法二：** 修改代码支持多用户（参考详细文档）

### Q: 下载速度慢？

这是为了避免被限制而设置的延迟，建议不要修改。

---

## ⚠️ 注意事项

1. **请遵守法律法规**
   - 仅供学习和个人使用
   - 尊重内容创作者版权
   - 不要用于商业目的

2. **合理使用**
   - 不要过于频繁请求
   - 建议检查间隔不少于5分钟
   - 注意存储空间占用

3. **保护隐私**
   - 妥善保管cookie
   - 不要泄露配置文件
   - 定期更新cookie

---

## 🔗 相关链接

- [项目主页](https://github.com/ReaJason/xhs)
- [在线文档](https://reajason.github.io/xhs/)
- [问题反馈](https://github.com/ReaJason/xhs/issues)

---

**祝使用愉快！** 🎉

如有问题，欢迎提Issue或参考详细文档。
