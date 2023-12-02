import jsonlines
import scrapy
from pathlib import Path



class contentSpider(scrapy.Spider):

    name = "contents"    # Your spider name. Each instance of a QuoteSpider will share the same name.
    start_urls = []
    print(Path.cwd())
    with jsonlines.open('./results.jsonl') as f:

        for line in f.iter():

            start_urls.append(line["pageLink"])
    
    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.
        target = response.xpath(".//div[@class='main-content']")    # For each quote element in the current page...

            # text = quote.xpath(".//span[@class='text']/text()").get()                    # Extract the quote text as a string.
                # author = quote.xpath(".//small[@class='author']/text()").get()	     # Extract the author name as a string.
                # tags = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()  # Extract the quote tags as a list of strings.
        name = target.xpath(".//h1[@class='detail-desc-make-model']/text()").get()
        transmission = target.xpath(".//li[@class='listing-bullet-transmission']/text()").get()
        mileage = target.xpath(".//li[@class='detail-bullet-mileage']/text()").get()
        drive = target.xpath(".//li[@class='listing-bullet-drive']/text()").get()
        desc = target.xpath(".//div[@class='detail-desc']/div/p/text()").get()

        yield {"name" : name, "transmission" : transmission, "mileage" : mileage, "driver-position": drive, "desc":desc}





