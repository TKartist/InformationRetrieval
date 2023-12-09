import scrapy


class contentSpiderCCS(scrapy.Spider):
    name = "contents_ccs"  # Your spider name. Each instance of a QuoteSpider will share the same name.

    start_urls = ["https://www.classiccarsforsale.co.uk/year-1885-2017"]

    def parse(
        self, response
    ):  # Funcion called every crawled web page. The response parameter will contain the web site response.
        cars = response.xpath('.//*[@class="listing"]')
        for car in cars:
            year = car.xpath(
                './/div[@class="listing-desc"]/div[@class="listing-desc-year"]/text()'
            ).get()
            price = car.xpath(
                './/div[@class="listing-desc"]/div[@class="listing-desc-price"]/text()'
            ).get()
            image = car.xpath('.//div[@class="listing-img"]/a/img/@src').get()
            pageLink = response.urljoin(
                car.xpath('.//div[@class="listing-img"]/a/@href').extract_first()
            )
            link = car.xpath(
                './/div[@class="listing-desc"]/div[@class="listing-desc-make-model"]/a/@href'
            ).extract_first()
            link_vals = link.split("/")
            make = link_vals[1]
            model = link_vals[2]
            yield {
                "make": make,
                "image": image,
                "model": model,
                "year": year,
                "price": price,
                "desc": "",
                "link": pageLink,
            }
        # print(carLinks)
        next_page = response.xpath("//a[@class='btn nxt-link']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
