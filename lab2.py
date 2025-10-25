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