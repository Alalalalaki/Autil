"""General Scraping Class"""

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests_html import HTMLSession
from requests_html import HTML
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tenacity import retry, stop_after_attempt

import pandas as pd
import string
import zipfile


class scraping_general:

    def __init__(self, headers=None):
        self.today = datetime.today()
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'} if headers is None else headers

        session = HTMLSession()
        session.headers.update(headers)
        self.session = session

        self.load_mode = DesiredCapabilities.CHROME

    def get_url(self, url, headers=None, timeout=14, verbose=True, sleep=14):
        """from url get content. allow one retry after sleep."""
        try:
            r = self.session.get(url, headers=headers, timeout=timeout)
        except Exception as e:
            if verbose:
                print(url, str(e))
            time.sleep(sleep)
            # self.login()
            r = self.session.get(url, headers=headers, timeout=timeout)
        return r

    def get_browser(self, headless=True, wait=14, load_mode='eager', load_timeout=14):
        """
        Can set load_mode to 'eager', 'none' or 'normal' (default)
        """
        options = Options()
        options.headless = headless
        options.add_argument("window-size=1920,1080")
        if load_mode:
            self.load_mode["pageLoadStrategy"] = load_mode
            browser = webdriver.Chrome(options=options, desired_capabilities=self.load_mode)
        else:
            browser = webdriver.Chrome(options=options)

        browser.implicitly_wait(wait)
        browser.set_page_load_timeout(load_timeout)
        return browser

    @retry(stop=stop_after_attempt(2))
    def get_url_by_browser(self, browser, url, encoding='utf-8', sleep=0, verbose=False):
        """
        From url get content by browser. allow one retry after sleep.
        Can remove the try except code and all more retry if using @retry.
        """
        try:
            browser.get(url)
            time.sleep(sleep)
        except Exception as e:
            if verbose:
                print(url, str(e))
            time.sleep(sleep)
            browser.get(url)
        r = HTML(html=browser.page_source, default_encoding=encoding)
        return r

    @retry(stop=stop_after_attempt(5))
    def get_content_by_browser(self, browser, encoding='utf-8', sleep=2):
        """
        Only the last part of get_url_by_browser
        """
        time.sleep(sleep)
        r = HTML(html=browser.page_source, default_encoding=encoding)
        return r

    def parse_tr(self, tr, url):
        no_td = len(tr.find('td'))
        no_th = len(tr.find('th'))
        if (no_td == 1) & (no_th == 1):
            n = tr.find('th', first=True).text
            c = tr.find('td', first=True).text
        elif (no_td == 2) & (no_th == 0):
            n = tr.find('td')[0].text
            c = tr.find('td')[1].text
        else:
            raise ValueError(f'Error: tr should be either 1th&1td or 2td: {url} - {tr.text}')
        return n, c
