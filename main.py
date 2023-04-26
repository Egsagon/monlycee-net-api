import ent, json

client = ent.ENT(**json.load(open('creds.json')))

print(
    client.userbase.search_groups()[0]
)