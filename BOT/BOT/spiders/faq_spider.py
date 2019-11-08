import scrapy
from scrapy import signals
import json

question=[]
answer = []
url_attachment=[]
url_word=[]


class FAQSpider(scrapy.Spider):
    name = "faq"

    start_urls = [
        "https://machinelearningmastery.com/faq/"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FAQSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        for i in range(1,8):
            _block = response.xpath("//li[@class='toctree-l1']["+str(i)+"]")
            _mainSection = response.xpath("//li[@class='toctree-l1']["+str(i)+"]/ul/li/a")                                       
            self.parse_ind_pages(response)



    def parse_ind_pages(self,response):
        global question,answer,url_word,url_attachment
        _preguntas = response.xpath("(//div[@class='ufaq-faq-category'])[2]/div/div")
        for i in range(len(_preguntas)):
            #Abrimos la pregunta
            #_preguntas[i].click()
            _title = _preguntas[i].xpath(".//h4/text()").extract()
            _description = _preguntas[i].xpath(".//div/div//text()").extract() 
            _attachs = response.xpath("(//div[@class='ufaq-faq-category'])["+str(i)+"]/div/div//div/div//a/@href").getall()
            question.append(_title)
            answer.append(_description)
            url_word.append(response.url)
            url_attachment.append([_attachs])

    def spider_idle(self):
        global question,answer,url_word,url_attachment
        json_total = {}
        for x in range(len(question)):
            json_d = {'question':question[x],'answer':answer[x],'url':url_word[x],'attachment_url':url_attachment[x]}
            json_total[x] = json_d
            json_total.update(json_d)


        with open('../../datasets/faq_ml.json', 'w') as outfile:
            json.dump(json_total, outfile)
            