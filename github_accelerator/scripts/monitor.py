# -*- coding: utf-8 -*-
"""
GitHub 镜像源监控检测脚本
功能：定期检测镜像源状态，记录日志，触发告警
"""

import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class MirrorMonitor:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'mirrors.json')
        self.config_path = config_path
        self.config = self.load_config()
        self.log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        self.backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backup')
        self._ensure_dirs()
        
    def _ensure_dirs(self):
        for dir_path in [self.log_dir, self.backup_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def backup_config(self) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'mirrors_{timestamp}.json')
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.log_change('backup', f'配置已备份: {backup_file}')
            self._cleanup_old_backups()
            return backup_file
        except Exception as e:
            self.log_change('error', f'备份失败: {e}')
            return None
    
    def _cleanup_old_backups(self):
        max_count = self.config.get('rollback_config', {}).get('max_backup_count', 10)
        backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith('mirrors_')])
        while len(backups) > max_count:
            old_file = os.path.join(self.backup_dir, backups.pop(0))
            try:
                os.remove(old_file)
            except:
                pass
    
    def log_change(self, change_type: str, message: str, details: Dict = None):
        log_file = os.path.join(self.log_dir, 'change_log.json')
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': change_type,
            'message': message,
            'details': details or {}
        }
        
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(entry)
        
        logs = logs[-1000:]
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except:
            pass
        
        print(f"[{entry['timestamp']}] [{change_type.upper()}] {message}")
    
    def test_mirror(self, mirror: Dict, timeout: int = 10) -> Tuple[bool, Optional[int]]:
        test_url = mirror.get('test_url', '')
        if not test_url:
            return False, None
        
        try:
            start_time = time.time()
            req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=timeout)
            elapsed = int((time.time() - start_time) * 1000)
            
            if response.getcode() == 200:
                return True, elapsed
            return False, None
        except urllib.error.URLError:
            return False, None
        except Exception:
            return False, None
    
    def check_github_access(self) -> Tuple[bool, Optional[int]]:
        try:
            start_time = time.time()
            req = urllib.request.Request('https://github.com', headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            elapsed = int((time.time() - start_time) * 1000)
            return response.getcode() == 200, elapsed
        except:
            return False, None
    
    def check_all_mirrors(self) -> Dict:
        results = {
            'timestamp': datetime.now().isoformat(),
            'github_accessible': False,
            'github_latency': None,
            'mirrors': []
        }
        
        gh_ok, gh_latency = self.check_github_access()
        results['github_accessible'] = gh_ok
        results['github_latency'] = gh_latency
        
        mirrors = self.config.get('mirrors', [])
        
        for mirror in mirrors:
            mirror_id = mirror.get('id', mirror.get('name'))
            success, latency = self.test_mirror(mirror)
            
            mirror['last_check'] = datetime.now().isoformat()
            mirror['check_count'] = mirror.get('check_count', 0) + 1
            
            if success:
                mirror['status'] = 'available'
                mirror['latency_ms'] = latency
                mirror['success_count'] = mirror.get('success_count', 0) + 1
            else:
                mirror['status'] = 'unavailable'
                mirror['latency_ms'] = None
            
            if mirror['check_count'] > 0:
                mirror['success_rate'] = round(mirror['success_count'] / mirror['check_count'], 2)
            
            results['mirrors'].append({
                'id': mirror_id,
                'name': mirror.get('name'),
                'status': mirror['status'],
                'latency_ms': latency,
                'success_rate': mirror['success_rate']
            })
        
        self.config['last_update'] = datetime.now().isoformat()
        self.save_config()
        
        self._check_alerts(results)
        
        return results
    
    def _check_alerts(self, results: Dict):
        alert_config = self.config.get('alert_config', {})
        if not alert_config.get('enabled', True):
            return
        
        min_success_rate = alert_config.get('min_success_rate', 0.5)
        max_latency = alert_config.get('max_latency_ms', 5000)
        
        alerts = []
        
        available_count = sum(1 for m in results['mirrors'] if m['status'] == 'available')
        if available_count == 0 and not results['github_accessible']:
            alerts.append({
                'level': 'critical',
                'message': '所有镜像源和GitHub都无法访问'
            })
        
        for mirror in results['mirrors']:
            if mirror['success_rate'] is not None and mirror['success_rate'] < min_success_rate:
                alerts.append({
                    'level': 'warning',
                    'message': f"镜像 {mirror['name']} 成功率过低: {mirror['success_rate']}"
                })
            
            if mirror['latency_ms'] is not None and mirror['latency_ms'] > max_latency:
                alerts.append({
                    'level': 'warning',
                    'message': f"镜像 {mirror['name']} 延迟过高: {mirror['latency_ms']}ms"
                })
        
        for alert in alerts:
            self.log_change('alert', alert['message'], {'level': alert['level']})
    
    def get_best_mirror(self) -> Optional[Dict]:
        mirrors = self.config.get('mirrors', [])
        available = [m for m in mirrors if m.get('status') == 'available']
        
        if not available:
            return None
        
        available.sort(key=lambda x: x.get('latency_ms', float('inf')))
        return available[0]
    
    def get_status_report(self) -> str:
        results = self.check_all_mirrors()
        
        report = []
        report.append("=" * 50)
        report.append("       GitHub 镜像源状态报告".center(40))
        report.append("=" * 50)
        report.append("")
        
        gh_status = "可访问" if results['github_accessible'] else "无法访问"
        gh_latency = f" ({results['github_latency']}ms)" if results['github_latency'] else ""
        report.append(f"[GitHub 直连] {gh_status}{gh_latency}")
        report.append("")
        report.append("[镜像源状态]")
        
        for mirror in results['mirrors']:
            status = "✓" if mirror['status'] == 'available' else "✗"
            latency = f" {mirror['latency_ms']}ms" if mirror['latency_ms'] else ""
            rate = f" (成功率: {mirror['success_rate']})" if mirror['success_rate'] else ""
            report.append(f"  {status} {mirror['name']}: {mirror['status']}{latency}{rate}")
        
        best = self.get_best_mirror()
        if best:
            report.append("")
            report.append(f"推荐使用: {best['name']} ({best.get('description', '')})")
        
        report.append("")
        report.append("=" * 50)
        
        return "\n".join(report)

def main():
    monitor = MirrorMonitor()
    
    print("\n[镜像源监控检测]")
    print(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    monitor.backup_config()
    
    report = monitor.get_status_report()
    print(report)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()