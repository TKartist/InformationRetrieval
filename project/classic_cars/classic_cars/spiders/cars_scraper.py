import scrapy


class CarSpider(scrapy.Spider):

    name = "classicCars"    # Your spider name. Each instance of a QuoteSpider will share the same name.


    start_urls = ["https://www.classiccarsforsale.co.uk/year-1885-2017"]


    def parse(self, response):    # Funcion called every crawled web page. The response parameter will contain the web site response.

        for car in response.xpath("//div[@class='listing-desc']"):    # For each quote element in the current page...

            # text = quote.xpath(".//span[@class='text']/text()").get()                    # Extract the quote text as a string.
            # author = quote.xpath(".//small[@class='author']/text()").get()	     # Extract the author name as a string.
            # tags = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()  # Extract the quote tags as a list of strings.
            year = car.xpath(".//div[@class='listing-desc-year']/text()").get()
            price = car.xpath(".//div[@class='listing-desc-price']/text()").get()
            milage = car.xpath(".//li[@class='listing-bullet-mileage']/text()").get()

            yield {'year': year, 'price': price, 'milage': milage}    # Return extracted data as a Python dict.

        # next_page = response.xpath("//li[@class='next']/a/@href").get()    # Extract next page link as a string.

        # if next_page:	 # If next page is not None, that is, if we have a next page to visit...

        #     yield response.follow(next_page, callback=self.parse)    # Follow the next page link. Return the next page response object.