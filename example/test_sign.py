#!/usr/bin/env python3
"""
测试签名功能脚本
用于快速诊断 monitor_user_notes.py 中签名卡住的问题
"""

import os
import sys
from time import sleep
from playwright.sync_api import sync_playwright


def test_sign_basic():
    """测试基本的签名功能"""
    print("="*60)
    print("🧪 测试 1: 基本签名功能")
    print("="*60)
    
    uri = "/api/sns/web/v1/user_posted?num=30&cursor=&user_id=5657d81c7c5bb814405de598&image_scenes=FD_WM_WEBP"
    
    try:
        print("📱 启动 Playwright...")
        with sync_playwright() as playwright:
            print("✅ Playwright 启动成功")
            
            print("🌐 启动 Chromium 浏览器...")
            chromium = playwright.chromium
            browser = chromium.launch(headless=True)
            print("✅ 浏览器启动成功")
            
            print("📄 创建浏览器上下文...")
            browser_context = browser.new_context()
            print("✅ 浏览器上下文创建成功")
            
            print("📑 创建新页面...")
            context_page = browser_context.new_page()
            print("✅ 页面创建成功")
            
            # 设置超时
            context_page.set_default_timeout(30000)
            
            print("🌍 导航到小红书页面...")
            print("   URL: https://www.xiaohongshu.com")
            context_page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
            print("✅ 页面加载完成")
            
            print("⏳ 等待 2 秒让页面完全加载...")
            sleep(2)
            
            # 检查页面标题
            title = context_page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查签名函数
            print("🔍 检查 window._webmsxyw 函数是否存在...")
            has_func = context_page.evaluate("() => typeof window._webmsxyw")
            print(f"   typeof window._webmsxyw = {has_func}")
            
            if has_func != "function":
                print("❌ 签名函数不存在!")
                print("\n可能的原因:")
                print("1. 页面未完全加载")
                print("2. 小红书更新了前端代码")
                print("3. 需要登录才能加载签名函数")
                print("4. 网络问题导致 JS 文件未加载")
                
                # 尝试等待更长时间
                print("\n⏳ 再等待 5 秒...")
                sleep(5)
                has_func = context_page.evaluate("() => typeof window._webmsxyw")
                print(f"   typeof window._webmsxyw = {has_func}")
                
                if has_func != "function":
                    browser.close()
                    return False
            
            print("✅ 签名函数存在")
            
            # 尝试调用签名函数
            print(f"\n✨ 尝试生成签名...")
            print(f"   URI: {uri[:80]}...")
            
            encrypt_params = context_page.evaluate(
                "([url, data]) => window._webmsxyw(url, data)", 
                [uri, None]
            )
            
            print("✅ 签名生成成功!")
            print(f"   X-s: {encrypt_params.get('X-s', 'N/A')[:50]}...")
            print(f"   X-t: {encrypt_params.get('X-t', 'N/A')}")
            
            browser.close()
            print("\n✅ 测试 1 通过!\n")
            return True
            
    except Exception as e:
        print(f"\n❌ 测试 1 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sign_with_cookie():
    """测试带 cookie 的签名功能"""
    print("="*60)
    print("🧪 测试 2: 带 Cookie 的签名功能")
    print("="*60)
    
    # 检查是否有配置文件
    config_file = "monitor_config.json"
    if not os.path.exists(config_file):
        print(f"⚠️  配置文件不存在: {config_file}")
        print("跳过此测试")
        return True
    
    import json
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    cookie = config.get("cookie", "")
    if not cookie or cookie == "your_cookie_here":
        print("⚠️  配置文件中没有有效的 cookie")
        print("跳过此测试")
        return True
    
    # 从 cookie 中提取 a1
    a1 = ""
    for item in cookie.split(";"):
        item = item.strip()
        if item.startswith("a1="):
            a1 = item.split("=", 1)[1]
            break
    
    if not a1:
        print("⚠️  Cookie 中没有找到 a1 值")
        print("跳过此测试")
        return True
    
    print(f"✅ 找到 a1 cookie: {a1[:20]}...")
    
    uri = "/api/sns/web/v1/user_posted?num=30&cursor=&user_id=5657d81c7c5bb814405de598&image_scenes=FD_WM_WEBP"
    
    try:
        print("📱 启动 Playwright...")
        with sync_playwright() as playwright:
            chromium = playwright.chromium
            browser = chromium.launch(headless=True)
            browser_context = browser.new_context()
            context_page = browser_context.new_page()
            context_page.set_default_timeout(30000)
            
            print("🌍 导航到小红书页面...")
            context_page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
            
            print("🍪 设置 a1 cookie...")
            browser_context.add_cookies([
                {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
            ])
            
            print("🔄 重新加载页面...")
            context_page.reload(wait_until="domcontentloaded")
            
            print("⏳ 等待 2 秒...")
            sleep(2)
            
            # 检查签名函数
            print("🔍 检查签名函数...")
            has_func = context_page.evaluate("() => typeof window._webmsxyw === 'function'")
            
            if not has_func:
                print("❌ 签名函数不存在!")
                browser.close()
                return False
            
            print("✨ 生成签名...")
            encrypt_params = context_page.evaluate(
                "([url, data]) => window._webmsxyw(url, data)", 
                [uri, None]
            )
            
            print("✅ 签名生成成功!")
            print(f"   X-s: {encrypt_params.get('X-s', 'N/A')[:50]}...")
            print(f"   X-t: {encrypt_params.get('X-t', 'N/A')}")
            
            browser.close()
            print("\n✅ 测试 2 通过!\n")
            return True
            
    except Exception as e:
        print(f"\n❌ 测试 2 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("🔧 小红书签名功能诊断工具")
    print("="*60)
    print("此工具将帮助诊断 monitor_user_notes.py 卡住的问题")
    print("="*60 + "\n")
    
    # 检查 playwright 是否安装
    try:
        import playwright
        print("✅ Playwright 已安装")
    except ImportError:
        print("❌ Playwright 未安装!")
        print("请运行: pip install playwright")
        print("然后运行: playwright install chromium")
        sys.exit(1)
    
    # 检查 chromium 是否安装
    print("检查 Chromium 浏览器...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("✅ Chromium 浏览器可用\n")
    except Exception as e:
        print(f"❌ Chromium 浏览器不可用: {e}")
        print("请运行: playwright install chromium")
        sys.exit(1)
    
    # 运行测试
    results = []
    
    print("\n" + "="*60)
    results.append(("基本签名功能", test_sign_basic()))
    
    print("\n" + "="*60)
    results.append(("带 Cookie 签名", test_sign_with_cookie()))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 所有测试通过! 签名功能正常")
        print("\n💡 建议:")
        print("1. 如果 monitor_user_notes.py 仍然卡住，请检查:")
        print("   - 网络连接是否正常")
        print("   - user_id 是否正确")
        print("   - cookie 是否有效")
        print("2. 可以在配置文件中设置 'use_headless': false 来查看浏览器运行情况")
    else:
        print("\n⚠️  部分测试失败")
        print("\n💡 可能的解决方案:")
        print("1. 确保网络连接正常，可以访问 xiaohongshu.com")
        print("2. 检查是否需要代理才能访问小红书")
        print("3. 尝试在配置文件中设置 'use_headless': false 查看详细情况")
        print("4. 检查小红书是否更新了前端代码（签名函数名称或实现改变）")
    
    print("\n")


if __name__ == "__main__":
    main()
