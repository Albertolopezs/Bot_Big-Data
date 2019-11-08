import scrapy
from scrapy import signals
import json

_words=[]
_descriptions=[]
_url_attachment=[]
_url_word=[]

class AnalyticsSpider(scrapy.Spider):
    name = "glossary-analitics-bd"

    start_urls = [
        "https://www.exasol.com/en/insights/big-data-and-analytics-glossary/"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AnalyticsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        word = response.xpath('//div[contains(@class,"et_pb")]//p//a')    
        for w in word:                    # set the limit here
            link= w.xpath('@href').getall()[0]
            print('------------>'+link)
            yield scrapy.Request(link, callback=self.parse_ind_pages)



    def parse_ind_pages(self,response):
        global _descriptions,_words,_url_word,_url_attachment
        question = response.xpath('//div[contains(@class,"et_pb_section_1")]//h2/text()')
        answer = response.xpath('//div[contains(@class,"et_pb_section_1")]//p/text()')
        images = response.xpath('//div[contains(@class,"et_pb_section_1")]//img')
        print(question[0].extract())
        img_tmp = []
        for j in range(len(question)):
            for k in range(len(images)):
                img_link = images.xpath('@src').getall()[k]
                img_tmp.append(img_link)
            _words.append(question[j].get())  
            _descriptions.append(answer[j].get())
            _url_attachment.append(img_tmp)
            _url_word.append(response.url)

    def spider_idle(self):
        global _descriptions,_words,_url_word,_url_attachment
        json_total ={}
        for x in range(len(_words)):
            json_d = {'Word':_words[x],'Description':_descriptions[x],'Url':_url_word[x],'Attachment_Url':_url_attachment[x]}
            json_total[x] = json_d
            json_total.update(json_d)


        page = self.start_urls[0].split("/")[-2]
        filename = '../../datasets/%s.json' % page
        with open(filename, 'wb') as f:
            json.dump(json_total, f)
        self.log('Saved file %s' % filename)         
    