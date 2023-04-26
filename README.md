# monlycee-net-api
An API wrapper for ent.iledefrance.fr

## Example usage


### Initialisation
```py
>>> import ent
>>>>

>>> client = ent.ENT('username', 'password')


# ----- Mails app ----- #

# Get amount of unread messages
>>> count = client.mail.unread_amount

# Get folders
>>> folders = client.mail.get_folders()

# Get mails
>>> mails = client.mail.get_mails(limit = 10)
# OR
>>> folders[...].get_mails(limit = 10)

# Get mail data
>>> mail = mails[0]
>>> mail.date
>>> mail.attachments
>>> mail.unread
>>> mail.user.sender
>>> mail.user.to # etc.

# Reply to a mail
>>> from ent.apps.mails import PreparedMail
>>> reply = PreparedMail.new(subject = 'Re: Subject',
                             content = 'Hello, world!')
>>> mail.reply(reply)

# Transfer a mail
>>> from ent.apps.base import User
>>> mail.transfer(User.from_id(...))

# Send a normal mail
>>> mail = PreparedMail.new(subject = 'Subject',
                            content = 'Hello, world!')
>>> client.mail.send(mail)

# ----- Rack app ----- #

# Get the user rack
>>> rack = client.rack.get_rack()

# Get rack data/file
>>> rack[0].sender
>>> rack[1].receiver
>>> rack[2].file.size
>>> rack[3].file.download()

# Get repo storage usage
>>> storage = client.rack.storage
>>> storage.used
>>> storage.limit
>>> storage.usage # in percentage

# Deposit a file to someone's rack
>>> client.rack.deposit(User.from_id(...), 'path/to/file.ext')

# ----- Userbase app ----- #

# Search for users
>>> client.userbase.search_users(query = '...')

# Search for groups
>>> client.userbase.search_groups(schools = [...])

# ----- Exercises app ----- #

# Get all exercises
>>> exs = client.exercises.get()

# Get exercise data
>>> e = exs[0]
>>> e.owner
>>> e.date.created
>>> e.date.modified
>>> e.date.submited
>>> e.result.score
>>> e.result.comment
>>> e.corrected
>>> e.archived # etc.
```

## TODO

More apps
