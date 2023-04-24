#                               #
# Structures common to all apps #
#                               #

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

# EOF