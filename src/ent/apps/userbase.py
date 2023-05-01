'''
Userbase app.
'''

from __future__ import annotations

from ent.apps import base
from typing import TYPE_CHECKING
from ent.apps.base import User, Group

if TYPE_CHECKING:
    from ent.core import ENT as Core


class Userbase_App(base.App):
    
    def __init__(self, client: Core) -> None:
        '''
        Represents an instance for the user ENT account.
        '''
        
        self.client = client
    
    def _base_search(self, **kwargs) -> dict:
        '''
        Handle sending POST requests to the server
        to search for groups or users.
        '''
        
        xsrf = self.client.session.cookies['XSRF-TOKEN']
        
        response = self.client.get(
            'communication/visible', 'POST',
            data = kwargs,
            headers = {'X-XSRF-TOKEN': xsrf},
            dump = True
        ).json()
        
        return response
    
    def search_users(self,
               query: str = '',
               classes: list[str] = None,
               schools: list[str] = None,
               functions: list[str] = None) -> list[User]:
        '''
        Search for users among the list the user has access to.
        '''
        
        users = self._base_search(
            search = query,
            classes = classes,
            structures = schools,
            functions = functions,
            types = ['User']
        )['users']
        
        return [User(data['id'],
                     data['displayName'],
                     data['profile']) for data in users]
    
    def search_groups(self,
                     query: str = '',
                     classes: list[str] = None,
                     schools: list[str] = None,
                     functions: list[str] = None,
                     group_type: str = 'Group') -> list[Group]:
        '''
        Search for groups among the list the groups has access to.
        '''
        
        groups = self._base_search(
            search = query,
            classes = classes,
            structures = schools,
            functions = functions,
            types = group_type,
            groupType = True,
            nbUsersInGroups = True
        )['groups']
        
        return [Group(data.get('id'),
                      data.get('name'),
                      data.get('groupDisplayName'),
                      data.get('nbUsers'),
                      data.get('profile'),
                      data.get('sortName'))
                for data in groups]

# EOF