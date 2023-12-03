import scrapy

class linkSpiderERC(scrapy.Spider):

    name = "pagelinks_erc" # spider name

    start_urls = ["https://www.erclassics.com/classic-cars-for-sale/"] # start location of scraping
    def parse(self, response):
        product_list = response.xpath('.//*[@class="product-heading-wrapper"]')
        for product in product_list:
            link = product.xpath(".//a/@href").extract_first()
            yield {"pagelink" : link}
        next_page = response.xpath('.//a[@class="next i-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
