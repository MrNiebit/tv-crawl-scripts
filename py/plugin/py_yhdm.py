# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json


class Spider(Spider):
    def getName(self):
        return "樱花动漫"

    def __init__(self):
        self.home_url = "http://www.yinghuacd.com"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "日本动漫": "japan",
            "国产动漫": "china",
            "美国动漫": "american",
            "动漫电影": "movie",
            "亲子动漫": "63",
            "OVA版": "36",
            "剧场版": "37",
            "真人版": "38",
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        # if filter:
        #     result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        res = self.fetch(self.home_url, headers=self.header)
        root = self.html(res.text)
        item_list = root.xpath('//div[@class="firs l"]/div[@class="img"][1]/ul/li')
        videos = []
        for item in item_list:
            href = item.xpath('./a/@href')[0]
            sid = self.regStr(href, '/show/(\\S+).html')
            name = item.xpath('./a/img/@alt')[0]
            pic = item.xpath('./a/img/@src')[0]
            mark = " ".join(item.xpath('./p[2]//text()'))
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if str(pg) == '1':
            category_url = self.home_url + '/%s/' % tid
        else:
            category_url = self.home_url + "/%s/%s.html" % (tid, pg)
        res = self.fetch(category_url, headers=self.header)
        root = self.html(res.text)
        item_list = root.xpath('//div[@class="lpic"]/ul/li')
        videos = []
        for item in item_list:
            href = item.xpath('./a/@href')[0]
            sid = self.regStr(href, '/show/(\\S+).html')
            name = item.xpath('./a/img/@alt')[0]
            pic = item.xpath('./a/img/@src')[0]
            mark = " ".join(item.xpath('./span[1]//text()'))
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        return {
            'list': videos,
            'page': pg,
            'pagecount': 99999,
            'limit': 99,
            'total': 999999
        }

    def detailContent(self, array):
        detail_url = self.home_url + "/show/%s.html" % array[0]
        res = self.fetch(detail_url, headers=self.header)
        root = self.html(res.text)
        pic = root.xpath("//div[contains(@class, 'thumb')]/img/@src")[0]
        title = root.xpath("//div[contains(@class, 'rate')]/h1/text()")[0]
        vod = {
            "vod_id": array[0],
            "vod_name": title,
            "vod_pic": pic,
            "type_name": " ".join(root.xpath("//div[@class='sinfo']/span[3]//text()")),
            "vod_year": " ".join(root.xpath("//div[@class='sinfo']/span[1]//text()")),
            "vod_area": " ".join(root.xpath("//div[@class='sinfo']/span[2]//text()")),
            "vod_remarks": root.xpath("//div[@class='sinfo']/p/text()")[0],
            "vod_actor": "",
            "vod_director": "",
            "vod_content": root.xpath("//div[@class='area']/div[@class='fire l']/div[@class='info']/text()")[0]
        }

        vod_play_from = '$$$'
        playFrom = []
        vodHeader = root.xpath('//ul[@id="menu0"]/li/text()')
        for v in vodHeader:
            playFrom.append(v)
        vod_play_from = vod_play_from.join(playFrom)

        vod_play_url = '$$$'
        playList = []
        vodList = root.xpath("//div[@id='main0']")
        for vl in vodList:
            vodItems = []
            aList = vl.xpath('./div/ul/li/a')
            for tA in aList:
                href = tA.xpath('./@href')[0]
                name = tA.xpath('./text()')[0]
                tId = self.regStr(href, '/v/(\\S+).html')
                vodItems.append(name + "$" + tId)
            joinStr = '#'
            joinStr = joinStr.join(vodItems)
            playList.append(joinStr)
        vod_play_url = vod_play_url.join(playList)

        vod['vod_play_from'] = vod_play_from
        vod['vod_play_url'] = vod_play_url

        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        search_url = self.home_url + '/search/{}/'.format(key)
        res = self.fetch(search_url, headers=self.header)
        root = self.html(res.text)
        item_list = root.xpath('//div[@class="lpic"]/ul/li')
        videos = []
        for item in item_list:
            href = item.xpath('./a/@href')[0]
            sid = self.regStr(href, '/show/(\\S+).html')
            name = item.xpath('./a/img/@alt')[0]
            pic = item.xpath('./a/img/@src')[0]
            mark = " ".join(item.xpath('./span[1]//text()'))
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        return {
            'list': videos
        }

    def playerContent(self, flag, id, vipFlags):
        detail_url = self.home_url + "/v/%s.html" % id
        res = self.fetch(detail_url, headers=self.header)
        root = self.html(res.text)
        play_url = root.xpath('//div[@id="playbox"]/@data-vid')[0]
        return {
            'parse': 0,
            'url': play_url.split('$')[0]
        }

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self, param):
        action = {
            'url': '',
            'header': '',
            'param': '',
            'type': 'string',
            'after': ''
        }
        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':
    spider = Spider()
    # res = spider.homeVideoContent()
    res = spider.categoryContent('japan', '1', None, None)
    # res = spider.detailContent(['5784'])
    # res = spider.searchContent('一', None)
    # res = spider.playerContent(None, '5649-30', None)
    print(json.dumps(res, ensure_ascii=False))
