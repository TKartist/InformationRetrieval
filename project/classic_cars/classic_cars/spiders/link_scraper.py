import scrapy


class linkSpider(scrapy.Spider):

    name = "pagelinks"    # Your spider name. Each instance of a QuoteSpider will share the same name.


    start_urls = ["https://www.classiccarsforsale.co.uk/year-1885-2017"]


    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.
        for car in response.xpath("//div[@class='listing-desc']"):    # For each quote element in the current page...

            # text = quote.xpath(".//span[@class='text']/text()").get()                    # Extract the quote text as a string.
                # author = quote.xpath(".//small[@class='author']/text()").get()	     # Extract the author name as a string.
                # tags = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()  # Extract the quote tags as a list of strings.
            link = response.urljoin(car.xpath("//div[@class='listing-desc-make-model']/a/@href").get())
            yield {"pageLink" : link}
        # print(carLinks)
        next_page = response.xpath("//a[@class='btn nxt-link']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        # next_page = response.xpath("//li[@class='next']/a/@href").get()    # Extract next page link as a string.

        # if next_page:	 # If next page is not None, that is, if we have a next page to visit...

        #     yield response.follow(next_page, callback=self.parse)    # Follow the next page link. Return the next page response object.