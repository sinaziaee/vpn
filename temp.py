import requests
import json

class V2RayAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, protocol, username, days_limit, transfer_rate_limit):
        url = f"{self.base_url}/xui/inbound/add"
        headers = {'Content-Type': 'application/json'}
        data = {
            'protocol': protocol,
            'username': username,
            'days_limit': days_limit,
            'transfer_rate_limit': transfer_rate_limit
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

# Example usage
v2ray_api = V2RayAPI('http://localhost:8080')
result = v2ray_api.create_user('vmess', 'my_username', 30, '1MB/s')
print(result)
