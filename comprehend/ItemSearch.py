import aws_wrapper as aws
from collections import namedtuple
class ItemSearch(object):

    def __init__(self,category=None,entities=None,key_phrases=None):
        self.category = category
        self.entities = entities
        self.key_phrases = key_phrases
        self.client = aws.AWSClient()
        self.keywords = []
        self.ignore = ['the','each','or','a','its','last',]

    def join_entities(self):
        """Union the words from entities
        """
        ent_text = []
        for e in self.entities['COMMERCIAL_ITEM']:
            for i in e.text.split():
                ent_text.append(i)
        kp_text = []
        for k in self.key_phrases:
            for i in k.text.split():
                kp_text.append(i)
        for key_phrase in self.key_phrases:
            count = 0
            for word in key_phrase.text.split():
                if word not in self.ignore:
                    count += ent_text.count(word) + kp_text.count(word)
            key_phrase.count += count
        self.key_phrases.sort(key=lambda x: x.count, reverse=True)
        self.key_phrases = self.key_phrases[:5]

    def naive_parse(self,count_threshold=1):
        """
        """
        keywords = []
        for ent in self.entities['COMMERCIAL_ITEM']:
            keywords.append(ent)
        for kp in self.key_phrases:
            found = False
            for key_word in keywords:
                if kp.text == key_word.text:
                    found = True
            if kp.count >= count_threshold:
                if not found:
                    keywords.append(kp)
            else:
                break
        self.keywords = keywords
        return keywords
        
    def search(self):
        """
        todo: naive search
        """
        kw_item_pair = namedtuple('KeywordItemsMapping',['keyword','items','timestamps'])
        self.join_entities()
        self.naive_parse()
        items = []
        for kw in self.keywords:
            print(kw)
            try:
                res_items = self.client.search_n(kw.text,self.category,1)
                items.append(kw_item_pair(kw.text,res_items,[]))
            except:
                pass


        return items
        
