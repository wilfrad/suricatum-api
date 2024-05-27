from enum import Enum

class Response:
    def __init__(self, selections, response_behavior=None):
        self.selections = selections
        self.response_behavior = response_behavior

class SubQuestion:
    def __init__(self, statement, selections, response_behavior=None):
        self.statement = statement
        self.selections = selections
        self.response_behavior = response_behavior

class Question:
    def __init__(self, id, statement, responses, question_behavior):
        self.id = id
        self.statement = statement
        if question_behavior == Survey.Behavior.MULTI.value or question_behavior == Survey.Behavior.INPUT.value:
            self.sub_questions = [ SubQuestion(**sub) for sub in responses ]
        else:
            self.responses = [ Response(**res) for res in responses ]
        self.question_behavior = question_behavior

class Survey:
    class Type(Enum):
        AUTO_COACHING = 'auto_coaching'
        TEST_OUTPLACEMENT = 'test_outplacement'
        META_SEARCH = 'meta_search'
        AI_POST_GENERATOR = 'ai_post_generator'
    
    class Behavior(Enum):
        SINGLE = 'single'
        MULTI = 'multi'
        LIST = 'list'
        INPUT = 'input'
    
    def __init__(self, questions):
        self.questions = [ Question(**quest) for quest in questions ]
    
    def get_survey_title(self, survey_name):
        
        if survey_name == self.Type.AUTO_COACHING.value :
            return 'Test de Auto-Coaching'
        
        if survey_name == self.Type.TEST_OUTPLACEMENT.value :
            return 'Test de Outplacement'
        
        if survey_name == self.Type.META_SEARCH.value :
            return 'Meta Buscador de ofertas'
        
        if survey_name == self.Type.AI_POST_GENERATOR.value :
            return 'Creador de posts'
        
        return '...'

    def get_total_questions(self):
        return sum(
            len(quest.sub_questions) 

            if quest.question_behavior == Survey.Behavior.MULTI.value or quest.question_behavior == Survey.Behavior.INPUT.value 
            else 1 
            
            for quest in self.questions
        )