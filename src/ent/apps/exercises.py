'''
Exercises app (qcms).
'''

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ent import utils
from ent.apps import base
from ent.apps.base import User

if TYPE_CHECKING:
    from ent.core import ENT as Core

@dataclass
class ExerciseDate:
    created:  datetime = None
    modified: datetime = None
    submited: datetime = None

@dataclass
class ExerciseResult:
    score:      float = None
    auto_score: float = None
    comment:    str = None

@dataclass
class Exercise:
    id:     int = None
    owner:  User = None
    date:   ExerciseDate = None
    result: ExerciseResult = None
    
    started:       bool = None
    deleted:       bool = None
    archived:      bool = None
    corrected:     bool = None
    is_training:   bool = None
    is_correcting: bool = None


class Exercises_App(base.App):
    
    def __init__(self, client: Core) -> None:
        
        self.client = client
    
    def get(self) -> None:
        '''
        Get all visible exercises.
        '''
        
        data = self.client.get('exercizer/subjects-copy').json()
        
        return [
            Exercise(
                id             = int(obj.get('id')),
                owner          = User.from_id(obj.get('owner')),
                
                date = ExerciseDate(
                    created    = utils.try_parse_exercise_date(obj.get('created')),
                    modified   = utils.try_parse_exercise_date(obj.get('modified')),
                    submited   = utils.try_parse_exercise_date(obj.get('submitted_date')),
                ),
                
                result = ExerciseResult(
                    score      = obj.get('final_score'),
                    auto_score = obj.get('calculated_score'),
                    comment    = obj.get('comment')
                ),
                
                started        = obj.get('has_been_started'),
                deleted        = obj.get('is_deleted'),
                archived       = obj.get('is_archived'),
                corrected      = obj.get('is_corrected'),
                is_training    = obj.get('is_training_copy'),
                is_correcting  = obj.get('is_correction_on_going')
            )
            
            for obj in data
        ]

# EOF