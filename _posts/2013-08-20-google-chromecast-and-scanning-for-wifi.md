---
layout: post
title: Google Chromecast and scanning for WiFi Networks
date: '2013-08-20'
author: jtdub
tags:
- Miscellaneous Hacking
- Google
- Wireshark
- Network Sniffing
- Online Privacy
- packetgeek.net
---

I've been playing around with the Google Chromecast this evening. One of the things that I've just run across is that it appears to periodically scan for wifi networks. I'll write more soon, but this is what I've found so far.

```bash
POST /setup/scan_wifi HTTP/1.1
Host: 10.10.10.10:8008
User-Agent: ChromecastApp/1.1.0.321 
Content-Length: 0
Accept: */*
Origin: https://www.google.com
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: keep-alive

HTTP/1.1 200 OK
Access-Control-Allow-Headers: Content-Type
Cache-Control: no-cache
Access-Control-Allow-Origin: https://www.google.com
Content-Length: 0

GET /setup/scan_results HTTP/1.1
Host: 10.10.10.10:8008
User-Agent: ChromecastApp/1.1.0.321 
Accept: */*
Origin: https://www.google.com
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: keep-alive

HTTP/1.1 200 OK
Access-Control-Allow-Headers: Content-Type
Cache-Control: no-cache
Access-Control-Allow-Origin: https://www.google.com
Content-Type: application/json
Content-Length: 674

[{"bssid":"APBSSID1","signal_level":-20,"ssid":"APSSID1","wpa_auth":7,"wpa_cipher":4,"wpa_id":0},{"bssid":"APBSSID2","signal_level":-63,"ssid":"APSSID2","wpa_auth":7,"wpa_cipher":4},{"bssid":"APBSSID3","signal_level":-66,"ssid":"APSSID3","wpa_auth":7,"wpa_cipher":4},{"bssid":"APBSSID4","signal_level":-68,"ssid":"APSSID4","wpa_auth":7,"wpa_cipher":4},{"bssid":"APBSSID5","signal_level":-68,"ssid":"APSSID5","wpa_auth":5,"wpa_cipher":3},{"bssid":"APBSSID6","signal_level":-69,"ssid":"APSSID6","wpa_auth":7,"wpa_cipher":4},{"bssid":"APBSSID7","signal_level":-67,"ssid":"APSSID7","wpa_auth":1,"wpa_cipher":1}]
```

I sanitized the IP Address of the Chromecast, the BSSID's and the SSID's of the access points that the Chromecast found.
