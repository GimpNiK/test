# 4. Факториал через reduce.
# 6. Создать генератор простых чисел.
# 10. Применить несколько функций к списку через map.
# 5. Реализовать собственный класс-итератор.
# 9. Реализовать pipeline обработки данных.
from functools import reduce
def factorial(n:int)-> int:
    if n<0:
        raise ValueError(f"Факториала {n} не существует")
    else:
        return reduce(lambda x,y: x*y, range(2,n+1),1)

def primes(n):
    prime_list = []
    for num in range(2,n):
        for prime in prime_list:
            if num % prime == 0:
                break
            if num < prime**2:
                prime_list.append(num)
                yield num
                break
        else:
            prime_list.append(num)
            yield num
    
for prime in primes(20):
    print(prime)