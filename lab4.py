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

def primes(n:int):
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
    
print([prime for prime in primes(30)])
    

factorials_square = map(lambda x: factorial(x) **2,[1,2,3,4])
print( *factorials_square)

class Primes:
    def __init__(self,n):
        self.n = n
    def __iter__(self):
        self._prime_list = []
        return self
    def __next__(self):
        prime_last = self._prime_list != [] and self._prime_list[-1] or 1
        for num in range(prime_last + 1,self.n):
            for prime in self._prime_list:
                if num % prime == 0:
                    break
                if num < prime**2:
                    self._prime_list.append(num)
                    return num
            else:
                self._prime_list.append(num)
                return num
        raise StopIteration
print("Prime_iterator: ",*Primes(20))

def pipeline(data, *funcs):
    for func in funcs:
        data = func(data)
    return data

pipeline(2,factorial,lambda x:x**2,print)
