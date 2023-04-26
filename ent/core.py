import json
import requests

from ent import consts
from ent import apps


class ENT:
    
    def __init__(self, username: str, password: str, login: bool = True) -> None:
        '''
        Represents a session to the open ENT.
        '''
        
        # Check credentials
        assert len(username) and len(password), 'Empty credentials'
        
        # Save credentials
        self.session = requests.Session()
        self.payload = {'email': username, 'password': password}
        
        self.apps = {}
        self.cache = {}
        
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
    
    # ---------- Apps ---------- #
    @property
    def mail(self) -> apps.mails.Mail_app:
        '''
        Mail application of the ENT.
        '''
        
        if not 'mail' in self.apps:
            self.apps['mail'] = apps.mails.Mail_app(self)
        
        return self.apps['mail']

    @property
    def account(self) -> apps.user.User_app:
        '''
        User account data.
        '''
        
        if not 'account' in self.apps:
            self.apps['account'] = apps.user.User_app(self)
        
        return self.apps['account']
    
    @property
    def userbase(self) -> apps.userbase.Userbase_App:
        '''
        Userbase.
        '''
        
        if not 'userbase' in self.apps:
            self.apps['userbase'] = apps.userbase.Userbase_App(self)
        
        return self.apps['userbase']

    @property
    def exercises(self) -> apps.exercises.Exercises_App:
        '''
        Exercises app.
        '''
        
        if not 'exercises' in self.apps:
            self.apps['exercises'] = apps.exercises.Exercises_App(self)
        
        return self.apps['exercises']

    @property
    def rack(self) -> apps.rack.Rack_App:
        '''
        The Rack app.
        '''
        
        if not 'rack' in self.apps:
            self.apps['rack'] = apps.rack.Rack_App(self)
        
        return self.apps['rack']

# EOF