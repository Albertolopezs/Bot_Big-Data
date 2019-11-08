import scrapy
from scrapy import signals
import json

_words=[]
_descriptions=[]
_url_attachment=[]
_url_word=[]

class ITSpider(scrapy.Spider):
    name = "it-glossary"

    start_urls = [
        "https://www.gartner.com/it-glossary"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ITSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        letra = response.xpath("//div[contains(@class,'btn')]/a")    
        for w in letra:                    # set the limit here
            link= self.start_urls[0]+w.xpath('@href').getall()[0]
            print('------------>'+link)
            yield scrapy.Request(link, callback=self.parse_word_pages)



    def parse_ind_pages(self,response):
        global _descriptions,_words,_url_word,_url_attachment
        question = response.xpath('//h2/text()')
        answer = response.xpath("//div[@class='summary']/text()")
        print(question[0].extract())
        img_tmp = []
        for j in range(len(question)):
            _words.append(question[j].get())  
            _descriptions.append(answer[j].get())
            _url_attachment.append([])
            _url_word.append(response.url)

    def parse_word_pages(self,response):
        letra = response.xpath("//div[@class='browse-list']//a")    
        for w in letra:                    # set the limit here
            link= self.start_urls[0]+ w.xpath('@href').getall()[0]
            print('------------>'+link)
            yield scrapy.Request(link, callback=self.parse_ind_pages)

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
    