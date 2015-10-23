"""
Script to deal with co-workers constantly @mentionig you in a HipChat room.

Grabs the last 5 messages in a room and checks for any @mentions; if you are mentioned, choose and send a response accordingly.
"""
import json
import time
import random
import requests

__author__ = "Mark Judice"
__email__ = "mark.judice@praetorian.com"

base = ''
token = ''
room_id = 4
response_pool = None

# Get token
with open('token.key', 'r') as infile:
    token = infile.read().splitlines()[0]

# Get base URL
with open('hostname.key', 'r') as infile:
    base = infile.read().splitlines()[0]

# Get responses
with open('responses.key', 'r') as infile:
    response_pool = infile.read().splitlines()

def send_response():
    response = random.choice(response_pool)
    post_body = json.dumps({'message' : response})
    headers = {'content-type' : 'application/json',
            'Authorization' : "Bearer {}".format(token) 
            }
    r = requests.post("{}v2/room/{}/message?auth_token={}".format(base, room_id, token), headers=headers, data=post_body)
    print(r.json())
    time.sleep(random.randint(2,5))



old_msg_ids = []

while True:
    r = requests.get("{}v2/room/{}/history/latest?max-results=5&auth_token={}".format(base, room_id, token))
    messages = r.json()['items']
    with open('juice_parser.json', 'w') as outfile:
        outfile.write(json.dumps(messages))
    # print(json.dumps(messages))
    for msg in messages:
        if msg['mentions'] != []:
            for mention in msg['mentions']:
                if mention['name'] == 'Mark Judice':
                    if msg['id'] not in old_msg_ids:
                        # print(msg['message'])
                        send_response()
                    old_msg_ids.append(msg['id'])


    print('\n---\n')
    time.sleep(random.randint(5,12)) # Random sleep before responses

