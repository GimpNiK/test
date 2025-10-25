# Средней сложности:
# 4. НОД двух чисел

#from math import gcd или
def gcd(a:int, b:int)->int:
    while b:
        a, b = b, a % b
    return a
print(gcd(6,9))