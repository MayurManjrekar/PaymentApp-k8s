import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
PROCESSOR_URL = os.getenv("PAYMENT_PROCESSOR_URL")

@app.route('/pay', methods=['POST'])
def pay():
    res = requests.post(f"{PROCESSOR_URL}/process", json=request.json)
    return jsonify(res.json())

@app.route('/health')
def health():
    return "OK"

@app.route('/metrics')
def metrics():
    return "requests_total 1"

app.run(host='0.0.0.0', port=8080)