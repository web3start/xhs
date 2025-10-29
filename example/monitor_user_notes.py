#!/usr/bin/env python3
"""
小红书用户笔记监控和自动下载工具

功能：
1. 定期监控指定小红书用户的笔记
2. 自动检测新发布的笔记
3. 自动下载新笔记的图片或视频到本地
4. 保存笔记元数据信息
5. 持久化跟踪已下载的笔记ID

使用方法：
1. 配置 config.json 文件（首次运行会自动创建模板）
2. 运行: python monitor_user_notes.py
"""

import datetime
import json
import os
import time
from pathlib import Path
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help


class NoteMonitor:
    """小红书笔记监控器"""
    
    def __init__(self, config_file="monitor_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.xhs_client = None
        self.downloaded_notes_file = self.config.get("downloaded_notes_file", "downloaded_notes.json")
        self.downloaded_notes = self.load_downloaded_notes()
        
    def load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        if not os.path.exists(self.config_file):
            default_config = {
                "cookie": "your_cookie_here",
                "user_id": "target_user_id_here",
                "download_dir": "./downloads",
                "check_interval": 300,
                "stealth_js_path": "./stealth.min.js",
                "use_headless": True,
                "max_retries": 3,
                "retry_delay": 2,
                "downloaded_notes_file": "downloaded_notes.json"
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            print(f"✅ 已创建默认配置文件: {self.config_file}")
            print("⚠️  请编辑配置文件，填入你的cookie和要监控的user_id")
            return default_config
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_downloaded_notes(self):
        """加载已下载的笔记ID列表"""
        if os.path.exists(self.downloaded_notes_file):
            with open(self.downloaded_notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"note_ids": [], "notes_metadata": {}}
    
    def save_downloaded_notes(self):
        """保存已下载的笔记ID列表"""
        with open(self.downloaded_notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.downloaded_notes, f, indent=4, ensure_ascii=False)
    
    def sign(self, uri, data=None, a1="", web_session=""):
        """
        签名函数，使用playwright调用浏览器生成签名
        如果签名经常失败，可以设置 use_headless=False 查看浏览器状态
        """
        for retry in range(self.config.get("max_retries", 3)):
            browser = None
            try:
                print(f"   🔐 正在生成签名 (URI: {uri[:50]}...)")
                with sync_playwright() as playwright:
                    stealth_js_path = self.config.get("stealth_js_path", "./stealth.min.js")
                    chromium = playwright.chromium
                    
                    # 可配置是否使用无头模式
                    use_headless = self.config.get("use_headless", True)
                    print(f"   🌐 启动浏览器 (headless={use_headless})...")
                    browser = chromium.launch(headless=use_headless)
                    
                    browser_context = browser.new_context()
                    
                    # 如果stealth.js文件存在，则添加
                    if os.path.exists(stealth_js_path):
                        print(f"   📄 加载 stealth.js")
                        browser_context.add_init_script(path=stealth_js_path)
                    else:
                        print(f"   ⚠️  stealth.js 文件不存在: {stealth_js_path}")
                    
                    context_page = browser_context.new_page()
                    print(f"   📡 加载小红书页面...")
                    
                    # 设置页面加载超时
                    context_page.set_default_timeout(30000)  # 30秒超时
                    context_page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
                    
                    if a1:
                        print(f"   🍪 设置 cookie (a1)")
                        browser_context.add_cookies([
                            {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
                        ])
                        context_page.reload(wait_until="domcontentloaded")
                    
                    # 等待页面加载
                    print(f"   ⏳ 等待页面加载完成...")
                    sleep(2)
                    
                    # 检查签名函数是否存在
                    print(f"   🔍 检查签名函数是否存在...")
                    has_sign_func = context_page.evaluate("() => typeof window._webmsxyw === 'function'")
                    if not has_sign_func:
                        raise Exception("window._webmsxyw 签名函数不存在，页面可能未完全加载")
                    
                    print(f"   ✨ 执行签名函数...")
                    encrypt_params = context_page.evaluate(
                        "([url, data]) => window._webmsxyw(url, data)", 
                        [uri, data]
                    )
                    
                    if not encrypt_params or "X-s" not in encrypt_params:
                        raise Exception("签名函数返回结果无效")
                    
                    print(f"   ✅ 签名生成成功")
                    
                    result = {
                        "x-s": encrypt_params["X-s"],
                        "x-t": str(encrypt_params["X-t"])
                    }
                    
                    browser.close()
                    return result
                    
            except Exception as e:
                # 确保浏览器被关闭
                if browser:
                    try:
                        browser.close()
                    except:
                        pass
                
                print(f"⚠️  签名失败 (重试 {retry + 1}/{self.config.get('max_retries', 3)}): {e}")
                if retry < self.config.get("max_retries", 3) - 1:
                    print(f"   💤 等待 {self.config.get('retry_delay', 2)} 秒后重试...")
                    sleep(self.config.get("retry_delay", 2))
        
        raise Exception("❌ 签名失败次数过多，请检查配置。建议:\n"
                       "   1. 运行 'python test_sign.py' 进行诊断\n"
                       "   2. 检查网络连接\n"
                       "   3. 查看 MONITOR_TROUBLESHOOTING.md 获取详细帮助")
    
    def init_client(self):
        """初始化小红书客户端"""
        cookie = self.config.get("cookie", "")
        if not cookie or cookie == "your_cookie_here":
            raise ValueError("❌ 请在配置文件中设置有效的cookie")
        
        self.xhs_client = XhsClient(cookie=cookie, sign=self.sign)
        print("✅ 小红书客户端初始化成功")
    
    def get_user_notes(self, user_id):
        """获取用户的所有笔记列表（简要信息）"""
        all_notes = []
        cursor = ""
        has_more = True
        
        print(f"📋 正在获取用户 {user_id} 的笔记列表...")
        
        while has_more:
            try:
                result = self.xhs_client.get_user_notes(user_id, cursor)
                notes = result.get("notes", [])
                all_notes.extend(notes)
                has_more = result.get("has_more", False)
                cursor = result.get("cursor", "")
                
                print(f"   已获取 {len(all_notes)} 条笔记...")
                
                if has_more:
                    sleep(1)  # 避免请求过快
                    
            except Exception as e:
                print(f"⚠️  获取笔记列表失败: {e}")
                break
        
        print(f"✅ 共获取 {len(all_notes)} 条笔记")
        return all_notes
    
    def download_note(self, note_info):
        """下载单个笔记的内容"""
        note_id = note_info.get("note_id")
        xsec_token = note_info.get("xsec_token", "")
        
        print(f"\n📥 开始下载笔记: {note_id}")
        
        # 获取笔记详细信息
        for retry in range(self.config.get("max_retries", 3)):
            try:
                note_detail = self.xhs_client.get_note_by_id(note_id, xsec_token)
                break
            except DataFetchError as e:
                print(f"⚠️  获取笔记详情失败 (重试 {retry + 1}/{self.config.get('max_retries', 3)}): {e}")
                if retry < self.config.get("max_retries", 3) - 1:
                    sleep(self.config.get("retry_delay", 2))
                else:
                    print(f"❌ 笔记 {note_id} 下载失败")
                    return False
        
        # 创建笔记目录
        title = note_detail.get("title", note_id)
        title = help.get_valid_path_name(title)
        
        # 添加时间戳避免重名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        note_dir = os.path.join(
            self.config.get("download_dir", "./downloads"),
            f"{title}_{note_id}_{timestamp}"
        )
        
        os.makedirs(note_dir, exist_ok=True)
        
        # 保存笔记元数据
        metadata = {
            "note_id": note_id,
            "title": note_detail.get("title", ""),
            "desc": note_detail.get("desc", ""),
            "type": note_detail.get("type", ""),
            "user": note_detail.get("user", {}),
            "tags": note_detail.get("tag_list", []),
            "interact_info": note_detail.get("interact_info", {}),
            "download_time": datetime.datetime.now().isoformat(),
            "xsec_token": xsec_token
        }
        
        metadata_file = os.path.join(note_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        print(f"   标题: {title}")
        print(f"   类型: {note_detail.get('type', 'unknown')}")
        
        # 下载视频或图片
        note_type = note_detail.get("type", "")
        download_success = False
        
        if note_type == "video":
            # 下载视频
            video_url = help.get_video_url_from_note(note_detail)
            if video_url:
                video_file = os.path.join(note_dir, f"{title}.mp4")
                try:
                    print(f"   正在下载视频...")
                    help.download_file(video_url, video_file)
                    print(f"   ✅ 视频已保存: {video_file}")
                    download_success = True
                except Exception as e:
                    print(f"   ❌ 视频下载失败: {e}")
            else:
                print(f"   ⚠️  未找到视频URL")
        else:
            # 下载图片
            img_urls = help.get_imgs_url_from_note(note_detail)
            if img_urls:
                print(f"   正在下载 {len(img_urls)} 张图片...")
                for idx, img_url in enumerate(img_urls):
                    img_file = os.path.join(note_dir, f"{title}_{idx + 1}.png")
                    try:
                        help.download_file(img_url, img_file)
                        print(f"   ✅ 图片 {idx + 1}/{len(img_urls)} 已保存")
                    except Exception as e:
                        print(f"   ❌ 图片 {idx + 1} 下载失败: {e}")
                download_success = True
            else:
                print(f"   ⚠️  未找到图片URL")
        
        if download_success:
            # 记录已下载
            self.downloaded_notes["note_ids"].append(note_id)
            self.downloaded_notes["notes_metadata"][note_id] = {
                "title": title,
                "download_time": datetime.datetime.now().isoformat(),
                "download_path": note_dir,
                "type": note_type
            }
            self.save_downloaded_notes()
            print(f"✅ 笔记 {note_id} 下载完成\n")
            return True
        
        return False
    
    def check_new_notes(self):
        """检查是否有新笔记"""
        user_id = self.config.get("user_id", "")
        if not user_id or user_id == "target_user_id_here":
            raise ValueError("❌ 请在配置文件中设置要监控的user_id")
        
        print(f"\n{'='*60}")
        print(f"🔍 检查新笔记 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # 获取用户笔记列表
        notes = self.get_user_notes(user_id)
        
        # 查找新笔记
        downloaded_ids = set(self.downloaded_notes["note_ids"])
        new_notes = [note for note in notes if note.get("note_id") not in downloaded_ids]
        
        if not new_notes:
            print("✅ 没有发现新笔记")
            return 0
        
        print(f"\n🎉 发现 {len(new_notes)} 条新笔记！")
        
        # 下载新笔记
        success_count = 0
        for i, note in enumerate(new_notes, 1):
            print(f"\n[{i}/{len(new_notes)}] ", end="")
            if self.download_note(note):
                success_count += 1
            sleep(2)  # 避免请求过快
        
        print(f"\n✅ 成功下载 {success_count}/{len(new_notes)} 条新笔记")
        return success_count
    
    def run_once(self):
        """执行一次检查"""
        try:
            if not self.xhs_client:
                self.init_client()
            self.check_new_notes()
        except Exception as e:
            print(f"❌ 执行出错: {e}")
            import traceback
            traceback.print_exc()
    
    def run_monitor(self):
        """持续监控模式"""
        print("\n" + "="*60)
        print("🚀 小红书笔记监控器启动")
        print("="*60)
        print(f"配置文件: {self.config_file}")
        print(f"监控用户: {self.config.get('user_id', 'unknown')}")
        print(f"检查间隔: {self.config.get('check_interval', 300)} 秒")
        print(f"下载目录: {self.config.get('download_dir', './downloads')}")
        print(f"已下载笔记数: {len(self.downloaded_notes['note_ids'])}")
        print("="*60 + "\n")
        
        # 初始化客户端
        self.init_client()
        
        # 持续监控
        while True:
            try:
                self.check_new_notes()
                
                check_interval = self.config.get("check_interval", 300)
                next_check = datetime.datetime.now() + datetime.timedelta(seconds=check_interval)
                print(f"\n⏰ 下次检查时间: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"💤 等待 {check_interval} 秒...\n")
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n\n👋 收到停止信号，正在退出...")
                break
            except Exception as e:
                print(f"\n❌ 监控出错: {e}")
                import traceback
                traceback.print_exc()
                print(f"\n⏰ 等待 60 秒后重试...\n")
                time.sleep(60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="小红书用户笔记监控和自动下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 持续监控模式（默认）
  python monitor_user_notes.py
  
  # 只执行一次检查
  python monitor_user_notes.py --once
  
  # 使用自定义配置文件
  python monitor_user_notes.py --config my_config.json
  
首次运行会自动创建配置文件模板，请编辑后再次运行。
        """
    )
    
    parser.add_argument(
        "--config",
        default="monitor_config.json",
        help="配置文件路径 (默认: monitor_config.json)"
    )
    
    parser.add_argument(
        "--once",
        action="store_true",
        help="只执行一次检查，不持续监控"
    )
    
    args = parser.parse_args()
    
    # 创建监控器
    monitor = NoteMonitor(config_file=args.config)
    
    # 执行监控
    if args.once:
        monitor.run_once()
    else:
        monitor.run_monitor()


if __name__ == '__main__':
    main()
