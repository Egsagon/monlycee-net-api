import os.path
from random import randint
from datetime import datetime

def try_parse_exercise_date(raw: str) -> datetime | None:
    
    format_ = '%Y-%m-%dT%H:%M:%S.%f'
    
    try: return datetime.strptime(raw, format_)
    except: pass

def try_parse_rack_date(raw: str) -> datetime | None:
    
    format_ = '%Y-%m-%dT%H:%M%z'
    
    try: return datetime.strptime(raw, format_)
    except: pass

def gen_rack_boundary(length = 30) -> str:
    '''
    Generate a rack content boundary for the backend
    to parse.
    '''
    
    return ''.join(str(randint(0, 9)) for _ in range(length))

def get_filename(path: str) -> str:
    '''
    Get the name of a file knowing its path.
    '''
    
    return os.path.split(path)[-1]

# EOF