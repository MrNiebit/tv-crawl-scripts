# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json
from urllib.parse import unquote
import base64


class Spider(Spider):  # 元类 默认的元类 type

    def __init__(self):
        self.home_url = "https://yanetflix.tv"

    def getName(self):
        return "鸭奈飞"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        # http://www.lezhutv.com/
        result = {}
        cateManual = {
            "电影": "dianying",
            "连续剧": "lianxuju",
            "动漫": "dongman",
            "综艺": "zongyi",
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        rsp = self.fetch(self.home_url, headers=self.header)
        root = self.html(rsp.text)
        vodList = root.xpath('//div[@class="module-items module-poster-items-small scroll-content"]/a')

        videos = []
        for vod in vodList:
            name = vod.xpath("./@title")[0]
            pic = vod.xpath(".//img/@data-original")[0]
            mark = vod.xpath('.//div[@class="module-item-note"]//text()')[0]
            sid = vod.xpath("./@href")[0]
            sid = self.regStr(sid, "/voddetail/(\\S+).html")
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
        result = {}
        url_path = "/vodshow/%s--------%s---.html" % (tid, pg)

        url = self.home_url + url_path

        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        vodList = root.xpath('//div[@class="module"]/a')
        videos = []
        for vod in vodList:
            name = vod.xpath("./@title")[0]
            pic = vod.xpath(".//img/@data-original")[0]
            mark = vod.xpath('.//div[@class="module-item-note"]//text()')[0]
            sid = vod.xpath("./@href")[0]
            sid = self.regStr(sid, "/voddetail/(\\S+).html")
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
        tid = array[0]
        url = self.home_url + '/voddetail/{0}.html'.format(tid)
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        node = root.xpath("//div[@class='module-info-main']")[0]
        title = node.xpath(".//h1/text()")[0]
        pic = root.xpath('//div[@class="module-info-poster"]//div[@class="module-item-pic"]/img/@data-original')[0]
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
        infoArray = node.xpath(".//div[@class='module-info-item']")
        for info in infoArray:
            content = info.xpath('string(.)')
            # if content.startswith('分類'):
            # 	vod['type_name'] = content
            # if content.startswith('年份'):
            # 	vod['vod_year'] = content
            # if content.startswith('地区'):
            # 	vod['vod_area'] = content
            #if content.startswith('片长'):
            #    vod['vod_remarks'] = content.replace('\n', '').replace('\t', '')
            if content.startswith('主演'):
                vod['vod_actor'] = content.replace('\n', '').replace('\t', '')
            if content.startswith('导演'):
                vod['vod_director'] = content.replace('\n', '').replace('\t', '')
        # if content.startswith('剧情'):
        # 	vod['vod_content'] = content.replace('\n','').replace('\t','')
        vod['vod_content'] = root.xpath('//div[@class="module-blocklist scroll-box scroll-box-y module-player-list"]/span//text()')[0]
        vod_play_from = '$$$'
        playFrom = []
        item_header_node = root.xpath('//div[@id="y-playList"]/div')
        for v in item_header_node:
            playFrom.append(v.xpath('./span/text()')[0] + '(' + v.xpath('./small/text()')[0] + ')')
        vod_play_from = vod_play_from.join(playFrom)

        vod_play_url = '$$$'
        playList = []
        vodList = root.xpath('//div[@id="panel1"]')

        for vl in vodList:
            vodItems = []
            aList = vl.xpath('./div[@class="module-play-list"]/div/a')
            for tA in aList:
                href = tA.xpath('./@href')[0]
                name = tA.xpath('.//text()')[0]
                tId = self.regStr(href, '/vodplay/(\\S+).html')
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
        url = self.home_url + "/vodsearch/{}----------1---.html".format(key)
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        print(root)
        vodList = root.xpath('//div[@class="module-items module-card-items"]/div')

        videos = []
        for vod in vodList:
            img_node = vod.xpath('./a//div[@class="module-item-pic"]/img')[0]
            name = img_node.xpath("./@alt")[0]
            pic = img_node.xpath("./@data-original")[0]

            mark = vod.xpath('./a//div[@class="module-item-note"]//text()')[0]
            sid = vod.xpath("./a/@href")[0]
            sid = self.regStr(sid, "/voddetail/(\\S+).html")
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

    def playerContent(self, flag, id, vipFlags):
        # https://meijuchong.cc/static/js/playerconfig.js
        result = {}
        url = self.home_url + '/vodplay/{}.html'.format(id)
        rsp = self.fetch(url, headers=self.header)
        config_str = self.regStr(rsp.text, 'player_aaaa=(\\S+?)<')
        config_json = json.loads(config_str)

        result["parse"] = 1
        result["playUrl"] = self.config['player'][config_json['from']]['parse'].replace(r'\/', '/')
        result["url"] = unquote(base64.b64decode(config_json['url']).decode())
        result["header"] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Referer": "https://yanetflix.com"
        }
        return result

    config = {
        "player": {
            "NetflixOME": {
                "show": "NetflixA",
                "des": "NetflixA",
                "ps": "1",
                "parse": "https:\/\/netflixku.4kya.com\/?url="
            },
            "QEys": {
                "show": "NetflixB",
                "des": "NetflixB",
                "ps": "1",
                "parse": "https:\/\/netflixku.4kya.com\/?url="
            },
            "NetflixC": {
                "show": "NetflixC",
                "des": "NetflixC",
                "ps": "1",
                "parse": "https:\/\/netflixku.4kya.com\/?url="
            },
            "NetflixD": {
                "show": "NetflixD",
                "des": "NetflixD",
                "ps": "1",
                "parse": "https:\/\/netflixku.4kya.com\/player\/?url="
            },
            "rx": {
                "show": "NetflixRX",
                "des": "NetflixRX",
                "ps": "1",
                "parse": "https:\/\/rx.4kya.com\/?url="
            },
            "dxzy": {
                "show": "NetflixDX",
                "des": "",
                "ps": "1",
                "parse": "https:\/\/dp.4kya.com\/dp\/?url="
            },
            "ffm3u8": {
                "show": "NetflixFF",
                "des": "NetflixFF",
                "ps": "1",
                "parse": "https:\/\/player.azx.me\/player\/index.php?key=0&api=https:\/\/netflix.mom\/&url="
            },
            "feifan": {
                "show": "NetflixFFZ",
                "des": "NetflixFFZ",
                "ps": "1",
                "parse": "https:\/\/player.azx.me\/player\/index.php?key=0&api=https:\/\/netflix.mom\/&url="
            },
            "lzm3u8": {
                "show": "NetflixLZ",
                "des": "",
                "ps": "1",
                "parse": "https:\/\/player.azx.me\/player\/index.php?key=0&api=https:\/\/yanetflix.com\/&url="
            },
            "liangzi": {
                "show": "NetflixLZX",
                "des": "",
                "ps": "0",
                "parse": ""
            },
            "netflixmom": {
                "show": "Netflix",
                "des": "",
                "ps": "1",
                "parse": "https:\/\/player.4kya.com\/?url="
            },
            "netflixpro": {
                "show": "NetflixPro",
                "des": "NetflixPro",
                "ps": "1",
                "parse": "https:\/\/player.4kya.com\/?url="
            },
            "netflixmax": {
                "show": "NetflixMAX",
                "des": "NetflixMAX",
                "ps": "1",
                "parse": "https:\/\/player.4kya.com\/?url="
            },
            "netflixlv": {
                "show": "NetflixLV",
                "des": "",
                "ps": "1",
                "parse": "https:\/\/netflixvip.4kya.com\/?url="
            },
            "netflixzx": {
                "show": "NetflixZX",
                "des": "",
                "ps": "1",
                "parse": "https:\/\/netflixku.4kya.com\/?url="
            },
            "haiwaikan": {
                "show": "翻墙源",
                "des": "翻墙源",
                "ps": "1",
                "parse": "https:\/\/player.azx.me\/player\/index.php?key=0&api=https:\/\/netflix.mom\/&url="
            },
            "youku": {
                "show": "youku",
                "des": "youku",
                "ps": "1",
                "parse": ""
            },
            "qiyi": {
                "show": "qiyi",
                "des": "",
                "ps": "1",
                "parse": ""
            }
        },
        "filter": {}
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    def localProxy(self, param):
        action = {}
        return [200, "video/MP2T", action, ""]


if __name__ == '__main__':

    spider = Spider()
    # res = spider.searchContent('龙珠', None)
    # res = spider.detailContent(['56492'])
    res = spider.categoryContent('dianying', '1', None, {})
    # res = spider.playerContent(None, '56492-1-1', None)
    print(json.dumps(res, ensure_ascii=False))
    pass