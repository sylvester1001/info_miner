# Info-Miner

A web information mining tool helps to gather and analyze search results from Google.

## Features

- Automated Google search with customizable keywords
- Headless browser operation
- Cross-platform support (Windows & macOS)
- Search result deduplication
- JSON and CSV output formats
- History tracking
- Configurable site filtering (translations, encyclopedias, dictionaries)

## Requirements

- Python 3.7+
- Google Chrome Browser
- Chrome WebDriver (automatically managed)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/info-miner.git
cd info-miner
```

2. Create a virtual environment:
```bash
python -m venv py_env
# On Windows
py_env\Scripts\activate
# On macOS
source py_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Search Settings
Edit `config.json` to customize your search settings:

```json
{
    "keywords": ["your", "search", "terms"],
    "search_settings": {
        "results_per_keyword": 10
    },
    "output_settings": {
        "output_dir": "data"
    }
}
```

### Excluded Sites
Edit `excluded_sites.json` to customize which websites to exclude from search results:

```json
{
    "translation_sites": [
        "translate.google.com",
        "translate.bing.com"
    ],
    "encyclopedia_sites": [
        "wikipedia.org",
        "baike.baidu.com"
    ],
    "dictionary_sites": [
        "dictionary.cambridge.org",
        "dictionary.com"
    ],
    "other_sites": [
        "webcache.googleusercontent.com"
    ]
}
```

You can add or remove domains in each category to customize which sites should be excluded from the search results.

## Usage

```bash
python src/miner.py
```

## Output

Results are saved in the `data` directory in both JSON and CSV formats. Each file contains:
- Timestamp
- Search keyword
- Search results (title and URL)

---

# Info-Miner (中文说明)

一个强大的网络信息挖掘工具，帮助您收集和分析来自Google的搜索结果。

## 功能特点

- 自动化Google搜索，支持自定义关键词
- 无界面浏览器操作
- 跨平台支持（Windows和macOS）
- 搜索结果去重
- JSON和CSV输出格式
- 历史记录追踪
- 可配置网站过滤（翻译、百科、词典等）

## 系统要求

- Python 3.7+
- Google Chrome浏览器
- Chrome WebDriver（自动管理）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/info-miner.git
cd info-miner
```

2. 创建虚拟环境：
```bash
python -m venv py_env
# Windows系统
py_env\Scripts\activate
# macOS系统
source py_env/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

### 搜索设置
编辑 `config.json` 来自定义搜索设置：

```json
{
    "keywords": ["搜索", "关键词"],
    "search_settings": {
        "results_per_keyword": 10
    },
    "output_settings": {
        "output_dir": "data"
    }
}
```

### 排除网站设置
编辑 `excluded_sites.json` 来自定义需要排除的网站：

```json
{
    "translation_sites": [
        "translate.google.com",
        "translate.bing.com"
    ],
    "encyclopedia_sites": [
        "wikipedia.org",
        "baike.baidu.com"
    ],
    "dictionary_sites": [
        "dictionary.cambridge.org",
        "dictionary.com"
    ],
    "other_sites": [
        "webcache.googleusercontent.com"
    ]
}
```

您可以在各个类别中添加或删除域名，以自定义需要排除的网站。

## 使用方法

```bash
python src/miner.py
```

## 输出结果

结果以JSON和CSV两种格式保存在 `data` 目录中，每个文件包含：
- 时间戳
- 搜索关键词
- 搜索结果（标题和URL）