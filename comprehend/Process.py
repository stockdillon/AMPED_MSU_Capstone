import comprehender
import ItemSearch
import deserializer as ds

class Processor(object):
    """
    """

    def __init__(self):
        pass

    def process(self,category,text):
        """takes in podcast text and pipelines it through the 
            comprehend module and the item searcher, returning
            a list of items

        Returns: list of amazon item objects
        """
        c = comprehender.Comprehender()
        kp = c.comprehend_key_phrases(text)
        ent = c.comprehend_entities(text)
        item_searcher = ItemSearch.ItemSearch(category,ent,kp)
        return item_searcher.search()

