import codecs, grpc, os, sys

sys.path.append(".")
sys.path.append("./lnd_deps")
from lnd_deps import walletunlocker_pb2 as lnrpc
from lnd_deps import walletunlocker_pb2_grpc as walletunlockerstub

os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
cert = open(os.path.expanduser("{lndir}/tls.cert"), "rb").read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel("localhost:10009", ssl_creds)
stub = walletunlockerstub.WalletUnlockerStub(channel)
pw = b"{pw}"
r = lnrpc.UnlockWalletRequest(wallet_password=pw)
response = stub.UnlockWallet(r)
print(response)
