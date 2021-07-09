#!/usr/bin/python3
import requests, re
url = 'http://192.168.1.254/cgi/cgi_basicStatus.js'
data = requests.get(url)

try:
    data.raise_for_status()
    print('Page Downloaded')
except Exception as exc:
    print('There was a problem: %s' % (exc))

# https://stackoverflow.com/questions/47515137/extracting-data-from-javascript-var-inside-script-with-python
linestatus = re.search('var linestatus = (.+)[,;]{1}', data.text).group(1)

lsRegex = re.compile(r"(\w+):'(.+?)'")
lsItems = lsRegex.findall(linestatus)

for x in range(len(lsItems)):
    print(lsItems[x][0] + " : " + lsItems[x][1])