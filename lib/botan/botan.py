import requests
import simplejson as json


def track(botan_token, chat_id, message_json, name='Message'):
    url_template = 'https://api.botan.io/track?token=#token#&uid=#uid#&name=#name#'
    url = url_template.replace('#token#', str(botan_token)).replace('#uid#', str(chat_id)).replace('#name#', name)
    headers = {'Content-type': 'application/json'}
    try:
        requests.post(url, data=json.dumps(message_json), headers=headers, timeout=1.0)
    except requests.exceptions.Timeout:
        # set up for a retry, or continue in a retry loop
        return False
    except requests.exceptions.RequestException as e:
        # catastrophic error
        print e
        return False
    return True

