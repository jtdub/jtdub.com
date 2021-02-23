#!/usr/bin/env python3

import os
import time


expire = os.getenv("EXPIRE")
subject = os.getenv("SUBJECT")
domain = os.getenv("DOMAIN")


def create_cert(expire, subject, domain, path="/opt/sslbot/etc/ssl"):
    return os.system(
        f"openssl req -x509 -newkey rsa:4096 -days {expire} -nodes -subj {subject} -keyout {path}/private/{domain}.key -out {path}/certs/{domain}.pem"
    )


while True:
    create_cert(expire, subject, domain)
    time.sleep(int(expire) * 86400)
