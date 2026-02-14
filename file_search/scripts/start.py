# -*- coding: utf-8 -*-
"""
文件搜索模块启动脚本
"""

import os
import sys
import argparse

VERSION = "1.0.0"

script_dir = os.path.dirname(os.path.abspath(__file__))

def show_menu():
    print("\n" + "=" * 50)
    print("  文件搜索".center(40))
    print(f"  版本: {VERSION}".center(40))
    print("=" * 50 + "\n")
    
    print("请选择功能:\n")
    print("  1. 搜索文件")
    print("  2. 启动 Everything")
    print("  0. 返回上级菜单\n")
    
    choice = input("请输入选项: ").strip()
    return choice

def run_search():
    global script_dir
    script_path = os.path.join(script_dir, "search.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        script_path = os.path.join(script_dir, "search.bat")
        if os.path.exists(script_path):
            os.system(script_path)
        else:
            print("[错误] 未找到搜索脚本")

def run_everything():
    global script_dir
    project_root = os.path.dirname(os.path.dirname(script_dir))
    everything_path = os.path.join(project_root, "tools", "Everything", "Everything.exe")
    
    if os.path.exists(everything_path):
        os.startfile(everything_path)
        print("[信息] Everything 已启动")
    else:
        print("[错误] 未找到 Everything，请先下载")

def parse_args():
    parser = argparse.ArgumentParser(description='文件搜索模块')
    parser.add_argument('-a', '--action', type=str, choices=['search', 'everything'],
                       help='直接执行指定功能')
    parser.add_argument('-q', '--query', type=str, help='搜索关键词')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.action == 'search':
        if args.query:
            global script_dir
            script_path = os.path.join(script_dir, "search.py")
            if os.path.exists(script_path):
                import subprocess
                subprocess.run([sys.executable, script_path, '-q', args.query])
            return
        run_search()
        return
    elif args.action == 'everything':
        run_everything()
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_search()
        elif choice == '2':
            run_everything()
        elif choice == '0':
            print("\n返回上级菜单...")
            break
        else:
            print("[错误] 无效选项，请重新输入")
            continue
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()