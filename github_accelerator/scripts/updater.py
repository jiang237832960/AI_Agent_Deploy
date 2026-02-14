# -*- coding: utf-8 -*-
"""
GitHub 镜像源更新脚本
功能：自动更新镜像配置，支持回滚
"""

import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional

class MirrorUpdater:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'mirrors.json')
        self.config_path = config_path
        self.config = self._load_config()
        self.log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        self.backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backup')
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        for dir_path in [self.log_dir, self.backup_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return {}
    
    def _save_config(self, config: Dict):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    def _log(self, level: str, message: str, details: Dict = None):
        log_file = os.path.join(self.log_dir, 'update_log.json')
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
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
        logs = logs[-500:]
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"[{level.upper()}] {message}")
    
    def backup_current_config(self) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'mirrors_{timestamp}.json')
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
        self._log('info', f'配置已备份: {backup_file}')
        self._cleanup_old_backups()
        return backup_file
    
    def _cleanup_old_backups(self):
        max_count = self.config.get('rollback_config', {}).get('max_backup_count', 10)
        backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith('mirrors_')])
        
        while len(backups) > max_count:
            old_file = os.path.join(self.backup_dir, backups.pop(0))
            try:
                os.remove(old_file)
                self._log('info', f'清理旧备份: {old_file}')
            except Exception as e:
                self._log('warning', f'清理备份失败: {e}')
    
    def get_available_backups(self) -> List[Dict]:
        backups = []
        for f in sorted(os.listdir(self.backup_dir), reverse=True):
            if f.startswith('mirrors_') and f.endswith('.json'):
                file_path = os.path.join(self.backup_dir, f)
                try:
                    stat = os.stat(file_path)
                    backups.append({
                        'filename': f,
                        'path': file_path,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except:
                    pass
        return backups
    
    def rollback(self, backup_file: str = None) -> bool:
        if backup_file is None:
            backups = self.get_available_backups()
            if not backups:
                self._log('error', '没有可用的备份文件')
                return False
            backup_file = backups[0]['path']
        
        if not os.path.exists(backup_file):
            self._log('error', f'备份文件不存在: {backup_file}')
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)
            
            self._save_config(backup_config)
            self.config = backup_config
            
            self._log('info', f'已回滚到: {backup_file}')
            return True
        except Exception as e:
            self._log('error', f'回滚失败: {e}')
            return False
    
    def fetch_github_ips(self) -> Dict[str, str]:
        hosts = {}
        try:
            req = urllib.request.Request(
                'https://api.github.com/meta',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response = urllib.request.urlopen(req, timeout=15)
            data = json.loads(response.read().decode())
            
            if 'hooks' in data:
                for ip in data['hooks'][:3]:
                    hosts['github.com'] = ip
                    break
            
            if 'web' in data:
                for ip in data['web'][:3]:
                    if 'github.com' not in hosts:
                        hosts['github.com'] = ip
                    break
            
            self._log('info', f'从GitHub API获取IP: {hosts}')
        except Exception as e:
            self._log('warning', f'获取GitHub IP失败: {e}')
        
        return hosts
    
    def update_hosts_from_remote(self) -> bool:
        self._log('info', '开始更新hosts配置...')
        
        backup_file = self.backup_current_config()
        
        new_hosts = self.fetch_github_ips()
        
        if not new_hosts:
            self._log('warning', '未获取到新的hosts配置')
            return False
        
        updated = False
        for domain, ip in new_hosts.items():
            if domain in self.config.get('hosts', {}):
                if self.config['hosts'][domain] != ip:
                    old_ip = self.config['hosts'][domain]
                    self.config['hosts'][domain] = ip
                    self._log('info', f'更新 {domain}: {old_ip} -> {ip}')
                    updated = True
        
        if updated:
            self.config['last_update'] = datetime.now().isoformat()
            self._save_config(self.config)
            self._log('info', 'hosts配置更新完成')
        else:
            self._log('info', 'hosts配置无需更新')
        
        return updated
    
    def add_mirror(self, mirror_config: Dict) -> bool:
        if 'id' not in mirror_config and 'name' not in mirror_config:
            self._log('error', '镜像配置缺少id或name')
            return False
        
        mirror_id = mirror_config.get('id', mirror_config.get('name'))
        
        self.backup_current_config()
        
        existing = False
        for i, m in enumerate(self.config.get('mirrors', [])):
            if m.get('id') == mirror_id or m.get('name') == mirror_id:
                self.config['mirrors'][i] = mirror_config
                existing = True
                break
        
        if not existing:
            if 'id' not in mirror_config:
                mirror_config['id'] = mirror_id
            mirror_config.setdefault('status', 'unknown')
            mirror_config.setdefault('last_check', None)
            mirror_config.setdefault('latency_ms', None)
            mirror_config.setdefault('success_rate', 0)
            mirror_config.setdefault('check_count', 0)
            mirror_config.setdefault('success_count', 0)
            self.config.setdefault('mirrors', []).append(mirror_config)
        
        self._save_config(self.config)
        self._log('info', f"镜像 {'更新' if existing else '添加'}: {mirror_id}")
        return True
    
    def remove_mirror(self, mirror_id: str) -> bool:
        self.backup_current_config()
        
        original_count = len(self.config.get('mirrors', []))
        self.config['mirrors'] = [
            m for m in self.config.get('mirrors', [])
            if m.get('id') != mirror_id and m.get('name') != mirror_id
        ]
        
        if len(self.config['mirrors']) < original_count:
            self._save_config(self.config)
            self._log('info', f'已删除镜像: {mirror_id}')
            return True
        
        self._log('warning', f'未找到镜像: {mirror_id}')
        return False
    
    def auto_update(self) -> Dict:
        result = {
            'timestamp': datetime.now().isoformat(),
            'hosts_updated': False,
            'mirrors_checked': 0,
            'mirrors_available': 0,
            'errors': []
        }
        
        try:
            result['hosts_updated'] = self.update_hosts_from_remote()
        except Exception as e:
            result['errors'].append(f'hosts更新失败: {e}')
        
        from monitor import MirrorMonitor
        monitor = MirrorMonitor(self.config_path)
        check_result = monitor.check_all_mirrors()
        
        result['mirrors_checked'] = len(check_result.get('mirrors', []))
        result['mirrors_available'] = sum(
            1 for m in check_result.get('mirrors', [])
            if m.get('status') == 'available'
        )
        
        if result['errors']:
            self._log('warning', f'自动更新完成，但有错误: {result["errors"]}')
        else:
            self._log('info', f'自动更新完成: hosts={result["hosts_updated"]}, 可用镜像={result["mirrors_available"]}/{result["mirrors_checked"]}')
        
        return result

def main():
    import sys
    
    updater = MirrorUpdater()
    
    print("\n" + "=" * 50)
    print("       GitHub 镜像源更新工具".center(40))
    print("=" * 50 + "\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'update':
            result = updater.auto_update()
            print(f"\n更新结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        elif command == 'rollback':
            backups = updater.get_available_backups()
            if backups:
                print("\n可用备份:")
                for i, b in enumerate(backups[:5]):
                    print(f"  {i+1}. {b['filename']} ({b['modified']})")
                
                choice = input("\n选择要回滚的备份 (输入序号，默认1): ").strip()
                idx = int(choice) - 1 if choice else 0
                
                if 0 <= idx < len(backups):
                    updater.rollback(backups[idx]['path'])
            else:
                print("没有可用的备份")
        
        elif command == 'list-backups':
            backups = updater.get_available_backups()
            print("\n可用备份:")
            for b in backups:
                print(f"  {b['filename']} - {b['modified']}")
        
        else:
            print(f"未知命令: {command}")
            print("可用命令: update, rollback, list-backups")
    
    else:
        print("请选择操作:")
        print("  1. 自动更新配置")
        print("  2. 查看备份列表")
        print("  3. 回滚到备份")
        print("  4. 退出")
        
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == '1':
            result = updater.auto_update()
            print(f"\n更新结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        elif choice == '2':
            backups = updater.get_available_backups()
            print("\n可用备份:")
            for b in backups:
                print(f"  {b['filename']} - {b['modified']}")
        
        elif choice == '3':
            backups = updater.get_available_backups()
            if backups:
                print("\n可用备份:")
                for i, b in enumerate(backups[:5]):
                    print(f"  {i+1}. {b['filename']} ({b['modified']})")
                
                sel = input("\n选择要回滚的备份 (输入序号): ").strip()
                try:
                    idx = int(sel) - 1
                    if 0 <= idx < len(backups):
                        updater.rollback(backups[idx]['path'])
                except:
                    print("无效选择")
            else:
                print("没有可用的备份")
    
    print()

if __name__ == "__main__":
    main()