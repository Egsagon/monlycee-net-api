'''
Userbooks app.
'''

from __future__ import annotations

from ent.apps import base
from typing import TYPE_CHECKING
from dataclasses import dataclass
from ent.apps.base import User, Group

if TYPE_CHECKING:
    from ent.core import ENT as Core

@dataclass
class Hobby:
    visible: bool = None
    category: str = None
    content: str = None

@dataclass
class Contact:
    tel: str
    email: str
    mobile: str

@dataclass
class UserbookData:
    mood: str = None
    health: str = None
    motto: str = None
    address: str = None
    birthdate: str = None
    contact: Contact = None
    hobbies: list[Hobby] = None
    relations: list[User] = None
    
    pfp_url: str = None


class Userbook_App(base.App):
    
    def __init__(self, client: Core) -> None:
        '''
        Represents an instance of the ENT userbook app.
        '''
        
        self.client = client
    
    def fetch(self, user: User) -> User:
        '''
        Fetch the userbook data for a user.
        '''
        
        # data = self.client.get('directory/userbook/' + user.id).json()
        
        raw = self.client.get('userbook/api/person?id=' + user.id)
        
        relations = raw.json()['result']
        data = relations[0]
        
        user.userbook = UserbookData(
            mood = data.get('mood'),
            health = data.get('health'),
            motto = data.get('motto'),
            address = data.get('address'),
            contact = Contact(
                tel = data.get('tel'),
                email = data.get('email'),
                mobile = data.get('mobile')
            ),
            hobbies = [
                Hobby(
                    visible = hobby.get('visibility') != 'PRIVE',
                    category = hobby.get('category'),
                    content = data.get('values')
                )
                for hobby in data.get('hobbies', [])
            ],
            relations = [
                User(
                    rel.get('relatedId'),
                    rel.get('relatedName'),
                    client = self.client
                ) for rel in relations
            ] if data.get('relatedId') is not None else [],
            pfp_url = data.get('photo')
        )
        
        return user

# EOF