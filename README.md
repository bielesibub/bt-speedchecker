# BT Broadband SpeedChecker

# Why?
I've got 150Mbps stay fast guarantee with BT (and I pay a premium for this) I don't think I've ever come close to that actual speed. I raised an issue with BT at the end of May 2023, they seemed surprised that I was questioning the real speed of my connection. Do BT really check that my connection is what I am paying for? If they do, why haven't I heard from them when it's not hit the mark? if not, why should it be **MY** responsibility to let them know it's slow? I hope that this is a way for me or anyone else to be able to check themselves.

Hopefully this might be useful to someone else out there.

I've trawled through the status objects and made the assumption that the *attainable_rate_down* and *attainable_rate_up* are the speeds that I should be looking at for the up/down speeds. **BT engineer confirmed this yesterday 6th June 2023

# Description
Simple python script to poll the bt router (bthomehub.home) and pull out the following data, from wan_conn.xml and cgi_basicStatus.js:

| Field | Description |
| :--- | :--- |
| timestamp | time of capture |
| uploadSpeed | from http://bthomehub.home/nonAuth/wan_conn.xml |
| downloadSpeed | from http://bthomehub.home/nonAuth/wan_conn.xml |
| systemUptime | from http://bthomehub.home/nonAuth/wan_conn.xml |
| status | from http://bthomehub.home/nonAuth/wan_conn.xml |   
| state | state, UP / DOWN from http://bthomehub.home/cgi/cgi_basicStatus.js |
| mode | DSL protocol from http://bthomehub.home/cgi/cgi_basicStatus.js |
| mod_type | modulation type from http://bthomehub.home/cgi/cgi_basicStatus.js |       
| snr_margin_down | If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9] - pulled from http://bthomehub.home/cgi/cgi_basicStatus.js |
| snr_margin_up | If SNR Margin is lower than 10dB or Line Attenuation higher than 45dB, your line quality is poor and may suffer from Internet dropping. In this condition, please contact your ISP to check your line quality. [https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjd4dGesqr_AhVGUcAKHcEVAXAQFnoECBIQAw&url=https%3A%2F%2Fwww.tp-link.com%2Fno%2Fsupport%2Ffaq%2F546%2F%23%3A~%3Atext%3DIf%2520SNR%2520Margin%2520is%2520lower%2Cto%2520check%2520your%2520line%2520quality.&usg=AOvVaw2mWeSuzI-ZhtdBl6h4biR9] - pulled from http://bthomehub.home/cgi/cgi_basicStatus.js |
| latn_down | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| latn_up | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| satn_down | Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js |
| satn_up | Signal Attenuation from http://bthomehub.home/cgi/cgi_basicStatus.js |
| output_power_down | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| output_power_up | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| rate_down | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| rate_up | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| attainable_rate_down | best rate download? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| attainable_rate_up | best rate upload? from http://bthomehub.home/cgi/cgi_basicStatus.js |
| chantype | ??? from http://bthomehub.home/cgi/cgi_basicStatus.js |

# How?
Run the speedchecker.py script and a csv will be created or appended to. Assumption that your router is findable using http://bthomehub.home

# Configuration
## My configuration:
Raspberry Pi with:
 - nginx webserver hosting https://github.com/c-lake/csv-charts
   - I load the csv from a network share into this page when I want to check the stats.
 - crontab running speedchecker.py every 5 minutes

### Example chart:
![Example speed chart](https://github.com/bielesibub/bt-speedchecker/blob/main/support/bt-speedchecker.png)

# Who am I?
I am a bored, medically retired, IT consultant. #UTV
