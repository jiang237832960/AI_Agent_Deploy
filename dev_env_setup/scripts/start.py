# -*- coding: utf-8 -*-
"""
开发环境配置模块启动脚本
"""

import os
import sys
import argparse

VERSION = "1.0.0"

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def show_menu():
    print("\n" + "=" * 50)
    print("  开发环境配置".center(40))
    print(f"  版本: {VERSION}".center(40))
    print("=" * 50 + "\n")
    
    print("请选择功能:\n")
    print("  1. 检测开发环境")
    print("  2. 一键部署项目")
    print("  0. 返回上级菜单\n")
    
    choice = input("请输入选项: ").strip()
    return choice

def run_detect():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "detect.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        script_path = os.path.join(script_dir, "detect.bat")
        if os.path.exists(script_path):
            os.system(script_path)
        else:
            print("[错误] 未找到环境检测脚本")

def run_deploy():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "deploy.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        script_path = os.path.join(script_dir, "deploy.bat")
        if os.path.exists(script_path):
            os.system(script_path)
        else:
            print("[错误] 未找到部署脚本")

def parse_args():
    parser = argparse.ArgumentParser(description='开发环境配置模块')
    parser.add_argument('-a', '--action', type=str, choices=['detect', 'deploy'],
                       help='直接执行指定功能')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.action == 'detect':
        run_detect()
        return
    elif args.action == 'deploy':
        run_deploy()
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_detect()
        elif choice == '2':
            run_deploy()
        elif choice == '0':
            print("\n返回上级菜单...")
            break
        else:
            print("[错误] 无效选项，请重新输入")
            continue
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()