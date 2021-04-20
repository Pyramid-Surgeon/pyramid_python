from pyramid_python.crypto.arnault import *


def test_arnault():
    """
    Test if resulting composite number passes the Miller Rabin test.
    """
    primes = Arnault([2, 3, 5, 7, 11]).perform()
    composite = 1
    for p in primes:
        composite *= p
    assert miller_rabin(composite, [2, 3, 5, 7, 11])


def miller_rabin(n, b):
    """
    Miller Rabin test.
    """
    basis = b
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
