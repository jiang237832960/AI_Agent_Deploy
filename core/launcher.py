# -*- coding: utf-8 -*-
"""
通用启动框架
提供标准化的启动流程管理
"""

import os
import sys
import json
import time
import argparse
import subprocess
import importlib
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any

VERSION = "1.0.0"

class LauncherError(Exception):
    pass

class DependencyError(LauncherError):
    pass

class ConfigError(LauncherError):
    pass

class ModuleInfo:
    def __init__(self, name: str, display_name: str, description: str,
                 script_path: str, dependencies: List[str] = None,
                 version: str = "1.0.0"):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.script_path = script_path
        self.dependencies = dependencies or []
        self.version = version

class Launcher:
    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = project_root
        self.config_dir = os.path.join(project_root, 'config')
        self.logs_dir = os.path.join(project_root, 'logs')
        self._ensure_dirs()
        self.config = self._load_global_config()
        self.modules: Dict[str, ModuleInfo] = {}
        self.start_time = None
        
    def _ensure_dirs(self):
        for dir_path in [self.config_dir, self.logs_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def _load_global_config(self) -> Dict:
        config_file = os.path.join(self.config_dir, 'settings.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[警告] 加载配置文件失败: {e}")
        return {}
    
    def register_module(self, module: ModuleInfo):
        self.modules[module.name] = module
    
    def register_modules(self, modules: List[ModuleInfo]):
        for module in modules:
            self.register_module(module)
    
    def check_python_version(self, min_version: tuple = (3, 7)) -> bool:
        current = sys.version_info[:2]
        if current < min_version:
            print(f"[错误] Python版本过低: {sys.version}")
            print(f"[要求] 需要 Python {min_version[0]}.{min_version[1]} 或更高版本")
            return False
        print(f"[信息] Python版本: {sys.version.split()[0]} ✓")
        return True
    
    def check_dependencies(self, dependencies: List[str]) -> Dict[str, bool]:
        results = {}
        all_ok = True
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                results[dep] = True
                print(f"[信息] 依赖 {dep} ✓")
            except ImportError:
                results[dep] = False
                all_ok = False
                print(f"[警告] 依赖 {dep} 未安装")
        
        return results
    
    def check_module_dependencies(self, module_name: str) -> bool:
        if module_name not in self.modules:
            print(f"[错误] 未找到模块: {module_name}")
            return False
        
        module = self.modules[module_name]
        if not module.dependencies:
            return True
        
        print(f"\n[检查] 模块 {module.display_name} 依赖...")
        results = self.check_dependencies(module.dependencies)
        
        failed = [k for k, v in results.items() if not v]
        if failed:
            print(f"[警告] 以下依赖未安装: {', '.join(failed)}")
            return False
        return True
    
    def load_module_config(self, module_name: str) -> Dict:
        module = self.modules.get(module_name)
        if not module:
            return {}
        
        module_dir = os.path.dirname(module.script_path)
        config_file = os.path.join(os.path.dirname(module_dir), 'config', 'settings.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[警告] 加载模块配置失败: {e}")
        return {}
    
    def run_module(self, module_name: str, args: List[str] = None) -> int:
        if module_name not in self.modules:
            print(f"[错误] 未找到模块: {module_name}")
            return 1
        
        module = self.modules[module_name]
        
        if not self.check_module_dependencies(module_name):
            return 1
        
        script_path = module.script_path
        if not os.path.exists(script_path):
            print(f"[错误] 脚本文件不存在: {script_path}")
            return 1
        
        self.start_time = time.time()
        
        try:
            if args:
                cmd = [sys.executable, script_path] + args
            else:
                cmd = [sys.executable, script_path]
            
            result = subprocess.run(cmd, cwd=os.path.dirname(script_path))
            return result.returncode
        except Exception as e:
            print(f"[错误] 运行模块失败: {e}")
            return 1
    
    def run_module_direct(self, module_name: str, args: List[str] = None) -> int:
        if module_name not in self.modules:
            print(f"[错误] 未找到模块: {module_name}")
            return 1
        
        module = self.modules[module_name]
        
        print("\n" + "=" * 50)
        print(f"  {module.display_name}".center(40))
        print(f"  版本: {module.version}".center(40))
        print("=" * 50 + "\n")
        
        if not self.check_module_dependencies(module_name):
            return 1
        
        script_path = module.script_path
        if not os.path.exists(script_path):
            print(f"[错误] 脚本文件不存在: {script_path}")
            return 1
        
        self.start_time = time.time()
        
        script_dir = os.path.dirname(script_path)
        original_dir = os.getcwd()
        original_argv = sys.argv.copy()
        
        try:
            os.chdir(script_dir)
            if args:
                sys.argv = [script_path] + args
            else:
                sys.argv = [script_path]
            
            import importlib.util
            spec = importlib.util.spec_from_file_location("__main__", script_path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["__main__"] = mod
            spec.loader.exec_module(mod)
            
            return 0
        except SystemExit as e:
            return e.code if e.code else 0
        except Exception as e:
            print(f"[错误] 运行模块失败: {e}")
            import traceback
            traceback.print_exc()
            return 1
        finally:
            os.chdir(original_dir)
            sys.argv = original_argv
    
    def show_status(self, module_name: str = None):
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        print("\n" + "-" * 50)
        print(f"  启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if module_name:
            print(f"  运行模块: {module_name}")
        print(f"  耗时: {elapsed:.2f} 秒")
        print("-" * 50 + "\n")
    
    def list_modules(self):
        print("\n可用模块列表:")
        print("-" * 50)
        for name, module in self.modules.items():
            print(f"  {name:20} - {module.description}")
        print("-" * 50 + "\n")
    
    def show_menu(self) -> Optional[str]:
        print("\n" + "=" * 50)
        print("  AI 助手工具集".center(40))
        print(f"  版本: {VERSION}".center(40))
        print("=" * 50 + "\n")
        
        print("请选择功能模块:\n")
        items = list(self.modules.items())
        for i, (name, module) in enumerate(items, 1):
            print(f"  {i}. {module.display_name}")
            print(f"     {module.description}\n")
        
        print(f"  {len(items) + 1}. 退出\n")
        
        try:
            choice = input("请输入选项: ").strip()
            if not choice:
                return None
            
            idx = int(choice)
            if 1 <= idx <= len(items):
                return items[idx - 1][0]
            elif idx == len(items) + 1:
                return None
            else:
                print("[错误] 无效选项")
                return None
        except ValueError:
            print("[错误] 请输入数字")
            return None
    
    def interactive_mode(self):
        while True:
            module_name = self.show_menu()
            if module_name is None:
                print("\n感谢使用，再见！\n")
                break
            
            self.run_module_direct(module_name)
            input("\n按回车键继续...")

def create_launcher(project_root: str = None) -> Launcher:
    return Launcher(project_root)

def get_default_modules(project_root: str) -> List[ModuleInfo]:
    return [
        ModuleInfo(
            name="system_info",
            display_name="系统环境检测",
            description="检测系统硬件信息（CPU、内存、硬盘、显卡等）及内存详细分析",
            script_path=os.path.join(project_root, "system_info_checker", "scripts", "start.py"),
            version="1.0.0"
        ),
        ModuleInfo(
            name="dev_env",
            display_name="开发环境配置",
            description="检测并一键部署开发环境（Node.js、Python、Java等）",
            script_path=os.path.join(project_root, "dev_env_setup", "scripts", "start.py"),
            version="1.0.0"
        ),
        ModuleInfo(
            name="github_accelerator",
            display_name="GitHub 加速",
            description="检测GitHub访问状态，配置镜像加速",
            script_path=os.path.join(project_root, "github_accelerator", "scripts", "start.py"),
            version="1.0.0"
        ),
        ModuleInfo(
            name="file_search",
            display_name="文件搜索",
            description="快速搜索本地文件",
            script_path=os.path.join(project_root, "file_search", "scripts", "start.py"),
            version="1.0.0"
        ),
    ]

def parse_args():
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
        '-a', '--args',
        type=str,
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
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    launcher = create_launcher(project_root)
    
    launcher.register_modules(get_default_modules(project_root))
    
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
        
        exit_code = launcher.run_module_direct(module_name, args.args)
        launcher.show_status(module_name)
        sys.exit(exit_code)
    
    launcher.interactive_mode()

if __name__ == "__main__":
    main()