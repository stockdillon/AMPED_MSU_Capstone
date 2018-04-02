import itertools
from pprint import pprint

import comprehender
import ItemSearch


class DeterminantFoundContinue(Exception):
    pass

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
            timestamp_mappings.setdefault(word, {'timestamps':[],'indices':[]})
            timestamp_mappings[word]['timestamps'].append(word_dict['start_time'])
            timestamp_mappings[word]['indices'].append(int(i))
        pprint("Timestamp mappings from Transcribe result: ")
        #for w,t in timestamp_mappings.items():
            #print(w,t)
        for item in items:
            key_phrase_tokens = item.keyword.strip().split() 
            if key_phrase_tokens[0] in timestamp_mappings:
                
                first_word_data = timestamp_mappings[key_phrase_tokens[0]]
                for i, first_word_index in enumerate(first_word_data['indices']):
                    phrase_timestamp = first_word_data['timestamps'][i]
                    for offset_in_phrase,token in enumerate(key_phrase_tokens[1:-1]):
                        if first_word_index + offset_in_phrase + 1 not in timestamp_mappings[token]['indices']:
                            #print("{} not found in {}".format(first_word_index+offset_in_phrase, timestamp_mappings[token]['indices']))
                            break

                    else:
                        item.timestamps.append(float(phrase_timestamp))
        return True

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
