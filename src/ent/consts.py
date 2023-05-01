'''
Constants for the core module.
'''

import re as regex

root = 'https://ent.iledefrance.fr/'

slash = '%2F'

class re:
    '''
    Useful compiled regexes for fast web scrapping.
    '''
    
    mail_get_folder_data = regex.compile(r"\"folders\": '(.*?)\'")


# Template for uploading files with the rack app.
rack_file_template = '''-----------------------------{boundary}
Content-Disposition: form-data; name="file"; filename="{filename}"
Content-Type: {filetype}

{content}
-----------------------------{boundary}
Content-Disposition: form-data; name="users"

{users}
-----------------------------{boundary}--
'''

# EOF