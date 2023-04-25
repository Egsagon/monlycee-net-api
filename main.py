import ent
import json

from ent.apps.base import User
from ent.apps.mails import PreparedMail

creds = json.load(open('creds.json'))
client = ent.ENT(**creds)


me = User.from_id('630016c2-e0cd-46c5-816d-53d029ba258b')

f = client.mail.get_folders()[-4]

ma = f.get_mails()[0]

ma.transfer(me)
