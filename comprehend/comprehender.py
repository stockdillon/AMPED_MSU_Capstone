import aws_wrapper as aws
import deserializer as ds
import itertools

from pprint import pprint

class Comprehender(object):
    """
    Channels a document through amazon comprehend,
    parses response data into:
    
    """
    def __init__(self,text=None,client=aws.AWSClient(),deserializer=None):
        self.text = text
        self.entities = None
        self.client = client
        self.deserializer = ds.Deserializer()

    def chunk_text(self,text,n=4000):
        """chunks text into sizes of n
        """
        return [text[i:i+n] for i in range(0, len(text), n)]


    def get_keyphrases_and_entities(self, text):
        CHUNK_SIZE = 4500
        chunks = self.chunk_text(text,CHUNK_SIZE)
        entities = []
        key_phrases = []
        chunk_offset = 0

        def add_offsets(entity_or_keyphrase_list, chunk_offset):
            """Takes in a list of entities (or key phrases) and adds the chunk offset to all of their offsets
            """
            for item in entity_or_keyphrase_list:
                item['BeginOffset'] += chunk_offset
                item['EndOffset'] += chunk_offset

        for chunk in chunks:
            entity_response = self.client.comprehend_entities(chunk)
            key_phrase_response = self.client.comprehend_key_phrases(chunk)
            add_offsets(entity_response['Entities'], chunk_offset)
            add_offsets(key_phrase_response['KeyPhrases'], chunk_offset)
            key_phrases += key_phrase_response['KeyPhrases']
            entities += entity_response['Entities']
            chunk_offset += CHUNK_SIZE
        entities = self.deserializer.deserialize_entities(entities)
        key_phrases = self.deserializer.deserialize_key_phrases(key_phrases)
        return key_phrases,entities


    def comprehend_sentiment(self, text):
        sentiment_object = self.client.comprehend_sentiment(text)
        return sentiment_object['Sentiment']

