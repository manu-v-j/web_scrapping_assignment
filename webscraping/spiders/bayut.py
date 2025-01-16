import scrapy

class ProjectSpider(scrapy.Spider):
    name = "bayut"
    allowed_domains = ["www.bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def parse(self, response):
        # Selecting all product listings
        products = response.css('li.a37d52f0')

        for item in products:
            # Extracting link from each product
            link = item.css("a.d40f2294::attr(href)").get()
            if link:
                yield response.follow(
                    link,
                    callback=self.parse_property,
                    meta={"link": response.urljoin(link)},  # Pass link to the next function
                )

        # Pagination Logic (Move to Next Page)
        # next_page = response.css('[title="Next"]::attr(href)').get()
        # if next_page:
        #     next_page_url = response.urljoin(next_page)
        #     yield response.follow(next_page_url, callback=self.parse)

    def parse_property(self, response):
        amount= response.css("span._2d107f6e::text").get()
        property_id = response.css("span._2fdf7fc5[aria-label='Reference']::text").get()
        purpose= response.css("span._2fdf7fc5[aria-label='Purpose']::text").get()
        Type= response.css("span._2fdf7fc5[aria-label='Type']::text").get()
        added_on= response.css("span._2fdf7fc5[aria-label='Reactivated date']::text").get()
        furnishing= response.css("span._2fdf7fc5[aria-label='Furnishing']::text").get()
        currency=response.css("span.d241f2ab::text").get()
        location=response.css("div.e4fd45f0::text").get()
        bedrooms=response.css("span._783ab618[aria-label='Beds'] span._140e6903::text").get()[0]
        bathrooms=response.css("span._783ab618[aria-label='Baths'] span._140e6903::text").get()[0]
        size=response.css("span._783ab618[aria-label='Area'] span._140e6903 span::text").get()
        agent_name=response.css("[aria-label='Agent name'] h2::text").get()
        breadcrumbs=response.css("span._43ad44d9::text").getall()
        amenities=response.css("span._7181e5ac::text").getall()
        description=response.css("span._3547dac9::text").getall()
        description = " ".join(description).strip()
        property_image_url=response.css("div._948d9e0a _5ae2bf48 _95d4067f::attr(href)").getall()

        yield {
            "property_id": property_id, 
            "purpose": purpose,
            "Type": Type,   
            "added_on": added_on,
            "furnishing": furnishing,
            "price": {
                "currency": currency,
                "amount": amount},
            "location": location,
            "bed_bath_size":{
                "bedrooms":int(bedrooms),
                "bathrooms":int(bathrooms),
                "size":size
            },
            "agent_name":agent_name,
            "primary_image_url":response.meta["link"],
            "breadcrumbs":breadcrumbs,
            "amenities":amenities,
            "description":description,
            "property_image_url":property_image_url
            
        }
