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
        response = self.client.comprehend_key_phrases(text)
        self.key_phrases = self.deserializer.deserialize_key_phrases(response['KeyPhrases'])
        return self.key_phrases


    def comprehend_sentiment(self):
        pass
