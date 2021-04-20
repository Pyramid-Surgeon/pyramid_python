from pyramid_python.crypto.JsonWebToken import Token
from Crypto.PublicKey import RSA
import random
import jwt

# TODO: There is some bug when e = 65537. Need to look into it
def test_pubkey_from_sig():
    """
    Test if resulting public key is correct.
    """
    lengths = [1024, 2048]
    exponents = [3, 65537]
    length = random.choice(lengths)
    e = random.choice(exponents)
    key = RSA.generate(length, e=e).export_key('PEM')
    tokens = []
    for _ in range(5):
        tokens.append(jwt.encode({"number": random.randint(0, 1000)}, key, algorithm="RS256"))
    e, n = Token(tokens).key_from_sig()
    assert n == RSA.importKey(key).n
    assert e == RSA.importKey(key).e
