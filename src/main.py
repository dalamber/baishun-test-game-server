import http.server
import socketserver
import json

from helpers import *
from dotenv import load_dotenv
import time
import os
import random
import logging

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
PORT = int(os.getenv('PORT', '8080'))

user_data = {}

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        print(f"Received GET request on path: {self.path} and host {self.headers['Host']}")
        # Serve the random image API endpoint
        resource_path = os.path.join(DIRECTORY, '..', 'resource', self.path.lstrip('/'))
        if os.path.exists(resource_path) and os.path.isfile(resource_path):
            self.serve_file(resource_path)
        else:
            self.send_error(404, "File not found")

    def serve_file(self, path):
        content_type = self.guess_type(path)
        with open(path, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(f.read())

    def guess_type(self, path):
        ext = os.path.splitext(path)[1]
        if ext == '.html':
            return 'text/html'
        elif ext == '.css':
            return 'text/css'
        elif ext == '.js':
            return 'application/javascript'
        elif ext == '.json':
            return 'application/json'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.jpg' or ext == '.jpeg':
            return 'image/jpeg'
        elif ext == '.webp':
            return 'image/webp'
        elif ext == '.ico':
            return 'image/x-icon'
        else:
            return 'application/octet-stream'

            
    def do_POST(self):
        print(f"Received POST request on path: {self.path} and host {self.headers['Host']}")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)
        response_data = {}

        if self.path == "/v1/api/get_sstoken":
            response_data = get_sstoken(self, request_data)
        elif self.path == '/v1/api/get_user_info':
            response_data = get_user_info(self, request_data)
        elif self.path == '/v1/api/change_balance':
            response_data = change_balance(self, request_data)
        else:
            response_data = {
                "code": 200,
                "message": "OK - But nothing to do here."
            }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

        print(f"Received POST request on path: {self.path} with data: {request_data} and response: {response_data}")

    def serve_favicon(self):
        favicon_path = os.path.join(DIRECTORY, 'favicon.png')
        if os.path.exists(favicon_path):
            with open(favicon_path, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.end_headers()
                self.wfile.write(f.read())
        
def get_sstoken(handler: SimpleHTTPRequestHandler, request_data: dict):
    # EXAMPLE REQUEST DATA FROM DOCS
    # {
    #     "app_id":21397507,
    #     "user_id":"id1001",
    #     "code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ" ,
    #     "signature":"c62d04ebdb5100e475f45f5ebe8c64ee",
    #     "signature_nonce":"5f0eb04d7603a9d8",
    #     "timestamp":1682674598
    # }

    # EXAMPLE RESPONSE DATA FROM DOCS
    # {
    #     "code": 0,
    #     "message": "succeed",
    #     "unique_id": "1682674739807011000",
    #     "data": {
    #         "ss_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    #         "expire_date": 1671096189000
    #     }
    # }

    validate_signature(request_data['signature'], request_data['signature_nonce'], APP_SECRET_KEY, request_data['timestamp'])

    global user_data

    current_timestamp_unix_time_ms = int(time.time() * 1000)

    token = ''
    expire = ''

    if request_data['user_id'] in user_data:
        token = user_data[request_data['user_id']].get('ss_token')
        expire = user_data[request_data['user_id']].get('ss_token_expire')
    else:
        token = generate_ss_token()
        expire = current_timestamp_unix_time_ms + 86400000 * 30 # in 30 days
        user_data[request_data['user_id']] = { 
            'ss_token': token, 
            'ss_token_expire' : expire,
            'user_name': get_random_user_name(),
            'user_avatar': 'Unknown',
            'balance': random.randint(100, 1000)
            }

    response = {
                "code": 0,
                "message": "succeed",
                "unique_id": str(current_timestamp_unix_time_ms) + os.urandom(8).hex(),
                "data" : {
                    "ss_token": token,
                    "expire_date": expire
                }
            }
    print(user_data)
    return response

def get_user_info(handler: SimpleHTTPRequestHandler, request_data: dict):
    # EXAMPLE REQUEST DATA FROM DOCS
    # {
    #     "app_id":21397507,
    #     "user_id":"id1001",
    #     "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    #     "client_ip":"110.86.1.130",
    #     "game_id":1010,
    #     "signature":"c62d04ebdb5100e475f45f5ebe8c64ee",
    #     "signature_nonce":"5f0eb04d7603a9d8",
    #     "timestamp":1682674598
    # }
    # 
    # EXAMPLE RESPONSE DATA FROM DOCS
    # {
    #     "code": 0,
    #     "message": "succeed",
    #     "unique_id": "1603289980002643968",
    #     "data": {
    #         "user_id": "id1001",
    #         "user_name": "tom",
    #         "user_avatar": "avatar.com",
    #         "balance":1000
    #     }
    # }
    validate_signature(request_data['signature'], request_data['signature_nonce'], APP_SECRET_KEY, request_data['timestamp'])

    global user_data

    if request_data['user_id'] in user_data:
        user_info = user_data[request_data['user_id']]
        response = {
            "code": 0,
            "message": "succeed",
            "unique_id": str(int(time.time() * 1000)) + os.urandom(8).hex(),
            "data": {
                "user_id": request_data['user_id'],
                "user_name": user_info.get('user_name', 'Unknown'),
                "user_avatar": user_info.get('user_avatar', 'Unknown'),
                "balance": user_info.get('balance', 0)
            }
        }
        return response

    pass


def change_balance(handler: SimpleHTTPRequestHandler, request_data: dict):
    # EXAMPLE REQUEST DATA FROM DOCS
    # {
    #     "app_id":21397507,
    #     "user_id":"id1001",
    #     "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    #     "currency_diff": -100,
    #     "game_id":1006,
    #     "room_id":"room_123",
    #     "game_round_id": "rlmy01pq-cqkdd39jyrmz",
    #     "order_id":"2R5PHkx43UQPQydCrmI71BVqXwH",
    #     "change_time_at":1638845715,
    #     "diff_msg":"bet",
    #     "signature":"c62d04ebdb5100e475f45f5ebe8c64ee",
    #     "signature_nonce":"5f0eb04d7603a9d8",
    #     "timestamp":1682674598
    # }
    # 
    # EXAMPLE RESPONSE DATA FROM DOCS
    # {
    #     "code": 0,
    #     "message": "succeed",
    #     "unique_id": "1603289541785956352",
    #     "data": {
    #     "currency_balance": 900 //total remaining value
    # }

    validate_signature(request_data['signature'], request_data['signature_nonce'], APP_SECRET_KEY, request_data['timestamp'])

    global user_data

    if request_data['user_id'] in user_data:
        user_info = user_data[request_data['user_id']]
        
        current_balance = user_info.get('balance', 0)
        diff = request_data['currency_diff']
        code = 0 if current_balance + diff >= 0 else 1008
        if code == 0:
            user_info['balance'] = current_balance + diff
            
        response = {
            "code": code,
            "message": "succeed",
            "unique_id": str(int(time.time() * 1000)) + os.urandom(8).hex(),
            "data": {
                "balance": user_info.get('balance', 0)
            }
        }
        return response

    pass
  
if __name__ == "__main__":
    try:
        httpd = socketserver.TCPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        httpd.server_close()
        print("Server has been shut down.")




# curl -Method POST -Uri http://localhost/v1/api/get_sstoken -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ", "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
# curl -Method POST -Uri http://localhost/v1/api/get_user_info -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "client_ip":"110.86.1.130", "game_id":1010, "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
# curl -Method POST -Uri http://localhost/v1/api/change_balance -ContentType "application/json" -Body '{"app_id":21397507,"user_id":"id1001","ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9","currency_diff":-100,"game_id":1006,"room_id":"room_123","game_round_id":"rlmy01pq-cqkdd39jyrmz","order_id":"2R5PHkx43UQPQydCrmI71BVqXwH","change_time_at":1638845715,"diff_msg":"bet","signature":"c62d04ebdb5100e475f45f5ebe8c64ee","signature_nonce":"5f0eb04d7603a9d8","timestamp":1682674598}' | Select-Object -Expand Content

# curl -Method POST -Uri https://badsantos.com/v1/api/get_sstoken -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ", "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
# curl -Method POST -Uri https://badsantos.com/v1/api/get_user_info -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "client_ip":"110.86.1.130", "game_id":1010, "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
# curl -Method POST -Uri https://badsantos.com/v1/api/change_balance -ContentType "application/json" -Body '{"app_id":21397507,"user_id":"id1001","ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9","currency_diff":-100,"game_id":1006,"room_id":"room_123","game_round_id":"rlmy01pq-cqkdd39jyrmz","order_id":"2R5PHkx43UQPQydCrmI71BVqXwH","change_time_at":1638845715,"diff_msg":"bet","signature":"c62d04ebdb5100e475f45f5ebe8c64ee","signature_nonce":"5f0eb04d7603a9d8","timestamp":1682674598}' | Select-Object -Expand Content
