
import random
import requests
from requests_html import HTMLSession
from seleniumwire import webdriver
from datetime import datetime


from API_KEYS import WEBSHARE


class ProxySession:

    def __init__(self, proxy_change_mode="hour"):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4844.35 Safari/537.36'}

        session = HTMLSession()
        session.headers.update(headers)
        self.session = session
        self.proxies = {}
        self.API_KEY = WEBSHARE

        self.update_proxy()

        assert proxy_change_mode in ["hour", "force"], "proxy_change_mode must be 'force' or 'hour'"
        self.proxy_change_mode = proxy_change_mode
        self.last_proxy_change_hour = datetime.today().hour
        self.hour_for_change = 1
        self.last_proxy_refresh_day = datetime.today().day
        self.day_for_refresh = 7

    def get_proxies(self):
        response = requests.get("https://proxy.webshare.io/api/proxy/list/?", headers={"Authorization": self.API_KEY})
        proxies_ = response.json()
        proxies = [{"http": f"http://{p['username']}:{p['password']}@{p['proxy_address']}:{p['ports']['http']}",
                    "https": f"http://{p['username']}:{p['password']}@{p['proxy_address']}:{p['ports']['http']}"
                    } for p in proxies_['results'] if p['valid']]
        return proxies

    def update_proxy(self):
        self.proxies = self.get_proxies()
        proxy = random.choice(self.proxies)
        self.session.proxies = proxy
        print("Update proxy: ", proxy["http"])

    def replace_proxy(self):
        hour_now = datetime.today().hour
        if self.proxy_change_mode == "force":
            self.update_proxy()
            self.last_proxy_change_hour = hour_now
        elif self.proxy_change_mode == "hour":
            if abs(hour_now - self.last_proxy_change_hour) >= self.hour_for_change:
                self.update_proxy()
                self.last_proxy_change_hour = hour_now

    def refresh_proxies(self):
        day_now = datetime.today().day
        if abs(day_now - self.last_proxy_refresh_day) >= self.day_for_refresh:
            self.proxies = self.get_proxies()
            self.last_proxy_refresh_day = day_now
        print("Refresh proxies")


class ProxyBrowser(ProxySession):
    def __init__(self,):
        super().__init__()

        self.proxy_options = None
        self.chrome_options = None
        self.browser = None

        self.set_option_proxy()
        self.set_option_chrome()
        self.set_browser()

    def set_option_proxy(self,):
        proxies = self.session.proxies
        proxies["no_proxy"] = 'localhost,127.0.0.1'
        proxy_options = {'proxy': proxies}
        self.proxy_options = proxy_options

    def set_option_chrome(self,):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        chrome_options.add_experimental_option("prefs", preferences)
        chrome_options.add_argument("disable-blink-features=AutomationControlled")
        self.chrome_options = chrome_options

    def get_timezone_geolocation(self):
        url = "http://ip-api.com/json/"
        response = self.session.get(url)
        return response.json()

    def set_browser_time_geo(self):
        res_json = self.get_timezone_geolocation()
        geo = {
            "latitude": res_json["lat"],
            "longitude": res_json["lon"],
            "accuracy": 1
        }
        tz = {
            "timezoneId": res_json["timezone"]
        }
        self.browser.execute_cdp_cmd("Emulation.setGeolocationOverride", geo)
        self.browser.execute_cdp_cmd("Emulation.setTimezoneOverride", tz)

    def set_browser(self, headless=True, wait=14):
        # not sure seleniumwire allow for load model thus remove the load module
        chrome_options = self.chrome_options
        chrome_options.headless = headless
        chrome_options.add_argument("window-size=1920,1080")

        browser = webdriver.Chrome(chrome_options=chrome_options, seleniumwire_options=self.proxy_options)
        browser.implicitly_wait(wait)
        self.browser = browser

    def reset_browser(self,):
        """After using `update_proxy` or `replace_proxy`, use this function to reset browser"""
        self.set_option_proxy()
        self.set_browser()
