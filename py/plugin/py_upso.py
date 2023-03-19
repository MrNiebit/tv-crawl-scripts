# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import requests
import json
import base64


class Spider(Spider):
    def getDependence(self):
        return ['py_ali']

    def getName(self):
        return "py_upso"

    def init(self, extend):
        self.ali = extend[0]
        print("============py_yiso============")
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        return result

    def homeVideoContent(self):
        result = {}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        return result

    header = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2049A Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36",
        "Referer": "https://upyunso.com/"
    }

    def detailContent(self, array):
        return self.ali.detailContent(array)

    def searchContent(self, key, quick):
        url = "https://api.upyunso.com/search?keyword={}&page=1&s_type=2".format(key)
        res = requests.get(url, verify=False, headers=self.header)
        text = base64.b64decode(res.text).decode('UTF-8')
        data_json = json.loads(text)
        videos = []
        for vod in data_json['result']['items'][2:]:
            videos.append({
                "vod_id": vod['page_url'],
                "vod_name": vod['title'].replace('<em>', '').replace('</em>', ''),
                "vod_pic": "https://inews.gtimg.com/newsapp_bt/0/13263837859/1000",
                "vod_remarks": vod['available_time']
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        return self.ali.playerContent(flag, id, vipFlags)

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self, param):
        action = {}
        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':
    spider = Spider()
    res = spider.searchContent('龙珠', None)
    print(json.dumps(res, ensure_ascii=False))
    pass
