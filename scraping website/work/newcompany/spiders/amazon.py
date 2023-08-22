import scrapy
from bs4 import BeautifulSoup

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = [
        f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
        for page in range(1, 21)  
    ]
    base_url = "https://www.amazon.in"

    def parse(self, response):
        products = response.css("div.s-result-list.s-search-results.sg-row div.s-asin")
        
        for product in products:
            link = self.base_url + product.css("h2 a.a-link-normal::attr(href)").get()
            name = product.css("span.a-size-medium.a-color-base.a-text-normal::text").get()
            price = product.css("span.a-price-whole::text").get()
            rating = product.css("span.a-icon-alt::text").get()
            reviews = product.css("span.a-size-base.s-underline-text::text").get()  
            
            if name and price and rating and reviews:
                yield {
                    "Product_link": link,
                    "Name": name.strip(),
                    "Price": price + " rs",
                    "Rating": rating,
                    "Reviews": reviews,
                }
                
                # After processing each product, follow the product link for Part 2 data
                # yield scrapy.Request(link, callback=self.parse_product_details)

    # def parse_product_details(self, response):
    #     description = response.css("#productDescription p::text").get()
    #     asin = response.css("th:contains('ASIN') + td::text").get()
    #     product_description = response.css("div#productDescription p::text").get()
    #     manufacturer = response.css("th:contains('Manufacturer') + td span::text").get()

    #     yield {
    #         "Description": description,
    #         "ASIN": asin,
    #         "Product_Description": product_description,
    #         "Manufacturer": manufacturer
    #     }
