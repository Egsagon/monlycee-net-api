'''
Home feed app.
'''


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ent import utils
from ent.apps import base
from ent.apps.base import User

if TYPE_CHECKING:
    from ent.core import ENT as Core

@dataclass
class Feed:
    id: str = None
    type: str = None
    event: str = None
    sender: User = None
    date: str = None
    content: str = None
    url: str = None


class Feed_App(base.App):
    
    def __init__(self, client: Core) -> None:
        
        self.client = client
    
    def fetch(self, **filters) -> list[Feed]:
        '''
        Fetch the last feed.
        '''
        
        # Build url
        url = 'timeline/lastNotifications'
        url += utils.build_feed_filters(filters)
        
        response = self.client.get(url).json()
        
        return [
            Feed(
                id = obj.get('_id'),
                type = obj.get('type'),
                event = obj.get('event-type'),
                sender = User(
                    id = obj.get('sender'),
                    name = obj.get('params', {}).get('username')
                ),
                content = obj.get('message'),
                url = obj.get('params', {}).get('uri') or \
                      obj.get('params', {}).get('resssourceUri'),
                date = utils.try_parse_exercise_date(obj.get('date')) # why do they never use the same format >_<
            )
            for obj in response.get('results', [])
        ]
        

# EOF   