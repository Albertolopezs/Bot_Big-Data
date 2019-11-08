import scrapy
from scrapy import signals
import json

_title=[]
_codeBlock = []
_descriptions=[]
_url_attachment=[]
_url_word=[]


class SKSpider(scrapy.Spider):
    name = "scikit"

    start_urls = [
        "https://scikit-learn.org/stable/user_guide.html"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SKSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        for i in range(1,8):
            _block = response.xpath("//li[@class='toctree-l1']["+str(i)+"]")
            _mainSection = response.xpath("//li[@class='toctree-l1']["+str(i)+"]/ul/li/a")                                       
            for k in range(len(_mainSection)):   
                sect = _mainSection[k]
                link= "https://scikit-learn.org/stable/"+ sect.xpath('@href').getall()[0]
                print('------------>'+link)
                yield scrapy.Request(link, callback=self.parse_ind_pages)



    def parse_ind_pages(self,response):
        global _descriptions,_title,_url_word,_url_attachment,_codeBlock
        _titles = question = response.xpath('//h2')
        for j in range(1,len(_titles)+1):
                _textP = response.xpath("//div[@class='section']/div[@class='section']["+str(j)+"]/p/text()")
                title = _titles[j-1].extract()
                _code = response.xpath("//div[@class='section']/div[@class='section']["+str(j)+"]//pre")
                _img = response.xpath("//div[@class='section']/div[@class='section']["+str(j)+"]//img")
                _text = ""
                _codeText = []
                _imgSrc = []
                for p in _textP:
                    _text += p.extract() + "\n"
                for code in _code:
                    print(code)
                    _codeText.append(code.extract())
                for img in _img:
                    _imgSrc.append(img.xpath('@src').getall()[0])
                _title.append(title)
                _descriptions.append(_text)
                _codeBlock.append(_codeText)
                _url_word.append(response.url)
                _url_attachment.append(_imgSrc)


    def spider_idle(self):
        global _descriptions,_title,_url_word,_url_attachment,_codeBlock
        json_total = {}
        for x in range(len(_title)):
            json_d = {'Title':_title[x],'Text':_descriptions[x],'Code_snippet':_codeBlock[x],'Url':_url_word[x],'Attachment_Url':_url_attachment[x]}
            json_total[x] = json_d
            json_total.update(json_d)


        with open('../../datasets/parrafos_sk.json', 'w') as outfile:
            json.dump(json_total, outfile)  
    