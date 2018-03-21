import comprehender
import ItemSearch
from pprint import pprint

class Processor(object):
    """
    """

    def __init__(self,client=None):
        self.client = client

    def extract_timestamps(self,key_phrase_object_dict,transcribe_items):
        """
        Takes in the searched items and returns the timestamps associated with each item
        """
        pprint("key_phrase_object_dict before timestamp extraction: ")
        pprint(key_phrase_object_dict)
        pprint("-----------------------------------")
        for entity_type in key_phrase_object_dict:
            #entities = key_phrase_object_dict[entity_type]
            for obj in key_phrase_object_dict[entity_type]:
                keyword = obj.text
                print("Looking for keyword: ", keyword)
                for item in transcribe_items:
                    word_from_transcribe_text = item['alternatives'][0]['content']
                    #print("Comparing against: ", word_from_transcribe_text)                  
                    if word_from_transcribe_text == keyword:
                        timestamp = item['start_time']
                        print("Found timestamp (" + timestamp + ") for keyword: " + keyword)
                        obj.timestamps.append(timestamp)
        pprint("key_phrase_object_dict after timestamp extraction: ")
        pprint(key_phrase_object_dict)
        

    def process(self,category,text,transcribe_JSON):
        """takes in podcast text and pipelines it through the 
            comprehend module and the item searcher, returning
            a list of items

        Returns: list of amazon item objects
        """
        textChunk = text[:5000]
        c = comprehender.Comprehender()
        kp = c.comprehend_key_phrases(textChunk)
        ent = c.comprehend_entities(textChunk)
        self.extract_timestamps(ent, transcribe_JSON['results']['items'])
        item_searcher = ItemSearch.ItemSearch(category,ent,kp)
        return item_searcher.search()

    

