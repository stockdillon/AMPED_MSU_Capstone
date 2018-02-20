import enum
import json
import collections

class ComprehendResponse(object):

    def __init__(self,name='Comprehend Response'):
        self.name = name

    def __repr__(self):
        return self.name

class ComprehendSentiment(ComprehendResponse):

    def __init__(self):
        pass

class ComprehendTextResponse(ComprehendResponse):

    def __init__(self,text,score,name='Comprehend Text Response'):
        super().__init__(name)
        self.text = text
        
class ComprehendKeyPhrase(ComprehendTextResponse):

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
    
    def __init__(self,text,score,begin_offset,end_offset,_type):
        super(ComprehendEntity,self).__init__(text,'Comprehend Entity')
        self.begin_offset = begin_offset
        self.end_offset = end_offset
        self.type = _type
        self.score = score

    def __repr__(self):
        return ('Comprehend Entity: Type:  {}  Text: {}  Score:  {}   BeginOffset:  {}  EndOffset:  {}'.format(
            self.type,self.text,self.score,self.begin_offset,self.end_offset))
        
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


ENTITY_TYPES = ['COMMERCIAL_ITEM',
    'DATE',
    'EVENT',
    'LOCATION',
    'ORGANIZATION',
    'OTHER',
    'PERSON',
    'QUANTITY',
    'TITLE']


class Deserializer(object):
    """
    Deserializes the data provided by Amazon's comprehend engine
    into a dictionary of entities, where key = type.
    Data is parsed as Json where key 'Entities' is a list of dictionaries.
    """
    
    def __init__(self,):
        pass

    def deserialize_entities(self,data):
        """
        deserializes the input data into the format {'entity_type' : [entities]}
        """
        entities = data['Entities']
        deserialized_entities = {key:[] for key in ENTITY_TYPES}
        for entity in entities:
            comp = entity_hook_handler(entity)
            deserialized_entities[comp.type].append(comp)
        for k,v in deserialized_entities.items():
            v = v.sort(key=lambda x: x.score, reverse=True)
        return deserialized_entities

    def deserialize_key_phrases(self,data):
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
            
        

        
        
        

        
        
        

    

    
        

    
    
