# Playwright new_page() 挂起问题修复说明

## 问题描述

在某些环境（特别是 ARM 架构或容器环境）中，Playwright 在调用 `browser_context.new_page()` 时会挂起，导致程序无法继续执行。

### 受影响的文件
- `example/test_sign.py`
- `example/monitor_user_notes.py`
- `example/basic_sign_server.py`
- `example/basic_usage.py`
- `example/login_qrcode.py`
- `example/login_phone.py`
- `example/quick_monitor_example.py`
- `xhs-api/app.py`

## 问题原因

Playwright 的 Chromium 浏览器在某些系统环境下需要特定的启动参数才能正常工作。特别是在：
- ARM 架构系统
- 容器环境（Docker 等）
- 没有图形界面的服务器环境
- 共享内存（/dev/shm）受限的环境

当缺少这些必要的启动参数时，`new_page()` 调用可能会无限期挂起。

## 解决方案

在调用 `chromium.launch()` 时添加必要的启动参数：

```python
browser = chromium.launch(
    headless=True,
    args=[
        '--disable-blink-features=AutomationControlled',  # 禁用自动化控制特征检测
        '--disable-dev-shm-usage',                        # 禁用 /dev/shm 使用（解决容器环境问题）
        '--no-sandbox'                                     # 禁用沙盒（在受限环境中必需）
    ]
)
```

### 参数说明

1. **`--disable-blink-features=AutomationControlled`**
   - 禁用浏览器的自动化控制检测
   - 使浏览器表现得更像普通用户浏览器
   
2. **`--disable-dev-shm-usage`**
   - 禁用 `/dev/shm` 共享内存的使用
   - 在容器环境中非常重要，因为容器可能限制了共享内存大小
   - 改为使用 `/tmp` 目录
   
3. **`--no-sandbox`**
   - 禁用 Chrome 的沙盒模式
   - 在某些受限环境（如容器或 ARM 架构）中必需
   - 注意：这会降低浏览器的安全性，仅在测试环境使用

## 修复验证

修复后可以通过以下方式验证：

```bash
# 运行测试脚本
python example/test_sign.py

# 或运行简单的验证测试
python test_playwright_fix.py
```

## 注意事项

1. 这些启动参数可能会降低浏览器的安全性，仅建议在开发和测试环境使用
2. 在生产环境中，应该考虑使用更安全的配置或专门的浏览器自动化服务
3. 如果在特定环境中仍有问题，可能需要安装额外的系统依赖：

```bash
sudo apt-get install libnspr4 libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 \
    libcups2t64 libxkbcommon0 libatspi2.0-0t64 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libcairo2 \
    libpango-1.0-0 libasound2t64
```

## 测试结果

修复前：
- `new_page()` 调用时程序挂起
- 无错误信息，程序永久停止响应

修复后：
- `new_page()` 立即成功返回
- 页面可以正常导航和交互
- 所有签名功能正常工作

## 相关问题

此修复解决了以下 issue：
- Playwright 在 ARM 架构上挂起
- 在 Docker 容器中运行时挂起
- `test_sign.py` 在"创建新页面"步骤卡住

## 参考资料

- [Playwright Docker 文档](https://playwright.dev/docs/docker)
- [Chrome 启动参数列表](https://peter.sh/experiments/chromium-command-line-switches/)
- [Playwright Troubleshooting](https://playwright.dev/docs/troubleshooting)
