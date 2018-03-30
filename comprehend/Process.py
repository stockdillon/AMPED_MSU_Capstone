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
        each containing meta data about a single word within the transcript.
        Also takes in a list of named tuples which contain: keyphrase, items returned using this keyphrase, and an empty list for the timestamps mapped to this particular keyphrase.

        Maps each keyphrase to a list of timestamps by iterating over the list of dictionaries,
        then updates each named tuple with the appropriate timestamp mappings.
        """
        timestamp_mappings = {}
        for i, word_dict in enumerate(transcribe_dicts):
            if word_dict['type'] == "punctuation":
                continue
            word = word_dict['alternatives'][0]['content']
            #pprint("word dict: {}".format(word_dict))
            timestamp_mappings.setdefault(word, {'timestamps':[],'indicies':[]})
            timestamp_mappings[word]['timestamps'].append(word_dict['start_time'])
            timestamp_mappings[word]['indicies'].append(int(i))
        pprint("Timestamp mappings from Transcribe result: {}".format(timestamp_mappings))
        for item in items:
            key_phrase_tokens = item.keyword.strip().split() 
            #print("Looking for key_phrase_tokens: ", key_phrase_tokens)
            if key_phrase_tokens[0] in timestamp_mappings:

                for i, token in enumerate(key_phrase_tokens[:-1]):
                    for index in timestamp_mappings[token]['indicies']:
                        #print("Current word: {}   Next word: {}".format(key_phrase_tokens[i], key_phrase_tokens[i+1]))
                        #print("Next word indicies: {}".format(timestamp_mappings[key_phrase_tokens[i+1]]['indicies']))
                        if key_phrase_tokens[i+1] in timestamp_mappings and index + 1 not in timestamp_mappings[key_phrase_tokens[i+1]]['indicies']:
                            continue

                item.timestamps.extend(timestamp_mappings[key_phrase_tokens[0]]['timestamps'])
                    
        #pprint("items after timestamp extraction: ")
        #pprint(items)
        return

    def process(self,category,text):
        """takes in podcast text and pipelines it through the 
            comprehend module and the item searcher, returning
            a list of items

        Returns: list of amazon item objects
        """
        n = 4000
        chunks = [text[i:i+n] for i in range(0, len(text), n)]
        #chunks = text.split('.')
        c = comprehender.Comprehender()

        kp = list(itertools.chain.from_iterable([c.comprehend_key_phrases(chunk) for chunk in chunks]))
        ent = list(itertools.chain.from_iterable([c.comprehend_entities(chunk) for chunk in chunks]))
        print("Entities: {}".format(ent))
        ent = dict.fromkeys(ent, list())

        item_searcher = ItemSearch.ItemSearch(category,ent,kp)
        return item_searcher.search()

    

