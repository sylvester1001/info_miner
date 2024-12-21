import json
import logging
from spider import GoogleSpider


class Runner:
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self.setup_logging()

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Starting search process...')
        try:
            spider = GoogleSpider()
            spider.run()
            self.logger.info('Search process completed successfully')
        except Exception as e:
            self.logger.error(f'Error during search process: {str(e)}')


if __name__ == '__main__':
    runner = Runner()
    runner.run()
