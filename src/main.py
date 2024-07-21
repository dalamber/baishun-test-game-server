from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import os
import json
from helpers import *
import logging
import post_handlers
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RESOURCE_DIR = os.path.join(DIRECTORY, '..', 'resource')
PORT = int(os.getenv('PORT', '8080'))

user_data = {}
logs = []

def add_logs(str):
    logs.append(str)
    if len(logs) > 1000:
        logs.pop(0)

app = Flask(__name__)

@app.before_request
def log_request_info():
    if request.method == 'POST':
        str = ''
        try:
            app.logger.debug('Request Path: %s', request.path)
            app.logger.debug('Request Headers: %s', request.headers)
            app.logger.debug('Request Body: %s', request.get_data())

            str = f'Current time:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>Request Path: {request.path}<br>Request Headers: {request.headers}<br>Request Body: {request.get_data()}<br>'
        except Exception as e:
            app.logger.error('Error logging request info: %s', e)
            str = f"Error logging request info: {e}<br>"
        add_logs(str)
        add_logs('-----------------------------------<br>')

@app.after_request
def log_response_info(response):
    if request.method == 'POST':
        str = ''
        try:
            app.logger.debug('Response Status: %s', response.status)
            app.logger.debug('Response Headers: %s', response.headers)
            app.logger.debug('Response Body: %s', response.get_data())

            str = f'Current time:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>Response Status: {response.status}<br>Response Headers: {response.headers}<br>Response Body: {response.get_data()}'
        except Exception as e:
            app.logger.error('Error logging response info: %s', e)
            str = f"Error logging response info: {e}<br>"
        add_logs(str)
        add_logs('-----------------------------------<br>')

    return response

@app.route('/v1/api/get_sstoken', methods=['POST'])
def api_get_sstoken():
    request_data = request.get_json()
    response_data = post_handlers.get_sstoken(request_data, user_data)
    return jsonify(response_data)

#https://baishun.badsantos.com/v1/api/update_sstoken
@app.route('/v1/api/update_sstoken', methods=['POST'])
def api_update_sstoken():
    request_data = request.get_json()
    response_data = post_handlers.update_sstoken(request_data, user_data)
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

@app.route('/logs')
def serve_logs():
    return '<br><br>'.join(logs)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('serve_index'))

if __name__ == "__main__":
    try:
        CORS(app)
        from waitress import serve
        serve(app, host="0.0.0.0", port=PORT, _quiet=False)
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
