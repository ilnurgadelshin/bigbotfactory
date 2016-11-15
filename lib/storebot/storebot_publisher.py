import requests
import simplejson as json
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot


def bot_published(bot_handler, cookie):
    url = "https://storebot.me/api/bots/check?id=%s" % bot_handler.get_me().username
    headers = {'Cookie': cookie}
    try:
        response = requests.post(url=url, headers=headers, timeout=2.0, verify=False)
        if response.status_code not in [200, 404, 406, 409]:
            # 404 - not found
            # 406 - not acceptable (it is yours and published)
            # 409 - already published (not yours)
            # 200 - ok
            BBFAlarmBot.alarm_developers("Something went wrong during checking bot in the storebot.me: "
                                         "status_code=" + str(response.status_code) + ", error message=" + response.text)
            return None
    except:
        return None  # show nothing in case of exception
    return response.status_code == 409 or response.status_code == 406


def publish_bot(bot_handler, cookie, languages, category):
    url = "https://storebot.me/add"
    headers = {'Cookie': cookie}
    params = dict()
    params["link"] = bot_handler.get_me().username
    params["name"] = bot_handler.get_me().first_name if bot_handler.get_me().first_name is not None else params["link"]
    params["categoryId"] = category
    params["languages"] = languages
    description = 'Created via @bbfbot \n' + bot_handler.about_bot
    params["description"] = description[:299]
    params["token"] = bot_handler.api_handler.get_token()
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers, timeout=3.0, verify=False)
        if response.status_code != 200:
            BBFAlarmBot.alarm_developers("Something went wrong during publishing bot to the storebot.me: "
                                         "status_code=" + str(response.status_code) + ", error message=" + response.text)
        return response.status_code == 200
    except:
        return False