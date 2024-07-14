from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import os
import json
from helpers import *
import logging
import post_handlers
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RESOURCE_DIR = os.path.join(DIRECTORY, '..', 'resource')
PORT = int(os.getenv('PORT', '8080'))

user_data = {}

app = Flask(__name__)

@app.route('/v1/api/get_sstoken', methods=['POST'])
def api_get_sstoken():
    request_data = request.get_json()
    response_data = post_handlers.get_sstoken(request_data, user_data)
    return jsonify(response_data)

@app.route('/v1/api/get_user_info', methods=['POST'])
def api_get_user_info():
    request_data = request.get_json()
    response_data = post_handlers.get_user_info(request_data, user_data)
    return jsonify(response_data)

@app.route('/v1/api/change_balance', methods=['POST'])
def api_change_balance():
    request_data = request.get_json()
    response_data = post_handlers.change_balance(request_data, user_data)
    return jsonify(response_data)

@app.route('/')
def serve_index():
    return send_from_directory(RESOURCE_DIR, 'index.html')

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(RESOURCE_DIR, 'favicon.png')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(RESOURCE_DIR, filename)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('serve_index'))

if __name__ == "__main__":
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=PORT, _quiet=False)
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
