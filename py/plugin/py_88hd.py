#!/usr/bin/python3
# --*-- coding: utf-8 --*--
# @Author: gitsilence
# @Time: 2022/12/26 16:32
import json

import sys

sys.path.append('..')
from base.spider import Spider
import requests
from urllib.parse import unquote


class Spider(Spider):

    def __init__(self):
        self.config = {
            "dplayer": {"tpm3u8": "淘片资源", "xkm3u8": "想看资源", "sdm3u8": "闪电资源", "bdxm3u8": "北斗资源",
                        "hnm3u8": "红牛资源", "wjm3u8": "无尽资源", "kbm3u8": "快播资源", "zjm3u8": "自建云",
                        "tt": "TT云", "tkm3u8": "天空资源", "mahua": "麻花资源", "baidu": "千度云",
                        "bilibili": "二次云", "migutv": "咪咕云", "aqd": "爱情岛播放源", "youku": "优酷播放源",
                        "wy": "微软云", "qq": "腾讯播放源", "sohu": "搜狐播放源", "qiyi": "奇艺播放源",
                        "letv": "乐视播放源", "pptv": "PPTV播放源", "mgtv": "芒果播放源", "panda": "熊猫云",
                        "kuyun": "酷云播放源", "zuidam3u8": "ZDm3u8播放源", "zkm3u8": "zkm3u8播放源",
                        "dbm3u8": "百度资源", "bjm3u8": "八戒播放源", "123kum3u8": "123资源", "xigua": "西瓜视频",
                        "m3u8": "m3u8播放源"}
        }
        self.home_url = 'https://www.88hd.com'
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Referer": "https://www.88hd.com/search/",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def homeContent(self, filter):
        # http://www.lezhutv.com/
        result = {}
        cateManual = {
            "电影": "1",
            "电视剧": "2",
            "动漫": "4",
            "综艺": "3"
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

    def getName(self):
        return '88影视'

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeVideoContent(self):
        rsp = self.fetch(self.home_url, headers=self.header)
        root = self.html(rsp.content.decode('UTF-8'))
        vodList = root.xpath('//div[@class="index-tj-l"]/ul/li/a')

        videos = []
        for vod in vodList:
            name = vod.xpath("./@title")[0]
            pic = vod.xpath("./img/@data-original")[0]
            mark = vod.xpath('./p[@class="other"]/i/text()')
            sid = vod.xpath("./@href")[0]
            sid = self.regStr(sid, "/detail/(\\S+).html")
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        result = {
            'list': videos
        }
        return result

    def categoryContent(self, tid, pg, filter, extend):
        url_path = "/vod-type-id-%s-pg-%s.html" % (tid, pg)
        url = self.home_url + url_path
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.content.decode('UTF-8'))
        item_path_list = root.xpath('//div[@class="index-area clearfix"]/ul/li/a')
        videos = []
        result = {}
        for a in item_path_list:
            name = a.xpath("./@title")[0]
            pic = a.xpath("./img/@data-original")[0]
            mark = a.xpath('./p[@class="other"]/i/text()')[0]
            sid = a.xpath("./@href")[0]
            sid = self.regStr(sid, "(\\S+).html")
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, array):
        # video-info-header
        tid = array[0]
        url = self.home_url + '{0}.html'.format(tid)
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.content.decode('UTF-8'))
        title = root.xpath("//div[@class='ct-c']/dl[1]/h1/text()")[0]
        pic = root.xpath("//div[@class='ct-l']/img/@src")[0]
        vod = {
            "vod_id": tid,
            "vod_name": title,
            "vod_pic": pic,
            "type_name": "",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": ""
        }
        vod['type_name'] = root.xpath("//div[@class='ct-c']/dl/dd[1]/text()")[0]
        vod['vod_year'] = root.xpath("//div[@class='ct-c']/dl/dd[5]/text()")[0]
        vod['vod_area'] = root.xpath("//div[@class='ct-c']/dl/dd[4]/text()")[0]
        vod['vod_remarks'] = root.xpath("//div[@class='ct-c']/dl/dd[2]/text()")[0]
        vod['vod_actor'] = root.xpath("//div[@class='ct-c']/dl/dt[2]/text()")[0]
        vod['vod_director'] = root.xpath("//div[@class='ct-c']/dl/dd[3]/text()")[0]
        vod['vod_content'] = root.xpath("//div[@class='ct-c']/div//text()")[0]

        vod_play_from = '$$$'
        playFrom = []
        vodHeader = root.xpath("//div[@class='playfrom tab8 clearfix']/ul/li//text()")
        for v in vodHeader:
            playFrom.append(v)
        vod_play_from = vod_play_from.join(playFrom)

        vod_play_url = '$$$'
        playList = []
        vodList = root.xpath("//div[@class='playlist clearfix']")
        for vl in vodList:
            vodItems = []
            aList = vl.xpath('./div/ul/li/a')
            for tA in aList:
                href = tA.xpath('./@href')[0]
                name = tA.xpath('./@title')[0]
                tId = self.regStr(href, '(\\S+).html')
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
        search_url = self.home_url + '/search/'
        data = {
            "wd": key,
            "submit": ""
        }
        rsp = requests.post(search_url, headers=self.header, data=data)
        root = self.html(rsp.content.decode('UTF-8'))
        vodList = root.xpath('//div[@class="index-area clearfix"]/ul/li/a')
        videos = []
        for vod in vodList:
            name = vod.xpath("./@title")[0]
            pic = vod.xpath("./img/@data-original")[0]
            mark = vod.xpath('./p[@class="other"]/i/text()')[0]
            sid = vod.xpath("./@href")[0]
            sid = self.regStr(sid, "(\\S+).html")
            videos.append({
                "vod_id": sid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": mark
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlag):
        player_url = self.home_url + id + '.html'
        rsp = self.fetch(player_url, headers=self.header)
        content = rsp.content.decode('UTF-8')
        video_ids_str = self.regStr(content, 'mac_url=unescape\(\'(.*?)\'\);')
        unicode_str = unquote(video_ids_str).replace('%', '\\').encode()
        video_ids_str = unicode_str.decode('unicode_escape')
        video_src_list = []
        source_list = video_ids_str.split('$$$')
        # print(video_ids_str)
        for source in source_list:
            video_src_list.append([id.split('$')[1].replace('\x02', '%2') for id in source.split('#')])
        # print(video_src_list)

        mac_from = self.regStr(content, "mac_from='(.*?)'")
        from_list = mac_from.split('$$$')
        src = int(self.regStr(id, 'src-(\d+)-'))
        num = int(self.regStr(id, 'num-(\d+)'))
        # print(src, num)
        rsp = self.fetch('https://www.88hd.com/player/%s.js' % from_list[src - 1], headers=self.header)
        player_url = self.regStr(rsp.text, 'src="(.*?)\'')
        result = {}
        result["parse"] = 1
        result["playUrl"] = player_url
        detail_url = player_url + video_src_list[src - 1][num - 1]
        result["url"] = video_src_list[src - 1][num - 1]

        # print(detail_url)
        rsp = self.fetch(detail_url)
        stream_url = self.regStr(rsp.text, 'video_url = \'(.*?)\'')
        # print(stream_url)
        if stream_url is not None and stream_url != '':
            result['parse'] = 0
            result["playUrl"] = ''
            result['url'] = stream_url
        result["header"] = ''
        return result

    def localProxy(self, param):
        action = {
            'url': '',
            'header': '',
            'param': '',
            'type': 'string',  # 文本内容
            'after': ''
        }
        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':
    spider = Spider()
    # res = spider.categoryContent('1', '1', None, None)
    res = spider.playerContent(None, '/vod-play-id-213261-src-3-num-1', None)
    # res = spider.detailContent(['/guochanju/202301/213261'])
    print(json.dumps(res, ensure_ascii=False))
