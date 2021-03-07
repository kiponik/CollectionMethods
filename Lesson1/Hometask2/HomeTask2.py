import requests
from pprint import pprint

client_id = "58efa175549cbbe34857"
client_secret = "a70cc1472f395ffe456b64b6ab018644"
concrete_params = {
    "client_id": client_id,
    "client_secret": client_secret
}
base_url = "https://api.artsy.net/api/tokens/xapp_token"

r = requests.post(base_url, params=concrete_params)
pprint(r.text)

headers = {
    "X-XAPP-Token": r.json()['token']
}

url = "https://api.artsy.net/api/sales"
r = requests.get(url, headers=headers)
pprint(r.json())

if r.ok:
    import json
    path = "sales.json"
    with open(path, "w") as f:
        json.dump(r.json(), f)