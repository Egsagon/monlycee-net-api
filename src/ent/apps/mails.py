'''
Mail app (zimbra)
'''

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass
from typing import Self, TYPE_CHECKING

from ent import consts
from ent.apps import base
from ent.apps.base import User

if TYPE_CHECKING:
    from ent.core import ENT as Core

@dataclass
class Folder:
    parent: Mail_app
    name: str
    id: int
    path: str
    unread: int
    subfolders: list
    
    def get_mails(self,
                  unread: bool = False,
                  limit: int = 10) -> list['Mail']:
        '''
        Get all mails for this folder.
        '''
        
        return self.parent.get_mails(unread = unread,
                                     folder = self,
                                     limit = limit)


@dataclass
class usersMailGroup:
    sender: User
    to: list[User]
    cc: list[User]
    bcc: list[User]
    
    @classmethod
    def parse(cls, data: dict, client: object) -> Self:
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
    
    def serialize(self, keys = ['to', 'cc', 'bcc']) -> None:
        '''
        Return a dict version of to, cc and bcc.
        '''
        
        return {k: [u.id for u in getattr(self, k)] for k in keys}


@dataclass
class Attachment:
    client: Core
    id: int
    url: str
    name: str
    type: str
    size: int
    
    @classmethod
    def parse(cls, data: dict, mail: Mail) -> Self:
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
        
        if path[-1] != '/': path += '/'
        
        with open(path + self.name, 'wb') as output:
            raw = self.client.get(self.url)
            output.write(raw.content)


@dataclass
class PreparedMail:
    subject: str
    content: str
    attachments: list[Attachment]
    user: usersMailGroup
    
    id: int = None
    
    @classmethod
    def new(cls,
            subject: str = None,
            content: str = None,
            to: list[User] = None,
            cc: list[User] = [],
            bcc: list[User] = [],
            attachments: list[str] = []) -> Self:
        '''
        Create a new mail.
        TODO - attachments upload
        '''
        
        if not isinstance(to, list): to = [to]
        if not isinstance(cc, list): cc = [cc]
        if not isinstance(bcc, list): bcc = [bcc]
        
        return cls(
            subject = subject,
            content = content,
            attachments = attachments,
            user = usersMailGroup(None, to, cc, bcc) # TODO fetch client data
        )


@dataclass
class Mail:
    client: Core
    
    id: int
    date: datetime
    subject: str
    unread: bool
    user: usersMailGroup
    has_attachment: bool
    data: dict = None
    content_data: dict = None
    
    @classmethod
    def parse(cls, data: dict, client: Core) -> Self:
        '''
        Build mail from ENT dict.
        '''
        
        mail_date = datetime.fromtimestamp(data.get('date') / 1000)
        
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

    def reply(self, mail: PreparedMail, force_redirect = False) -> None:
        '''
        Reply to this message with a prepared mail.
        
        Arguments
            mail: a PreparedMail instance.
            force_redirect: Use the PreparedMail user group instead.
        '''
        
        users = mail.user if force_redirect else self.user
        
        response = self.client.get(f'zimbra/send?In-Reply-To={self.id}', 'POST', data = dict(
            attachments = mail.attachments,
            body = mail.content,
            subject = mail.subject,
            **users.serialize()
        ), dump = True)
        
        return response

    def transfer(self, to: list[User] | User) -> None:
        '''
        Transfer a mail to another user.
        '''
        
        new = deepcopy(self)
        new.user.to = to if isinstance(to, list) else [to]
        self.client.mail.send(new) # TODO body not working


class Mail_app(base.App):
    
    def __init__(self, client: Core) -> None:
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
            return Folder(parent = self,
                          name = data['folderName'],
                          id = int(data['id']),
                          path = data['path'],
                          unread = int(data['unread']),
                          subfolders = [rec(f)
                                        for f in data['folders']])
        
        return [rec(data) for data in folders]

    def get_mails(self,
                  unread: bool = False,
                  folder: Folder = None,
                  limit: int = 10) -> list[Mail]:
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

    def send(self, mail: PreparedMail) -> None:
        '''
        Send a mail object to the ENT.
        '''
        
        # Attribute an id for the mail by sending empty draft
        mail.id = self.client.get('zimbra/draft', 'POST', data = dict(
            body = 'New Prepared request', to = [], cc = [], bcc = [], attachments = []
        ), dump = True).json().get('id')
        
        url = f'zimbra/send?id={mail.id}'
        
        response = self.client.get(url, 'POST', data = dict(
            attachments = mail.attachments,
            body = mail.content,
            subject = mail.subject,
            **mail.user.serialize()
        ), dump = True).json()
        
        if not response.get('sent'):
            raise ConnectionError('Failed to send email:', response)

# EOF