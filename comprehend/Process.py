import comprehender
import ItemSearch
from pprint import pprint
import itertools


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
        #pprint("Timestamp mappings from Transcribe result: {}".format(timestamp_mappings))
        for item in items:
            key_phrase_tokens = item.keyword.strip().split() 
            if key_phrase_tokens[0] in timestamp_mappings:

                break_ = False
                for i, token in enumerate(key_phrase_tokens[:-1]):
                    for index in timestamp_mappings[token]['indices']:
                        if key_phrase_tokens[i+1] in timestamp_mappings and index + 1 not in timestamp_mappings[key_phrase_tokens[i+1]]['indices']:
                            break_ = True
                            break
                    if break_:
                        break
                if break_:
                    continue

                item.timestamps.extend(float(tstamp) for tstamp in timestamp_mappings[key_phrase_tokens[0]]['timestamps'])
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

    

