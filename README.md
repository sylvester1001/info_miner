# Info-Miner

A powerful web information mining tool that helps you gather and analyze search results from Google.

## Features

- Automated Google search with customizable keywords
- Headless browser operation
- Cross-platform support (Windows & macOS)
- Search result deduplication
- JSON output format
- History tracking

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

## Usage

```bash
python src/miner.py
```

## Output

Results are saved in the `data` directory in JSON format with timestamp and keyword in the filename.

---

# Info-Miner (中文说明)

一个强大的网络信息挖掘工具，帮助您收集和分析来自Google的搜索结果。

## 功能特点

- 自动化Google搜索，支持自定义关键词
- 无界面浏览器操作
- 跨平台支持（Windows和macOS）
- 搜索结果去重
- JSON输出格式
- 历史记录追踪

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

## 使用方法

```bash
python src/miner.py
```

## 输出结果

结果以JSON格式保存在 `data` 目录中，文件名包含时间戳和关键词。