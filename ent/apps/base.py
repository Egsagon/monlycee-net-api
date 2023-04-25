# ----------------------------- #
# Structures common to all apps #
# ----------------------------- #

from typing import Self
from dataclasses import dataclass


class App:
    def __init__(self, client: object) -> None:
        '''
        Represents a base instance for an ENT app.
        '''
        
        self.client = client


@dataclass
class User:
    id: int
    name: str
    
    @classmethod
    def from_id(cls, id: str) -> Self:
        '''
        Fetch a user from its id.
        '''
        
        return cls(id = id, name = '<unknown>')

# EOF