import json
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import platform
import time
from history_manager import HistoryManager


class InfoMiner:
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.setup_driver()
        self.history_manager = HistoryManager()

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    # main function for setting up the driver

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # 基本设置
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 禁用 GPU 相关功能
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-gpu-sandbox')
        chrome_options.add_argument('--disable-gpu-compositing')
        chrome_options.add_argument('--disable-gpu-program-cache')
        chrome_options.add_argument('--disable-gpu-shader-disk-cache')
        chrome_options.add_argument('--disable-gpu-watchdog')
        chrome_options.add_argument('--disable-3d-apis')
        
        # 禁用缓存
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-cache')
        chrome_options.add_argument('--disable-offline-load-stale-cache')
        chrome_options.add_argument('--disk-cache-size=0')
        chrome_options.add_argument('--media-cache-size=0')
        
        # 其他优化设置
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-save-password-bubble')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # 平台特定设置
        system = platform.system()
        if system == 'Darwin' and platform.machine() == 'arm64':
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif system == 'Windows':
            chrome_options.add_argument('--disable-software-rasterizer')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            self.logger.info('Chrome driver initialized successfully')
        except Exception as e:
            self.logger.error(f'Chrome driver initialization failed: {str(e)}')
            raise

    def search(self, keyword):
        try:
            self.logger.info(f'开始搜索关键词: {keyword}')
            all_results = []
            page = 0
            required_results = self.config['search_settings']['results_per_keyword']

            while len(all_results) < required_results and page < 3:  # 最多查找3页
                self.logger.info(f'正在搜索第 {page + 1} 页')
                if page > 0:
                    try:
                        self.logger.info('尝试点击下一页按钮')
                        next_button = self.driver.find_element(By.ID, 'pnnext')
                        next_button.click()
                        time.sleep(3)
                    except Exception as e:
                        self.logger.info(f'没有更多页面: {str(e)}')
                        break
                else:
                    # 第一页的搜索逻辑
                    self.logger.info('访问 Google 搜索页面')
                    self.driver.get('https://www.google.com')
                    time.sleep(2)  # 等待页面加载

                    try:
                        self.logger.info('等待搜索框出现')
                        search_box = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.NAME, 'q'))
                        )
                        search_box.clear()
                        search_box.send_keys(keyword)
                        self.logger.info('输入搜索关键词并提交')
                        search_box.send_keys(Keys.RETURN)

                        # 等待搜索结果加载
                        self.logger.info('等待搜索结果加载')
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'search'))
                        )
                        time.sleep(5)  # 增加等待时间，确保结果完全加载
                    except TimeoutException as e:
                        self.logger.error(f'等待超时: {str(e)}')
                        return []

                    self.logger.info('开始提取搜索结果')
                # 使用更精确的选择器来查找搜索结果
                selectors = [
                    '#search .g div.yuRUbf',  # 主要搜索结果
                    '#rso .g div.yuRUbf',  # 备用搜索结果
                ]

                page_results = []
                for selector in selectors:
                    if len(page_results) >= required_results:
                        break

                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        self.logger.info(
                            f'使用选择器 {selector} 找到 {len(elements)} 个结果'
                        )

                        for element in elements:
                            if len(page_results) >= required_results:
                                break

                            try:
                                # 直接从yuRUbf div中获取标题和链接
                                title_element = element.find_element(
                                    By.CSS_SELECTOR, 'h3'
                                )
                                link_element = element.find_element(
                                    By.CSS_SELECTOR, 'a'
                                )

                                title = title_element.text.strip()
                                url = link_element.get_attribute('href')

                                if (
                                    title
                                    and url
                                    and not any(r['url'] == url for r in page_results)
                                ):
                                    if (
                                        url.startswith('http')
                                        and not url.startswith(
                                            'https://webcache.googleusercontent.com'
                                        )
                                        and not url.startswith(
                                            'https://translate.google.com'
                                        )
                                    ):
                                        result = {'title': title, 'url': url}
                                        # 检查是否是新的结果
                                        if not self.history_manager.is_url_seen(
                                            keyword, url
                                        ):
                                            self.logger.info(f'找到新结果: {title}')
                                            page_results.append(result)
                            except Exception as e:
                                self.logger.debug(f'提取结果失败: {str(e)}')
                                continue
                    except Exception as e:
                        self.logger.debug(
                            f'使用选择器 {selector} 查找元素失败: {str(e)}'
                        )
                        continue

                # 添加新的未见过的结果
                for result in page_results:
                    if len(all_results) < required_results:
                        all_results.append(result)
                        self.history_manager.add_result(keyword, result)
                        self.logger.info(f'添加新结果到历史记录: {result["title"]}')
                    else:
                        break

                self.logger.info(f'当前已找到 {len(all_results)} 个新结果')
                page += 1

                if not page_results:  # 如果当前页面没有新的结果，退出循环
                    self.logger.info('当前页面没有新的结果，停止搜索')
                    break

            if len(all_results) < required_results:
                self.logger.warning(
                    f'只找到 {len(all_results)} 个新结果，期望找到 {required_results} 个'
                )

            return all_results

        except TimeoutException:
            self.logger.error(f'搜索超时: {keyword}')
            return []
        except Exception as e:
            self.logger.error(f'搜索过程发生错误: {str(e)}')
            return []

    def save_results(self, keyword, results):
        if not results:
            self.logger.warning(f'No new results to save for keyword: {keyword}')
            return

        output_dir = self.config['output_settings']['output_dir']
        os.makedirs(output_dir, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{output_dir}/{date_str}_{keyword.replace(' ', '_')}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    {'keyword': keyword, 'date': date_str, 'results': results},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            self.logger.info(f'Results saved to {filename}')
        except Exception as e:
            self.logger.error(f'Error saving results to file: {str(e)}')

    def run(self):
        self.logger.info('Starting search process...')
        for keyword in self.config['keywords']:
            self.logger.info(f'Searching for keyword: {keyword}')
            results = self.search(keyword)
            self.save_results(keyword, results)
        self.driver.quit()
        self.logger.info('Search process completed.')


if __name__ == '__main__':
    miner = InfoMiner()
    miner.run()
