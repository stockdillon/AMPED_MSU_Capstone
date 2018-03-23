import comprehender
import ItemSearch
from pprint import pprint
import itertools

class Processor(object):
    """
    """

    def __init__(self,client=None):
        self.client = client

    def extract_timestamps(self,transcribe_dicts,items):
        """
        Takes in a list of dictionaries returned from Transcribe,
        each containing information about a single word within the transcript.
        Also takes in a list of named tuples which contain: keyphrase, items returned using this keyphrase, and an empty list for the timestamps mapped to this particular keyphrase.

        Maps each keyphrase to a list of timestamps by iterating over the list of dictionaries,
        then updates each named tuple with the appropriate timestamp mappings.
        """
        timestamp_mappings = {}
        for word_dict in transcribe_dicts:
            if word_dict['type'] == "punctuation":
                continue
            pprint("word dict: {}".format(word_dict))
            timestamp_mappings.setdefault(word_dict['alternatives'][0]['content'], []).append(word_dict['start_time'])
        pprint("Timestamp mappings from Transcribe result: {}".format(timestamp_mappings))
        pprint("items before timestamp extraction: ")
        pprint(items)
        pprint("-----------------------------------")
        for item in items:
            keyword = item.keyword.strip().split()[0] #This is only pulling the FIRST word in the keywords used
            print("Looking for keyword: ", keyword)
            if keyword in timestamp_mappings:
                item.timestamps.extend(timestamp_mappings[keyword])
                    
        pprint("items after timestamp extraction: ")
        pprint(items)
        return

    def process(self,category,text):
        """takes in podcast text and pipelines it through the 
            comprehend module and the item searcher, returning
            a list of items

        Returns: list of amazon item objects
        """
        n = 4998
        chunks = [text[i:i+n] for i in range(0, len(text), n)]
        c = comprehender.Comprehender()
        """
        kp = []
        ent = []
        for chunk in chunks:
            kp += c.comprehend_key_phrases(chunk)
            ent += c.comprehend_entities(chunk)
        else:
            ent = dict.fromkeys(ent, list())
        """


        kp = list(itertools.chain.from_iterable([c.comprehend_key_phrases(chunk) for chunk in chunks]))
        ent = list(itertools.chain.from_iterable([c.comprehend_entities(chunk) for chunk in chunks]))
        ent = dict.fromkeys(ent, list())

        item_searcher = ItemSearch.ItemSearch(category,ent,kp)
        return item_searcher.search()

    

