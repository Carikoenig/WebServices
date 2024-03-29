## channel.py - a channel detecting the input language
##

from flask import Flask, request, render_template, jsonify
import json
import requests
import datetime
import random
from googletrans import LANGUAGES
from googletrans import Translator
import traceback

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

# Create Flask app
app = Flask(__name__, static_folder='css', static_url_path='/static')
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

HUB_URL: 'https://temporary-server.de'
SERVER_AUTHKEY = 'Crr-K3d-2N'
CHANNEL_AUTHKEY = '3344556'
CHANNEL_NAME = "Translation-Channel"
CHANNEL_ENDPOINT = "http://localhost:5003"
CHANNEL_FILE = 'messages.json'

@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
            "name": CHANNEL_NAME,
            "endpoint": CHANNEL_ENDPOINT,
            "authkey": CHANNEL_AUTHKEY}))

    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        return

def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name':CHANNEL_NAME}),  200

# GET: Return list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400
    # fetch channels from server
    return jsonify(read_messages())

# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    # fetch channels from server
    # check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400
    # add message to messages
    messages = read_messages()
    messages.insert(0, {'content':message['content'], 'sender':message['sender'], 'timestamp':message['timestamp'],  'channel_origin': 'translation-channel'})
    # add Bot answer message
    # LANGCODES = dict(map(reversed, LANGUAGES.items()))
    translator = Translator()
    print('LAGUAGES keys()', list(LANGUAGES.keys()))
    random_lang = random.choice(list(LANGUAGES.keys()))
    print('random_lang', random_lang)
    user_message = str(message.get('content', '')) 
    lang_from = translator.detect(user_message).lang
    print('lang_from', lang_from)
    translated_text = translator.translate(user_message, src='auto', dest = random_lang).text
    
    messages.insert(0, {'content':'Here is a translation from ' + LANGUAGES[lang_from] + ' into ' + LANGUAGES[random_lang] + ' : ' + str(translated_text), 'sender': 'TransBot', 'timestamp':datetime.datetime.now().isoformat(),  'channel_origin': 'translation-channel'})
    save_messages(messages) 
    return "OK", 200

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()
    return messages

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)


@app.errorhandler(500)
def internal_error(exception):
   return "<pre>"+traceback.format_exc()+"</pre>"

# Start development web server
if __name__ == '__main__':
    app.run(port=5003, debug=True)
