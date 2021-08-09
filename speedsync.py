#!/usr/bin/python3
import requests
import re
import csv
import os
import sys
import time

os.chdir(sys.path[0]) # set working directory to save csv when run as cron job
url = 'http://192.168.1.254/cgi/cgi_basicStatus.js'
data = requests.get(url)

# Extract Line Status from BT HomeHub
linestatus = re.search('var linestatus = (.+)[,;]{1}', data.text).group(1) # extract line status
# https://stackoverflow.com/questions/47515137/extracting-data-from-javascript-var-inside-script-with-python
lsRegex = re.compile(r"(\w+):'(.+?)'")

# regex to extract the values from linestatus
# group 1 (key) matches any word character one or more times
# group 2 (value) mathces any char one or more times

lsItems = lsRegex.findall(linestatus)
lsKey = []
lsValue = []
for x in range(len(lsItems)):
    lsKey.append(lsItems[x][0]) # buld list of line status keys from .js
    lsValue.append(lsItems[x][1]) # buld list of line status values from .js


# regex to extract the values from the wan_link_rate_list - group 4 contains upload/download rates used under Status page.
wanRateLinkRate = re.search("(var wan_link_rate_list=\[\[')(.+)('],\n\[')(.+)('],\n\[')(.+)'", data.text).group(4) # extract WAN rate list
wanRateLinkRateList = wanRateLinkRate.split("%3B") # index 0 = Upload Rate and index 1 = Download Rate
wanRateLinkRateList = wanRateLinkRateList[:2] # keeps index 0 and 1

# Build CSV file
time = time.strftime('%d-%m-%Y %H:%M:%S') # assigns time to use in csv when adding values
file_exists = os.path.isfile('syncresults.csv')
with open('syncresults.csv', "a") as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists: # check if file exists
        writer.writerow(['time', 'upload rate', 'download rate'] + lsKey) # add header to csv file if file doesn't exist
    writer.writerow([time] + wanRateLinkRateList + lsValue) # add time and values to csv file




