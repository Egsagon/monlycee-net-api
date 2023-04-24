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
                cache: bool = True,
                complete_path = True) -> requests.Response:
        '''
        Make a request to the target.
        '''
        
        url = (consts.root if complete_path else '') + path
        
        key = f'{method}:{path}{data}'
        
        # Get from cache
        if cache and key in self.cache:
            return self.cache.get(key)
        
        # Send the request
        response = self.session.request(method, url, data = data)
        
        if not response.ok:
            raise ConnectionError('Failed to send request', key, 'Got response:', response.content)
        
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
    
    @property
    def mail(self) -> apps.mails.Mail_app:
        '''
        Mail application of the ENT.
        '''
        
        if not 'mail' in self.apps:
            self.apps['mail'] = apps.mails.Mail_app(self)
        
        return self.apps['mail']

# EOF