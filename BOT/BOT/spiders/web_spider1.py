import scrapy
import json


class BDSpider(scrapy.Spider):
    name = "glossary-bd"

    start_urls = [
        "https://bigdata-madesimple.com/big-data-a-to-zz-a-glossary-of-big-data-terminology/"
    ]

    def parse(self, response):
        json_total ={ }
        words, descriptions, url_word, url_attachment = self.get_text(response)
        for x in range(len(words)):
            json_d = {'Word':words[x],'Description':descriptions[x],'Url':url_word[x],'Attachment_Url':url_attachment[x]}
            json_total[x] = json_d
            json_total.update(json_d)


        page = response.url.split("/")[-2]
        filename = '../../datasets/%s.json' % page
        with open(filename, 'wb') as f:
            json.dump(json_total, f)
        self.log('Saved file %s' % filename)

    def get_text(self,response):
        descriptions = []
        words= []
        url_word = []
        url_attachment = []

        word = response.xpath('(//div[contains(@class,"entry-content")]//h3//strong)').extract()
        description = response.xpath('//div[contains(@class,"entry-content")]/p').extract()

        for i in range(len(word)-1):
            if(i >=11):
                words.append(word[i+1])  
            else:
                words.append(word[i])   
            print('Word:',words[-1])
            descriptions.append(description[i+1])  
            url_word.append(response.request.url)
            url_attachment.append([])

        

        return words, descriptions, url_word, url_attachment