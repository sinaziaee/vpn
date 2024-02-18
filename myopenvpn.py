import os
import subprocess

def create_openvpn_config(config_name, client_ip, server_ip, port):
    # Define the path where you want to save the OpenVPN configuration files
    config_dir = '/root/'

    # Create the directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Define the content of the OpenVPN configuration file
    config_content = f"""
    # OpenVPN client configuration
    client
    dev tun
    proto udp
    remote {server_ip} {port}
    resolv-retry infinite
    nobind
    persist-key
    persist-tun
    remote-cert-tls server
    cipher AES-256-CBC
    auth SHA256
    verb 3
    <ca>
    # Contents of your ca.crt file here
    </ca>
    <cert>
    # Contents of your client.crt file here
    </cert>
    <key>
    # Contents of your client.key file here
    </key>
    """

    # Write the configuration content to a new file
    config_file_path = os.path.join(config_dir, f'{config_name}.conf')
    with open(config_file_path, 'w') as f:
        f.write(config_content)

    # Return the path to the created config file
    return config_file_path

# Example usage
config_name = 'client1'
client_ip = '89.44.243.89'  # Change this to the desired client IP address
server_ip = '89.44.243.89'  # Change this to your server's IP address
port = 1194  # Change this to the desired port

config_file_path = create_openvpn_config(config_name, client_ip, server_ip, port)
print(f"OpenVPN config file created at: {config_file_path}")
