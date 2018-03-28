import aws_wrapper as aws
from collections import namedtuple

MAX_KEY_PHRASES = 5

class ItemSearch(object):

    def __init__(self,category=None,entities=None,key_phrases=None):
        self.category = category
        self.entities = entities
        self.key_phrases = key_phrases
        self.client = aws.AWSClient()
        self.keywords = []

    def naive_parse(self,count_threshold=1):
        """
        """
        keywords = []
        # ????????????????????????????????????????????????
        # I DON'T UNDERSTAND?
        # ????????????????????????????????????????????????
        # comm_products = self.entities['COMMERCIAL_ITEM']
        # for i in comm_products:
        #     keywords.append(i)
        for kp in self.key_phrases:
            if kp.count >= count_threshold:
                keywords.append(kp)
            else:
                break
        self.keywords = keywords
        print("Keywords returned: {}".format(keywords))
        return keywords
        
    def search(self):
        """
        todo: naive search
        """
        kw_item_pair = namedtuple('KeywordItemsMapping',['keyword','items','timestamps'])
        self.naive_parse()
        items = []
        for kw in self.keywords:
            try:
                res_items = self.client.search_n(kw.text,self.category,5)
                items.append(kw_item_pair(kw.text,res_items,[]))
            except:
                pass


        return items
        
