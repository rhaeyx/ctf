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
        print('result', result)
    except Exception as e:
        print(e)
        result = str(e)

    return jsonify({"output": result}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, debug=False)
