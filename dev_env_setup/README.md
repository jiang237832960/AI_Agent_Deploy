# 开发环境检测与配置

检测系统中的开发环境（Node.js、Python、Java、Go 等），并支持一键部署常见项目。

## 功能特点

- 检测已安装的开发工具版本
- 检测未安装但提供安装指引
- 一键部署常见项目类型
- 用户自定义安装路径（非 C 盘）
- 自动配置环境变量
- 生成一键启动脚本

## 工具列表

| 脚本 | 说明 |
|------|------|
| start.py | 模块启动入口（菜单模式） |
| detect.py | 检测开发环境 |
| deploy.py | 一键部署项目 |

## 支持的项目类型

| 类型 | 检测工具 | 部署支持 |
|------|---------|---------|
| Node.js | node, npm, pnpm, yarn | ✓ |
| Python | python, pip, conda | ✓ |
| Java | java, javac, maven, gradle | ✓ |
| Go | go | ✓ |
| Rust | rustc, cargo | ✓ |
| Docker | docker | ✓ |
| Git | git | ✓ |

## 使用方法

### 方式一：通过主程序启动

```bash
# 菜单模式
python main.py -m dev_env

# 直接检测环境
python main.py -m dev_env -- -a detect

# 直接部署项目
python main.py -m dev_env -- -a deploy
```

### 方式二：独立运行

```bash
# 菜单模式
python scripts/start.py

# 检测环境
python scripts/detect.py

# 部署项目
python scripts/deploy.py
```

### 方式三：批处理文件

双击运行：
- `scripts/detect.bat` - 检测开发环境
- `scripts/deploy.bat` - 一键部署项目

## 检测输出示例

```
========================================
         开发环境检测报告
========================================

【Node.js】
  状态：已安装
  版本：v20.10.0
  npm：10.2.3
  路径：C:\Program Files\nodejs\node.exe

【Python】
  状态：已安装
  版本：Python 3.11.5
  路径：C:\Python311\python.exe

【Java】
  状态：已安装
  版本：openjdk 17.0.9
  路径：C:\Program Files\Java\jdk-17

【Go】
  状态：未安装
  建议：从 https://golang.org/dl/ 下载安装

【Git】
  状态：已安装
  版本：git version 2.43.0
  路径：C:\Program Files\Git\cmd\git.exe

========================================
         检测完成！
========================================
```

## 部署流程示例

```
========================================
         项目一键部署
========================================

请选择要部署的项目类型：
  1. 前端项目 (Vue/React/Next.js)
  2. Python Web (FastAPI/Django/Flask)
  3. Node.js 后端 (Express/NestJS)
  4. Java 项目 (Spring Boot)
  5. Go 项目
  6. 自定义 Git 仓库

请输入选项 (1-6): 1

请选择前端框架：
  1. Vue 3
  2. React
  3. Next.js
  4. Vite

请输入选项 (1-4): 1

请输入安装目录（建议选择非系统盘）:
例如: D:\my-projects

请输入路径: D:\my-projects\vue-project

正在检测 Node.js... 已安装 v20.10.0

正在克隆项目... 完成
正在安装依赖... 完成
正在配置环境... 完成
正在生成启动脚本... 完成

========================================
         部署完成！
========================================

项目路径：D:\my-projects\vue-project
启动命令：双击 start.bat 或运行 npm run dev
```

## 前置条件

- Windows 10/11 系统
- Python 3.7+
- 部署前确保网络连接正常（用于克隆仓库）

## 配置文件说明

`config/projects.json` 包含支持部署的项目配置，包括：
- 项目类型
- Git 仓库地址
- 安装命令
- 启动命令
- 环境变量

## 常见问题

### Q: 安装路径可以选 C 盘吗？

A: 可以，但不推荐。系统盘空间有限，建议选择 D、E 等非系统盘。

### Q: 部署失败怎么办？

A: 检查以下内容：
1. 网络是否正常
2. 目标目录是否有写入权限
3. 对应的运行时是否已安装

### Q: 如何修改已配置的环境变量？

A: 可以手动修改系统环境变量，或删除项目后重新部署。