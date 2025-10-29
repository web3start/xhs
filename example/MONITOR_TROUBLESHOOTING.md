# 小红书笔记监控器故障排查指南

## 问题: 监控器卡在"正在获取用户笔记列表"

### 症状
运行 `monitor_user_notes.py` 后显示：
```
📋 正在获取用户 5657d81c7c5bb814405de598 的笔记列表...
```
然后就一直卡住，没有进一步输出。

### 原因分析

监控器卡住通常是因为**签名生成过程**出现问题。`monitor_user_notes.py` 使用 Playwright 启动浏览器来生成小红书 API 所需的签名（x-s 和 x-t 参数），如果这个过程失败或超时，程序就会卡住。

可能的具体原因：
1. **Playwright 浏览器未正确安装**
2. **网络问题** - 无法访问 xiaohongshu.com
3. **页面加载超时** - 小红书页面加载时间过长
4. **签名函数不存在** - `window._webmsxyw` 函数未加载
5. **系统资源不足** - 浏览器启动失败

---

## 解决方案

### 步骤 1: 运行诊断工具

我们提供了一个诊断工具来快速定位问题：

```bash
cd example
python test_sign.py
```

这个工具会：
- ✅ 检查 Playwright 是否正确安装
- ✅ 检查 Chromium 浏览器是否可用
- ✅ 测试基本的签名功能
- ✅ 测试带 Cookie 的签名功能
- ✅ 提供详细的错误信息

### 步骤 2: 根据诊断结果解决问题

#### 问题 A: Playwright 或 Chromium 未安装

**错误信息:**
```
❌ Playwright 未安装!
```
或
```
❌ Chromium 浏览器不可用
```

**解决方法:**
```bash
# 安装 Playwright
pip install playwright

# 安装 Chromium 浏览器
playwright install chromium
```

#### 问题 B: 签名函数不存在

**错误信息:**
```
❌ 签名函数不存在!
typeof window._webmsxyw = undefined
```

**可能原因:**
1. 页面加载不完整
2. 小红书更新了前端代码
3. 需要先登录

**解决方法:**

**方法 1: 增加等待时间**

编辑 `monitor_user_notes.py`，在签名函数中增加等待时间：
```python
# 将 sleep(2) 改为 sleep(5)
sleep(5)
```

**方法 2: 使用非无头模式调试**

编辑 `monitor_config.json`:
```json
{
  "use_headless": false,
  ...
}
```

这样可以看到浏览器窗口，观察页面加载情况。

**方法 3: 使用备用签名服务**

考虑使用项目提供的 `xhs-api` 签名服务（如果可用）。

#### 问题 C: 网络问题

**错误信息:**
```
TimeoutError: Timeout 30000ms exceeded
```
或无法连接到 xiaohongshu.com

**解决方法:**

1. **检查网络连接**
   ```bash
   curl https://www.xiaohongshu.com
   ```

2. **配置代理** (如果需要)
   
   编辑 `monitor_user_notes.py`，在浏览器启动时添加代理：
   ```python
   browser = chromium.launch(
       headless=use_headless,
       proxy={"server": "http://your-proxy:port"}
   )
   ```

3. **增加超时时间**
   
   编辑 `monitor_user_notes.py`:
   ```python
   context_page.set_default_timeout(60000)  # 从 30000 改为 60000
   ```

#### 问题 D: Cookie 无效

**症状:** 即使签名成功，仍然无法获取笔记列表

**解决方法:**

1. **重新获取 Cookie**
   - 打开浏览器，登录小红书网页版
   - 打开开发者工具 (F12)
   - 访问任意页面
   - 在 Network 标签中找到请求
   - 复制 Cookie 值

2. **更新配置文件**
   编辑 `monitor_config.json`:
   ```json
   {
     "cookie": "your_new_cookie_here",
     ...
   }
   ```

3. **验证 Cookie 格式**
   Cookie 应该包含以下关键字段:
   - `a1=...`
   - `web_session=...`
   
   示例:
   ```
   a1=xxxxx; webId=xxxxx; web_session=xxxxx; ...
   ```

### 步骤 3: 使用增强版监控器

