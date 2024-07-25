from helpers import *

def get_sstoken(request_data, user_data):
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

    is_signature_valid = validate_signature(request_data['signature'], request_data['signature_nonce'], app_secret_key(), request_data['timestamp'])
    # fail request if signature is invalid


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
            'user_avatar': 'https://baishun.badsantos.com/default_userpic.png',
            'balance': random.randint(10000, 20000)
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
    return response

def update_sstoken(request_data, user_data):
    # EXAMPLE REQUEST DATA FROM DOCS
    # {
    #     "app_id":21397507,
    #     "user_id":"id1001",
    #     "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    #     "signature":"c62d04ebdb5100e475f45f5ebe8c64ee",
    #     "signature_nonce":"5f0eb04d7603a9d8",
    #     "timestamp":1682674598
    # }
    # EXAMPLE RESPONSE DATA FROM DOCS
    # {
    #     "code": 0,
    #     "message": "succeed",
    #     "unique_id": "1603289541785956352",
    #     "data": {
    #     "ss_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"， //updated ss_token
    #     "expire_date": 1671096189000 //Expiration timestamp, milliseconds
    # }
    is_signature_valid = validate_signature(request_data['signature'], request_data['signature_nonce'], app_secret_key(), request_data['timestamp'])
    # fail request if signature is invalid

    current_timestamp_unix_time_ms = int(time.time() * 1000)

    token = generate_ss_token()
    expire = current_timestamp_unix_time_ms + 86400000 * 30 # in 30 days
    user_data[request_data['user_id']]['ss_token'] = token
    user_data[request_data['user_id']]['ss_token_expire'] = expire

    response = {
                "code": 0,
                "message": "succeed",
                "unique_id": str(current_timestamp_unix_time_ms) + os.urandom(8).hex(),
                "data" : {
                    "ss_token": token,
                    "expire_date": expire
                }
            }
    return response



def get_user_info(request_data, user_data):
    # EXAMPLE REQUEST DATA FROM DOCS
    # req:
    # {
    # "app_id":21397507,
    # "user_id":"id1001",
    # "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    # "client_ip":"110.86.1.130",
    # "game_id":1010,
    # "signature":"c62d04ebdb5100e475f45f5ebe8c64ee",
    # "signature_nonce":"5f0eb04d7603a9d8",
    # "timestamp":1682674598
    # }
    #
    # # EXAMPLE RESPONSE DATA FROM DOCS
    # rsp:
    # {
    # "code": 0,
    # "message": "succeed",
    # "unique_id": "1603289980002643968",
    # "data": {
    # "user_id": "id1001",
    # "user_name": "tom",
    # "user_avatar": "avatar.com",
    # "balance":1000
    # }


    is_signature_valid = validate_signature(request_data['signature'], request_data['signature_nonce'], app_secret_key(), request_data['timestamp'])
    # fail request if signature is invalid


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
            'user_avatar': 'https://baishun.badsantos.com/default_userpic.png',
            'balance': random.randint(10000, 20000)
            }

    response = {
                "code": 0,
                "message": "succeed",
                "unique_id": str(current_timestamp_unix_time_ms) + os.urandom(8).hex(),
                "data" : {
                    "user_id": request_data['user_id'],
                    "user_name" : user_data[request_data['user_id']].get('user_name', ''),
                    "user_avatar" : user_data[request_data['user_id']].get('user_avatar', ''),
                    "balance" : user_data[request_data['user_id']].get('balance', 0)
                }
            }
    return response

def change_balance(request_data, user_data):
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

    is_signature_valid = validate_signature(request_data['signature'], request_data['signature_nonce'], app_secret_key(), request_data['timestamp'])
    # fail request if signature is invalid

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
                "currency_balance": user_info.get('balance', 0)
            }
        }
    return response
