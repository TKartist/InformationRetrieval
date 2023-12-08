import jsonlines
import scrapy


class contentSpiderCCC(scrapy.Spider):
    name = "contents_ccc"  # Your spider name. Each instance of a QuoteSpider will share the same name.
    start_urls = []
    with jsonlines.open("./JSONS/links_ccc.jsonl") as f:
        for line in f.iter():
            start_urls.append(line["pageLink"])

    def parse(
        self, response
    ):  # Funcion called every crawled web page. The response parameter will contain the web site response.
        pageLink = response.url
        content = response.xpath(
            './/div[@class="p-description font-hostile-takeover"]/p'
        )  # For each quote element in the current page...
        summary = ""
        for p in content:
            summary = summary + (p.xpath(".//text()").extract_first()) + "\n"
        listings = response.xpath('.//li[@class="border-btm p-productID"]/span')
        counter = 0
        for span in listings:
            if counter == 1:
                listId = span.xpath(".//text()").get()
            counter += 1
        prices = response.xpath('.//li[@class="border-btm p-price"]/span')
        counter = 0
        for span in prices:
            if counter == 1:
                price = span.xpath(".//text()").get()
            counter += 1
        years = response.xpath('.//li[@class="border-btm dt-start"]/span')
        counter = 0
        for span in years:
            if counter == 1:
                year = span.xpath(".//text()").get()
            counter += 1
        makes = response.xpath('.//li[@class="border-btm p-manufacturer"]/span')
        counter = 0
        for span in makes:
            if counter == 1:
                make = span.xpath(".//text()").get()
            counter += 1
        models = response.xpath('.//li[@class="border-btm p-model"]/span')
        counter = 0
        for span in models:
            if counter == 1:
                model = span.xpath(".//text()").get()
            counter += 1
        imageLink = response.xpath(
            './/img[@class="u-photo img-fluid"]/@src'
        ).extract_first()
        yield {
            "make": make,
            "image": imageLink,
            "model": model,
            "year": year,
            "price": price,
            "desc": summary,
            "link": pageLink,
        }
