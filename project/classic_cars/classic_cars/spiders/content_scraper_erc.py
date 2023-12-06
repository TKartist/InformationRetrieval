import jsonlines
import scrapy

class contentSpiderERC(scrapy.Spider):

    name = "contents_erc"    # Your spider name. Each instance of a QuoteSpider will share the same name.
    start_urls = []
    with jsonlines.open('./links_erc.jsonl') as f:

        for line in f.iter():

            start_urls.append(line["pagelink"])
    
    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.
        pageLink = response.url
        content = response.xpath('.//div[@class="product-description"]/div[@class="std"]/p')    # For each quote element in the current page...
        summary = response.xpath('.//div[@class="product-name"]/h1/text()').get() + " \n"
        for p in content:
            summary = summary + (p.xpath('.//text()').get()) + '\n'
        price = response.xpath('.//span[@class="price"]/text()').get()

        product_detail = response.xpath('.//div[@class="product-attributes"]/ul/li')
        counter = 0
        for det in product_detail:
            val = det.xpath('.//span[@class="data"]/text()').get()
            if counter == 0:
                referenceNumber = val
            elif counter == 1:
                make = val
            elif counter == 2:
                model = val
            elif counter == 3:
                year = val
            counter += 1
            
        imageLink = response.xpath('.//img[@class="product-img-top"]/@src').extract_first()

        yield {"make":make, "image":imageLink,  "model": model, "year": year, "price":price, "desc" : summary, "link": pageLink}




