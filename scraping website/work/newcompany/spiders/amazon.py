import scrapy

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = [
        f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
        for page in range(1, 2)
    ]
    base_url = "https://www.amazon.in"

    def parse(self, response):
        products = response.css("div.s-result-list.s-search-results.sg-row div.s-asin")
        
        count = 0
        
        for product in products:
            name = product.css("span.a-size-medium.a-color-base.a-text-normal::text").get()
            price = product.css("span.a-price-whole::text").get()
            rating = product.css("span.a-icon-alt::text").get()
            reviews = product.css("span.a-size-base.s-underline-text::text").get()  
            product_link = product.xpath('h2/a/@href').get()


                     
            if name and price and rating and reviews:
                yield {
                    "Product Link" : product_link,
                    "Name": name.strip(),
                    "Price": price + "rs",
                    "Rating": rating,
                    "Reviews": reviews,  
                }
                count += 1 
