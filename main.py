import ent
import json

creds = json.load(open('creds.json'))
client = ent.ENT(**creds)

# print(client.mail.unread_amount)

folders = client.mail.get_folders()

mails = client.mail.get_mails(limit = 10)

print(mails[1].attachments)