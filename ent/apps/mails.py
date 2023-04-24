import json
from ent import consts
from ent.apps import base
from ent.apps.base import User
from dataclasses import dataclass
from datetime import date, datetime
from typing import Generator
from bs4 import BeautifulSoup as Soup

# TODO add client var to all dataclasses

@dataclass
class Folder:
    name: str
    id: int
    path: str
    unread: int
    subfolders: list

@dataclass
class usersMailGroup:
    sender: User
    to: list[User]
    cc: list[User]
    bcc: list[User]
    
    @classmethod
    def parse(cls, data: dict, client: object) -> object:
        '''
        Build from ENT dict.
        '''
        
        names = {k: v for k, v in data.get('displayNames')}
        sender = data.get('from')
        
        return cls(
            sender = User(id = sender, name = names[sender]),
            to = [User(id = id, name = names[id]) for id in data.get('to')],
            cc = [User(id = id, name = names[id]) for id in data.get('cc')],
            bcc = [User(id = id, name = names[id]) for id in data.get('bcc')],
        )


@dataclass
class Attachment:
    client: object
    id: int
    url: str
    name: str
    type: str
    size: int
    
    @classmethod
    def parse(cls, data: dict, mail: object) -> object:
        '''
        Build from ENT dict.
        '''
        
        id = data.get('id')
        
        return cls(
            client = mail.client,
            id = id,
            url = f'zimbra/message/{mail.id}/attachment/{id}',
            name = data.get('filename'),
            type = data.get('contentType'),
            size = data.get('size')
        )
    
    def download(self, path: str) -> None:
        '''
        Download the ressource.
        '''
        
        with open(path, 'wb') as output:
            raw = self.client.session.get(path)
            output.write(raw.content)


@dataclass
class Mail:
    client: object
    
    id: int
    date: int
    subject: str
    unread: bool
    user: usersMailGroup
    has_attachment: bool
    data: dict = None
    content_data: dict = None
    
    @classmethod
    def parse(cls, data: dict, client: object) -> object:
        '''
        Build mail from ENT dict.
        '''
        
        mail_date = data.get('date') # TODO parse
        
        return cls(
            client = client,
            id = int(data.get('id')),
            date = mail_date,
            subject = data.get('subject'),
            unread = data.get('unread'),
            has_attachment = data.get('hasAttachment'),
            user = usersMailGroup.parse(data, client),
            data = data
        )

    def fetch(self) -> None:
        '''
        Fetch the content of the mail.
        '''
        
        url = f'zimbra/message/{self.id}'
        self.content_data = self.client.get(url).json()

    @property
    def attachments(self) -> list[Attachment]:
        '''
        Get the mail attachments.
        '''
        
        if not self.content_data: self.fetch()
        return [Attachment.parse(data, self)
                for data in self.content_data.get('attachments')]
    
    @property
    def folder(self) -> Folder:
        '''
        Get the parent folder of the mail.
        '''
        
        pass
    
    @property
    def content(self) -> str:
        '''
        Get raw content of the mail.
        '''
        
        if not self.content_data: self.fetch()
        return self.content_data.get('body')
        
        

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
    
    def get_folders(self) -> list[Folder]:
        '''
        Get all folders from the ENT account.
        '''
        
        # Get raw body
        raw = self.client.get('zimbra/zimbra').text
        
        # Parse folders
        js = consts.re.mail_get_folder_data.findall(raw)[0]
        folders = json.loads(js)
        
        # Recursively build folders structure
        def rec(data: dict) -> Folder:
            return Folder(name = data['folderName'],
                          id = int(data['id']),
                          path = data['path'],
                          unread = int(data['unread']),
                          subfolders = [rec(f)
                                        for f in data['folders']])
        
        return [rec(data) for data in folders]

    def get_mails(self,
                  unread: bool = False,
                  folder: Folder = None,
                  limit: int = 10) -> Generator[Mail, None, None]:
        '''
        Get a list of mails.
        '''
        
        folder = folder.path.replace('/', consts.slash) if folder else '%2FInbox'
        u = f'zimbra/list?folder={folder}&page={{}}&unread={str(unread).lower()}'
        
        mails = []
        
        # Fetch mails
        for i in range(0, limit, 10):    
            mails += self.client.get(u.format(i // 10)).json()
        
        # Parse mails
        return [Mail.parse(mail, self.client) for mail in mails]

# EOF