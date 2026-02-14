# -*- coding: utf-8 -*-
"""
项目一键部署脚本
功能：先检测所有环境，再列出适配项目供用户选择
"""

import subprocess
import os
import json
import sys
import urllib.request

def check_all_environments():
    """检测所有已安装的开发环境"""
    envs = {}
    
    tools = {
        'node': ('node', '--version', 'Node.js'),
        'python': ('python', '--version', 'Python'),
        'java': ('java', '--version', 'Java'),
        'go': ('go', 'version', 'Go'),
        'git': ('git', '--version', 'Git'),
    }
    
    for key, (cmd, arg, name) in tools.items():
        try:
            result = subprocess.run(
                [cmd, arg],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                envs[key] = {'name': name, 'version': version, 'installed': True}
            else:
                envs[key] = {'name': name, 'version': None, 'installed': False}
        except:
            envs[key] = {'name': name, 'version': None, 'installed': False}
    
    return envs

def get_available_projects(envs):
    """根据已安装的环境获取可部署的项目"""
    projects = []
    
    if envs.get('node', {}).get('installed'):
        projects.append({
            'id': 'frontend',
            'name': '前端项目 (Vue/React/Next.js)',
            'require': 'Node.js',
            'tool': 'node',
            'git_url': 'https://github.com/vuejs/create-vue.git',
            'install_cmd': 'npm install',
            'dev_cmd': 'npm run dev',
            'project_name': 'vue3'
        })
    
    if envs.get('python', {}).get('installed'):
        projects.append({
            'id': 'python',
            'name': 'Python Web (FastAPI/Django/Flask)',
            'require': 'Python',
            'tool': 'python',
            'git_url': 'https://github.com/tiangolo/fastapi.git',
            'install_cmd': 'pip install -r requirements.txt',
            'dev_cmd': 'uvicorn main:app --reload',
            'project_name': 'fastapi'
        })
    
    if envs.get('node', {}).get('installed'):
        projects.append({
            'id': 'nodejs',
            'name': 'Node.js 后端 (Express/NestJS)',
            'require': 'Node.js',
            'tool': 'node',
            'git_url': 'https://github.com/expressjs/express.git',
            'install_cmd': 'npm install',
            'dev_cmd': 'node index.js',
            'project_name': 'express'
        })
    
    if envs.get('java', {}).get('installed'):
        projects.append({
            'id': 'java',
            'name': 'Java 项目 (Spring Boot)',
            'require': 'Java',
            'tool': 'java',
            'git_url': 'https://github.com/spring-projects/spring-boot.git',
            'install_cmd': 'mvn install -DskipTests',
            'dev_cmd': 'mvn spring-boot:run',
            'project_name': 'springboot'
        })
    
    if envs.get('go', {}).get('installed'):
        projects.append({
            'id': 'go',
            'name': 'Go 项目 (Gin)',
            'require': 'Go',
            'tool': 'go',
            'git_url': 'https://github.com/gin-gonic/gin.git',
            'install_cmd': 'go mod download',
            'dev_cmd': 'go run main.go',
            'project_name': 'gin'
        })
    
    return projects

def get_all_projects():
    """获取所有可用项目"""
    return [
        {
            'id': 'frontend',
            'name': '前端项目 (Vue/React/Next.js)',
            'require': 'Node.js',
            'tool': 'node',
            'git_url': 'https://github.com/vuejs/create-vue.git',
            'install_cmd': 'npm install',
            'dev_cmd': 'npm run dev',
            'project_name': 'vue3'
        },
        {
            'id': 'python',
            'name': 'Python Web (FastAPI/Django/Flask)',
            'require': 'Python',
            'tool': 'python',
            'git_url': 'https://github.com/tiangolo/fastapi.git',
            'install_cmd': 'pip install -r requirements.txt',
            'dev_cmd': 'uvicorn main:app --reload',
            'project_name': 'fastapi'
        },
        {
            'id': 'nodejs',
            'name': 'Node.js 后端 (Express/NestJS)',
            'require': 'Node.js',
            'tool': 'node',
            'git_url': 'https://github.com/expressjs/express.git',
            'install_cmd': 'npm install',
            'dev_cmd': 'node index.js',
            'project_name': 'express'
        },
        {
            'id': 'java',
            'name': 'Java 项目 (Spring Boot)',
            'require': 'Java',
            'tool': 'java',
            'git_url': 'https://github.com/spring-projects/spring-boot.git',
            'install_cmd': 'mvn install -DskipTests',
            'dev_cmd': 'mvn spring-boot:run',
            'project_name': 'springboot'
        },
        {
            'id': 'go',
            'name': 'Go 项目 (Gin)',
            'require': 'Go',
            'tool': 'go',
            'git_url': 'https://github.com/gin-gonic/gin.git',
            'install_cmd': 'go mod download',
            'dev_cmd': 'go run main.go',
            'project_name': 'gin'
        }
    ]

def install_git():
    """安装 Git"""
    print("\n正在下载 Git...")
    url = "https://git-scm.com/download/win"
    try:
        subprocess.Popen(['start', url])
    except:
        print(f"请访问 {url} 下载 Git")
    
    print("[!] 已打开浏览器，请下载并安装 Git")
    print("[!] 安装完成后，请重新运行部署脚本")
    input("\n按回车键退出...")
    sys.exit(1)

def select_directory():
    """让用户选择安装目录"""
    print("\n请选择安装目录（建议选择非系统盘，如 D:\\Projects）")
    print("示例：D:\\Projects\\my-project")
    print()
    
    while True:
        path = input("请输入安装路径：").strip().strip('"')
        
        if not path:
            print("路径不能为空，请重新输入！")
            continue
        
        drive = os.path.splitdrive(path)[0]
        if drive:
            drive_letter = drive[0].upper()
            if drive_letter in ['C', 'D', 'E', 'F', 'G']:
                confirm = input(f"检测到您选择的是 {drive_letter} 盘，确定继续吗？(y/n): ").strip().lower()
                if confirm != 'y':
                    continue
        
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            try:
                os.makedirs(parent, exist_ok=True)
            except Exception as e:
                print(f"无法创建目录：{e}")
                continue
        
        return path

def clone_project(git_url, target_dir):
    """克隆项目"""
    print(f"\n正在从 GitHub 克隆项目...")
    print(f"仓库地址：{git_url}")
    
    try:
        if os.path.exists(target_dir):
            print(f"目标目录已存在，跳过克隆")
            return True
        
        result = subprocess.run(
            ['git', 'clone', git_url, target_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("克隆成功！")
            return True
        else:
            print(f"克隆失败：{result.stderr}")
            return False
    except FileNotFoundError:
        print("未找到 Git，正在安装...")
        install_git()
        return False
    except subprocess.TimeoutExpired:
        print("克隆超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"克隆失败：{e}")
        return False

def install_dependencies(project_dir, install_cmd):
    """安装依赖"""
    print(f"\n正在安装依赖...")
    print(f"执行命令：{install_cmd}")
    
    try:
        os.chdir(project_dir)
        result = subprocess.run(
            install_cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("依赖安装成功！")
            return True
        else:
            print(f"安装失败：{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("安装超时，请检查网络或手动安装")
        return False
    except Exception as e:
        print(f"安装失败：{e}")
        return False

def create_start_script(project_dir, project_type, dev_cmd):
    """生成启动脚本"""
    print(f"\n正在生成启动脚本...")
    
    script_content = f'''@echo off
chcp 65001 >nul
title {project_type} 项目

cd /d "%~dp0"

echo ========================================
echo      正在启动 {project_type} 项目...
echo ========================================
echo.

{dev_cmd}

pause
'''
    
    script_path = os.path.join(project_dir, 'start.bat')
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"启动脚本已生成：start.bat")
        return True
    except Exception as e:
        print(f"生成启动脚本失败：{e}")
        return False

def main():
    print("\n" + "="*50)
    print("         项目一键部署".center(40))
    print("="*50 + "\n")
    
    print("="*50)
    print("     第一步：检测已安装的开发环境".center(40))
    print("="*50 + "\n")
    
    envs = check_all_environments()
    
    for key, env in envs.items():
        if env['installed']:
            print(f"   [√] {env['name']}: {env['version']}")
        else:
            print(f"   [ ] {env['name']}: 未安装")
    
    print("\n" + "="*50)
    print("     第二步：选择要部署的项目".center(40))
    print("="*50 + "\n")
    
    available_projects = get_available_projects(envs)
    
    if available_projects:
        print("根据您已安装的环境，可部署以下项目：\n")
        
        for i, proj in enumerate(available_projects, 1):
            print(f"  {i}. {proj['name']} - 需要 {proj['require']}")
        
        print(f"\n  0. 查看所有项目（即使环境未安装）")
        
        print()
        choice = input(f"请输入选项 (0-{len(available_projects)}): ").strip()
        
        if choice == '0':
            projects = get_all_projects()
            print("\n所有可用项目：\n")
            for i, proj in enumerate(projects, 1):
                print(f"  {i}. {proj['name']} - 需要 {proj['require']}")
            print()
            full_choice = input(f"请输入选项 (1-{len(projects)}): ").strip()
            try:
                idx = int(full_choice) - 1
                if 0 <= idx < len(projects):
                    selected_project = projects[idx]
                else:
                    print("无效选项！")
                    return
            except ValueError:
                print("请输入数字！")
                return
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(available_projects):
                    selected_project = available_projects[idx]
                else:
                    print("无效选项！")
                    return
            except ValueError:
                print("请输入数字！")
                return
    else:
        print("未检测到任何开发环境，请先安装以下任意环境：")
        print("  - Node.js (前端项目)")
        print("  - Python (Python Web项目)")
        print("  - Java (Java项目)")
        print("  - Go (Go项目)")
        print()
        
        print("或者选择查看所有项目：\n")
        print("  0. 查看所有项目")
        
        print()
        choice = input("请输入选项 (0): ").strip()
        
        if choice == '0':
            projects = get_all_projects()
            print("\n所有可用项目：\n")
            for i, proj in enumerate(projects, 1):
                print(f"  {i}. {proj['name']} - 需要 {proj['require']}")
            print()
            full_choice = input(f"请输入选项 (1-{len(projects)}): ").strip()
            try:
                idx = int(full_choice) - 1
                if 0 <= idx < len(projects):
                    selected_project = projects[idx]
                else:
                    print("无效选项！")
                    return
            except ValueError:
                print("请输入数字！")
                return
        else:
            return
    
    print(f"\n已选择：{selected_project['name']}")
    
    target_dir = select_directory()
    
    if not clone_project(selected_project['git_url'], target_dir):
        input("\n按回车键退出...")
        return
    
    if selected_project['install_cmd']:
        if not install_dependencies(target_dir, selected_project['install_cmd']):
            print("依赖安装失败，但您可以稍后手动安装")
    
    create_start_script(target_dir, selected_project['project_name'], selected_project['dev_cmd'])
    
    print("\n" + "="*50)
    print("         部署完成！".center(40))
    print("="*50)
    print(f"\n项目路径：{target_dir}")
    print(f"启动命令：双击 start.bat 或手动运行对应命令")
    print()
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
