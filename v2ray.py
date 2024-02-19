import json
import base64

def generate_vmess_protocol(server_address, server_port, user_id, user_traffic, user_duration_days, xui_panel_port):
    config = {
        "v": "2",
        "ps": "new_user",
        "add": server_address,
        "port": server_port,
        "id": user_id,
        "aid": "2",
        "net": "tcp",
        "type": "none",
        "host": "",
        "path": "",
        "tls": "",
        "sni": "",
        "remarks": "",
        "tolerance": ""
    }

    if user_traffic > 0:
        config['path'] = f"stats/{user_traffic}mi"

    expires_at = (datetime.datetime.utcnow() + datetime.timedelta(days=user_duration_days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    config['tolerance'] = expires_at

    vmess_json = json.dumps(config, separators=(',', ':'))
    vmess_base64 = base64.urlsafe_b64encode(vmess_json.encode()).decode()

    return f"vmess://{vmess_base64}?xui=127.0.0.1:{xui_panel_port}"

if __name__ == "__main__":
    import datetime

    server_address = "89.44.243.89"
    server_port = 5122
    user_id = "sina5"  # You should generate a random UUID for user ID
    user_traffic = 1  # 1GB
    user_duration_days = 36
    xui_panel_port = 2053

    vmess_protocol = generate_vmess_protocol(server_address, server_port, user_id, user_traffic, user_duration_days, xui_panel_port)
    print(vmess_protocol)
