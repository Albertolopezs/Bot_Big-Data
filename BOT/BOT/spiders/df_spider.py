import scrapy
from scrapy import signals
import json

_title=[]
_codeBlock = []
_descriptions=[]
_url_attachment=[]
_url_word=[]


class PandasSpider(scrapy.Spider):
    name = "pandas"

    start_urls = [
        "https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PandasSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def parse(self, response):
        for i in range(1,8):
            _block = response.xpath("//li[@class='toctree-l1']["+str(i)+"]")
            _mainSection = response.xpath("//li[@class='toctree-l1']["+str(i)+"]/ul/li/a")                                       
            self.parse_ind_pages(response)



    def parse_ind_pages(self,response):
        global _descriptions,_title,_url_word,_url_attachment,_codeBlock
        _titles = response.xpath("//h2")
        for i in range(1,len(_titles)):
            _path = "//div[@class='section']/div[@class='section']["+str(i)+"]"
            _codeBlocks = response.xpath("//pre[preceding::h2["+str(i)+"] and following::h2["+str(len(_titles)-i)+"]]")

            _pre = response.xpath("//pre")
            #Get the index of the first pre element
            _preIndex = 0
            for _pre_ind in range(1,len(_pre)):
                
                if(_pre[_pre_ind] == _codeBlocks[0]):
                    _preIndex = _pre_ind
                    break

            for j in range(len(_codeBlocks)):
                _textP = response.xpath(_path+"//p[preceding::pre["+str(_preIndex+j)+"] and following::pre["+str(len(_pre)-(_preIndex+j))+"]]//text()")
                _img = response.xpath(_path+"//img[preceding::pre["+str(_preIndex+j)+"] and following::pre["+str(len(_pre)-(_preIndex+j))+"]]")
                title = response.xpath(_path+"/h2/text()").extract()
                _imgSrc = []
                text = ""
                for _i in _img:
                    _imgSrc.append(_i.xpath('@src').getall()[0])
                for _textPj in _textP:
                    text += _textPj.extract()
                _codeText = _codeBlocks[j].extract()
                print(title)
                print(text)
                print(_codeText)
                print(response.url)
                _title.append(title)
                _descriptions.append(text)
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


        with open('../../datasets/parrafos_df.json', 'w') as outfile:
            json.dump(json_total, outfile)  
    