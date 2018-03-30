import aws_wrapper as aws
import deserializer as ds
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

    def comprehend_entities(self,text):
        """
        """
        chunks = self.chunk_text(text,4000)
        responses = [self.client.comprehend_entities(chunk) for chunk in chunks][0]
        self.entities = self.deserializer.deserialize_entities(responses)
        return self.entities

    def comprehend_key_phrases(self,text):
        """        
        sentiment_object = self.client.comprehend_sentiment(text)
        if sentiment_object['Sentiment'] == "NEGATIVE":
            print("{} has a negative sentiment\n\n\n\n".format(text))
            return 
        else:
            print("{} has a positive or neutral sentiment\n\n\n\n".format(text))
        """
        chunks = self.chunk_text(text, 4000)
        responses = [self.client.comprehend_key_phrases(chunk)['KeyPhrases'] for chunk in chunks][0]
        self.key_phrases = self.deserializer.deserialize_key_phrases(responses)
        return self.key_phrases

"""
    def comprehend_sentiment(self, transcribe_word_items):
        sentence = ""
        for word_item in transcribe_word_items:
            current_word = word_item['alternatives'][0]['content']
            if word_item['type'] == 'punctuation':
                if current_word == '.':
                    sentence = sentence.strip() + '.'
                    sentiment_obj = comprehend_client.detect_sentiment(
                        Text=sentence,
                        LanguageCode='en'
                    )
                    sentiment = sentiment_obj['Sentiment']
                    sentence = ""
                    continue
                else:
                    sentence = sentence.strip() + current_word + ' '
                    continue
            sentence += current_word + ' '
        return
"""
