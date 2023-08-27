import requests as req
import json

url = 'https://webbackend.cdsc.com.np/api/meroShare/capital/'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

res = req.get(url=url, headers=headers)

if res.status_code == 200:
    json_object = json.dumps(res.json())
    with open('capitals.json', 'w') as file:
        file.write(json_object)
        print('Check capitals.json file in your directory!')