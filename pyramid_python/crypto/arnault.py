from functools import reduce
from typing import List, Dict
from math import gcd
import random


class Arnault:
    """
    Solver class that attempts to find strong pseudoprimes to the miller-rabin test according to the method presented by F. Arnault in https://www.sciencedirect.com/science/article/pii/S0747717185710425.
    """
    def __init__(self, base_list: List[int]) -> None:
        # if h % 2 == 0:
        #  raise ValueError('h must be odd.')
        self.base_list = base_list
        self.h = 3
        """
        h != 3 is currently unsupported, we cannot imagine a situation in which a different h is required, see remark 2.3 in the aforementioned paper for implementation instructions. 
        """

    def legendre(self, a: int, p: int) -> int:
        """
        Calculates the Legendre Symbol of a and prime p.
        """
        if p % a == 0:
            return 0
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    def egcd(self, a: int, b: int) -> (int, int, int):
        """
        Extended Euclidean Algorithm on a and b.
        """
        if a == 0:
            return b, 0, 1
        g, x1, y1 = self.egcd(b%a, a)
        x = y1 - (b//a) * x1
        y = x1
        return g, x, y

    def solve_single(self, p1: (int, int), p2: (int, int)) -> (int, int):
        """
        Solve two congruences using the EUA.
        """
        g, x, y = self.egcd(p1[0], p2[0])
        l = (p1[1] - p2[1]) // g
        s = p1[1] - p1[0] * x * l
        assert p1[0]*x*l + p2[0]*y*l == p1[1]-p2[1]
        return self.lcm(p1[0], p2[0]), s % self.lcm(p1[0], p2[0])

    def solve(self, n: List[int], a: List[int]) -> (int, int):
        """
        Repeatedly solve pairs of congruences.
        """
        return reduce(self.solve_single, zip(n, a))

    def lcm(self, x: int, y: int) -> int:
        """
        Lowest common multiple of x and y.
        """
        return x * y // gcd(x, y)

    def random_z(self, S_a: List[List[int]]) -> List[int]:
        """
        Randomly select z_a from each set.
        """
        return [random.choice(s) for s in S_a]

    def fermat_test(self, p: int, k: int = 100) -> bool:
        """
        Runs a fermat primality test.
        """
        for _ in range(k):
            a = random.randint(2, p-2)
            if gcd(a, p) != 1:
                return False
            if pow(a, p-1, p) != 1:
                return False
        return True  # Probably prime.

    def find_sets(self) -> (Dict[int, List[int]], List[int]):
        """
        Tries k values until all sets are non-empty.
        """
        while True:
            Sa = {}
            k = []
            k_temp = list(set(self.generate_primes(self.base_list[-1] * 4)) - set(self.base_list))
            for _ in range(self.h-1):
                prime_temp = k_temp[random.randint(0, len(k_temp) - 1)]
                k.append(prime_temp)
                k_temp.remove(prime_temp)  # Prevent duplicates.

            for base in self.base_list:
                base_set = set()
                for potential_prime in self.generate_primes((10*self.h+1)*base)[1:]: #wtf?
                    if self.legendre(base, potential_prime) == -1:
                        prime_to_add = potential_prime % (4*base)
                        if prime_to_add % 2 != 0:
                            base_set.add(potential_prime % (4*base))
                new_set = base_set
                for ki in k:
                    k_inv = pow(ki, -1, 4*base)
                    temp_set = set([(k_inv * (a + ki - 1)) % (4*base) for a in base_set])
                    new_set = new_set.intersection(temp_set)
                if len(new_set) == 0:
                    break
                if len(Sa) == 0 and len(new_set) == 1: # Small heuristic, lowers chances of failure significantly.
                    break
                Sa[base] = sorted(new_set)
            else:
                break

        return Sa, k

    def perform(self, p1_lower_bound: int = 0, verbose: bool = False) -> List[int]:
        """
        Runs the solver.
        """
        Sa, k = self.find_sets()

        m = [k[0], k[1]] + [base * 4 for base in Sa]
        k_a = [pow(-k[1], -1, k[0]), pow(-k[0], -1, k[1])] # Only works for h=3, not general to arbitrary h.

        pos = [Sa[base] for base in Sa]

        if verbose:
            print(f'solving sets: {pos} with k values {k}')

        while True:
            z_selection = k_a + self.random_z(pos)
            try:
                n, z = self.solve(m, z_selection)
                if verbose:
                    print(f'found solution condition z={z}, n={n}')
                break
            except:
                pass

        # Search for primes that satisfy constraints.
        sol = [4] * (self.h - 1)
        p1 = z + p1_lower_bound * n
        while True:
            while not self.fermat_test(p1):
                p1 += n

            for i in range(self.h - 1):
                sol[i] = k[i]*(p1 - 1) + 1
                if not self.fermat_test(sol[i]):
                    p1 += n
                    break
            else:
                break

        return [p1] + sol

    def generate_primes(self, n: int) -> List[int]:
        """
        Generates a list of all possible primes between 1 and n.
        """
        sieve = [True] * n
        for i in range(3, int(n**0.5)+1, 2):
            if sieve[i]:
                sieve[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
        return [2] + [i for i in range(3, n, 2) if sieve[i]]
