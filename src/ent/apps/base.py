'''
Basic structures shared between apps.
'''

from __future__ import annotations
from dataclasses import dataclass
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from ent.apps.userbook import UserbookData
    from ent.core import ENT as Core

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
    
    client: Core = None
    userbook: UserbookData = None
    
    @classmethod
    def from_id(cls, id: str) -> Self:
        '''
        Fetch a user from its id.
        '''
        
        return cls(id = id, name = '<unknown>')
    
    @property
    def book(self) -> UserbookData:
        '''
        The userbook content of the user.
        '''
        
        if self.userbook is None:
            self.client.userbook.fetch(self)
        
        return self.userbook

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