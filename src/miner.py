import json
import logging
import os
import csv
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
    def __init__(self, config_path='config.json', excluded_sites_path='excluded_sites.json'):
        self.config = self._load_config(config_path)
        self.excluded_sites = self._load_excluded_sites(excluded_sites_path)
        self.setup_logging()
        self.setup_driver()
        self.history_manager = HistoryManager()

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_excluded_sites(self, excluded_sites_path):
        try:
            with open(excluded_sites_path, 'r', encoding='utf-8') as f:
                excluded_sites = json.load(f)
                # Flatten all categories into a single list
                return [
                    domain
                    for category in excluded_sites.values()
                    for domain in category
                ]
        except Exception as e:
            self.logger.error(f'Error loading excluded sites: {str(e)}')
            return []

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
            self.logger.info(f'Starting search for keyword: {keyword}')
            all_results = []
            page = 0
            required_results = self.config['search_settings']['results_per_keyword']

            while len(all_results) < required_results and page < 3:  # Max 3 pages
                self.logger.info(f'Searching page {page + 1}')
                if page > 0:
                    try:
                        self.logger.info('Attempting to click next page button')
                        next_button = self.driver.find_element(By.ID, 'pnnext')
                        next_button.click()
                        time.sleep(3)
                    except Exception as e:
                        self.logger.info(f'No more pages available: {str(e)}')
                        break
                else:
                    # First page search logic
                    self.logger.info('Accessing Google search page')
                    self.driver.get('https://www.google.com')
                    time.sleep(2)  # Wait for page load

                    try:
                        self.logger.info('Waiting for search box')
                        search_box = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.NAME, 'q'))
                        )
                        search_box.clear()
                        search_box.send_keys(keyword)
                        self.logger.info('Entering search keyword and submitting')
                        search_box.send_keys(Keys.RETURN)

                        # Wait for search results
                        self.logger.info('Waiting for search results to load')
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'search'))
                        )
                        time.sleep(5)  # Additional wait to ensure results are loaded
                    except TimeoutException as e:
                        self.logger.error(f'Timeout waiting for results: {str(e)}')
                        return []

                    self.logger.info('Starting to extract search results')
                # Use precise selectors for search results
                selectors = [
                    '#search .g div.yuRUbf',  # Main search results
                    '#rso .g div.yuRUbf',     # Alternative search results
                ]

                page_results = []
                for selector in selectors:
                    if len(page_results) >= required_results:
                        break

                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        self.logger.info(
                            f'Found {len(elements)} results using selector {selector}'
                        )

                        for element in elements:
                            if len(page_results) >= required_results:
                                break

                            try:
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
                                        and not any(domain in url.lower() for domain in self.excluded_sites)
                                    ):
                                        result = {'title': title, 'url': url}
                                        if not self.history_manager.is_url_seen(
                                            keyword, url
                                        ):
                                            self.logger.info(f'Found new result: {title}')
                                            page_results.append(result)
                            except Exception as e:
                                self.logger.debug(f'Failed to extract result: {str(e)}')
                                continue
                    except Exception as e:
                        self.logger.debug(
                            f'Failed to find elements with selector {selector}: {str(e)}'
                        )
                        continue

                # Add new unseen results
                for result in page_results:
                    if len(all_results) < required_results:
                        all_results.append(result)
                        self.history_manager.add_result(keyword, result)
                        self.logger.info(f'Added new result to history: {result["title"]}')
                    else:
                        break

                self.logger.info(f'Currently found {len(all_results)} new results')
                page += 1

                if not page_results:
                    self.logger.info('No new results on current page, stopping search')
                    break

            if len(all_results) < required_results:
                self.logger.warning(
                    f'Only found {len(all_results)} new results, expected {required_results}'
                )

            return all_results

        except TimeoutException:
            self.logger.error(f'Search timeout for keyword: {keyword}')
            return []
        except Exception as e:
            self.logger.error(f'Error during search process: {str(e)}')
            return []

    def save_results(self, keyword, results):
        if not results:
            self.logger.warning(f'No new results to save for keyword: {keyword}')
            return

        output_dir = self.config['output_settings']['output_dir']
        os.makedirs(output_dir, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        base_filename = f"{output_dir}/{date_str}_{keyword.replace(' ', '_')}"

        # Save as JSON
        json_filename = f"{base_filename}.json"
        try:
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(
                    {'keyword': keyword, 'date': date_str, 'results': results},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            self.logger.info(f'Results saved to JSON: {json_filename}')
        except Exception as e:
            self.logger.error(f'Error saving results to JSON file: {str(e)}')

        # Save as CSV
        csv_filename = f"{base_filename}.csv"
        try:
            with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['keyword', 'date', 'title', 'url'])
                writer.writeheader()
                for result in results:
                    writer.writerow({
                        'keyword': keyword,
                        'date': date_str,
                        'title': result['title'],
                        'url': result['url']
                    })
            self.logger.info(f'Results saved to CSV: {csv_filename}')
        except Exception as e:
            self.logger.error(f'Error saving results to CSV file: {str(e)}')

    def run(self):
        self.logger.info('Starting search process...')
        for keyword in self.config['keywords']:
            self.logger.info(f'Processing keyword: {keyword}')
            results = self.search(keyword)
            self.save_results(keyword, results)
        self.driver.quit()
        self.logger.info('Search process completed successfully.')


if __name__ == '__main__':
    miner = InfoMiner()
    miner.run()
