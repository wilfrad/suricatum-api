from abc import ABC, abstractmethod
from enum import Enum

class Checker(ABC):
    
    @abstractmethod
    def validate(self, data_list):
        pass
    
    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_results(self):
        pass

class AutoCoachingChecker(Checker):
    def __init__(self, responses, results):
        self.responses = responses
        self.results = results
    
    def validate(self, data_list):
        scores = {}

        #get data from survey responses
        for quest_id_str, selection_obj in data_list.items():
            for item in self.results:
                quest_id = int(quest_id_str)
                
                if len(item['triggers']) < quest_id:
                    continue
                
                trigger = item['triggers'][quest_id - 1]
                
                if any(value in trigger['responses'] for value in list(selection_obj.values())):
                    recommend = item['recommend']['name']
                    scores[recommend] = scores.get(recommend, 0) + 1

        self.scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def get_response(self, selection):
        tip = None
        
        for item in self.responses:
            for response in item['option-response']:
                if response['id'] in list(selection.values()):
                    tip = response['tip']
                    break
        
        return tip

    def get_results(self):
        return self.scores_sorted
    
class TestOutplacementChecker(Checker):
    def __init__(self, axis, recommends, rating, axis_score_focus_rating):
        self.axis = axis
        self.recommends = recommends
        self.rating= rating
        self.axis_score_focus_rating = axis_score_focus_rating
    
    class _ValidateMode(Enum):
        SUM = 'sum'
        SUB = 'sub'
        PROP = 'prop'
    ######################################################
    # Validate private methods
    def _match(self, quest_id):
        for cur_axis in self.axis:
            for response in cur_axis['responses']:
                if quest_id == response['quest_id']:
                    return { 
                        '_id': cur_axis['id'],
                        'score': 0,
                        'short_name': cur_axis['name'].split('-')[1].strip(),
                        'name': cur_axis['name'],
                        'max_score': cur_axis['max-score'],
                        'options' : response['options'] 
                    }
        
        return None
    
    _is_continue_calc = False
    _prev_calc = 0
    
    def _calc_score(self, score, mode):
        if mode== self._ValidateMode.SUB:
            if self.is_continue_calc:
                self.is_continue_calc = False
                return abs(self._prev_calc - score)
            else:
                self.is_continue_calc = True
                self._prev_calc = score
                return 0
            
        if mode == self._ValidateMode.PROP:
            if self.is_continue_calc:
                self.is_continue_calc = False
                k = 2
                return abs(k - self._prev_calc / score + k)
            else:
                self.is_continue_calc = True
                self._prev_calc = score
                return 0
        
        return score
    ######################################################
    def validate(self, data_list):            
        score = {}
        
        for quest_id_str, selection_obj in data_list.items():
            quest_id = int(quest_id_str)
            _match = self._match(quest_id)
            
            if _match is None:
                continue
            
            result = None
            for selection in list(selection_obj.values()):
                for option in _match['options']:
                    if option['key'] == selection:
                        result = self._calc_score(option['score'], option['mode'])
            
            _match['score'] = score.get(_match['_id'], {'score': 0})['score'] + result
            
            score[_match['_id']] = _match
            
        self.score = score
    
    ######################################################
    # Response private methods
    def _get_scores_array(self, data):
        scores = []
        
        for item in data.values():
            scores.append(item['score'])
        
        return scores
    
    def _get_axis_array(self, data):
        axis_arr = []
        
        for item in data.values():
            axis = {}
            
            axis['name'] = item['name']
            axis['short_name'] = item['short_name']
            
            for rating in self.rating:
                cur_score = item['score']
                if cur_score > rating['score-range'][0] and cur_score < rating['score-range'][1]:
                    axis['rating_id'] = rating['id']
                    axis['color_rgb'] = rating['color-rgb']
                    axis['color_hex'] = rating['color-hex']
                    
            axis_arr.append(axis)
        
        return axis_arr
    
    def _get_tips_array(self, data):
        tips = []
        
        for item in data.values():
            tip = {}
            
            axis = self._get_axis_array({ 'item': item })[0]
            
            tip['color_hex'] = axis['color_hex']
            tip['name'] = axis['name']
            
            for recommend in self.recommends:
                if recommend['axis'] == item['_id']:
                    for result in recommend['results']:
                        if axis['rating_id'] == result['rating']:
                            tip['text'] = result['paragraph']
            
            tips.append(tip)
        
        return tips
    ######################################################
    def get_response(self, data):
        self.validate(data)
        
        result = self.get_results()
        
        return {
            'data': self._get_scores_array(result),
            'chart_axis': self._get_axis_array(result),
            'tips': self._get_tips_array(result),
            'ratings': self.rating
        }

    def get_results(self):
        return self.score
    
class MetaSearchChecker(Checker):
    def __init__(self) -> None:
        return
    
    def validate(self):
        return

    def get_results(self):
        return