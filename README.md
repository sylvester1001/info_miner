# Info-Spider

一个自动化的信息采集工具，用于收集特定关键词的 Google 搜索结果。

## 功能特点

- 支持多个关键词搜索
- 自动获取Google搜索结果
- 智能历史记录管理，避免重复内容
- 每次运行获取新的搜索结果
- 保存搜索结果的标题和URL
- 可扩展的架构设计，支持后续添加更多数据源

## 技术栈

- **Python 3.x**: 主要编程语言
- **Selenium**: 用于网页爬取，可以处理动态加载的内容
- **ChromeDriver**: Selenium的WebDriver，用于控制Chrome浏览器
- **logging**: 用于日志记录
- **JSON**: 用于配置文件和数据存储
- 后续会添加 csv 和 excel 的存储格式以方便数据分析

## 项目结构

```
info-spider/
├── README.md
├── requirements.txt
├── config.json
├── src/
│   ├── __init__.py
│   ├── spider.py
│   ├── scheduler.py
│   ├── utils.py
│   └── history_manager.py
├── data/
│   ├── search_results/    # 搜索结果存储目录
│   └── history.json      # 搜索历史记录文件
```

## 安装说明

1. 克隆项目
2. 创建并激活Python虚拟环境：
   ```bash
   python -m venv py_env
   source py_env/bin/activate  # Linux/Mac
   # 或
   .\py_env\Scripts\activate  # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 安装Chrome浏览器和对应版本的ChromeDriver
4. 配置config.json文件，添加搜索关键词

## 配置说明

在 `config.json` 文件中配置：

```json
{
    "keywords": ["关键词1", "关键词2"],
    "search_settings": {
        "results_per_keyword": 5,
        "search_engine": "google"
    },
    "output_settings": {
        "output_dir": "data/search_results",
        "file_format": "json"
    }
}
```

## 使用方法

1. 运行程序：
   ```bash
   python src/scheduler.py
   ```

2. 程序会自动：
   - 为每个关键词搜索新的结果
   - 跳过已经在历史记录中的结果
   - 将新结果保存到 `data/search_results` 目录
   - 更新历史记录

## 特性说明

### 历史记录管理
- 程序会记住每个关键词已经搜索过的URL
- 每次运行时会自动跳过已经见过的结果
- 历史记录保存在 `data/history.json` 文件中
- 可以使用 `history_manager.clear_history()` 清除历史记录 或 手动删除 `data/history.json` 文件

### 搜索结果存储
- 每次搜索的结果以JSON格式保存
- 文件名包含时间戳和关键词
- 每个结果包含标题和URL信息

## 后续规划

- 支持更多搜索引擎
- 添加特定论坛的数据采集
- 支持更多数据存储格式
- 添加数据分析功能
- 提供Web界面进行配置和查看结果