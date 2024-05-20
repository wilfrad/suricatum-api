from surveys.survey import Survey
from surveys.validation import Checker, AutoCoachingChecker, TestOutplacementChecker, MetaSearchChecker, AiPostGeneratorChecker
from json import loads

META_SEARCH_SURVEY = None
AUTO_COACHING_SURVEY = None
TEST_OUTPLACEMENT_SURVEY = None
AI_POST_GENERATOR = None

META_SEARCH_VALIDATION = None
AUTO_COACHING_VALIDATION = None
TEST_OUTPLACEMENT_VALIDATION = None
AI_POST_GENERATOR_VALIDATION = None

def init_builder():
    global AUTO_COACHING_SURVEY
    global TEST_OUTPLACEMENT_SURVEY
    global META_SEARCH_SURVEY
    global AI_POST_GENERATOR
    
    if AUTO_COACHING_SURVEY is None:
        with open("app/surveys/data/auto_coaching_questions.json", "r", encoding='utf-8') as file:
            AUTO_COACHING_SURVEY = file.read()
    
    if TEST_OUTPLACEMENT_SURVEY is None:
        with open("app/surveys/data/test_outplacement_questions.json", "r", encoding='utf-8') as file:
            TEST_OUTPLACEMENT_SURVEY = file.read()
            
    if META_SEARCH_SURVEY is None:
        with open("app/surveys/data/meta_search_questions.json", "r", encoding='utf-8') as file:
            META_SEARCH_SURVEY = file.read()

    if AI_POST_GENERATOR is None:
        with open("app/surveys/data/user_profile_postai_question.json", "r", encoding='utf-8') as file:
            AI_POST_GENERATOR = file.read()
            
    global AUTO_COACHING_VALIDATION
    global TEST_OUTPLACEMENT_VALIDATION
    global META_SEARCH_VALIDATION
    global AI_POST_GENERATOR_VALIDATION

    if AUTO_COACHING_VALIDATION is None:
        with open("app/surveys/data/auto_coaching_validation.json", "r", encoding='utf-8') as file:
            AUTO_COACHING_VALIDATION = file.read()
    
    if TEST_OUTPLACEMENT_VALIDATION is None:
        with open("app/surveys/data/test_outplacement_validation.json", "r", encoding='utf-8') as file:
            TEST_OUTPLACEMENT_VALIDATION = file.read()
    """
    if META_SEARCH_VALIDATION is None:
        with open("app/surveys/data/meta_search_validation.json", "r", encoding='utf-8') as file:
            META_SEARCH_VALIDATION = file.read()
    """        

def get_survey(survey_name) -> Survey:
    init_builder()
    
    if survey_name == Survey.Type.AUTO_COACHING.value:
        data_dict = loads(AUTO_COACHING_SURVEY)
        return Survey(data_dict)
    
    if survey_name == Survey.Type.TEST_OUTPLACEMENT.value:
        data_dict = loads(TEST_OUTPLACEMENT_SURVEY)
        return Survey(data_dict)
    
    if survey_name == Survey.Type.META_SEARCH.value:
        data_dict = loads(META_SEARCH_SURVEY)
        return Survey(data_dict)
    
    if survey_name == Survey.Type.AI_POST_GENERATOR.value:
        data_dict = loads(AI_POST_GENERATOR)
        return Survey(data_dict)
    
    return None

def get_Checker(survey_name) -> Checker:
    init_builder()
    
    if survey_name == Survey.Type.AUTO_COACHING.value:
        data_dict = loads(AUTO_COACHING_VALIDATION)
        return AutoCoachingChecker(data_dict['response'], data_dict['results'])
    
    if survey_name == Survey.Type.TEST_OUTPLACEMENT.value:
        data_dict = loads(TEST_OUTPLACEMENT_VALIDATION)
        return TestOutplacementChecker(**data_dict)
    
    if survey_name == Survey.Type.META_SEARCH.value:
        #data_dict = loads(META_SEARCH_VALIDATION)
        return MetaSearchChecker()
    
    if survey_name == Survey.Type.AI_POST_GENERATOR.value:
        #data_dict = loads(AI_POST_GENERATOR_VALIDATION)
        return AiPostGeneratorChecker()
    
    return None