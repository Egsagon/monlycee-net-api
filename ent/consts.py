import re as regex

root = 'https://ent.iledefrance.fr/'

slash = '%2F'

class re:
    
    mail_get_folder_data = regex.compile(r"\"folders\": '(.*?)\'")


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