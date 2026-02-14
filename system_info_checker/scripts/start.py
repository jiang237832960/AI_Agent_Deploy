# -*- coding: utf-8 -*-
"""
系统环境检测模块启动脚本
"""

import os
import sys
import argparse
import subprocess

VERSION = "1.0.0"

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def show_menu():
    print("\n" + "=" * 50)
    print("  系统环境检测".center(40))
    print(f"  版本: {VERSION}".center(40))
    print("=" * 50 + "\n")
    
    print("请选择功能:\n")
    print("  1. 系统硬件信息检测")
    print("  2. 内存详细分析")
    print("  0. 返回上级菜单\n")
    
    choice = input("请输入选项: ").strip()
    return choice

def run_system_info():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "system_info.bat")
    
    if os.path.exists(script_path):
        subprocess.run(script_path, shell=True)
    else:
        print("[错误] 未找到系统检测脚本")

def run_memory_checker():
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, "memory_checker.bat")
    
    if os.path.exists(script_path):
        subprocess.run(script_path, shell=True)
    else:
        print("[错误] 未找到内存检测脚本")

def parse_args():
    parser = argparse.ArgumentParser(description='系统环境检测模块')
    parser.add_argument('-a', '--action', type=str, choices=['system', 'memory'],
                       help='直接执行指定功能')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.action == 'system':
        run_system_info()
        return
    elif args.action == 'memory':
        run_memory_checker()
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_system_info()
        elif choice == '2':
            run_memory_checker()
        elif choice == '0':
            print("\n返回上级菜单...")
            break
        else:
            print("[错误] 无效选项，请重新输入")
            continue
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()