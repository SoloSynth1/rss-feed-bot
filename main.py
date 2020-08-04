import google.auth
from googleapiclient.discovery import build
from flask import Flask, request, json

import responses
import subscriptions


PORT = 8080
HOST = "0.0.0.0"
SCOPES = ['https://www.googleapis.com/auth/chat.bot']

credentials, project_id = google.auth.default()
credentials = credentials.with_scopes(scopes=SCOPES)
chat = build('chat', 'v1', credentials=credentials)

app = Flask(__name__)


@ app.route('/', methods=['POST'])
def home_post():

    event_data = request.get_json()
    event_type = event_data['type']
    resp = {}

    try:
        if event_type == 'REMOVED_FROM_SPACE':
            print("event is REMOVED_FROM_SPACE")
            subscriptions.delete_all(event_data['space']['name'])
            return json.jsonify({})     # no need to respond

        elif event_type == 'ADDED_TO_SPACE':
            print("event is ADDED_TO_SPACE")
            resp = responses.welcome(event_data)

        elif event_type == 'MESSAGE':
            print("event is MESSAGE")
            print("message: {}".format(event_data['message']))
            if 'text' in event_data['message']:
                resp = parse_command(event_data)

        # fail-over case when resp is empty
        if not resp:
            resp = responses.unknown_command(event_data)

    except Exception as e:
        resp = responses.error(event_data)

    return json.jsonify(resp)


def parse_command(event_data):
    try:
        resp = {}
        message = event_data['message']
        print(message)
        parts = message['argumentText'].strip().split(" ", 1)  # check first word
        print(parts)
        space = event_data['space']['name']

        command = parts[0].lower()
        if command == "add":
            url, name = parts[1].split(" ", 1)
            url = url.lower()
            creator = event_data['user']['email']
            timestamp = event_data['eventTime']
            subscription_id = subscriptions.create(space, url, name, creator, timestamp)
            if subscription_id:
                resp = responses.subscription_created(event_data, name)
        elif command == "list":
            items = subscriptions.list_all(space)
            resp = responses.subscription_list(event_data, items)
        elif command == "remove":
            name = parts[1].strip(" ")
            subscription_id = subscriptions.remove_by_name(space, name)
            if subscription_id:
                resp = responses.subscription_removed(event_data, name)
            else:
                resp = responses.subscription_name_not_found(event_data, name)
        return resp
    except:
        return {}


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
