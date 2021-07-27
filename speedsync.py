#!/usr/bin/python3
import requests, re, csv, os.path, time
url = 'http://192.168.1.254/cgi/cgi_basicStatus.js'
data = requests.get(url)

try:
    data.raise_for_status()
    print('Page Downloaded')
except Exception as exc:
    print('There was a problem: %s' % (exc))

# https://stackoverflow.com/questions/47515137/extracting-data-from-javascript-var-inside-script-with-python
linestatus = re.search('var linestatus = (.+)[,;]{1}', data.text).group(1) # extract line status

# regex to extract the values from linestatus
# group 1 matches any word character 1 or more times
# group 2 mathces any char 1 or more times
lsRegex = re.compile(r"(\w+):'(.+?)'")
lsItems = lsRegex.findall(linestatus)
lsKey = []
lsValue = []
for x in range(len(lsItems)):
    lsKey.append(lsItems[x][0]) # line status headers from .js
    lsValue.append(lsItems[x][1]) # line status values from .js


time = time.strftime('%d-%m-%Y %H:%M:%S') # assigns time to use in csv when adding values
file_exists = os.path.isfile('syncresults.csv')
with open('syncresults.csv', "a") as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists: # check if file exists
        writer.writerow(['time'] + lsKey) # add header to csv file if file doesn't exist
    writer.writerow([time] + lsValue) # add time and values to csv file




