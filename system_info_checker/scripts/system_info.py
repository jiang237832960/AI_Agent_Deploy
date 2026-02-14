# -*- coding: utf-8 -*-
"""
系统环境检测脚本
功能：检测 Windows 系统详细信息
"""

import subprocess
import platform
import os
import sys

def get_windows_version():
    """获取 Windows 版本信息"""
    try:
        result = subprocess.run(
            ['systeminfo'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        output = result.stdout
        
        info = {}
        for line in output.split('\n'):
            if 'OS 名称' in line:
                info['os_name'] = line.split(':')[-1].strip()
            elif 'OS 版本' in line:
                info['os_version'] = line.split(':')[-1].strip()
            elif '系统类型' in line:
                info['system_type'] = line.split(':')[-1].strip()
            elif '处理器' in line and '已安装' in line:
                info['cpu'] = line.split(':')[-1].strip()
            elif '物理内存总量' in line:
                info['total_memory'] = line.split(':')[-1].strip()
        return info
    except Exception as e:
        return {"error": str(e)}

def get_cpu_info():
    """获取 CPU 信息"""
    try:
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 4:
                return {
                    'name': ' '.join(parts[:-3]),
                    'cores': parts[-3],
                    'threads': parts[-2],
                    'max_mhz': parts[-1]
                }
    except:
        pass
    
    return {
        'name': platform.processor(),
        'cores': '未知',
        'threads': '未知',
        'max_mhz': '未知'
    }

def get_memory_info():
    """获取内存信息"""
    try:
        result = subprocess.run(
            ['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize /Value'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        output = result.stdout
        total = 0
        free = 0
        for line in output.split('\n'):
            if 'TotalVisibleMemorySize' in line:
                total = int(line.split('=')[1]) // 1024
            elif 'FreePhysicalMemory' in line:
                free = int(line.split('=')[1]) // 1024
        
        used = total - free
        used_percent = (used / total * 100) if total > 0 else 0
        
        return {
            'total': f"{total} MB ({total/1024:.1f} GB)",
            'free': f"{free} MB ({free/1024:.1f} GB)",
            'used': f"{used} MB ({used/1024:.1f} GB)",
            'percent': f"{used_percent:.1f}%"
        }
    except Exception as e:
        return {'error': str(e)}

def get_disk_info():
    """获取硬盘信息"""
    disks = []
    try:
        result = subprocess.run(
            ['wmic', 'logicaldisk', 'get', 'DeviceID,Size,FreeSpace,VolumeName'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        lines = result.stdout.strip().split('\n')[1:]
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    device_id = parts[0]
                    if device_id.endswith(':'):
                        try:
                            size = int(parts[1]) // (1024*1024*1024)
                            free = int(parts[2]) // (1024*1024*1024) if len(parts) > 2 else 0
                            used = size - free
                            used_percent = (used / size * 100) if size > 0 else 0
                            volume_name = ' '.join(parts[3:]) if len(parts) > 3 else '本地磁盘'
                            
                            disks.append({
                                'device': device_id,
                                'name': volume_name,
                                'total': size,
                                'free': free,
                                'used': used,
                                'used_percent': used_percent
                            })
                        except:
                            pass
    except Exception as e:
        pass
    return disks

def get_gpu_info():
    """获取显卡信息"""
    gpus = []
    try:
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'Name,AdapterRAM,DriverVersion'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        lines = result.stdout.strip().split('\n')[1:]
        for line in lines:
            if line.strip():
                parts = line.strip().split('  ')
                parts = [p.strip() for p in parts if p.strip()]
                if parts:
                    name = parts[0]
                    ram = parts[1] if len(parts) > 1 else '未知'
                    if 'AdapterRAM' in ram:
                        try:
                            ram_gb = int(ram.split('=')[1]) / (1024**3)
                            ram = f"{ram_gb:.1f} GB"
                        except:
                            ram = '未知'
                    gpus.append({'name': name, 'ram': ram})
    except Exception as e:
        pass
    return gpus

def print_header():
    """打印头部"""
    print("\n" + "="*50)
    print("         系统环境检测报告".center(40))
    print("="*50 + "\n")

def print_section(title):
    """打印章节标题"""
    print(f"\n【{title}】")

def main():
    print_header()
    
    # 操作系统信息
    print_section("操作系统")
    print(f"  系统名称：{platform.system()} {platform.release()}")
    print(f"  版本：{platform.version()}")
    print(f"  架构：{platform.machine()}")
    print(f"  系统位数：{'64位 (x64)' if platform.machine().endswith('64') else '32位 (x86)'}")
    
    # CPU 信息
    print_section("CPU 处理器")
    cpu = get_cpu_info()
    print(f"  型号：{cpu.get('name', '未知')}")
    print(f"  核心数：{cpu.get('cores', '未知')}")
    print(f"  线程数：{cpu.get('threads', '未知')}")
    print(f"  主频：{cpu.get('max_mhz', '未知')} MHz")
    
    # 内存信息
    print_section("内存")
    mem = get_memory_info()
    if 'error' not in mem:
        print(f"  总量：{mem.get('total', '未知')}")
        print(f"  可用：{mem.get('free', '未知')}")
        print(f"  已使用：{mem.get('used', '未知')}")
        print(f"  使用率：{mem.get('percent', '未知')}")
    else:
        print(f"  获取失败：{mem.get('error')}")
    
    # 硬盘信息
    print_section("硬盘")
    disks = get_disk_info()
    for disk in disks:
        print(f"  {disk['device']} ({disk['name']})")
        print(f"    已用 {disk['used']} GB / 总计 {disk['total']} GB  使用率 {disk['used_percent']:.1f}%")
    
    # 显卡信息
    print_section("显卡")
    gpus = get_gpu_info()
    for i, gpu in enumerate(gpus, 1):
        print(f"  显卡 {i}：{gpu.get('name', '未知')}")
        print(f"    显存：{gpu.get('ram', '未知')}")
    
    if not gpus:
        print("  未检测到显卡信息")
    
    print("\n" + "="*50)
    print("         检测完成！".center(40))
    print("="*50 + "\n")
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
