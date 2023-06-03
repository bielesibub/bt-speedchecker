import requests
import os
import datetime
import xml.etree.ElementTree as ET
import json
import re

from bs4 import BeautifulSoup

"""
curl 'http://bthomehub.home/nonAuth/ajax.js' \
-X 'GET' \
-H 'Cookie: logout=not; urn=1393433039ba30d0' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Host: bthomehub.home' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15' \
-H 'Accept-Language: en-GB,en;q=0.9' \
-H 'Referer: http://bthomehub.home/basic_-_status.htm' \
-H 'Connection: keep-alive'

curl 'http://bthomehub.home/nonAuth/wan_conn.xml' \
-X 'GET' \
-H 'Referer: http://bthomehub.home/basic_-_status.htm' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Host: bthomehub.home' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15' \
-H 'Accept-Language: en-GB,en;q=0.9' \

-H 'Connection: keep-alive'
-H 'Cookie: logout=not; urn=1393433039ba30d0' \
"""
request_headers = { "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                    "Host": "bthomehub.home",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Referer": "http://bthomehub.home/basic_-_status.htm",
                    "Connection": "keep-alive",
                    "Cookie": "'Cookie: logout=not; urn=1393433039ba30d0" }
# connect to the hub, scrape data, push data to a csv
output_csv = os.path.join(os.getcwd(), "btspeed.csv")

#get current time stamp
now = datetime.datetime.now().isoformat()

#if output file doesn't exist, create it
output_csv_exists = os.path.isfile(output_csv)

status_page_xml = requests.get('http://bthomehub.home/nonAuth/wan_conn.xml', headers=request_headers)

basic_status_js = requests.get('http://bthomehub.home/cgi/cgi_basicStatus.js', headers=request_headers)

simple_status_re = re.compile('var linestatus = (.*)') #var linestatus = (.*?);')

simple_status = simple_status_re.findall(basic_status_js.content.decode('utf-8'))
# top and tail the response
simple_status = simple_status[0].lstrip('[').rstrip(',').replace("'",'"')
simple_status = re.sub('(\w+)\s?:\s?("?[^",]+"?,?)', "\"\g<1>\":\g<2>", simple_status)

simple_status_dict = json.loads( simple_status )
print( simple_status_dict )

#basic_status_js = BeautifulSoup(basic_status_js.content, 'html.parser')
#status_page_html = requests.get('http://bthomehub.home/basic_-_status.htm')
#status_page_html = BeautifulSoup(status_page_html.content, 'html.parser')
#print(status_page_html.prettify())
current_status_dict = {}
current_status_dict['timestamp'] = now


if status_page_xml.status_code == 200:
    status_page = ET.fromstring(status_page_xml.content)
    # sed -r '/wan_conn_volume_list/{N;s/.*\[.//;s/[^0-9]\],$//;s/%3B/ /g;s/^[0-9]+ ([0-9]+) ([0-9]+)$/\1 \2/g;p};d'
    status_rate_arr = status_page.findall( ".//status_rate")[0].get("value")
    sysuptime = status_page.findall( ".//sysuptime")[0].get("value")
    # returns [['0%3B0%3B0%3B0'], ['49141000%3B107853000%3B0%3B0'], ['0%3B0%3B0%3B0'], null

    status_rate_arr = status_rate_arr.replace('[', '').replace(']','').replace(' ','').replace("'",'').split(',')


    # #broadband, #FirmwareVersion, #FirmwareUpdated, #SerialNumber, #NetworkUptime, #SystemUptime, #BTWiFi
    # #Upstream
    
    #current_status_dict['statusRateArr'] = status_rate_arr[1].split('%3B')
    current_status_dict['uploadSpeed'] = status_rate_arr[1].split('%3B')[0] #status_page.find("p", {"id": "Upstream"})
    current_status_dict['downloadSpeed'] = status_rate_arr[1].split('%3B')[1] #status_page.find("p", {"id": "Upstream"})
    current_status_dict['systemUptime'] = sysuptime

    current_status_dict['status'] = status_page.findall( ".//link_status")[0].get("value").split('%3B')[0]

    for key, value in simple_status_dict.items():
        current_status_dict[key] = value
    #current_status_dict['statusArr'] = status_page.findall( ".//link_status")[0].get("value").split('%3B')
else:

    current_status_dict['uploadSpeed'] = '0'
    current_status_dict['downloadSpeed'] = '0'
    current_status_dict['systemUptime'] = '0'

    current_status_dict['status'] = f'unavailable response code {status_page_xml.status_code}'

    for key, value in simple_status_dict.items():
        current_status_dict[key] = value

"""

current_status_dict['broadband'] = status_page.select('#broadband')[0].text
current_status_dict['firmware'] = status_page.select('#FirmwareVersion')[0].text
current_status_dict['firmwareUpdated'] = status_page.select('#FirmwareUpdated')[0].text
current_status_dict['serialNumber'] = status_page.select('#SerialNumber')[0].text
current_status_dict['networkUptime'] = status_page.select('#NetworkUptime')[0].text
current_status_dict['systemUptime'] = status_page.select('#SystemUptime')[0].text
current_status_dict['btWifi'] = status_page.select('#BTWiFi')[0].text
"""
keys = []
values = []

if not output_csv_exists:
    with open(output_csv, 'w') as output_csv_file:

        for key, value in current_status_dict.items():
            keys.append( key )
            values.append( value )
 
        output_csv_file.write(",".join( keys ) + '\n')
        output_csv_file.write(",".join( values ) + '\n')


else:
    with open(output_csv, 'a') as output_csv_file:
        for key, value in current_status_dict.items():
            values.append( value )

        output_csv_file.write(",".join( values ) + '\n')

          
       


