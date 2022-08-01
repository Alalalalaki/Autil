
import random
import requests
from requests_html import HTMLSession
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
