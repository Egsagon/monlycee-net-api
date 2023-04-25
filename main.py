import ent
import json

from ent.apps.mails import PreparedMail

creds = json.load(open('creds.json'))
client = ent.ENT(**creds)

m = PreparedMail.new( 'test subject 2', 'test content', to = ['630016c2-e0cd-46c5-816d-53d029ba258b'])

print(client.mail.send(m))