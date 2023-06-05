# BT SpeedChecker
 
# Description:
Simple python script to poll the bt router (bthomehub.home) and pull out the followiing data:

|timestamp|               time of capture|
|uploadSpeed|            from http://bthomehub.home/nonAuth/wan_conn.xml|
|downloadSpeed|           from http://bthomehub.home/nonAuth/wan_conn.xml|
|systemUptime|            from http://bthomehub.home/nonAuth/wan_conn.xml|
|status|                  from http://bthomehub.home/nonAuth/wan_conn.xml|   
|state|                   state, UP / DOWN from http://bthomehub.home/cgi/cgi_basicStatus.js|
|mode|                    DSL protocol from http://bthomehub.home/cgi/cgi_basicStatus.js|
|mod_type|                modulation type from http://bthomehub.home/cgi/cgi_basicStatus.js|       
|snr_margin_down|         If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9] - from http://bthomehub.home/cgi/cgi_basicStatus.js|
|snr_margin_up|           If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9]
                        from http://bthomehub.home/cgi/cgi_basicStatus.js|
|latn_down|               ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|latn_up|                 ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|satn_down|               Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js|
|satn_up|                 Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js|
|output_power_down|       ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|output_power_up|         ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|rate_down|               ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|rate_up|                 ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|attainable_rate_down|    best rate download? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|attainable_rate_up|      best rate upload? from http://bthomehub.home/cgi/cgi_basicStatus.js|
|chantype|                ??? from http://bthomehub.home/cgi/cgi_basicStatus.js|

# How?
Run the speedchecker.py script and a csv will be created or appended to. Assumption that your router is findable usin bthomehub.hom

# Why?
I've got 150Mbps stay fast guarantee with BT, I don't think I've ever come near to that, hopefully this is a way of checking. 

# Configuration
## My configuration:
Raspberry Pi
 - nginx webserver hosting https://github.com/c-lake/csv-charts
 - crontab running speedchecker.py every 5 minutes
