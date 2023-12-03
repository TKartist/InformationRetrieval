import scrapy


class linkSpiderCCC(scrapy.Spider):

    name = "pagelinks_ccc"    # Your spider name. Each instance of a QuoteSpider will share the same name.


    start_urls = ["https://classiccars.com/listings/find?ps=60"]


    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.
        cars = response.xpath('.//*[@class="search-result-item w100 featured"]')
        for car in cars:
            link = response.urljoin(car.xpath('.//a[@class="d-block w100 dark-link"]/@href').extract_first())
            yield {"pageLink" : link}
            
        # print(carLinks)
        next_page = response.xpath("//a[@title='Go to page ►']/@href").get()
        print(next_page)
        if next_page:
            newPage = response.urljoin(next_page)
            print(newPage)
            yield response.follow(newPage, callback=self.parse)

        # next_page = response.xpath("//li[@class='next']/a/@href").get()    # Extract next page link as a string.

        # if next_page:	 # If next page is not None, that is, if we have a next page to visit...

        #     yield response.follow(next_page, callback=self.parse)    # Follow the next page link. Return the next page response object.