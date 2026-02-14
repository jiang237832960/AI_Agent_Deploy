# -*- coding: utf-8 -*-
"""
GitHub 加速配置脚本
功能：智能检测GitHub连通性，自动配置加速
"""

import subprocess
import time
import json
import os
import sys
import shutil
import urllib.request
from datetime import datetime

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_backup_dir():
    return os.path.join(os.path.dirname(get_script_dir()), '..', 'backup')

def ensure_backup_dir():
    backup_dir = get_backup_dir()
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def backup_file(file_path, prefix=''):
    if not os.path.exists(file_path):
        return None
    backup_dir = ensure_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if prefix:
        backup_name = f"{prefix}.{timestamp}.backup"
    else:
        backup_name = f"{os.path.basename(file_path)}.{timestamp}.backup"
    backup_path = os.path.join(backup_dir, backup_name)
    try:
        shutil.copy2(file_path, backup_path)
        print(f"  已备份：{backup_path}")
        return backup_path
    except Exception as e:
        print(f"  备份失败：{e}")
        return None

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'mirrors.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def test_url(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        return response.getcode() == 200
    except:
        return False

def test_url_speed(url, timeout=10):
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        elapsed = (time.time() - start_time) * 1000
        return int(elapsed)
    except:
        return None

def print_header():
    print("\n" + "="*50)
    print("       GitHub 访问加速配置".center(40))
    print("="*50 + "\n")

def main():
    print_header()
    
    print("[步骤 1] 检测 GitHub 连通性...\n")
    print("  测试 github.com...", end=' ')
    
    gh_accessible = test_url('https://github.com', timeout=10)
    
    if gh_accessible:
        print("可访问")
        print("\n" + "="*50)
        print("   GitHub 访问正常，无需加速！")
        print("="*50 + "\n")
        
        choice = input("是否仍要测试镜像源？(Y/N): ").strip().upper()
        if choice != 'Y':
            input("\n按回车键退出...")
            return
    else:
        print("无法访问")
    
    print("\n[步骤 2] 测试镜像源...\n")
    
    config = load_config()
    if not config:
        print("无法加载配置文件！")
        input("按回车键退出...")
        return
    
    mirrors = config.get('mirrors', [])
    available_mirrors = []
    
    for mirror in mirrors:
        test_url_str = mirror.get('test_url', '')
        if not test_url_str:
            continue
        
        print(f"  测试 {mirror['name']}...", end=' ')
        latency = test_url_speed(test_url_str)
        
        if latency:
            print(f"可用 ({latency} ms)")
            available_mirrors.append((mirror, latency))
        else:
            print("不可用")
    
    print()
    
    if not available_mirrors:
        print("="*50)
        print("   未找到可用的镜像源。")
        print("   请检查网络连接。")
        print("="*50 + "\n")
        input("按回车键退出...")
        return
    
    if not gh_accessible:
        print("="*50)
        print("   GitHub 无法直接访问。")
        print("   检测到可用镜像源。")
        print("="*50 + "\n")
        
        choice = input("是否启用加速？(Y/N): ").strip().upper()
        if choice != 'Y':
            input("\n按回车键退出...")
            return
    
    available_mirrors.sort(key=lambda x: x[1])
    fastest = available_mirrors[0][0]
    print(f"\n推荐使用：{fastest['name']} ({fastest.get('description', '')})")
    
    print("\n" + "="*50)
    print("   请选择配置方式：")
    print("="*50)
    print("  1. 配置 Hosts 文件加速")
    print("  2. 配置 Git 代理")
    print("  3. 全部配置")
    print("  4. 退出")
    print()
    
    choice = input("请输入选项 (1-4): ").strip()
    
    if choice == '4':
        return
    
    if choice in ['1', '3']:
        hosts_dict = config.get('hosts', {})
        if hosts_dict:
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
            print("\n正在备份 hosts 文件...")
            backup_file(hosts_path, 'hosts')
            
            print("\n正在添加 GitHub 加速 hosts...")
            try:
                with open(hosts_path, 'r', encoding='utf-8') as f:
                    hosts_content = f.read()
            except:
                hosts_content = ''
            
            new_entries = []
            for domain, ip in hosts_dict.items():
                if domain not in hosts_content:
                    new_entries.append(f"{ip} {domain}\n")
            
            if new_entries:
                with open(hosts_path, 'a', encoding='utf-8') as f:
                    f.write('\n# GitHub 加速配置\n')
                    for entry in new_entries:
                        f.write(entry)
                    f.write('\n')
                print(f"  已添加 {len(new_entries)} 条记录")
            else:
                print("  hosts 文件已包含所需记录")
            
            print("\n提示：以管理员身份运行 ipconfig /flushdns 刷新 DNS")
    
    if choice in ['2', '3']:
        print("\n请选择代理类型：")
        print("  1. HTTP 代理 (如 Clash、V2Ray)")
        print("  2. GitHub 镜像")
        
        p_choice = input("\n请输入选项 (1-2): ").strip()
        
        if p_choice == '1':
            proxy_addr = input("请输入代理地址 (默认 http://127.0.0.1:7890): ").strip()
            if not proxy_addr:
                proxy_addr = "http://127.0.0.1:7890"
            
            subprocess.run(['git', 'config', '--global', 'http.proxy', proxy_addr])
            subprocess.run(['git', 'config', '--global', 'https.proxy', proxy_addr])
            print(f"  代理配置完成：{proxy_addr}")
        
        elif p_choice == '2':
            print("  GitHub 镜像配置已完成")
            print("  使用方式：将 github.com 替换为 ghproxy.com")
            print("  例如：https://ghproxy.com/https://github.com/xxx/xxx.git")
    
    print("\n" + "="*50)
    print("       配置完成！")
    print("="*50 + "\n")
    
    print("提示：")
    print("  1. 运行 restore.bat 可还原原始设置")
    print("  2. 运行 ipconfig /flushdns 刷新 DNS")
    print()
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()