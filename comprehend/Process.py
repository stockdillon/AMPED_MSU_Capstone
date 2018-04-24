import itertools
from pprint import pprint

import comprehender
import ItemSearch
from collections import namedtuple
from decimal import *


class DeterminantFoundContinue(Exception): pass

class Processor(object):
    """
    """

    def __init__(self,client=None):
        self.client = client
        self.comprehender = comprehender.Comprehender()

    #def extract_timestamps(self,transcribe_dicts,items,offset_in_transcript=0):
    def extract_timestamps(self):
        """
        Takes in a list of dictionaries returned from Transcribe,
        each containing meta data about a single word within the transcript.
        Also takes in a list of named tuples which contain: keyphrase, items returned using this keyphrase, and an empty list for the timestamps mapped to this particular keyphrase.

        Maps each keyphrase to a list of timestamps by iterating over the list of dictionaries,
        then updates each named tuple with the appropriate timestamp mappings.
        """
        timestamp_mappings = {}
        for i, word_dict in enumerate(self.transcribe_dicts):
            if word_dict['type'] == "punctuation":
                continue
            word = word_dict['alternatives'][0]['content']
            timestamp_mappings.setdefault(word, {'timestamps':[],'indices':[]})
            timestamp_mappings[word]['timestamps'].append(word_dict['start_time'])
            timestamp_mappings[word]['indices'].append(int(i))
        pprint("Timestamp mappings from Transcribe result: ")
        #for w,t in timestamp_mappings.items():
            #print(w,t)
        for item in self.keyphrase_tuples:
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

    def process(self,category,transcript_text, transcribe_dicts):
        """takes in podcast text and pipelines it through the 
            comprehend module and the item searcher, returning
            a list of items

        Returns: list of amazon item objects
        """

        self.transcribe_dicts = transcribe_dicts
        self.transcript_text = transcript_text

        self.get_cost_of_job()
 
        keyphrase_objects, entity_objects = self.comprehender.get_keyphrases_and_entities(transcript_text)
        item_searcher = ItemSearch.ItemSearch(category,entity_objects,keyphrase_objects)

        self.keyphrase_tuples = item_searcher.search()
        self.extract_timestamps()

        for kpt in self.keyphrase_tuples:
            self.get_sentiment_window(kpt,transcript_text,30)
        
        #return [kpt for kpt in self.keyphrase_tuples]
        return [kpt for kpt in self.keyphrase_tuples if kpt.sentiment['POSITIVES'] >= kpt.sentiment['NEGATIVES']]

    def get_sentiment_window(self,kw_item_pair, text, length):
        """
        Takes the indices of a search term in the text and creates a window of length inside the text.
        Computes sentiment analysis on the given slice of text within the text.

        Args:
        index: the index in the text
        text: the text body to index where to get sentiment from
        length: the length of the window to get sentiment
        """
        half_window = int(length/2)
        sentiments = []
        for indices in kw_item_pair.offsets:
            #the returned indices in the text where the items term was found
            left_pos = indices[0]
            right_pos = indices[1]
            left = left_pos - half_window
            right = right_pos + half_window
            if (left < 0):
                print("CASE 1 TRIGGERED")
                #the window goes past the beginning of the text
                left = 0
                right = right_pos + 2*half_window - left_pos
                if right > len(text)-1:
                    right = len(text)-1
            elif (right > len(text)-1):
                print("CASE 2 TRIGGERED")
                #the right side of window goes past the text
                right = len(text)-1
                left = left_pos - 2*half_window - right_pos
                if left < 0:
                    left = 0
            #print("Keyword: {}  offsets: {}".format(kw_item_pair.keyword, kw_item_pair.offsets))
            #print("Length of text: {}".format(len(text)))
            #print("Indices: {}".format(indices))
            #print("Left: {}   Right: {}   Half Window Size: {}".format(left,right,half_window))
            if right - left < 5000:
                sentiments.append(self.comprehender.comprehend_sentiment(text[left:right]))
        mixed = sentiments.count('MIXED')
        negatives = sentiments.count('NEGATIVE')
        positives = sentiments.count('POSITIVE')
        neutrals = sentiments.count('NEUTRAL')

        kw_item_pair.sentiment = {'NEGATIVES' : negatives, 'POSITIVES' : positives, 'NEUTRALS' : neutrals, 'MIXED' : mixed}
        
        #print(sentiments)
        #print('negatives: ',negatives)
        #print('positives: ',positives)
        #print('neutrals: ',neutrals)
                
    def test_window(self):
        kw_item_pair = namedtuple('KeywordItemsMapping', ['keyword', 'items', 'timestamps', 'sentiment', 'count', 'offsets'])
        test = kw_item_pair(1,1,1,1,1,[(11,22),(55,68)])
        text = "I love the apple iphone. It is my favorite. I hate the Samsung Galaxy. It is my least favorite"
        self.get_sentiment_window(test,text,20)

            

    def get_cost_of_job(self):
        for word_dict in self.transcribe_dicts[::-1]:
            if 'start_time' in word_dict:
                print(word_dict['start_time'])
                self.transcribe_seconds = float(word_dict['start_time'])
                break
        getcontext().prec = 3
        self.transcribe_cost = self.transcribe_seconds * .0004
        self.comprehend_cost = Decimal(Decimal(len(self.transcript_text)) / Decimal(100.0) * Decimal(.0001))
        #cost = transcribe_cost + comprehend_cost
        #print("Transcribe Cost: {}".format(self.transcribe_cost))
        #print("Comprehend Cost: {}".format(self.comprehend_cost))
        #return transcribe_cost, comprehend_cost
