# -*- coding: utf-8 -*-

from telegram.objects.telegram_response import TelegramResponse
from telegram_utils.string import to_utf8
import requests
import traceback


class TelegramConnector(object):
    @classmethod
    def _encoded_dict(cls, in_dict):
        out_dict = {}
        for k, v in in_dict.iteritems():
            out_dict[k] = to_utf8(v)
        return out_dict

    @classmethod
    def make_request(cls, token, function_name, params=None, files_dict=None, timeout=None):
        # params must be a dict of str -> str
        url = 'https://api.telegram.org/bot%s/%s' % (token, function_name)
        if params is not None:
            params = cls._encoded_dict(params)
        try:
            html_response = requests.post(url, data=params, files=files_dict, verify=True, timeout=timeout)
        except Exception:
            return TelegramResponse(ok=False, description=traceback.format_exc(),
                                    error_code=TelegramResponse.ERROR_CODE_EXCEPTION)
        return TelegramResponse.gen_from_json(html_response.json())
