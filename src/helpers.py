import random, os, hashlib, time

def app_secret_key():
    return os.getenv('APP_SECRET_KEY')

def generate_signature(signature_nonce, app_key, timestamp):
    data = f"{signature_nonce}{app_key}{timestamp}"
    h = hashlib.md5()
    h.update(data.encode('utf-8'))
    return h.hexdigest()

def generate_signature_nonce():
    return os.urandom(8).hex()

def generate_ss_token():
    return os.urandom(16).hex()

def validate_signature(signature, signature_nonce, app_key, timestamp):
    expected = generate_signature(signature_nonce, app_key, timestamp)
    return signature == expected

def get_random_user_name():
    names = ['Tom', 'Jerry', 'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi',
             'Ivan', 'Jack', 'Karl', 'Linda', 'Mike', 'Nancy', 'Oliver', 'Peter', 'Quincy', 'Rachel',
             'Steve', 'Tina', 'Ursula', 'Victor', 'Wendy', 'Xander', 'Yvonne', 'Zack']
    
    return random.choice(names) + '_' + time.strftime("%H%M%S")
