import simplejson as json
import urllib
from telegram_utils.string import to_utf8


def search_results(query_text):
    query = urllib.urlencode({'q': to_utf8(query_text)})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    return data['results']