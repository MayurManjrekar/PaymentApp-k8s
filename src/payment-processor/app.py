from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    return jsonify({"status": "processed"})

@app.route('/health')
def health():
    return "OK"

@app.route('/metrics')
def metrics():
    return "requests_total 1"

app.run(host='0.0.0.0', port=8080)