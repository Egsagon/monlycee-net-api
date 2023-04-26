import ent, json

client = ent.ENT(**json.load(open('creds.json')))

rec = client.userbase.search_users('KEIZER')[0]

print(
    client.rack.deposit(rec, 'test.txt')
)