import urllib.request as lib
import json
webURL = lib.urlopen("https://api.nasa.gov/planetary/apod?date=2017-03-31&api_key=DEMO_KEY")
contents = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
x = json.loads(contents.decode(encoding))
print(x['url'])
