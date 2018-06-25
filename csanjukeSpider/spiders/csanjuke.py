import scrapy
import re

from csanjukeSpider.items import CsanjukespiderItem


class CsanjukeSpider(scrapy.Spider):
    name = 'csanjuke'
    allowed_domains = ['cs.anjuke.com']
    url = 'https://cs.anjuke.com/sale/p{}/'
    page = 1
    start_urls = [url.format(page)]
    
    def parse(self, response):
        links = response.xpath('//ul[@id="houselist-mod-new"]//li//div[@class="house-title"]/a/@href').extract()
        print('正在爬取第{}页，本页有{}个房源\n'.format(self.page, len(links)))
        print('本页的url是:{}'.format(response.url))
        for link in links:
            yield scrapy.Request(link, meta={'url': link}, callback=self.parse_item)
        if response.xpath('//a[@class="aNxt"]'):
            self.page += 1
            yield scrapy.Request(self.url.format(self.page), callback=self.parse)
        
    def parse_item(self, response):
        responseUrl = response.url
        requestUrl = response.meta['url']
        if responseUrl == str(requestUrl):
            f = lambda x: x if x else [None]*3
            f1 = lambda x: x.strip() if x else None
            item = CsanjukespiderItem()
            item['house_link'] = response.url
            item['long_title'] = response.xpath('//h3[@class="long-title"]/text()').extract()[0].strip()
            print('正在爬取:{}'.format(item['long_title']))
            item['c_label'] = 1 if response.xpath('//i[@class="guarantee_icon"]') else 0
            #item['house_pics'] = response.xpath('//div[@class="img_wrap"]/img/@data-src').extract()
            info = response.xpath('//span[@class="house-encode"]/text()').extract()[0].split()[1].split('，')
            item['num'] = info[0]
            item['release_time'] = info[1].split('：')[1]
            try:
                house_info = response.xpath('//div[@class="houseInfo-detail clearfix"]//dd')
            except:
                item['community'],item['location'],item['built_year'],item['house_type'],item['house_structure'],item['house_space'],item['house_orientation'],item['house_floor'],item['unit_price'],item['down_payment'],item['decoration'] = [None]*11
            item['community'] = f(house_info[0].xpath('./a/text()').extract())[0]
            s = f(house_info[1].xpath('.//p[@class="loc-text"]/text()').extract())[1]
            pattern = re.compile('[0-9a-zA-Z\\u4e00-\\u9fa5]+')
            item['location'] = '-'.join(house_info[1].xpath('.//a/text()').extract() + pattern.findall(s))
            item['built_year'] = f(house_info[2].xpath('./text()').extract())[0]
            item['house_type'] = f(house_info[3].xpath('./text()').extract())[0]
            item['house_structure'] = ''.join(pattern.findall(f(house_info[4].xpath('./text()').extract())[0]))
            item['house_space'] = f(house_info[5].xpath('./text()').extract())[0]
            item['house_orientation'] = f(house_info[6].xpath('./text()').extract())[0]
            item['house_floor'] = f1(f(house_info[7].xpath('./text()').extract())[0])
            item['unit_price'] = f(house_info[8].xpath('./text()').extract())[0]
            item['down_payment'] = f1(f(house_info[9].xpath('./text()').extract())[0])
            #item['monthly_payment'] =
            item['decoration'] = f1(f(house_info[11].xpath('./text()').extract())[0])
            try:
                h = response.xpath('//div[@class="houseInfo-desc"]')[0]
            except:
                item['house_advantage'],item['owner_thought'],item['community_supporting'],item['commission'] = [None]*4
            item['house_advantage'] = ''.join(h.xpath('.//span[@style]/text()').extract())
            item['owner_thought'] = f1(''.join(h.xpath('.//div[@class="houseInfo-item"][2]/div/text()').extract()))
            item['community_supporting'] = f1(''.join(h.xpath('.//div[@class="houseInfo-item"][3]/div/text()').extract()))
            item['commission'] = f(h.xpath('.//div[@class="houseInfo-item"][4]//span[@class="tags-service tags-money"]/text()').extract())[0]
            item['community_overview'] = f(response.xpath('//dl[@class="info-character good-character"]/*/text()').extract())[0]
            item['community_defects'] = f(response.xpath('//dl[@class="info-character bad-character"]/*/text()').extract())[0]
            yield item
        else:
            print('---------------------Your request is redirect,retrying----------------------')
            yield scrapy.Request(url=str(requestUrl), meta={'url': requestUrl}, callback=self.parse_item, dont_filter=True)

