from bs4 import BeautifulSoup
import requests
import json

class ItemWebData(object):
    def __init__(self, item):
        self.title = str(item.title)
        self.price = str(item.formatted_price)
        self.brand = str(item.brand)
        self.asin = str(item.asin)
        self.images = list(set(map(lambda _: str(_.LargeImage.URL), item.images)))
        self.url = str(item.offer_url)
        #self.description = item.description        
        self.parsed_response = item.parsed_response
        self.has_reviews = bool(item.parsed_response.CustomerReviews['HasReviews'])
        self.reviews_url = None
        self.rating = 0.0
        self.review_count = 0
        self.sales_rank = self.parsed_response.SalesRank
        self.is_adult = item.is_adult
        self.availability = item.availability_type
        
    def retrieve_web_data(self):        
        if self.has_reviews:
            self.reviews_url = self.parsed_response.CustomerReviews['IFrameURL']
            response = requests.get(self.reviews_url)
            assert response.ok, "BAD REQUEST while getting rating for product"
            soup = BeautifulSoup(response.content, 'html.parser')
            self.rating = self.get_rating(soup)
            self.review_count = self.get_review_count(soup)
            return True
        else:
            return False
    
    def get_rating(self, soup):
        print(self.reviews_url)
        ratings = [float(_.text.strip('%')) for _ in soup.find_all('div', {'class': 'histoCount'})]
        stars = 0.0
        for i, percentage in enumerate(ratings):
            stars += (5-i)*(percentage)*(0.01)
        return stars

    def get_review_count(self, soup):
        review_count = soup.find(('div', {'class': 'tiny'})).find('b')
        review_count = review_count.text if review_count else 0
        #review_count.strip()
        #review_count = review_count[:review_count.index("Reviews") - 1]
        print("Review count: {}".format(review_count))
        return 0
    
    @property
    def dict(self):
        return {
            'title': self.title,
            'price': self.price,
            'brand': self.brand,
            'asin': self.asin,
            'images': self.images,
            'url': self.url,
            #'has_reviews': self.has_reviews,
            'reviews_url': self.reviews_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'sales_rank': self.sales_rank
        }
    
    @property
    def json(self):
        return json.dumps(self.dict)
         