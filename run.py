from flask import Flask, render_template, jsonify
import threading
import requests
import time

app = Flask(__name__)

fans_count = 0
#此处自行添加修改uid
uid = 'UID'
uid_name = ''

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

def get_uid_name():
    global uid_name
    response_card=requests.get(f'https://api.vc.bilibili.com/account/v1/user/cards?uids={uid}',headers=headers)
    card=response_card.json()
    uid_name=card['data'][0]['name']

def get_fans_count():
    global fans_count
    while True:
        response = requests.get(f'https://api.bilibili.com/x/relation/stat?vmid={uid}',headers=headers)
        data = response.json()
        fans_count = data['data']['follower']
        time.sleep(5)

threading.Thread(target=get_fans_count).start()

@app.route('/')
def index():
    return render_template('fans.html', uid_name=uid_name)

@app.route('/update')
def update():
    return jsonify(fans_count=fans_count)

if __name__ == '__main__':
    get_uid_name()
    app.run(debug=True)
