import aws_wrapper as aws
from collections import namedtuple
class ItemSearch(object):

    def __init__(self,category=None,entities=None,key_phrases=None):
        self.category = category
        self.entities = entities
        self.key_phrases = key_phrases
        self.client = aws.AWSClient()
        self.keywords = []

    def naive_parse(self,count_threshold=2):
        """
        """
        keywords = []
        comm_products = self.entities['COMMERCIAL_ITEM']
        for i in comm_products:
            keywords.append(i)
        for kp in self.key_phrases:
            if kp.count >= count_threshold:
                keywords.append(kp)
            else:
                break
        self.keywords = keywords
        return keywords
        
    def search(self):
        """
        todo: naive search
        """
        kw_item_pair = namedtuple('KeywordItemsMapping',['keyword','items'])
        self.naive_parse()
        items = []
        for kw in self.keywords:
            res_items = self.client.search_n(kw.text,self.category,1)
            items.append(kw_item_pair(kw.text,res_items))

        return items
        
