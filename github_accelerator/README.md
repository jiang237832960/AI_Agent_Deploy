# GitHub 访问加速

完整的 GitHub 访问加速解决方案，包括访问检测、智能加速、监控更新、告警通知等功能。

## 功能特点

- **智能检测**：自动检测 GitHub 及镜像源连通性、延迟、速度
- **智能加速**：自动选择最快镜像源配置加速
- **监控更新**：实时监控镜像源状态，自动更新配置
- **告警通知**：支持邮件和 Webhook 告警通知
- **一键还原**：修改前自动备份，支持配置回滚

## 工具列表

| 脚本 | 说明 |
|------|------|
| start.py | 模块启动入口（菜单模式） |
| check.py | 检测 GitHub 访问状态 |
| accelerate.py | 配置加速（智能检测+配置） |
| monitor.py | 监控镜像源状态 |
| updater.py | 更新镜像配置、回滚 |
| alerter.py | 告警通知模块 |

## 使用方法

### 方式一：通过主程序启动

```bash
# 菜单模式
python main.py -m github_accelerator

# 直接检测
python main.py -m github_accelerator -- -a check

# 直接配置加速
python main.py -m github_accelerator -- -a accelerate

# 监控镜像源
python main.py -m github_accelerator -- -a monitor

# 更新配置
python main.py -m github_accelerator -- -a update
```

### 方式二：独立运行

```bash
# 菜单模式
python scripts/start.py

# 检测访问状态
python scripts/check.py

# 配置加速
python scripts/accelerate.py

# 监控镜像源
python scripts/monitor.py

# 更新配置
python scripts/updater.py
```

### 方式三：批处理文件

双击运行：
- `scripts/check.bat` - 检测 GitHub 访问
- `scripts/accelerate.bat` - 配置加速
- `scripts/monitor.bat` - 监控镜像源
- `scripts/updater.bat` - 更新配置

## 智能加速流程

```
┌─────────────────────────────────────┐
│  步骤 1：检测 GitHub 连通性          │
│  - 测试 github.com 是否可访问        │
│  - 如可访问，提示无需加速            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  步骤 2：测试镜像源                  │
│  - ghproxy.com                       │
│  - fastgit.org                       │
│  - jsdelivr                          │
│  - gitclone.com                      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  步骤 3：选择配置方式                │
│  - Hosts 文件加速                    │
│  - Git 代理配置                      │
│  - 全部配置                          │
└─────────────────────────────────────┘
```

## 监控更新系统

### 配置文件 (config/mirrors.json)

```json
{
    "version": "1.0.0",
    "update_interval_hours": 24,
    "mirrors": [...],
    "alert_config": {
        "enabled": true,
        "email": "",
        "webhook": "",
        "min_success_rate": 0.5
    }
}
```

### 日志文件

- `logs/change_log.json` - 变更日志
- `logs/update_log.json` - 更新日志
- `logs/alert_log.json` - 告警日志

### 备份文件

- `backup/mirrors_*.json` - 配置备份
- `backup/hosts.*.backup` - hosts 文件备份

## 检测输出示例

```
==================================================
                 GitHub 访问状态检测
==================================================

正在检测 GitHub 访问状态，请稍候...

【主要域名检测】

检测 github.com...
  状态：可访问
  延迟：737 ms
  速度：1387.9 KB/s

【镜像源检测】

检测 ghproxy...
  状态：无法访问

检测 fastgit...
  状态：可访问
  延迟：503 ms
  速度：2035.7 KB/s

检测 gitclone...
  状态：可访问
  延迟：421 ms
  速度：2432.1 KB/s

【推荐】

  最低延迟：gitclone (421 ms)

==================================================
                     检测完成！
==================================================
```

## 加速配置说明

### 1. Hosts 文件修改

自动将以下 IP 地址添加到 hosts 文件：
- github.com
- github.global.ssl.fastly.net
- assets.github.com
- raw.githubusercontent.com

### 2. Git 代理配置

```bash
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

### 3. 镜像源替换

常用 GitHub 镜像：
- `https://ghproxy.com/` + 原地址
- `https://fastgit.org/` + 原地址
- `https://gitclone.com/` + 原地址

## 命令行参数

### updater.py

```bash
# 自动更新
python updater.py update

# 查看备份列表
python updater.py list-backups

# 回滚到备份
python updater.py rollback
```

## 前置条件

- Windows 10/11 系统
- Python 3.7+
- 修改 hosts 需要管理员权限

## 常见问题

### Q: 加速配置需要重启电脑吗？

A: 不需要，配置完成后运行 `ipconfig /flushdns` 刷新 DNS 即可生效。

### Q: 如何还原配置？

A: 运行 `updater.bat` 选择回滚功能，或手动删除 hosts 文件中的 GitHub 相关行。

### Q: 为什么还是无法访问？

A: 可能是代理软件未开启，或需要使用 VPN。请检查网络连接。

### Q: 如何配置告警通知？

A: 编辑 `config/mirrors.json` 中的 `alert_config` 部分，配置邮箱或 Webhook 地址。