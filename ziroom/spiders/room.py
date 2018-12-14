# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import pytesseract
from ..items import ZiroomItem
from scrapy_redis.spiders import RedisSpider

###分布式与scrapy转换的收需要改继承的类   和   redis-key
class RoomSpider(scrapy.Spider):
    name = 'room'
    # redis_key = "RoomSpider:start_urls"
    allowed_domains = ['ziroom.com']
    start_urls = ['http://www.ziroom.com/z/nl/z2.html/']

    def parse(self, response):
        city1_list = response.xpath('//dl[@class="clearfix"]/dd/div[@class="clearfix t"]/a[2]')
        type = city1_list.xpath('./text()').extract_first()
        city1_href = city1_list.xpath('./@href').extract_first()
        item = ZiroomItem()
        item['type'] = type
        if city1_href is not None:
            new_href = 'http:'+city1_href
            yield scrapy.Request(url=new_href, meta={'meta1': item}, callback=self.city2)

    def city2(self, response):
        meta1 = response.meta['meta1']
        city2_list = response.xpath('//dl[@class="clearfix zIndex6"]/dd/ul[@class="clearfix filterList"]/li/span[@class="tag"]/a')

        for city2s in city2_list:
            city2 = city2s.xpath('./text()').extract_first()#区名
            city2_href = city2s.xpath('./@href').extract_first()
            count = response.xpath('//div[@class="pages"]/a[4]/text()').extract_first()#页数
            print(count)
            ###翻页爬取
            for i in range(1, int(count) + 1):
                item = ZiroomItem()
                item['type'] = meta1['type']
                item['type_area'] = city2
                new_href = 'http:{}?p={}'.format(city2_href, str(i))
                # print(new_href)
                yield scrapy.Request(url=new_href, meta={'meta2': item}, callback=self.city3)

    # def city2(self, response):
    #     meta1 = response.meta['meta1']
    #     city2_list = response.xpath('//dl[@class="clearfix zIndex6"]/dd/ul[@class="clearfix filterList"]/li/span[@class="tag"]/a')
    #
    #     for city2s in city2_list:
    #         city2 = city2s.xpath('./text()').extract_first()
    #         city2_href = city2s.xpath('./@href').extract_first()
    #         item = ZiroomItem()
    #         item['type'] = meta1['type']
    #         item['type_area'] = city2
    #         if city2_href is not None:
    #             new_href = 'http:' + city2_href
    #             yield scrapy.Request(url=new_href, meta={'meta2': item}, callback=self.city3)
    #         count = response.xpath('//div[@class="pages"]/a[4]').extract_first()
    #         href = response.xpath('//dl[@class="clearfix zIndex6"]/dd/ul[@class="clearfix filterList"]/li/span[@class="tag"]/a/@href').extract_first()
    #         for i in range(2,int(count)+1):
    #             url = 'http:{}?p={}'.format(href,str(i))
    #             print(url)
    #             yield scrapy.Request(url=url,callback=self.parse())
    def city3(self, response):
        meta2 = response.meta['meta2']
        city3_list = response.xpath('//div[@class="t_newlistbox"]/ul[@id="houseList"]/li[@class="clearfix"]')
        for city3s in city3_list:
            name = city3s.xpath('./div[@class="txt"]/h3/a/text()').extract_first()
            rental = city3s.xpath('./div[@class="txt"]/h4/span/text()').extract_first()
            area = city3s.xpath('./div[@class="txt"]/div[@class="detail"]/p[1]/span[1]/text()').extract_first()
            floor = city3s.xpath('./div[@class="txt"]/div[@class="detail"]/p[1]/span[2]/text()').extract_first()
            hall = city3s.xpath('./div[@class="txt"]/div[@class="detail"]/p[1]/span[3]/text()').extract_first()
            distance = city3s.xpath('./div[@class="txt"]/div[@class="detail"]/p[2]/span/text()').extract_first()
            subway = city3s.xpath('./div[@class="txt"]/p[@class="room_tags clearfix"]/span[1]/text()').extract_first()
            heating = city3s.xpath('./div[@class="txt"]/p[@class="room_tags clearfix"]/span[2]/text()').extract_first()
            friend_home = city3s.xpath('./div[@class="txt"]/p[@class="room_tags clearfix"]/a/span/text()').extract_first()
            price = city3s.xpath('./div[@class="priceDetail"]/p[@class="priceDetail"]/span[1]/text()').extract_first()
            item = ZiroomItem()
            item['type'] = meta2['type']
            item['type_area'] = meta2['type_area']
            item['name'] = name
            item['rental'] = rental.strip()
            item['area'] = area
            item['floor'] = floor
            item['hall'] = hall
            item['distance'] = distance
            item['subway'] = subway
            item['heating'] = heating
            item['friend_home'] = friend_home
            item['price'] = price
            yield item
    #
    # def city4(self, response):
    #     meta3 = response.meta['meta3']
    #     city4_list = response.xpath('//tr[@class="towntr"]/td[2]/a')
    #     for city4s in city4_list:
    #         city4 = city4s.xpath('./text()').extract_first()
    #         city4_href = city4s.xpath('./@href').extract_first()
    #         item = ShengshiliandongItem()
    #         item['first_city'] = meta3['first_city']
    #         item['second_city'] = meta3['second_city']
    #         item['third_city'] = meta3['third_city']
    #         item['fouth_city'] = city4
    #         if city4_href is not None:
    #             new_href = response.urljoin(city4_href)
    #             yield scrapy.Request(url=new_href, meta={'meta4': item}, callback=self.city5)
    #
    # def city5(self, response):
    #     meta4 = response.meta['meta4']
    #     city5_list = response.xpath('//tr[@class="villagetr"]/td[3]/text()').extract()
    #     for city5s in city5_list:
    #         item = ShengshiliandongItem()
    #         item['first_city'] = meta4['first_city']
    #         item['second_city'] = meta4['second_city']
    #         item['third_city'] = meta4['third_city']
    #         item['fouth_city'] = meta4['fouth_city']
    #         item['fifth_city'] = city5s
    #         yield item