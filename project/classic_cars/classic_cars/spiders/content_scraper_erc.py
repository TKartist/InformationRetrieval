import jsonlines
import scrapy

class contentSpiderERC(scrapy.Spider):

    name = "contents_erc"    # Your spider name. Each instance of a QuoteSpider will share the same name.
    start_urls = []
    with jsonlines.open('./links_erc.jsonl') as f:

        for line in f.iter():

            start_urls.append(line["pagelink"])
    
    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.
        content = response.xpath('.//div[@class="product-description"]/div[@class="std"]/p')    # For each quote element in the current page...
        summary = ""
        for p in content:
            summary = summary + (p.xpath('.//text()').get()) + '\n'
        name = response.xpath('.//div[@class="product-name"]/h1/text()').get()
        price = response.xpath('.//span[@class="price"]/text()').get()
        yield {"name":name, "price":price, "desc" : summary}




