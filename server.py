from flask import Flask, request
import json
import requests
import random
import time

app = Flask(__name__)

DATAFILE = '/home/viruslobster/dishesbot/people.json'
BOT_ID = '2108dd3097acb1cc379b4b5945'

messages = [
    '@%s, time to do the dishes!',
    'aye @%s, do the dishes!'
]

with open(DATAFILE, 'r') as f:
    data = json.load(f)

def get_message():
    i = random.randint(0,len(messages)-1)
    return messages[i]

def get_dish_washer():
    i = data['next_washer']
    return data['people'][i]

def increment_washer():
    data['next_washer'] = (data['next_washer'] + 1) % len(data['people'])


@app.route('/groupme', methods=['POST'])
def groupme_callback():
    req = request.get_json()
    print(req)

    if "dishesbot" in req['text'].lower():
        time.sleep(1)
        washer = get_dish_washer()
        msg = get_message() % washer['name']
        request_data = {
            'bot_id': BOT_ID,
            'text': msg,
            'attachments': [
                {
                    'type': 'mentions',
                    'loci': [
                        [msg.find("@"), len(washer["name"])+1]
                    ],
                    'user_ids': [
                        washer['userid']
                    ]
                }
            ]
        }
        print(request_data)

        requests.post("https://api.groupme.com/v3/bots/post", json=request_data)

        increment_washer()

        with open(DATAFILE, 'w') as f:
            json.dump(data, f)
    return ''
    

@app.route('/')
def main():
    i = data['next_washer']
    return data['people'][i]

