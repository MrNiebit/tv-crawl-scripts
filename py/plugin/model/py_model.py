# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json


class Spider(Spider):

    def getName(self):
        return "Model"

    def __init__(self):
        pass

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "电视剧": "dianshiju",
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
        videos = []
        sid = ""
        name = ""
        pic = ""
        mark = ""
        videos.append({
            # sid /xxx.html
            "vod_id": sid,
            # 影片名
            "vod_name": name,
            # 图片地址
            "vod_pic": pic,
            # 更新集数
            "vod_remarks": mark
        })
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        videos = []
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
        result = {}
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
        vod['vod_play_from'] = vod_play_from
        vod['vod_play_url'] = vod_play_url

        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        videos = []
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

        return {
            # parse 0: 直链  1：嗅探URL
            'pare': 0,
            'url': ''
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
