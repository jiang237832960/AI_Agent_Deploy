# -*- coding: utf-8 -*-
"""
文件搜索脚本（集成 Everything）
功能：使用 Everything 进行极速文件搜索
"""

import subprocess
import os
import json
import sys
import urllib.request
import zipfile

def get_script_dir():
    """获取脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(get_script_dir()), 'config', 'settings.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_everything_path():
    """获取 Everything 路径"""
    base_dir = os.path.abspath(os.path.join(get_script_dir(), '..', '..'))
    es_path = os.path.join(base_dir, 'tools', 'Everything', 'es.exe')
    
    if os.path.exists(es_path):
        return es_path
    
    alt_paths = [
        os.path.join(base_dir, 'tools', 'Everything', 'es.exe'),
        r'C:\Program Files\Everything\es.exe',
        r'C:\Program Files (x86)\Everything\es.exe',
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_everything_dir():
    """获取 Everything 目录"""
    base_dir = os.path.abspath(os.path.join(get_script_dir(), '..', '..'))
    return os.path.join(base_dir, 'tools', 'Everything')

def download_everything():
    """自动下载 Everything"""
    es_dir = get_everything_dir()
    
    if not os.path.exists(es_dir):
        os.makedirs(es_dir, exist_ok=True)
    
    print("   [!] 未找到 Everything，正在下载...")
    print()
    
    es_zip = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'Everything.zip')
    download_url = "https://www.voidtools.com/Everything-1.4a.zip"
    
    print(f"正在下载 Everything...")
    print(f"下载地址：{download_url}")
    print()
    
    try:
        def download_progress(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size) if total_size > 0 else 0
            print(f"\r下载进度: {percent}%", end='', flush=True)
        
        urllib.request.urlretrieve(download_url, es_zip, download_progress)
        print()
    except Exception as e:
        print()
        print("[!] 自动下载失败，正在打开浏览器...")
        try:
            subprocess.Popen(['start', 'https://www.voidtools.com/zh-cn/downloads/'])
        except:
            pass
        return None
    
    print("下载完成，正在解压...")
    print()
    
    try:
        with zipfile.ZipFile(es_zip, 'r') as zip_ref:
            zip_ref.extractall(es_dir)
        os.remove(es_zip)
    except Exception as e:
        print(f"[!] 解压失败：{e}")
        return None
    
    es_path = os.path.join(es_dir, 'es.exe')
    if os.path.exists(es_path):
        print("   [√] Everything 下载完成")
        print(f"   路径：{es_path}")
        print()
        print("提示：首次运行会建立索引，请稍候...")
        return es_path
    
    return None

def check_everything():
    """检查 Everything 是否可用，不存在则自动下载"""
    es_path = get_everything_path()
    
    if es_path:
        return es_path
    
    print("未找到 Everything，需要下载")
    choice = input("是否现在下载？(y/n): ").strip().lower()
    
    if choice == 'y' or choice == '是':
        return download_everything()
    
    return None

def search_filename(es_path, keyword, max_results=100):
    """按文件名搜索"""
    try:
        result = subprocess.run(
            [es_path, keyword, '-n', str(max_results)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        else:
            return []
    except Exception as e:
        print(f"搜索出错：{e}")
        return []

def search_extension(es_path, ext, max_results=100):
    """按扩展名搜索"""
    keyword = f"*.{ext}"
    return search_filename(es_path, keyword, max_results)

def search_size(es_path, size_condition, max_results=100):
    """按大小搜索"""
    try:
        result = subprocess.run(
            [es_path, f"size:{size_condition}", '-n', str(max_results)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        else:
            return []
    except Exception as e:
        print(f"搜索出错：{e}")
        return []

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def parse_search_result(line):
    """解析搜索结果行"""
    parts = line.split('\t')
    
    if len(parts) >= 2:
        path = parts[0]
        size_str = parts[1] if len(parts) > 1 else '0'
        
        try:
            size = int(size_str)
            size_formatted = format_size(size)
        except:
            size_formatted = '未知'
        
        return {
            'path': path,
            'size': size_formatted,
            'size_bytes': int(size_str) if size_str.isdigit() else 0
        }
    
    return {'path': line, 'size': '未知', 'size_bytes': 0}

def main():
    print("\n" + "="*50)
    print("         文件搜索（Everything）".center(40))
    print("="*50 + "\n")
    
    es_path = check_everything()
    
    if not es_path:
        print("\n无法使用 Everything 功能")
        input("\n按回车键退出...")
        return
    
    config = load_config()
    max_results = config.get('max_results', 100) if config else 100
    
    print(f"Everything 路径：{es_path}\n")
    
    print("请选择搜索方式：\n")
    print("  1. 按文件名搜索")
    print("  2. 按扩展名搜索")
    print("  3. 按大小搜索")
    print()
    
    while True:
        try:
            choice = input("请输入选项 (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("无效选项，请重新输入！")
        except:
            pass
    
    results = []
    
    if choice == '1':
        keyword = input("\n请输入搜索关键词：").strip()
        if keyword:
            print(f"\n正在搜索：{keyword}...")
            results = search_filename(es_path, keyword, max_results)
    
    elif choice == '2':
        ext = input("\n请输入扩展名（如：py, js, txt）：").strip().strip('.')
        if ext:
            print(f"\n正在搜索 *.{ext} 文件...")
            results = search_extension(es_path, ext, max_results)
    
    elif choice == '3':
        print("\n大小条件示例：")
        print("  >10MB  - 大于 10MB")
        print("  <100KB - 小于 100KB")
        print("  1MB-10MB - 1MB 到 10MB 之间")
        print()
        
        size_cond = input("请输入大小条件：").strip()
        if size_cond:
            print(f"\n正在搜索符合条件的文件...")
            results = search_size(es_path, size_cond, max_results)
    
    print("\n" + "="*50)
    print(f"         搜索结果".center(40))
    print("="*50 + "\n")
    
    valid_results = [r for r in results if r.strip()]
    
    if valid_results:
        print(f"找到 {len(valid_results)} 个结果：\n")
        
        for i, line in enumerate(valid_results[:max_results], 1):
            info = parse_search_result(line)
            print(f"{i}. {info['path']}")
            print(f"   大小：{info['size']}")
            print()
    else:
        print("未找到匹配结果")
        print()
    
    print("="*50)
    print("         搜索完成！".center(40))
    print("="*50 + "\n")
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
