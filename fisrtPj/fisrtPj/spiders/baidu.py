import scrapy
from ..items import CityItem
from lxml import etree
import requests
import json
import  re
import time
class BaiduSpider(scrapy.Spider):
    name = 'busline'

    start_urls = {
        "https://{}.8684.cn/".format('hefei'),
    }

    def parse(self, response):
        items = []
        a_list = response.xpath(
            "//div[@class='bus-layer depth w120']/div[@class='pl10'][1]/div[@class='list']/a/@href").extract()
        all_urls = [response.url + a.strip("/") for a in a_list]  # url前缀列表
        a_list2 = response.xpath(
            "//div[@class='bus-layer depth w120']/div[@class='pl10'][2]/div[@class='list']/a/@href").extract()
        all_urls2 = [response.url + a.strip("/") for a in a_list2]  # url前缀列表
        all_urls = all_urls+all_urls2
        for a in all_urls:
            print(a)
            tree = etree.HTML(requests.get(url=a).text)
            detail_href = tree.xpath("//div[@class='list clearfix']/a/@href")
            for detail in detail_href:
                all_urls_1 = response.url + detail.strip("/")
                tree = etree.HTML(requests.get(url=all_urls_1).text)
                # 公交线路名称
                line_name = tree.xpath("//div[@class='layout-left']/div[@class='bus-lzinfo mb20']//h1/text()")[0]
                index = line_name.find('公交车路线')
                line_name=line_name[2:index]
                time.sleep(2)
                #请求线路经过站点数据
                url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=559bdffe35eec8c8f4dae959451d705c&output=json&city={}&offset=2&keywords={}&platform=JS'.format('合肥', line_name)
                r = requests.get(url).text
                rt = json.loads(r)
                if rt['buslines']:
                    if len(rt['buslines']) == 0:  # 有名称没数据
                        print(line_name+'没有数据！')
                    else:
                        #获取站点数据
                     for cc in range(len(rt['buslines'])):
                         up_down=cc
                         bus_setop = rt['buslines'][cc]["start_stop"]+"-"+rt['buslines'][cc]["end_stop"]
                         bus_cost = rt['buslines'][cc]["total_price"]
                         bus_type = rt['buslines'][cc]["type"]
                         bus_polyline = rt['buslines'][cc]["polyline"]
                         bus_company= rt['buslines'][cc]["company"]
                         for station_list in rt['buslines'][cc]['busstops']:
                             lineItem = CityItem()
                             lineItem["bus_name"] = line_name
                             #上下行
                             lineItem["bus_direction"] = up_down
                             # 起始点
                             lineItem["bus_setop"] = bus_setop
                             #站点
                             lineItem["bus_station"] = station_list["name"]
                             #坐标
                             lineItem["bus_location"] = station_list["location"]
                             #站点序号
                             lineItem["bus_sequence"] = station_list["sequence"]
                             #票价
                             lineItem["bus_cost"] = bus_cost
                             #类型
                             lineItem["bus_type"] = bus_type
                             #线路Polyline
                             lineItem["bus_polyline"] = bus_polyline
                             #所属公司
                             lineItem["bus_company"] = bus_company
                             print(lineItem)
                             items.append(lineItem)
        return items