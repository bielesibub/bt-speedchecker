"""
Author: bielesibub
Date  : 03/06/2023

Description:
Simple python script to poll the bt router (bthomehub.home) and pull out the followiing data:

timestamp               time of capture
uploadSpeed             from http://bthomehub.home/nonAuth/wan_conn.xml
downloadSpeed           from http://bthomehub.home/nonAuth/wan_conn.xml
systemUptime            from http://bthomehub.home/nonAuth/wan_conn.xml
status                  from http://bthomehub.home/nonAuth/wan_conn.xml    
state                   state, UP / DOWN from http://bthomehub.home/cgi/cgi_basicStatus.js
mode                    DSL protocol from http://bthomehub.home/cgi/cgi_basicStatus.js
mod_type                modulation type from http://bthomehub.home/cgi/cgi_basicStatus.js       
snr_margin_down         If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9]
                        from http://bthomehub.home/cgi/cgi_basicStatus.js
snr_margin_up           If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9]
                        from http://bthomehub.home/cgi/cgi_basicStatus.js
latn_down               ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
latn_up                 ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
satn_down               Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js
satn_up                 Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js
output_power_down       ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
output_power_up         ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
rate_down               ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
rate_up                 ??? from http://bthomehub.home/cgi/cgi_basicStatus.js
attainable_rate_down    best rate download? from http://bthomehub.home/cgi/cgi_basicStatus.js
attainable_rate_up      best rate upload? from http://bthomehub.home/cgi/cgi_basicStatus.js
chantype                ??? from http://bthomehub.home/cgi/cgi_basicStatus.js

Why?:
I've got 150Mbps stay fast guarantee with BT, I don't think I've ever come near to that, hopefully this is a way of checking.

"""

import requests
import os
import datetime
import xml.etree.ElementTree as ET
import json
import re
from urllib.parse import unquote

from bs4 import BeautifulSoup

# referer is the only important part here, the rest have been kept just in case
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
simple_status    = simple_status_re.findall(basic_status_js.content.decode('utf-8'))
# top and tail the response and change ' to "
simple_status    = simple_status[0].lstrip('[').rstrip(',').replace("'",'"')

# https://stackoverflow.com/questions/48524894/dynamically-double-quote-keys-in-text-to-form-valid-json-string-in-python
simple_status      = re.sub('(\w+)\s?:\s?("?[^",]+"?,?)', "\"\g<1>\":\g<2>", simple_status)
simple_status_dict = json.loads( simple_status )

fw_ver         = re.findall( r'var fw_ver="(.*)";', basic_status_js.content.decode('utf-8'))
serial_no      = re.findall( r'var serial_no="(.*)";', basic_status_js.content.decode('utf-8'))
fw_update_time = re.findall( r"var fw_update_time='(.*)';", basic_status_js.content.decode('utf-8'))
lan_service_ip = re.findall( r'var lan_service_ip="(.*)";', basic_status_js.content.decode('utf-8'))

simple_status_dict['fw_ver']         = unquote( fw_ver[0] )
simple_status_dict['serial_no']      = unquote( serial_no[0] )
simple_status_dict['fw_update_time'] = unquote( fw_update_time[0] )
simple_status_dict['lan_service_ip'] = unquote( lan_service_ip[0] )

current_status_dict = {}
current_status_dict['timestamp'] = now


if status_page_xml.status_code == 200:
    status_page     = ET.fromstring(status_page_xml.content)
    status_rate_arr = status_page.findall( ".//status_rate")[0].get("value")
    sysuptime       = status_page.findall( ".//sysuptime")[0].get("value")

    status_rate_arr = status_rate_arr.replace('[', '').replace(']','').replace(' ','').replace("'",'').split(',')

    current_status_dict['uploadSpeed']   = status_rate_arr[1].split('%3B')[0]
    current_status_dict['downloadSpeed'] = status_rate_arr[1].split('%3B')[1]
    current_status_dict['systemUptime']  = sysuptime

    current_status_dict['status'] = status_page.findall( ".//link_status")[0].get("value").split('%3B')[0]

    for key, value in simple_status_dict.items():
        current_status_dict[key] = value

else:

    current_status_dict['uploadSpeed']   = '0'
    current_status_dict['downloadSpeed'] = '0'
    current_status_dict['systemUptime']  = '0'

    current_status_dict['status'] = f'unavailable response code {status_page_xml.status_code}'

    for key, value in simple_status_dict.items():
        current_status_dict[key] = value

keys = []
values = []

# if output file doesn't exist, create it with header
if not output_csv_exists:
    with open(output_csv, 'w') as output_csv_file:

        for key, value in current_status_dict.items():
            keys.append( key )
            values.append( value )
 
        output_csv_file.write(",".join( keys ) + '\n')
        output_csv_file.write(",".join( values ) + '\n')

# if output file does exist, append the latest data
else:
    with open(output_csv, 'a') as output_csv_file:
        for key, value in current_status_dict.items():
            values.append( value )

        output_csv_file.write(",".join( values ) + '\n')

          
       


