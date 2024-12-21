# Info-Spider

一个自动化的信息采集工具，用于定期收集特定关键词的搜索结果。

## 功能特点

- 支持多个关键词搜索
- 自动获取Google搜索结果
- 每日定时运行
- 保存搜索结果的标题和URL
- 可扩展的架构设计，支持后续添加更多数据源

## 技术栈

- **Python 3.x**: 主要编程语言，具有丰富的库生态系统
- **Selenium**: 用于网页爬取，可以处理动态加载的内容
- **Schedule**: 用于实现定时任务
- **ChromeDriver**: Selenium的WebDriver，用于控制Chrome浏览器
- **logging**: 用于日志记录
- **JSON**: 用于配置文件和数据存储

## 项目结构

```
info-spider/
├── README.md
├── requirements.txt
├── config.json
├── src/
│   ├── __init__.py
│   ├── spider.py`
│   ├── scheduler.py
│   └── utils.py
└── data/
    └── search_results/
```

## 安装说明

1. 克隆项目
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 安装Chrome浏览器和对应版本的ChromeDriver
4. 配置config.json文件，添加搜索关键词

## 使用方法

1. 配置搜索关键词：
   ```json
   {
     "keywords": ["关键词1", "关键词2"]
   }
   ```

2. 运行程序：
   ```bash
   python src/scheduler.py
   ```

## 后续规划

- 支持更多搜索引擎
- 添加特定论坛的数据采集
- 支持更多数据存储格式
- 添加数据分析功能
- 提供Web界面进行配置和查看结果 