import scrapy
from scrapy import signals
import json

_words=[]
_descriptions=[]
_url_attachment=[]
_url_word=[]

class GoogleSpider(scrapy.Spider):
    name = "googlespider"

    start_urls = [
        "https://www.google.com/"
    ]
    base_url = "http://www.google.com/search?q="
    glossary_json = {}
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GoogleSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        self.glossary_json = self.load_glossary()
        print(self.glossary_json)
        for i in range(len(self.glossary_json)):                    # set the limit here
            link= self.base_url+self.glossary_json[str(i)]["Word"]
            print('------------>'+link)
            yield scrapy.Request(link, callback=self.parse_ind_pages)



    def load_glossary(self):
        with open('../../datasets/glossary-of-common-statistics-and-machine-learning-terms.json') as f:
            return json.load(f)


    def parse_ind_pages(self,response):
        global _descriptions,_words,_url_word,_url_attachment
        block = response.xpath('//div[contains(@class,"related-question-pair")]')
        print("Bloque",block)
        for quest_selector in block:
            print("pregunta")
            question = response.xpath('/g-accordion-expander//div[contains(@class,"match-mod")]/text()').extract()
            print(question)
            answer = quest_selector.xpath("/g-accordion-expander//div[@class='mod']/text()").extract()
            url_attach = quest_selector.xpath('/g-accordion-expander//a/@href')
            url_tmp = []
            for url in url_attach:
                url_tmp.append(url.extract())

            _words.append(question)  
            _descriptions.append(answer)
            _url_attachment.append(url_tmp)
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
    