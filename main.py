# -*- coding: utf-8 -*-
"""
AI 助手工具集 - 主启动脚本
统一入口管理所有子模块
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.launcher import (
    create_launcher, 
    get_default_modules, 
    VERSION
)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='AI 助手工具集 - 统一启动入口',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-m', '--module',
        type=str,
        help='直接启动指定模块'
    )
    parser.add_argument(
        'extra_args',
        nargs='*',
        help='传递给模块的参数'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='列出所有可用模块'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'AI 助手工具集 v{VERSION}'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    launcher = create_launcher(PROJECT_ROOT)
    launcher.register_modules(get_default_modules(PROJECT_ROOT))
    
    if not launcher.check_python_version():
        sys.exit(1)
    
    if args.list:
        launcher.list_modules()
        return
    
    if args.module:
        module_name = args.module
        if module_name not in launcher.modules:
            print(f"[错误] 未找到模块: {module_name}")
            print("使用 --list 查看所有可用模块")
            sys.exit(1)
        
        exit_code = launcher.run_module_direct(module_name, args.extra_args)
        launcher.show_status(module_name)
        sys.exit(exit_code)
    
    launcher.interactive_mode()

if __name__ == "__main__":
    main()