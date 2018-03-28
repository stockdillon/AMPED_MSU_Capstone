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

    def comprehend_entities(self,text):
        """
        """
        response = self.client.comprehend_entities(text)
        self.entities = self.deserializer.deserialize_entities(response)
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
        response = self.client.comprehend_key_phrases(text)
        self.key_phrases = self.deserializer.deserialize_key_phrases(response['KeyPhrases'])
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