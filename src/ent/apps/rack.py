'''
Rack app (casier)
'''

from __future__ import annotations

import filetype
from datetime import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass

from ent import utils
from ent import consts
from ent.apps import base
from ent.apps.base import User

if TYPE_CHECKING:
    from ent.core import ENT as Core


@dataclass
class RackStorage:
    used: int = None
    limit: int = None
    
    @property
    def usage(self) -> float:
        '''
        Percentage of storage usage.
        '''
        
        return self.used / self.limit * 100

@dataclass
class RacKFile:
    url: str = None
    type: str = None
    size: int = None
    charset: str = None
    
    def download(self, path: str) -> None:
        '''
        Download the file to a location.
        '''
        
        pass # TODO

@dataclass
class Rack:
    id: str = None
    name: str = None
    date: datetime = None
    
    sender: User = None
    receiver: User = None
    file: RacKFile = None


class Rack_App(base.App):
    
    def __init__(self, client: Core) -> None:
        '''
        Represent an instance of the rack ENT app.
        '''
        
        self.client = client
        self.rack_storage: RackStorage = None
    
    def get_rack(self) -> None:
        '''
        Get the content of the user rack.
        '''
        
        data = self.client.get('rack/list').json()
        meta = [obj.get('metadata') or {} for obj in data]
        
        return [
            Rack(
                id          = obj.get('_id'),
                name        = obj.get('name'),
                date        = utils.try_parse_rack_date(obj.get('sent')),
                sender      = User(obj.get('from'), obj.get('fromName')),
                receiver    = User(obj.get('to'), obj.get('toName')),
                
                file = RacKFile(
                    url     = consts.root + 'rack/get/' + obj.get('file', 'unknown'),
                    type    = meta.get('content-type'),
                    size    = meta.get('size'),
                    charset = meta.get('charset')
                )
            )
            
            for obj, meta in zip(data, meta)
        ]
    
    def deposit(self, users: User | list[User], path: str) -> None:
        '''
        Deposit a file to somebody's rack.
        '''
        
        if not isinstance(users, list): users = [users]
        
        # Fetch file data
        filename = utils.get_filename(path)
        ftype = filetype.guess(path)
        ftype = ftype.mime if ftype else 'text/plain' 
        
        with open(path, 'rb') as file:
            filebody = file.read()
        
        xsrf = self.client.session.cookies['XSRF-TOKEN']
        bound = utils.gen_rack_boundary()
        
        raw = consts.rack_file_template.format(
            name = 'file',
            filename = filename,
            boundary = bound,
            content = filebody,
            filetype = ftype,
            users = ','.join([u.id for u in users])
        )
        
        response = self.client.get(
            'rack?thumbnail=120x120', 'POST',
            data = raw,
            headers = {
                'X-XSRF-TOKEN': xsrf,
                'Content-Type': f'multipart/form-data; boundary=---------------------------{bound}'
            }
        ).json()
        
        if not response.get('success'):
            raise Exception(f'Failed to transmit {path}:', response)
    
    def refresh_storage_usage(self) -> None:
        '''
        Refresh the allocated storage data.
        '''
        
        uid = self.client.account.user.id
        data = self.client.get('workspace/quota/user/' + uid).json()
        
        self.rack_storage = RackStorage(
            used = data.get('quota'),
            limit = data.get('storage')
        )
    
    @property
    def storage(self) -> RackStorage:
        '''
        User' storage data.
        '''
        
        if not self.rack_storage: self.refresh_storage_usage()
        return self.rack_storage

# EOF