'''
Core module of the API.
'''

import json
import requests

from ent import consts
from ent import apps

class ENT:
    
    def __init__(self,
                 username: str,
                 password: str,
                 login: bool = True) -> None:
        '''
        Represents an ENT session.
        '''
        
        # Check credentials
        assert len(username) and len(password), 'Empty credentials'
        
        # Save credentials
        self.session = requests.Session()
        self.payload = {'email': username, 'password': password}
        
        self.apps = {}
        self.cache = {}
        
        # Build apps
        # TODO - Find a way to generate them dynamically
        self.mail      = apps.mails.Mail_app(self)
        self.account   = apps.user.User_app(self)
        self.userbase  = apps.userbase.Userbase_App(self)
        self.exercises = apps.exercises.Exercises_App(self)
        self.rack      = apps.rack.Rack_App(self)
        self.userbook  = apps.userbook.Userbook_App(self)
        self.feed      = apps.feed.Feed_App(self)
        
        if login: self.login()
    
    def get(self,
                path: str,
                method: str = 'GET',
                data: dict = None,
                headers: dict = None,
                cache: bool = True,
                complete_path = True,
                dump: bool = False,
                inject_token: bool = False # TODO
                ) -> requests.Response:
        '''
        Make a request to the target.
        '''
        
        url = (consts.root if complete_path else '') + path
        
        key = f'{method}:{path}{data}///{headers}'
        
        # Get from cache
        if cache and key in self.cache:
            return self.cache.get(key)
        
        # Inject XRSF
        if inject_token:
            
            xsrf = self.session.cookies['XSRF-TOKEN']
            end = {'X-XSRF-TOKEN': xsrf}
            
            headers = end if headers is None else headers | end
        
        # Send the request
        if dump: data = json.dumps(data)
        response = self.session.request(method, url, data = data, headers = headers)
        
        if not response.ok:
            raise ConnectionError('Failed to send request', key, 'Got response:', response.content, 'with code', response)
        
        return response

    def login(self) -> None:
        '''
        Attempts to login to the ENT.
        '''
        
        # Send credentials
        self.get('auth/login', 'POST', self.payload)
        
        # Check if authentificated
        if not self.session.cookies.get('XSRF-TOKEN'):
            raise ConnectionRefusedError('Invalid credentials.')

# EOF