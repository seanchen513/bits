"""
12/25/19

Check divisibility using bit operators (no modulus)

Divisors grouped by method: 
- powers of 2
- 1 + powers of 2: 3, 5, 9, 17
- 7, 11, 13, 19 (using binary version of a general trick)
- combos: 6 (2 and 3), 10 (2 and 5), 12 (3 and 4), 14 (2 and 7), 
    15 (3 and 5), 18 (2 and 9), 20 (4 and 5), ...

Next: 21, ...

All integers can be decomposed as a product of a power of 2 and
an odd number.  So can always check divisibility using bit operators.

"""

###############################################################################


def multiple_of_2(n):
    return n & 1 == 0

def multiple_of_4(n):
    return n & 3 == 0

def multiple_of_8(n):
    return n & 7 == 0

def multiple_of_16(n):
    return n & 15 == 0

def multiple_of_32(n):
    return n & 31 == 0

# Used by multiple_of_d()
def multiple_of_power_of_2(n, p):
    return n & (2**p - 1) == 0


###############################################################################

# This is equivalent to checking the alternating sum of (binary) digits.
def multiple_of_3b(n):
    odd_count = even_count = 0

    if n < 0: n = -n
    if n == 0: return True # base case
    if n == 1: return False # base case

    while n:
        if n & 1: odd_count += 1
        if n & 2: even_count += 1
        n >>= 2

    return multiple_of_3(abs(odd_count - even_count))

###############################################################################
# For divisors d = 1 + 2**p
###############################################################################

"""
Example:
Check if integer is multiple of 5 (same idea as for 3, 9, 17, 33, 65, …, 2**k + 1)
Use facts:
    n/5 = n/4 - n/20
    n/k = floor(n/k) + (n % k) / k

n/5 = floor(n/4) + (n%4)/4 - [floor(n/4) + (n%4)/4] / 5
    = floor(n/4) - [floor(n/4) - n%4] / 5

So need to check if floor(n/4) - n%4 is multiple of 5, so we can recurse on it

floor(n/4) is same as n >> 2
n % 4 is same as n & 3
"""

def multiple_of_3(n):
    if n < 0: n = -n
    if n == 0 or n == 3: return True
    if n < 3: return False

    # floor(n/2) - n%2 == (n >> 1) - (n & 1)
    return multiple_of_3b((n >> 1) - (n & 1))

def multiple_of_5(n):
    if n < 0: n = -n
    if n == 0 or n == 5: return True
    if n < 5: return False

    # floor(n/4) - n%4 == (n >> 2) - (n & 3)
    return multiple_of_5((n >> 2) - (n & 3))

def multiple_of_9(n):
    if n < 0: n = -n
    if n == 0 or n == 9: return True
    if n < 9: return False

    # floor(n/8) - n%8 == (n >> 3) - (n & 7)
    return multiple_of_9((n >> 3) - (n & 7))

def multiple_of_17(n):
    if n < 0: n = -n
    if n == 0 or n == 17: return True
    if n < 17: return False

    # floor(n/16) - n%16 == (n >> 4) - (n & 15)
    return multiple_of_17((n >> 4) - (n & 15))

# could write a general function for d = 1 + 2**p
# ...
# return multiple_of_((n >> p) - (n & (2**p - 1)))


###############################################################################
# A general method
###############################################################################

"""
https://math.stackexchange.com/questions/2228122/general-rule-to-determine-if-a-binary-number-is-divisible-by-a-generic-number

Note 11 (decimal) = 0b1011 and 6 = 0b110, but we don't use these facts in the
code here.

Write n = 2k + j (decimal form) (2 for base 2)
Assume 11 divides n.

n + 11j = 2k + 12j = 2(k + 6j) also divisible by 11.

So 11 divides k + 6j (since 2 and 11 are relatively prime)

So take binary rep. of n, truncate rightmost 1 and following 0s, add 6, 
and keep repeating until we reach 0 or 11 (in which case, n is divisible by 11),
or 1..10 (in which case, n is not divisible by 11).
"""
def multiple_of_11(n):
    if n < 0: n = -n
    if n == 0 or n == 11: return True
    if n < 11: return False

    # right shift until 0th bit is 1
    while n & 1 == 0:
        n >>= 1

    # right shift one more time to discard rightmost set bit
    n >>= 1

    # add 6 = 0b110
    n += 6

    return multiple_of_11(n)


"""
n = 2k + j (decimal form)

Assume 3 divides n.
n + 3j = 2k + 4j = 2(k + 2j)

Assume 5 divides n.
n + 5j = 2k + 6j = 2(k + 3j)

Assume 7 divides n.
n + 7j = 2k + 8j = 2(k + 4j)

Assume 9 divides n.
n + 9j = 2k + 10j = 2(k + 5j)

Assume d divides n, where d is odd.
n + d*j = 2k + (d+1)j = 2 ( k + [(d+1)/2] * j )
"""

# Assume d is odd positive integer.
def multiple_of_odd(n, d):
    if n < 0: n = -n
    if (n == 0) or (n == d): return True
    if n < d: return False

    # right shift until 0th bit is 1
    while n & 1 == 0:
        n >>= 1

    # right shift one more time to discard rightmost set bit
    n >>= 1

    #n += (d + 1) // 2
    n += (d >> 1) + 1
    return multiple_of_odd(n, d)


# General divisibility
def multiple_of_d(n, d):
    p = 0 # power for 2**p

    while d & 1 == 0:
        d >>= 1
        p += 1

    return multiple_of_odd(n, d) and multiple_of_power_of_2(n, p)


###############################################################################
### Specific combos

def multiple_of_6(n):
    return (n & 1 == 0) and multiple_of_3(n)

def multiple_of_10(n):
    return (n & 1 == 0) and multiple_of_5(n)

def multiple_of_12(n):
    return multiple_of_3(n) and multiple_of_4(n)

def multiple_of_14(n):
    return multiple_of_2(n) and multiple_of_odd(n, 7)

def multiple_of_15(n):
    return multiple_of_3(n) and multiple_of_5(n)

def multiple_of_18(n):
    return multiple_of_2(n) and multiple_of_9(n)

def multiple_of_20(n):
    return multiple_of_4(n) and multiple_of_5(n)

###############################################################################

for i in range(2000):
    #print("{}: {}".format(i, multiple_of_3(i)))
    #if multiple_of_3(i): print(i)
    #if multiple_of_3b(i): print(i)
    #if multiple_of_3c(i): print(i)
    #if multiple_of_19(i): print(i)
    #if multiple_of_20(i): print(i)

    #if multiple_of_odd(i, 21): print(i)
    if multiple_of_d(i, 3*5*8): print(i)

