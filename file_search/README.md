# 文件搜索（集成 Everything）

集成 Everything 快速搜索本地文件，支持按文件名、类型、大小等多种方式搜索。

## 功能特点

- 调用 Everything es.exe 进行极速搜索
- 支持按文件名搜索
- 支持按文件类型筛选
- 支持按大小范围筛选
- 显示文件路径、大小、修改时间
- 支持导出搜索结果

## 工具列表

| 脚本 | 说明 |
|------|------|
| start.py | 模块启动入口（菜单模式） |
| search.py | 文件搜索 |

## 使用方法

### 方式一：通过主程序启动

```bash
# 菜单模式
python main.py -m file_search

# 直接搜索
python main.py -m file_search -- -a search

# 指定关键词搜索
python main.py -m file_search -- -a search -q "python"

# 启动 Everything
python main.py -m file_search -- -a everything
```

### 方式二：独立运行

```bash
# 菜单模式
python scripts/start.py

# 文件搜索
python scripts/search.py

# 指定关键词搜索
python scripts/search.py -q "python"
```

### 方式三：批处理文件

双击运行：
- `scripts/search.bat` - 文件搜索

## 搜索示例

### 按文件名搜索
```
请输入搜索关键词：python
```

### 按文件类型搜索
```
请选择搜索类型：
  1. 按文件名搜索
  2. 按扩展名搜索
  3. 按大小搜索
请输入选项：2

请输入扩展名（如：py, js, txt）：py
```

### 按大小搜索
```
请选择搜索类型：3

请输入大小范围（如：>10MB, <100MB）：>100MB
```

## 输出示例

```
========================================
         搜索结果
========================================

找到 15 个匹配结果：

1. D:\Projects\python\main.py
   大小：2.5 KB | 修改时间：2024-01-15 14:30

2. D:\Projects\python\utils.py
   大小：1.8 KB | 修改时间：2024-01-14 09:20

...

========================================
         搜索完成！
========================================
```

## 前置条件

- Windows 10/11 系统
- Python 3.7+
- Everything 工具（已内置在 `tools/Everything` 目录）
- 首次使用需先运行 `tools/Everything/download_everything.bat` 下载 Everything
- Everything 首次运行后会自动建立索引

## 配置说明

`config/settings.json` 包含搜索配置：

```json
{
    "everything_path": "../tools/Everything/es.exe",
    "max_results": 100,
    "show_hidden": false,
    "search_modes": {
        "filename": "按文件名",
        "extension": "按扩展名",
        "size": "按大小",
        "date": "按修改时间"
    }
}
```

## 常见问题

### Q: 搜索不到文件？

A: 请确保 Everything 已运行并完成索引。首次使用请先运行 `tools/Everything/download_everything.bat` 下载 Everything，然后运行 Everything.exe 建立索引。

### Q: 搜索结果很少？

A: Everything 需要时间来建立索引。让 Everything 在后台运行一会儿，然后重新搜索。

### Q: 如何加快搜索速度？

A: Everything 建立索引后，搜索是实时的。确保 Everything 一直在系统托盘运行即可。