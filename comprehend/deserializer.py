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
    """

    def __init__(self,text,score,name='Comprehend Text Response'):
        super().__init__(name)
        self.text = text
        self.timestamps = []

        
class ComprehendKeyPhrase(ComprehendTextResponse):
    """Comprehend Key Phrase Entity

    Attributes:
    count: The number of times the key phrase text is in the document
    offsets: List of offsets for the location of the word in the document
    scores: List of scores between 0-1 corresponding to offsets of the likelihood that the text was a key phrase.
    """

    def __init__(self,text,score,begin_offset,end_offset):
        super(ComprehendKeyPhrase,self).__init__(text,'Comprehend Key Phrase')
        self.count = 1
        self.offsets = []
        self.scores = []
        self.add_offset(begin_offset,end_offset)
        self.add_score(score)

    def inc(self):
        self.count += 1

    def add_offset(self,begin,end):
        self.offsets.append((begin,end))

    def add_score(self, score):
        self.scores.append(score)

    def __repr__(self):
        return ('Comprehend Key Phrase: Text: {}  Score:  {}  Count: {}  Offsets:  {}'.format(
            self.text,self.scores,self.count,self.offsets))
    
class ComprehendEntity(ComprehendTextResponse):
    """

    Attributes:
    begin_offset: Beginning of offset in document
    end_offset: Ending offset in document
    type: The type of the Entity, enumerated by EntityType class
    score: The score of the entity between 0-1 of the likelihood of relevance
    timestamps: The timestamps associated withe this Entity
    """
    
    def __init__(self,text,score,begin_offset,end_offset,_type):
        super(ComprehendEntity,self).__init__(text,'Comprehend Entity')
        self.begin_offset = begin_offset
        self.end_offset = end_offset
        self.type = _type
        self.score = score

    def __repr__(self):
        return ('Comprehend Entity: Type:  {}  Text: {}  Score:  {}   BeginOffset:  {}  EndOffset:  {} Timestamps:  {}'.format(
            self.type,self.text,self.score,self.begin_offset,self.end_offset,self.timestamps))
        
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
    into a dictionary of entities, where key = type.
    Data is parsed as Json where key 'Entities' is a list of dictionaries.
    """

    ENTITY_TYPES = ['COMMERCIAL_ITEM', 'DATE', 'EVENT', 'LOCATION','ORGANIZATION','OTHER','PERSON','QUANTITY','TITLE']

    def __init__(self,): pass

    def deserialize_entities(self,data):
        """deserializes the input data into the format {'entity_type' : [entities]}
        """
        entities = data['Entities']
        deserialized_entities = {key:[] for key in self.ENTITY_TYPES}
        for entity in entities:
            comp = entity_hook_handler(entity)
            deserialized_entities[comp.type].append(comp)
        for k, v in deserialized_entities.items():
            v = v.sort(key=lambda x: x.score, reverse=True)
        return deserialized_entities

    def deserialize_key_phrases(self,data):
        """Deserlializes key phrases and returns a list of them ordered by count desc [ComprehendResponse,]
        """
        parsed = {}
        for key_phrase in data:
            text = key_phrase['Text']
            if text in parsed:
                temp_kp = parsed[text]
                temp_kp.inc()
                temp_kp.add_score(key_phrase['Score'])
                temp_kp.add_offset(key_phrase['BeginOffset'],
                                    key_phrase['EndOffset'])
            else:
                parsed[text] = key_phrase_hook_handler(key_phrase)
        parsed = [v for v in parsed.values()]
        parsed.sort(key=lambda x: x.count, reverse=True)
        return parsed

            
        

        
        
        

        
        
        

    

    
        

    
    
