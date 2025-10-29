#!/usr/bin/env python3
"""
小红书笔记监控 - 快速示例

这是一个简化版的监控脚本，展示核心功能。
适合快速上手和学习使用。
"""

import json
import os
import time
from datetime import datetime
from time import sleep

from playwright.sync_api import sync_playwright
from xhs import XhsClient, help


def sign(uri, data=None, a1="", web_session=""):
    """签名函数 - 使用playwright生成请求签名"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.xiaohongshu.com")
        
        if a1:
            context.add_cookies([
                {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
            ])
            page.reload()
        
        sleep(1)
        encrypt_params = page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
        browser.close()
        
        return {
            "x-s": encrypt_params["X-s"],
            "x-t": str(encrypt_params["X-t"])
        }


def download_note(xhs_client, note_info, download_dir="./downloads"):
    """下载单个笔记"""
    note_id = note_info.get("note_id")
    xsec_token = note_info.get("xsec_token", "")
    
    print(f"📥 开始下载笔记: {note_id}")
    
    # 获取笔记详情
    note_detail = xhs_client.get_note_by_id(note_id, xsec_token)
    
    # 创建保存目录
    title = help.get_valid_path_name(note_detail.get("title", note_id))
    note_dir = os.path.join(download_dir, f"{title}_{note_id}")
    os.makedirs(note_dir, exist_ok=True)
    
    print(f"   标题: {title}")
    
    # 保存元数据
    metadata = {
        "note_id": note_id,
        "title": note_detail.get("title", ""),
        "desc": note_detail.get("desc", ""),
        "type": note_detail.get("type", ""),
        "user": note_detail.get("user", {}),
        "interact_info": note_detail.get("interact_info", {}),
        "download_time": datetime.now().isoformat()
    }
    
    with open(os.path.join(note_dir, "metadata.json"), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    # 下载内容
    note_type = note_detail.get("type", "")
    
    if note_type == "video":
        # 下载视频
        video_url = help.get_video_url_from_note(note_detail)
        if video_url:
            video_file = os.path.join(note_dir, f"{title}.mp4")
            help.download_file(video_url, video_file)
            print(f"   ✅ 视频已保存")
    else:
        # 下载图片
        img_urls = help.get_imgs_url_from_note(note_detail)
        print(f"   正在下载 {len(img_urls)} 张图片...")
        for idx, img_url in enumerate(img_urls):
            img_file = os.path.join(note_dir, f"{title}_{idx + 1}.png")
            help.download_file(img_url, img_file)
            print(f"   ✅ 图片 {idx + 1}/{len(img_urls)} 已保存")
    
    print(f"✅ 笔记下载完成\n")
    return note_id


def monitor_user(cookie, user_id, download_dir="./downloads", check_interval=300):
    """
    监控指定用户的笔记
    
    参数:
        cookie: 你的小红书cookie
        user_id: 要监控的用户ID
        download_dir: 下载保存目录
        check_interval: 检查间隔（秒）
    """
    
    # 初始化客户端
    print("🚀 初始化小红书客户端...")
    xhs_client = XhsClient(cookie=cookie, sign=sign)
    
    # 已下载笔记记录文件
    downloaded_file = "downloaded_notes.json"
    
    # 加载已下载记录
    if os.path.exists(downloaded_file):
        with open(downloaded_file, 'r') as f:
            downloaded_ids = set(json.load(f))
    else:
        downloaded_ids = set()
    
    print(f"✅ 初始化完成")
    print(f"📊 已下载笔记数: {len(downloaded_ids)}")
    print(f"👤 监控用户: {user_id}")
    print(f"⏰ 检查间隔: {check_interval} 秒\n")
    
    # 开始监控循环
    while True:
        try:
            print(f"\n{'='*60}")
            print(f"🔍 检查新笔记 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")
            
            # 获取用户笔记列表
            result = xhs_client.get_user_notes(user_id)
            notes = result.get("notes", [])
            
            print(f"📋 用户共有 {len(notes)} 条笔记")
            
            # 找出新笔记
            new_notes = [note for note in notes if note.get("note_id") not in downloaded_ids]
            
            if new_notes:
                print(f"🎉 发现 {len(new_notes)} 条新笔记！\n")
                
                # 下载新笔记
                for i, note in enumerate(new_notes, 1):
                    print(f"[{i}/{len(new_notes)}] ", end="")
                    note_id = download_note(xhs_client, note, download_dir)
                    downloaded_ids.add(note_id)
                    sleep(2)  # 避免请求过快
                
                # 保存已下载记录
                with open(downloaded_file, 'w') as f:
                    json.dump(list(downloaded_ids), f)
                
                print(f"✅ 成功下载 {len(new_notes)} 条新笔记")
            else:
                print("✅ 没有发现新笔记")
            
            # 等待下次检查
            next_check = datetime.now().timestamp() + check_interval
            next_check_time = datetime.fromtimestamp(next_check).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n⏰ 下次检查时间: {next_check_time}")
            print(f"💤 等待 {check_interval} 秒...\n")
            
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\n\n👋 收到停止信号，正在退出...")
            break
        except Exception as e:
            print(f"\n❌ 出错: {e}")
            print("⏰ 等待 60 秒后重试...\n")
            time.sleep(60)


def main():
    """
    主函数 - 在这里配置你的参数
    """
    
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
    
    # 参数验证
    if COOKIE == "your_cookie_here":
        print("❌ 错误: 请设置你的Cookie")
        print("\n如何获取Cookie:")
        print("1. 打开浏览器，访问 https://www.xiaohongshu.com")
        print("2. 登录你的账号")
        print("3. 按F12打开开发者工具")
        print("4. 点击Network标签")
        print("5. 刷新页面，点击任意请求")
        print("6. 在Request Headers中找到Cookie字段并复制")
        print("\n复制后，修改本文件中的 COOKIE 变量\n")
        return
    
    if USER_ID == "target_user_id_here":
        print("❌ 错误: 请设置要监控的用户ID")
        print("\n如何获取用户ID:")
        print("1. 访问要监控的用户主页")
        print("2. URL格式为: https://www.xiaohongshu.com/user/profile/用户ID")
        print("3. 复制URL中的用户ID")
        print("\n复制后，修改本文件中的 USER_ID 变量\n")
        return
    
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 开始监控
    monitor_user(
        cookie=COOKIE,
        user_id=USER_ID,
        download_dir=DOWNLOAD_DIR,
        check_interval=CHECK_INTERVAL
    )


if __name__ == '__main__':
    main()
