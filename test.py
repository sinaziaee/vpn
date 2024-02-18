from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

def generate_certificate_authority():
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create a CA certificate
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'OpenVPN CA'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'OpenVPN CA'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.utcnow())
    builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(private_key.public_key())
    # builder = builder.add_extension(
    #     extension=x509.BasicConstraints(ca=True, path_length=None),
    #     critical=True,
    # )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )

    # Sign the certificate with its own private key
    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    # Write the CA certificate and private key to files
    with open("ca_certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))
    with open("ca_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def generate_client_certificate(username):
    # Generate a private key for the client
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create a Certificate Signing Request (CSR)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, username),
    ])).sign(private_key, hashes.SHA256(), default_backend())

    # Load the CA private key
    with open("ca_private_key.pem", "rb") as f:
        ca_private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    # Load the CA certificate
    with open("ca_certificate.pem", "rb") as f:
        ca_certificate = x509.load_pem_x509_certificate(f.read(), default_backend())

    # Sign the CSR with the CA private key to create the client certificate
    client_certificate = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_certificate.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True
        )
        .sign(private_key=ca_private_key, algorithm=hashes.SHA256(), backend=default_backend())
    )

    # Write the client certificate and private key to files
    with open(f"{username}_certificate.pem", "wb") as f:
        f.write(client_certificate.public_bytes(encoding=serialization.Encoding.PEM))
    with open(f"{username}_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def generate_ovpn_file(username, server_ip, output_file):
    # OpenVPN configuration template
    config_template = """
    client
    dev tun
    proto udp
    remote {server_ip} 1194
    resolv-retry infinite
    nobind
    user nobody
    group nogroup
    persist-key
    persist-tun
    remote-cert-tls server
    cipher AES-256-CBC
    verb 3
    auth-nocache
    key-direction 1
    <ca>
    -----BEGIN CERTIFICATE-----
    Insert CA certificate here
    -----END CERTIFICATE-----
    </ca>
    <cert>
    -----BEGIN CERTIFICATE-----
    Insert client certificate here
    -----END CERTIFICATE-----
    </cert>
    <key>
    -----BEGIN PRIVATE KEY-----
    Insert client private key here
    -----END PRIVATE KEY-----
    </key>
    """

    # Load client certificate and private key
    with open(f"{username}_certificate.pem", "rb") as f:
        client_certificate = f.read()
    with open(f"{username}_private_key.pem", "rb") as f:
        client_private_key = f.read()

    # Replace placeholders with actual values
    config_data = config_template.format(server_ip=server_ip)
    config_data = config_data.replace("Insert CA certificate here", client_certificate.decode())
    config_data = config_data.replace("Insert client certificate here", client_certificate.decode())
    config_data = config_data.replace("Insert client private key here", client_private_key.decode())

    # Write configuration data to the output file
    with open(output_file, 'w') as f:
        f.write(config_data)

    print(f"OpenVPN configuration file for {username} has been generated: {output_file}")

# Generate CA certificate and private key
generate_certificate_authority()

# Generate client certificate and private key for sina2
username = "sina2"
generate_client_certificate(username)

# Generate OpenVPN configuration file for sina2
server_ip = "89.44.243.89"
output_file = f"{username}.ovpn"
generate_ovpn_file(username, server_ip, output_file)
