# Pyramid-python
This repository contains Python scripts created during CTFs, which have been modified in order to suit a global usage. Generally speaking this repository is reserved for scripts we couldn't find pre-existing tools or programs for, for example obscure cryptographic algorithms.

# Installation

```sh
git clone https://github.com/Pyramid-Surgeon/pyramid_python.git
cd pyramid_python
python setup.py install --user
```

# Documentation

## Arnaults method.
Arnaults method, as described in https://www.sciencedirect.com/science/article/pii/S0747717185710425, attempts to find pseudo primes which pass the miller-rabin test for a predefined set of bases.

Example usage:
```python
from pyramid_python.crypto import *

base_list = [2,3,5,7,11]
ar = Arnault(base_list)
ar.perform()
```
This will return 3 primes which make up a composite number which will pass the miller-rabin test for the bases 2,3,5,7,11.
```python
[286472803, 11745384883, 3724146427]
```
