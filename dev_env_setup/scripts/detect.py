# -*- coding: utf-8 -*-
"""
开发环境检测脚本
功能：检测系统中已安装的开发工具
"""

import subprocess
import os
import json

def check_tool(name, cmd):
    """检测工具是否已安装"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            return {"installed": True, "version": version}
        else:
            return {"installed": False, "version": None}
    except FileNotFoundError:
        return {"installed": False, "version": None}
    except Exception as e:
        return {"installed": False, "version": None, "error": str(e)}

def get_tool_path(cmd):
    """获取工具路径"""
    try:
        result = subprocess.run(
            f"where {cmd.split()[0]}",
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    return None

def detect_nodejs():
    """检测 Node.js"""
    info = check_tool("node", "node --version")
    if info["installed"]:
        info["path"] = get_tool_path("node")
        npm_info = check_tool("npm", "npm --version")
        info["npm_version"] = npm_info["version"] if npm_info["installed"] else None
    return info

def detect_python():
    """检测 Python"""
    info = check_tool("python", "python --version")
    if info["installed"]:
        info["path"] = get_tool_path("python")
    return info

def detect_java():
    """检测 Java"""
    info = check_tool("java", "java --version")
    if info["installed"]:
        info["path"] = get_tool_path("java")
        javac_info = check_tool("javac", "javac --version")
        info["javac"] = javac_info["version"] if javac_info["installed"] else None
    return info

def detect_go():
    """检测 Go"""
    info = check_tool("go", "go version")
    if info["installed"]:
        info["path"] = get_tool_path("go")
    return info

def detect_rust():
    """检测 Rust"""
    info = check_tool("rustc", "rustc --version")
    if info["installed"]:
        info["path"] = get_tool_path("rustc")
    return info

def detect_docker():
    """检测 Docker"""
    info = check_tool("docker", "docker --version")
    if info["installed"]:
        info["path"] = get_tool_path("docker")
    return info

def detect_git():
    """检测 Git"""
    info = check_tool("git", "git --version")
    if info["installed"]:
        info["path"] = get_tool_path("git")
    return info

def print_header():
    """打印头部"""
    print("\n" + "="*50)
    print("         开发环境检测报告".center(40))
    print("="*50 + "\n")

def main():
    print_header()
    
    print("正在检测开发环境，请稍候...\n")
    
    # 检测各项工具
    tools = {
        "Node.js": detect_nodejs(),
        "Python": detect_python(),
        "Java": detect_java(),
        "Go": detect_go(),
        "Rust": detect_rust(),
        "Docker": detect_docker(),
        "Git": detect_git()
    }
    
    # 打印结果
    for name, info in tools.items():
        print(f"【{name}】")
        if info["installed"]:
            print(f"  状态：已安装")
            print(f"  版本：{info.get('version', '未知')}")
            if info.get("path"):
                print(f"  路径：{info['path']}")
            if info.get("npm_version"):
                print(f"  npm：{info['npm_version']}")
            if info.get("javac"):
                print(f"  javac：{info['javac']}")
        else:
            print(f"  状态：未安装")
            print(f"  建议：从官方网站下载安装")
        print()
    
    # 统计
    installed_count = sum(1 for t in tools.values() if t["installed"])
    total_count = len(tools)
    
    print("="*50)
    print(f"         检测完成！已安装 {installed_count}/{total_count}")
    print("="*50 + "\n")
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
