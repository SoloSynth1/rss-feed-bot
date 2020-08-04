HELP_TEXT = '''
Currently supported commands are:
`add`: Subscribe a RSS feed. Type in `@{bot-name} add {rss-feed} {name}`, for example, `@Bot add https://www.reddit.com/r/news/.rss Reddit News`.
`list`: List active subscriptions. Type in `@{bot-name} list`.
`remove`: Remove subscription. Type in `@{bot-name} remove {name}` ,for example, `@Bot remove Reddit News`.'''

WELCOME_TEXT = '''I am RSS Feed Bot. Give me a RSS feed URL, and I will push the feed to this conversation!'''

DO_NOT_UNDERSTNAD_TEXT = "Sorry, I do not understand what you are saying."

ADDED_TO_DM_TEXT = '''Thanks for adding me to a DM, {}!👋'''

ADDED_TO_ROOM_TEXT = '''Thanks for adding me to {}, {}!👋'''

UNKNOWN_SITUATION_TEXT = '''You are not supposed to be able to see this message.😰 This probably means this bot has ran into errors.
Please kindly report this situation to our developers, thank you so much!'''

EXECUTION_ERROR_TEXT = """Sorry, error occurred when trying to execute the command.
Please kindly report this situation to our developers, thank you so much!"""

SUBSCRIPTION_CREATION_TEXT = '''Subscription "{}" created.'''

SUBSCRIPTION_REMOVAL_TEXT = '''Subscription "{}" removed.'''

SUBSCRIPTION_LIST_TEXT = """Here are the active subscriptions:"""

SUBSCRIPTION_NO_ITEM_TEXT = """This conversation currently does not have any subscriptions."""

SUBSCRIPTION_ITEM_TEXT = 'Item #{}. "{}"({}), created by {} at {}'

SUBSCRIPTION_NAME_NOT_FOUND_TEXT = '''Sorry, I cannot find a subscription named "{}" in this conversation.'''


def get_thread_id(event_data):
    return event_data['message']['thread']


def unknown_command(event_data):
    response = {
        "text": "\n".join([DO_NOT_UNDERSTNAD_TEXT, HELP_TEXT]),
        "thread": get_thread_id(event_data)
    }
    return response


def welcome(event_data):
    space = event_data['space']
    sender_name = event_data['user']['displayName']
    if space['type'] == 'ROOM':
        thankyou_text = ADDED_TO_ROOM_TEXT.format(space['displayName'], sender_name)
    elif space['type'] == 'DM':
        thankyou_text = ADDED_TO_DM_TEXT.format(sender_name)
    else:
        # Unknown space type
        thankyou_text = UNKNOWN_SITUATION_TEXT
    response = {
        "text": "\n".join([thankyou_text, WELCOME_TEXT, HELP_TEXT]),
    }
    return response


def error(event_data):
    response = {
        "text": EXECUTION_ERROR_TEXT,
        "thread": get_thread_id(event_data)
    }
    return response


def subscription_created(event_data, name):
    response = {
        "text": SUBSCRIPTION_CREATION_TEXT.format(name),
        "thread": get_thread_id(event_data)
    }
    return response


def subscription_removed(event_data, name):
    response = {
        "text": SUBSCRIPTION_REMOVAL_TEXT.format(name),
        "thread": get_thread_id(event_data)
    }
    return response


def subscription_name_not_found(event_data, name):
    response = {
        "text": SUBSCRIPTION_NAME_NOT_FOUND_TEXT.format(name),
        "thread": get_thread_id(event_data)
    }
    return response


def subscription_list(event_data, subscriptions):
    if subscriptions:
        items = [SUBSCRIPTION_ITEM_TEXT.format(i+1, subscription['name'], subscription['feed'], subscription['creator'],
                                               subscription['timestamp']) for i, subscription in enumerate(subscriptions)]
        response = {
            "text": "\n".join([SUBSCRIPTION_LIST_TEXT]+items),
            "thread": get_thread_id(event_data)
        }
    else:
        response = {
            "text": SUBSCRIPTION_NO_ITEM_TEXT,
            "thread": get_thread_id(event_data)
        }
    return response
