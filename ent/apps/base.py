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
    id: int = None
    name: str = None
    type: str = None # TODO
    level: str = None # TODO
    groups: list[str] = None # TODO
    classes: list[str] = None # TODO
    schools: list[str] = None # TODO
    
    @classmethod
    def from_id(cls, id: str) -> Self:
        '''
        Fetch a user from its id.
        '''
        
        return cls(id = id, name = '<unknown>')

@dataclass
class Group:
    id: str = None
    name: str = None
    title: str = None
    length: int = None
    profile: str = None
    sort_name: str = None
    
    @property
    def users(self) -> list[User]:
        '''
        A list of users in this group.
        '''
        
        pass # TODO

# EOF