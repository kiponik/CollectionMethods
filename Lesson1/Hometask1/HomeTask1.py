import requests
import json

user_id = 'kiponik'
x = requests.get('https://api.github.com/users/' + user_id + '/repos')
print(x.status_code)

with open('repo.json', 'w') as json_file:
    json.dump(x.text, json_file)