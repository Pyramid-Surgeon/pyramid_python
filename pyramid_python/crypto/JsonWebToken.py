from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from typing import List, Dict
from gmpy2 import mpz, gcd, c_div
from functools import reduce
import base64
import random


"""
Major way this differs from the one used in the Union CTF is the use of mpz. Stolen with love from
https://github.com/silentsignal/rsa_sign2n/blob/release/standalone/jwt_forgery.py
"""


class Token:
    def __init__(self, tokens: List[str], exponent: List[int] = [3, 65567], verbose: bool = False) -> None:
        # Error catching
        assert tokens is not None
        for e in exponent:
            assert e % 2 != 0

        # Setup prerequisites for key_from_sig
        self.token_list = {}
        self.exponent = exponent
        self.verbose = verbose
        # Get bit-length
        self.k = len(base64.urlsafe_b64decode(tokens[0].split('.')[2] + "==="))
        for token in tokens:
            self.prepare_token(token)

    """
    Calculates the message signature pairs required for key_from_sig
    """
    def prepare_token(self, token: str) -> None:
        token_elements = token.split('.')
        checksum = SHA256.new(
            str(token_elements[0] + '.' + token_elements[1]).encode('ascii')
                              )
        padded_checksum = pkcs1_15._EMSA_PKCS1_V1_5_ENCODE(checksum, self.k).hex()
        signature = (base64.urlsafe_b64decode(token_elements[2] + "===")).hex()
        self.token_list[padded_checksum] = signature

    def key_from_sig(self) -> (int, int):
        """
        gcd(c1**e - m1, c2**e - m2, cn**e - mn) as described in:
        https://crypto.stackexchange.com/questions/30289/is-it-possible-to-recover-an-rsa-modulus-from-its-signatures/30301#30301
        And expanded on in:
        https://crypto.stackexchange.com/questions/33642/given-enough-rsa-signature-values-is-it-possible-to-determine-the-public-key-va
        """
        # Check if signature lengths match.
        if len({len(i) for i in self.token_list}) != 1:
            Exception("Token signatures are not all the same length!")

        for e in self.exponent:
            ti = []
            for checksum in self.token_list:
                ti.append(pow(mpz(int(self.token_list[checksum], 16)), mpz(e)) - mpz(int(checksum, 16)))
            N = reduce(lambda x, y: gcd(x, y), ti)
            # If the N is too short, say 1 or 2, this cannot be correct.
            if N.bit_length() > 100:
                checksum = random.choice(list(self.token_list))
                for i in range(1, 100):
                    # Verify N
                    if pow(int(self.token_list[checksum], 16), e, c_div(N, mpz(i))) == int(checksum, 16):
                        n = int(c_div(N, mpz(i)))
                        return e, n
        return None, None
