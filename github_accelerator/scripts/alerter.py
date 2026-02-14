# -*- coding: utf-8 -*-
"""
告警通知模块
功能：发送告警通知（支持邮件、Webhook等）
"""

import json
import os
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class AlertNotifier:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'mirrors.json')
        self.config_path = config_path
        self.config = self._load_config()
        self.log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _log_alert(self, alert: Dict):
        log_file = os.path.join(self.log_dir, 'alert_log.json')
        
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(alert)
        logs = logs[-500:]
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def send_email(self, subject: str, body: str, recipients: List[str] = None) -> bool:
        alert_config = self.config.get('alert_config', {})
        email_config = alert_config.get('email', {})
        
        if not email_config or not recipients:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config.get('sender', '')
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            smtp_server = email_config.get('smtp_server', '')
            smtp_port = email_config.get('smtp_port', 587)
            smtp_user = email_config.get('smtp_user', '')
            smtp_pass = email_config.get('smtp_pass', '')
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False
    
    def send_webhook(self, webhook_url: str, data: Dict) -> bool:
        if not webhook_url:
            return False
        
        try:
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=json_data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'GitHub-Mirror-Monitor/1.0'
                }
            )
            response = urllib.request.urlopen(req, timeout=10)
            return response.getcode() in [200, 201, 204]
        except Exception as e:
            print(f"发送Webhook失败: {e}")
            return False
    
    def send_alert(self, level: str, message: str, details: Dict = None) -> Dict:
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'details': details or {},
            'notified': False,
            'notification_methods': []
        }
        
        alert_config = self.config.get('alert_config', {})
        
        if not alert_config.get('enabled', True):
            self._log_alert(alert)
            return alert
        
        webhook_url = alert_config.get('webhook', '')
        if webhook_url:
            webhook_data = {
                'text': f"[{level.upper()}] {message}",
                'level': level,
                'timestamp': alert['timestamp'],
                'details': details
            }
            
            if self.send_webhook(webhook_url, webhook_data):
                alert['notified'] = True
                alert['notification_methods'].append('webhook')
        
        email = alert_config.get('email', '')
        if email:
            subject = f"[GitHub镜像监控] {level.upper()}: {message}"
            body = f"""
告警级别: {level.upper()}
告警时间: {alert['timestamp']}
告警信息: {message}

详细信息:
{json.dumps(details, indent=2, ensure_ascii=False)}
"""
            if self.send_email(subject, body, [email]):
                alert['notified'] = True
                alert['notification_methods'].append('email')
        
        self._log_alert(alert)
        
        print(f"[告警] [{level.upper()}] {message}")
        if alert['notified']:
            print(f"  已通过 {', '.join(alert['notification_methods'])} 发送通知")
        
        return alert
    
    def check_and_alert(self, monitor_results: Dict) -> List[Dict]:
        alerts = []
        alert_config = self.config.get('alert_config', {})
        
        min_success_rate = alert_config.get('min_success_rate', 0.5)
        max_latency = alert_config.get('max_latency_ms', 5000)
        
        if not monitor_results.get('github_accessible'):
            available_mirrors = sum(
                1 for m in monitor_results.get('mirrors', [])
                if m.get('status') == 'available'
            )
            
            if available_mirrors == 0:
                alert = self.send_alert(
                    'critical',
                    'GitHub和所有镜像源都无法访问',
                    {'github_accessible': False, 'mirrors_checked': len(monitor_results.get('mirrors', []))}
                )
                alerts.append(alert)
        
        for mirror in monitor_results.get('mirrors', []):
            if mirror.get('status') != 'available':
                alert = self.send_alert(
                    'warning',
                    f"镜像源 {mirror['name']} 不可用",
                    {'mirror': mirror['name'], 'status': mirror['status']}
                )
                alerts.append(alert)
            
            elif mirror.get('latency_ms') and mirror['latency_ms'] > max_latency:
                alert = self.send_alert(
                    'warning',
                    f"镜像源 {mirror['name']} 延迟过高",
                    {'mirror': mirror['name'], 'latency_ms': mirror['latency_ms']}
                )
                alerts.append(alert)
            
            if mirror.get('success_rate') is not None and mirror['success_rate'] < min_success_rate:
                alert = self.send_alert(
                    'warning',
                    f"镜像源 {mirror['name']} 成功率过低",
                    {'mirror': mirror['name'], 'success_rate': mirror['success_rate']}
                )
                alerts.append(alert)
        
        return alerts

def main():
    notifier = AlertNotifier()
    
    print("\n[告警通知测试]")
    
    alert = notifier.send_alert(
        'info',
        '告警系统测试',
        {'test': True, 'timestamp': datetime.now().isoformat()}
    )
    
    print(f"\n告警结果: {json.dumps(alert, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()