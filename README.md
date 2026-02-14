# AI 助手工具集

一个功能强大的 Windows 系统工具集，包含系统环境检测、开发环境配置、GitHub 加速访问、文件搜索等功能。

## 功能概览

| 功能模块 | 说明 |
|---------|------|
| 系统环境检测 | 检测 Windows 版本、CPU、显卡、内存、硬盘等硬件信息 |
| 内存详细分析 | 深入分析内存使用情况，找出占用内存的进程和系统缓存 |
| 开发环境配置 | 检测并一键部署 Node.js、Python、Java、Go 等开发环境 |
| GitHub 加速 | 检测 GitHub 访问状态，自动配置镜像加速，支持监控和更新 |
| 文件搜索 | 集成 Everything 快速搜索本地文件 |

## 快速开始

### 方式一：统一启动入口（推荐）

双击 `main.bat` 或运行以下命令：

```bash
# 交互式菜单
python main.py

# 列出所有模块
python main.py --list

# 直接启动指定模块
python main.py -m system_info
python main.py -m github_accelerator -- -a check
```

### 方式二：独立运行子模块

直接双击对应功能文件夹中的 `.bat` 文件：

```
├── system_info_checker/scripts/
│   ├── start.bat              # 系统检测菜单
│   ├── system_info.bat        # 系统硬件检测
│   └── memory_checker.bat     # 内存详细分析
├── dev_env_setup/scripts/
│   ├── start.bat              # 开发环境菜单
│   ├── detect.bat             # 检测开发环境
│   └── deploy.bat             # 一键部署项目
├── github_accelerator/scripts/
│   ├── start.bat              # GitHub加速菜单
│   ├── check.bat              # 检测 GitHub 访问
│   ├── accelerate.bat         # 配置 GitHub 加速
│   ├── monitor.bat            # 监控镜像源状态
│   └── updater.bat            # 更新镜像配置
└── file_search/scripts/
    ├── start.bat              # 文件搜索菜单
    └── search.bat             # 搜索文件
```

## 功能详细介绍

### 1. 系统环境检测 (system_info_checker)

检测系统硬件信息：
- 操作系统版本、架构、位数
- CPU 型号、核心数、线程数、频率
- 内存总量、可用、已使用、使用率
- 硬盘分区、总容量、已用空间
- 显卡型号和显存大小

### 2. 内存详细分析 (memory_checker)

专门用于分析内存使用情况：
- 物理内存总量、已使用、可用
- 系统内核/缓存占用（非分页池、分页池、系统缓存）
- 分页文件（虚拟内存）使用情况
- 进程内存排行 Top 15
- 内存平衡检查

### 3. 开发环境配置 (dev_env_setup)

检测并一键部署开发环境：
- Node.js / npm
- Python / pip
- Java
- Go
- Rust
- Docker
- Git

### 4. GitHub 加速 (github_accelerator)

完整的 GitHub 访问加速解决方案：
- **访问检测**：检测 GitHub 及镜像源连通性
- **智能加速**：自动选择最快镜像源
- **监控更新**：实时监控镜像源状态
- **自动更新**：自动更新镜像配置
- **告警通知**：支持邮件和 Webhook 告警
- **一键还原**：支持配置回滚

### 5. 文件搜索 (file_search)

集成 Everything 快速搜索本地文件

## 环境要求

- **操作系统**：Windows 10/11（32位或64位）
- **必需**：Python 3.7+
- **可选**：Everything（文件搜索功能，已内置便携版）

## 项目结构

```
AI_Agent_Deploy/
├── main.py                          # 主启动脚本
├── main.bat                         # 批处理入口
├── core/
│   └── launcher.py                  # 通用启动框架
├── config/
│   └── settings.json                # 全局配置
├── logs/                            # 日志目录
├── tools/
│   └── Everything/                  # Everything 便携版
├── system_info_checker/             # 系统环境检测
│   ├── README.md
│   └── scripts/
│       ├── start.py
│       ├── system_info.py
│       └── memory_checker.py
├── dev_env_setup/                   # 开发环境配置
│   ├── README.md
│   ├── scripts/
│   │   ├── start.py
│   │   ├── detect.py
│   │   └── deploy.py
│   └── config/
│       └── projects.json
├── github_accelerator/              # GitHub 加速
│   ├── README.md
│   ├── scripts/
│   │   ├── start.py
│   │   ├── check.py
│   │   ├── accelerate.py
│   │   ├── monitor.py
│   │   ├── updater.py
│   │   └── alerter.py
│   ├── config/
│   │   └── mirrors.json
│   ├── logs/
│   └── backup/
└── file_search/                     # 文件搜索
    ├── README.md
    ├── scripts/
    │   ├── start.py
    │   └── search.py
    └── config/
        └── settings.json
```

## 命令行参数

```bash
# 显示帮助
python main.py -h

# 列出所有模块
python main.py --list

# 启动指定模块
python main.py -m <module_name>

# 传递参数给模块
python main.py -m <module_name> -- [模块参数]
```

## 备份与还原

修改系统文件前，程序会自动创建备份：

- `github_accelerator/backup/` - hosts 文件和配置备份
- `github_accelerator/logs/` - 变更日志和告警日志

如需还原，运行 `updater.bat` 选择回滚功能。

## 许可证

MIT License

## 注意事项

1. 修改系统文件需要管理员权限
2. 首次运行可能需要等待 Everything 建立索引
3. 建议定期运行监控脚本检查镜像源状态