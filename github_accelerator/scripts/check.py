# -*- coding: utf-8 -*-
"""
GitHub 访问检测脚本
功能：检测 GitHub 访问状态和速度
"""

import subprocess
import time
import json
import os
import sys
import socket
import urllib.request
import urllib.error

def test_connection(url, timeout=10):
    """测试连接状态和速度"""
    try:
        start_time = time.time()
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        content = response.read(1024)  # 只读取前1KB
        elapsed = (time.time() - start_time) * 1000
        
        speed = len(content) / elapsed * 1000  # KB/s
        
        return {
            "accessible": True,
            "latency": int(elapsed),
            "speed": round(speed, 1),
            "status_code": response.getcode()
        }
    except urllib.error.URLError as e:
        return {
            "accessible": False,
            "latency": None,
            "speed": None,
            "error": str(e)
        }
    except Exception as e:
        return {
            "accessible": False,
            "latency": None,
            "speed": None,
            "error": str(e)
        }

def test_ping(host, timeout=5):
    """测试 ping 延迟"""
    try:
        result = subprocess.run(
            ['ping', '-n', '1', '-w', str(timeout * 1000), host],
            capture_output=True,
            text=True,
            timeout=timeout + 1
        )
        
        output = result.stdout
        if '平均' in output or 'Average' in output:
            # 提取延迟数值
            if '平均' in output:
                parts = output.split('平均 = ')[1].split('ms')[0]
            else:
                parts = output.split('Average = ')[1].split('ms')[0]
            
            latency = int(parts.split('/')[1].replace('ms', ''))
            return latency
        return None
    except:
        return None

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'mirrors.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def print_header():
    """打印头部"""
    print("\n" + "="*50)
    print("       GitHub 访问状态检测".center(40))
    print("="*50 + "\n")

def main():
    print_header()
    
    print("正在检测 GitHub 访问状态，请稍候...\n")
    
    config = load_config()
    test_urls = config.get('test_urls', []) if config else []
    
    if not test_urls:
        test_urls = [
            "https://github.com",
            "https://raw.githubusercontent.com",
            "https://github.com/facebook/react"
        ]
    
    results = []
    
    # 测试主要域名
    domains = [
        ("github.com", "https://github.com"),
        ("raw.githubusercontent.com", "https://raw.githubusercontent.com"),
        ("githubusercontent.com", "https://github.com/facebook/react")
    ]
    
    print("【主要域名检测】\n")
    
    for name, url in domains:
        print(f"检测 {name}...")
        result = test_connection(url, timeout=15)
        
        status = "可访问" if result["accessible"] else "无法访问"
        
        if result["accessible"]:
            print(f"  状态：{status}")
            print(f"  延迟：{result['latency']} ms")
            print(f"  速度：{result['speed']} KB/s")
        else:
            print(f"  状态：{status}")
            if result.get("error"):
                print(f"  错误：{result['error'][:50]}")
        
        print()
        results.append((name, result))
    
    # 测试镜像源
    if config and config.get('mirrors'):
        print("【镜像源检测】\n")
        
        mirror_results = []
        
        for mirror in config['mirrors']:
            name = mirror['name']
            test_url = mirror.get('test_url', '')
            
            if not test_url:
                continue
            
            print(f"检测 {name}...")
            result = test_connection(test_url, timeout=10)
            
            if result["accessible"]:
                status = "可访问"
                print(f"  状态：{status}")
                print(f"  延迟：{result['latency']} ms")
                print(f"  速度：{result['speed']} KB/s")
                mirror_results.append((name, result['latency'], result['speed']))
            else:
                status = "无法访问"
                print(f"  状态：{status}")
            
            print()
        
        # 推荐最优镜像
        if mirror_results:
            print("【推荐】\n")
            
            # 按延迟排序
            mirror_results.sort(key=lambda x: x[1])
            
            best = mirror_results[0]
            print(f"  最低延迟：{best[0]} ({best[1]} ms)\n")
    
    print("="*50)
    print("       检测完成！".center(40))
    print("="*50 + "\n")
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()
