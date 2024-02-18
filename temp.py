import json

def generate_vless_config(server_ip, user_id, port=443, flow="xtls-rprx-direct", path="/path"):
    config = {
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": server_ip,
                            "port": port,
                            "users": [
                                {
                                    "id": user_id,
                                    "security": "auto"
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": "ws",
                    "wsSettings": {
                        "path": path
                    }
                }
            }
        ]
    }
    return config

def save_config(config, filename):
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

# Example usage
server_ip = "89.44.243.89"
user_id = "sina2"  # You can generate a unique user ID
vless_config = generate_vless_config(server_ip, user_id)

save_config(vless_config, "sina2_vless.json")
