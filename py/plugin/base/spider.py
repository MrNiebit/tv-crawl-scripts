import requests
from lxml import etree
import re


class Spider:
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    def fetch(self, url, headers=None):
        return requests.get(url, headers=headers)

    def html(self, text):
        return etree.HTML(text)

    def regStr(self, text, reg):
        res_list = re.findall(reg, text)
        if res_list is None or len(res_list) < 1:
            return None
        return res_list[0]