我们已经更新了 `monitor_user_notes.py`，添加了详细的日志输出。现在运行时会显示：

```
📋 正在获取用户 5657d81c7c5bb814405de598 的笔记列表...
   🔐 正在生成签名 (URI: /api/sns/web/v1/user_posted?...)
   🌐 启动浏览器 (headless=True)...
   📡 加载小红书页面...
   ⏳ 等待页面加载完成...
   🔍 检查签名函数是否存在...
   ✨ 执行签名函数...
   ✅ 签名生成成功
```

如果卡在某一步，就可以知道具体哪里出了问题。

### 步骤 4: 重新运行监控器

```bash
cd example  # 或你的工作目录
python monitor_user_notes.py
```

如果只想测试一次（不持续监控）：
```bash
python monitor_user_notes.py --once
```

---

## 配置建议

### 推荐的配置文件 (monitor_config.json)

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

### 配置字段说明

| 字段 | 说明 | 默认值 | 建议 |
|------|------|--------|------|
| `cookie` | 小红书 Cookie | - | 必填，需定期更新 |
| `user_id` | 要监控的用户ID | - | 必填 |
| `download_dir` | 下载目录 | `./downloads` | 可自定义 |
| `check_interval` | 检查间隔(秒) | 300 | 建议 ≥ 300，避免频繁请求 |
| `stealth_js_path` | stealth.js 路径 | `./stealth.min.js` | 可选，但推荐使用 |
| `use_headless` | 无头模式 | true | 调试时设为 false |
| `max_retries` | 最大重试次数 | 3 | 网络不稳定时可增加 |
| `retry_delay` | 重试延迟(秒) | 2 | - |

---

## 性能优化建议

### 1. 减少签名调用
签名生成需要启动浏览器，比较耗时。可以考虑：
- 增加检查间隔 (`check_interval`)
- 使用外部签名服务（如项目中的 xhs-api）

### 2. 使用 stealth.js
下载 `stealth.min.js` 可以降低被检测为机器人的风险：
```bash
wget https://cdn.jsdelivr.net/npm/puppeteer-extra-plugin-stealth@latest/stealth.min.js
```

### 3. 避免频繁请求
- `check_interval` 设置为至少 5 分钟（300秒）
- 使用 `sleep()` 在批量操作之间添加延迟

---

## 常见问题 FAQ

### Q1: 为什么需要 Cookie?
A: Cookie 用于身份验证，没有有效的 Cookie 无法访问小红书 API。

### Q2: Cookie 多久失效?
A: 通常 1-7 天，取决于小红书的策略。建议定期更新。

### Q3: 可以同时监控多个用户吗?
A: 可以运行多个监控器实例，每个使用不同的配置文件：
```bash
python monitor_user_notes.py --config user1_config.json &
python monitor_user_notes.py --config user2_config.json &
```

### Q4: 如何获取 user_id?
A: 
1. 访问用户主页，如 `https://www.xiaohongshu.com/user/profile/5657d81c7c5bb814405de598`
2. URL 中的最后一部分就是 user_id

### Q5: 监控器占用资源太多怎么办?
A: 
- 确保使用无头模式 (`use_headless: true`)
- 增加检查间隔
- 关闭不需要的浏览器扩展

### Q6: 可以在服务器上运行吗?
A: 可以，但需要安装相关依赖：
```bash
# Ubuntu/Debian
apt-get install -y wget unzip fontconfig locales gconf-service libasound2 \
  libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 \
  libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \
  libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
  libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 \
  libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 \
  libnss3 lsb-release xdg-utils

# 然后安装 Playwright 浏览器
playwright install --with-deps chromium
```

---

## 联系支持

如果以上方法都无法解决问题，请提供以下信息：

1. `test_sign.py` 的完整输出
2. `monitor_user_notes.py` 的输出（显示卡在哪一步）
3. 操作系统和 Python 版本
4. 网络环境（是否使用代理等）

---

## 更新日志

### 2025-01-29
- ✅ 添加详细的日志输出
- ✅ 添加页面加载超时控制
- ✅ 添加签名函数存在性检查
- ✅ 创建 `test_sign.py` 诊断工具
- ✅ 创建本故障排查指南
