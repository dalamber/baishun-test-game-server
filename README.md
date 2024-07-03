# How to use

1. Clone the repository
2. Rename the `.env.example` file to `.env`
3. Run the app using Docker
```bash
docker-compose up --build --detach
```

# Baishun API Documentation

## Get SSToken for a user
#### Powershell
```powershell
curl -Method POST -Uri https://baishun.badsantos.com/v1/api/get_sstoken -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ", "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
```
#### Bash
```bash
curl -X POST https://baishun.badsantos.com/v1/api/get_sstoken \
-H "Content-Type: application/json" \
-d '{"app_id":21397507, "user_id":"id1001", "code":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ", "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}'
```

## Get user info
#### Powershell
```powershell
curl -Method POST -Uri https://baishun.badsantos.com/v1/api/get_user_info -ContentType "application/json" -Body '{"app_id":21397507, "user_id":"id1001", "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "client_ip":"110.86.1.130", "game_id":1010, "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}' | Select-Object -Expand Content
```
#### Bash
```bash
curl -X POST https://baishun.badsantos.com/v1/api/get_user_info \
-H "Content-Type: application/json" \
-d '{"app_id":21397507, "user_id":"id1001", "ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "client_ip":"110.86.1.130", "game_id":1010, "signature":"c62d04ebdb5100e475f45f5ebe8c64ee", "signature_nonce":"5f0eb04d7603a9d8", "timestamp":1682674598}'
```

## Decrement coins balance
#### Powershell
```powershell
curl -Method POST -Uri https://baishun.badsantos.com/v1/api/change_balance -ContentType "application/json" -Body '{"app_id":21397507,"user_id":"id1001","ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9","currency_diff":-100,"game_id":1006,"room_id":"room_123","game_round_id":"rlmy01pq-cqkdd39jyrmz","order_id":"2R5PHkx43UQPQydCrmI71BVqXwH","change_time_at":1638845715,"diff_msg":"bet","signature":"c62d04ebdb5100e475f45f5ebe8c64ee","signature_nonce":"5f0eb04d7603a9d8","timestamp":1682674598}' | Select-Object -Expand Content
```
#### Bash
```bash 
curl -X POST https://baishun.badsantos.com/v1/api/change_balance \
-H "Content-Type: application/json" \
-d '{"app_id":21397507,"user_id":"id1001","ss_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9","currency_diff":-100,"game_id":1006,"room_id":"room_123","game_round_id":"rlmy01pq-cqkdd39jyrmz","order_id":"2R5PHkx43UQPQydCrmI71BVqXwH","change_time_at":1638845715,"diff_msg":"bet","signature":"c62d04ebdb5100e475f45f5ebe8c64ee","signature_nonce":"5f0eb04d7603a9d8","timestamp":1682674598}'
```
