import jsonlines
import scrapy
from pathlib import Path


class contentSpiderCCS(scrapy.Spider):
    name = "contents_ccs"  # Your spider name. Each instance of a QuoteSpider will share the same name.
    start_urls = []
    with jsonlines.open("./JSONS/results.jsonl") as f:
        for line in f.iter():
            start_urls.append(line["pageLink"])

    def parse(
        self, response
    ):  # Funcion called every crawled web page. The response parameter will contain the web site response.
        target = response.xpath(
            ".//div[@class='main-content']"
        )  # For each quote element in the current page...

        # text = quote.xpath(".//span[@class='text']/text()").get()                    # Extract the quote text as a string.
        # author = quote.xpath(".//small[@class='author']/text()").get()	     # Extract the author name as a string.
        # tags = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()  # Extract the quote tags as a list of strings.
        name = target.xpath(".//h1[@class='detail-desc-make-model']/text()").get()
        url = response.url
        url_read = url.split("/")
        make = url_read[3]
        model = url_read[4]

        name_read = name.split(" ")
        year = name_read[0]
        price = name_read[len(name_read) - 1]
        desc = name + " \n "
        desc += target.xpath(".//div[@class='detail-desc']/div/p/text()").get()
        imageLinks = response.xpath(".//img/@src").extract_first()

        yield {
            "make": make,
            "image": imageLinks,
            "model": model,
            "year": year,
            "price": price,
            "desc": desc,
            "link": url,
        }
