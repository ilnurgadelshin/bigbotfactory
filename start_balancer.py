from optparse import OptionParser

import tornado.httpserver
import tornado.ioloop
import tornado.web

import boto3
import simplejson as json

from lib.throttling.throttle_banner import ThrottleBanner
from telegram.objects.update import TelegramUpdate
from telegram.api.core.bbf_alarm_bot import BBFAlarmBot
from lib.globals.globals import GlobalParams


class BotAPIHandler(tornado.web.RequestHandler):
    CLIENT = boto3.client('lambda')

    @tornado.web.asynchronous
    def post(self, api_version, bot_handler, token, bot_name):
        bot_name = bot_name if bot_name else ""
        response_str = api_version + " " + bot_handler + " " + token + " " + bot_name
        update_str = self.request.body
        update = TelegramUpdate.gen_from_json_str(update_str)
        if update.message is None:
            #  we currently don't support inline queries
            self.finish()
            return
        if not update.message.has_non_empty_content():
            self.finish()
            return

        if update and update.message and THROTTLE_BANNER.ban_period:
            chat_id = update.message.chat.id
            response_str += " user" + " " + str(chat_id)
            if THROTTLE_BANNER.can_perform_request(chat_id):
                message = json.dumps({
                    'token': token,
                    'bot_handler': bot_handler,
                    'update_str': update_str,
                    GlobalParams.API_VERSION_PARAM: api_version,
                })

                self.CLIENT.invoke(
                    FunctionName='incoming_message' + '__' + api_version,
                    InvocationType='Event',
                    LogType='None',
                    Payload=message,
                )
            else:
                response_str += " " + "is banned"
        print response_str
        self.set_status(200)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/bots/(?P<api_version>[^\/]+)/(?P<bot_handler>[^\/]+)/(?P<token>[^\/]+)/?(?P<bot_name>[^\/]+)?", BotAPIHandler),
        ]

        settings = dict(
            debug=False,
            autoreload=True
        )
        BBFAlarmBot.alarm_developers('Balancer is getting started...')
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    parser = OptionParser()
    parser.add_option("-p", "--port", help="port", type="int", default=8080)
    parser.add_option("-r", "--max-user-rps", help="max possible rps for user", type="int", default=5)
    parser.add_option("-b", "--ban-period", help="period of time (in seconds) for ban", type="int", default=86400)
    (options, args) = parser.parse_args()

    global THROTTLE_BANNER
    THROTTLE_BANNER = ThrottleBanner(options.max_user_rps, options.ban_period)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
