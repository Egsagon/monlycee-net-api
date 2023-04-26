from __future__ import annotations

from ent.apps import base
from ent.apps.base import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ent.core import ENT as Core


class User_app(base.App):
    
    def __init__(self, client: Core) -> None:
        '''
        Represents an instance able to fetch the user
        account data.
        '''
        
        self.client = client
        self.data: dict = None
    
    def refresh(self) -> None:
        '''
        Update the account data.
        '''
    
        self.data = self.client.get('auth/oauth2/userinfo', cache = False).json()
    
    @property
    def user(self) -> User:
        '''
        The user account representation.
        '''
        
        if not self.data: self.refresh()
        return User(
            id = self.data['userId'],
            name = self.data['username'],
            type = self.data['type'],
            groups = self.data['groupsIds'], # TODO classify
            classes = self.data['classes'], # &
            schools = self.data['structures'] # &
        )

# EOF