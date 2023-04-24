import re as regex

root = 'https://ent.iledefrance.fr/'

slash = '%2F'

class re:
    
    mail_get_folder_data = regex.compile(r"\"folders\": '(.*?)\'")