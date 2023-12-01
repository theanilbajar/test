import pandas as pd
import numpy as np

# write a function to check if nuber is prime
def is_prime(n):
    if n == 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# create a method to find the new ways to ping a pub sub topic in gcp

