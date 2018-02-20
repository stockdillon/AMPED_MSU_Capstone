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
        textChunk = text[:5000]
        c = comprehender.Comprehender()
        kp = c.comprehend_key_phrases(textChunk)
        ent = c.comprehend_entities(textChunk)
        item_searcher = ItemSearch.ItemSearch(category,ent,kp)
        return item_searcher.search()

