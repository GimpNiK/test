# Средней сложности:
# 4. НОД двух чисел

#from math import gcd или
def gcd(a:int, b:int)->int:
    while b:
        a, b = b, a % b
    return a
print(gcd(6,9))

# 6. Калькулятор
def calculator(a: float, b: float, operation: str) -> float:
    match operation:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            if b == 0:
                raise ZeroDivisionError("Ошибка: деление на ноль")
            return a / b
        case _:
            raise TypeError("Ошибка: неподдерживаемая операция. Используйте '+', '-', '*', '/'")
print(calculator(2,3,"/"))

# 10. Словарь квадратов чисел
from typing import Dict
def squares_dict(n:int) -> Dict[int,int]:
    return {i: i**2 for i in range(1, n+1)}
print(squares_dict(10))

# Повышенной сложности:
# 5. Сгенерировать список Фибоначчи
def fibonacci(n)->int:
    """
    Генератор последовательности Фибоначчи.
    n: количество чисел для генерации.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a  
        a, b = b, a + b 

fib = [i for i in fibonacci(10)]
print(fib)