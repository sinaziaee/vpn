from v2ray import V2Ray
v2ray = V2Ray('89.44.243.89', '5432', 'session_token')
result = v2ray.create_account('vmess', 'My V2Ray Account', 10, 30)
if result:
    print(result)
else:
    print('Failed to create account')