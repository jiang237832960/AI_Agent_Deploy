# -*- coding: utf-8 -*-
"""
GitHub 加速模块启动脚本
"""

import os
import sys
import argparse

VERSION = "1.0.0"

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def show_menu():
    print("\n" + "=" * 50)
    print("  GitHub 加速".center(40))
    print(f"  版本: {VERSION}".center(40))
    print("=" * 50 + "\n")
    
    print("请选择功能:\n")
    print("  1. 检测 GitHub 访问状态")
    print("  2. 配置加速")
    print("  3. 监控镜像源状态")
    print("  4. 更新镜像配置")
    print("  5. 还原配置")
    print("  0. 返回上级菜单\n")
    
    choice = input("请输入选项: ").strip()
    return choice

def run_check():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "check.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        print("[错误] 未找到检测脚本")

def run_accelerate():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "accelerate.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        script_path = os.path.join(script_dir, "accelerate.bat")
        if os.path.exists(script_path):
            os.system(script_path)
        else:
            print("[错误] 未找到加速配置脚本")

def run_monitor():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "monitor.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        print("[错误] 未找到监控脚本")

def run_updater():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "updater.py")
    
    if os.path.exists(script_path):
        import subprocess
        subprocess.run([sys.executable, script_path])
    else:
        print("[错误] 未找到更新脚本")

def run_restore():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "restore.bat")
    
    if os.path.exists(script_path):
        os.system(script_path)
    else:
        print("[错误] 未找到还原脚本")

def parse_args():
    parser = argparse.ArgumentParser(description='GitHub 加速模块')
    parser.add_argument('-a', '--action', type=str, 
                       choices=['check', 'accelerate', 'monitor', 'update', 'restore'],
                       help='直接执行指定功能')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.action == 'check':
        run_check()
        return
    elif args.action == 'accelerate':
        run_accelerate()
        return
    elif args.action == 'monitor':
        run_monitor()
        return
    elif args.action == 'update':
        run_updater()
        return
    elif args.action == 'restore':
        run_restore()
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_check()
        elif choice == '2':
            run_accelerate()
        elif choice == '3':
            run_monitor()
        elif choice == '4':
            run_updater()
        elif choice == '5':
            run_restore()
        elif choice == '0':
            print("\n返回上级菜单...")
            break
        else:
            print("[错误] 无效选项，请重新输入")
            continue
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()