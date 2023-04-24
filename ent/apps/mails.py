from ent.apps import base

class Mail_app(base.App):
    
    def __init__(self, client) -> None:
        '''
        Represents the mails app.
        '''
        
        self.client = client
    
    @property
    def unread_amount(self) -> int:
        '''
        Fetch the amount of unread messages.
        '''
        
        url = 'zimbra/count/INBOX?unread=true'
        return self.client.get(url).json()['count']