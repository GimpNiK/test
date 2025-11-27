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

