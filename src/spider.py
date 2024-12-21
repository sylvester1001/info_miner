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

class GoogleSpider:
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.setup_driver()

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        
        # 使用本地Chrome浏览器
        if platform.system() == 'Darwin' and platform.machine() == 'arm64':
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            self.logger.info("Chrome driver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

    def search(self, keyword):
        try:
            # 访问Google搜索页面
            self.logger.info(f"Navigating to Google search for keyword: {keyword}")
            self.driver.get('https://www.google.com')
            
            # 等待搜索框出现并输入关键词
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            
            # 等待搜索结果加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search'))
            )
            
            # 确保页面完全加载
            time.sleep(3)
            
            # 获取搜索结果
            results = []
            
            # 使用多个选择器来查找搜索结果
            selectors = [
                '#search .g',
                '#rso .g',
                '.MjjYud',
                'div[data-hveid]'
            ]
            
            for selector in selectors:
                if len(results) >= self.config['search_settings']['results_per_keyword']:
                    break
                    
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    self.logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    
                    for element in elements:
                        if len(results) >= self.config['search_settings']['results_per_keyword']:
                            break
                            
                        try:
                            # 尝试获取标题和链接
                            title_element = element.find_element(By.CSS_SELECTOR, 'h3')
                            link_element = element.find_element(By.CSS_SELECTOR, 'a')
                            
                            title = title_element.text.strip()
                            url = link_element.get_attribute('href')
                            
                            if title and url and not any(r['url'] == url for r in results):
                                if (url.startswith('http') and 
                                    not url.startswith('https://webcache.googleusercontent.com') and
                                    not url.startswith('https://translate.google.com')):
                                    results.append({
                                        'title': title,
                                        'url': url
                                    })
                                    self.logger.info(f"Added result: {title}")
                        except Exception as e:
                            self.logger.debug(f"Failed to extract result: {str(e)}")
                            continue
                except Exception as e:
                    self.logger.debug(f"Failed to find elements with selector {selector}: {str(e)}")
                    continue
            
            if len(results) < self.config['search_settings']['results_per_keyword']:
                self.logger.warning(f"Only found {len(results)} results for keyword: {keyword}, expected {self.config['search_settings']['results_per_keyword']}")
            
            return results
            
        except TimeoutException:
            self.logger.error(f"Timeout while searching for keyword: {keyword}")
            return []
        except Exception as e:
            self.logger.error(f"Error during search for keyword {keyword}: {str(e)}")
            return []

    def save_results(self, keyword, results):
        if not results:
            self.logger.warning(f"No results to save for keyword: {keyword}")
            return

        output_dir = self.config['output_settings']['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{output_dir}/{date_str}_{keyword.replace(' ', '_')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'keyword': keyword,
                    'date': date_str,
                    'results': results
                }, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Results saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving results to file: {str(e)}")

    def run(self):
        self.logger.info("Starting search process...")
        for keyword in self.config['keywords']:
            self.logger.info(f"Searching for keyword: {keyword}")
            results = self.search(keyword)
            self.save_results(keyword, results)
        self.driver.quit()
        self.logger.info("Search process completed.")

if __name__ == '__main__':
    spider = GoogleSpider()
    spider.run() 