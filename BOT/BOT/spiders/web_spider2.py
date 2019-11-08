import scrapy
import json


class MLSpider(scrapy.Spider):
    name = "glossary-ml"

    start_urls = [
        'https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/'
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

        tables =response.xpath('//div[contains(@class,"su-table")]').extract()
        word = response.xpath('(//div[contains(@class,"entry-content")]//h3//strong)/td//text()').extract()
        print(word)
        description = response.xpath('//div[contains(@class,"entry-content")]/p').extract()

        for i in range(1,len(tables)):
            sub_tables = response.xpath('//div[contains(@class,"su-table")]['+str(i)+']/table').extract()
            print('Sub-Tablas: ', len(sub_tables))
            for j in range(1,len(sub_tables)+1):
                list_words = response.xpath('//div[contains(@class,"su-table")]['+str(i)+']/table['+str(j)+']/tbody/tr').extract()
                print('Lista palabras: ', len(list_words))
                for k in range(2,len(list_words)+1):
                    """Word"""
                    row =  response.xpath('//div[contains(@class,"su-table")]['+str(i)+']/table['+str(j)+']/tbody/tr['+str(k)+']/td//text()').extract()

                    word = row[0]
                    words.append(word)
                    description = row[1]
                    descriptions.append(description)               
                    print('Word:',word)
                    
                    """Attachments_url"""
                    
                    attachments = response.xpath('//div[contains(@class,"su-table")]['+str(i)+']/table['+str(j)+']/tbody/tr['+str(k)+']/td//img').xpath('@src').getall()
                    attachments_url = []
                    for attach in attachments:
                        print(attach)
                        attachments_url.append(attach) 
                    
                    url_attachment.append(attachments_url)
                    url_word.append(response.request.url)

        

        return words, descriptions, url_word, url_attachment

