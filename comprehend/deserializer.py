import enum
import json
import collections

class ComprehendResponse(object):
    """Base Class for the amazon comprehend response

    Attributes:
        name: The name of the type of object
    """

    def __init__(self,name='Comprehend Response'):
        self.name = name

    def __repr__(self):
        return self.name

class ComprehendSentiment(ComprehendResponse):
    """TODO
    """

    def __init__(self):
        pass

class ComprehendTextResponse(ComprehendResponse):
    """Comprehend Text Entity Base Class

    Attributes:
        text: the text associated with the comprehend response
        count: The number of times the key phrase text is in the document
        offsets: List of offsets for the location of the word in the document
        scores: List of scores between 0-1 corresponding to offsets of the likelihood that the text was a key phrase.
    """

    def __init__(self,text,score,begin_offset,end_offset,name='Comprehend Text Response'):
        super().__init__(name)
        self.text = text
        self.count = 1
        self.offsets = []
        self.scores = []
        self.add_offset(begin_offset,end_offset)
        self.add_score(score)
        self.timestamps = []
        self.sentiment = None

    def inc(self):
        self.count += 1

    def add_offset(self,begin,end):
        self.offsets.append((begin,end))

    def add_score(self, score):
        self.scores.append(score)

        
class ComprehendKeyPhrase(ComprehendTextResponse):
    """Comprehend Key Phrase Entity


    """

    def __init__(self,text,score,begin_offset,end_offset):
        super(ComprehendKeyPhrase,self).__init__(text,score,begin_offset,end_offset,'Comprehend Key Phrase')

    def __repr__(self):
        return ('Comprehend Key Phrase: Text: {}  Score:  {}  Count: {}  Offsets:  {}  Timestamps: {}  Sentiment: {}  Count: {}'.format(
            self.text,self.scores,self.count,self.offsets,self.timestamps,self.sentiment,self.count))
    
class ComprehendEntity(ComprehendTextResponse):
    """
    """
    
    def __init__(self,text,score,begin_offset,end_offset,_type):
        super(ComprehendEntity,self).__init__(text,score,begin_offset,end_offset,'Comprehend Entity')
        self.type = _type
        
    def __repr__(self):
        return ('Comprehend Entity: Type:  {}  Text: {}  Scores:  {} Count: {} Offsets:  {} Timestamps:  {}  Sentiment: {}  Count: {}'.format(
            self.type,self.text,self.scores,self.count,self.offsets,self.timestamps,self.sentiment,self.count))

        
    class EntityType(enum.Enum):
        """
        Enumerations for parsing the amazon comprehend data
        """
        COMMERCIAL_ITEM = 'COMMERCIAL_ITEM'
        DATE = 'DATE'
        EVENT = 'EVENT'
        LOCATION = 'LOCATION'
        ORGANIZATION = 'ORGANIZATION'
        OTHER = 'OTHER'
        PERSON = 'PERSON'
        QUANTITY = 'QUANTITY'
        TITLE = 'TITLE'


def entity_hook_handler(json):
    return ComprehendEntity(text=json['Text'],
                            score=json['Score'],
                            begin_offset=json['BeginOffset'],
                            end_offset=json['EndOffset'],
                            _type=json['Type'])

def key_phrase_hook_handler(json):
    return ComprehendKeyPhrase(text=json['Text'],
                            score=json['Score'],
                            begin_offset=json['BeginOffset'],
                            end_offset=json['EndOffset'])


class Deserializer(object):
    """
    Deserializes the data provided by Amazon's comprehend engine
    """

    ENTITY_TYPES = ['COMMERCIAL_ITEM', 'DATE', 'EVENT', 'LOCATION',
                    'ORGANIZATION', 'OTHER', 'PERSON', 'QUANTITY', 'TITLE']

    def __init__(self,): pass

    def parse_dicts(self, data, hook_handler):
        """Parses json objects into a list of entities given a hook handler,

        Args:
            data: the json data to be serialized
            hook_handler: anonymous function to convert json -> entity
        """
        parsed = {}
        for key_phrase in data:
            text = key_phrase['Text']
            if text in parsed:
                temp_kp = parsed[text]
                temp_kp.inc()
                temp_kp.add_score(key_phrase['Score'])
                print(text, key_phrase['BeginOffset'], key_phrase['EndOffset'], "@@@@@@@@@@@@@@@@@")
                temp_kp.add_offset(key_phrase['BeginOffset'],
                                   key_phrase['EndOffset'])
            else:
                parsed[text] = hook_handler(key_phrase)

        parsed = [v for v in parsed.values()]

        return parsed

    def deserialize_entities(self, entities):
        """deserializes the input data into the format {'entity_type' : [entities]}

        Args:
            data: data comes in the form of an Amazon Comprehend JSON response
                {
                    "Entities": [
                        {
                            "Text": "Bob",
                            "Score": 1.0,
                            "Type": "PERSON",
                            "BeginOffset": 0,
                            "EndOffset": 3
                        },
                    ],
                }
            
        Returns:
        
        """
        entities_type_sorted = {key: [] for key in self.ENTITY_TYPES}
        for e in entities:
            entities_type_sorted[e['Type']].append(e)

        for k, v in entities_type_sorted.items():
            entities_type_sorted[k] = self.parse_dicts(v, entity_hook_handler)

        return entities_type_sorted

    def deserialize_key_phrases(self, key_phrases):
        """Deserlializes key phrase entities and returns a list of them ordered by count desc [ComprehendResponse,]
        """
        parsed = self.parse_dicts(key_phrases, key_phrase_hook_handler)
        parsed.sort(key=lambda x: x.count, reverse=True)
        return parsed

            
        

        
        
        

        
        
        

    

    
        

    
    
