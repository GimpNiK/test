# 4. Класс «Фигура» (площадь, периметр).
# 6. Класс со статическим методом.
# 10. Создать класс-итератор.

# 5. Класс для сериализации объектов в JSON.
# 9. Использовать abc для абстрактного класса.

import abc
class Figure(abc.ABC):
    @abc.abstractmethod
    def square(self) -> float:
        ...
    @abc.abstractmethod
    def perimeter(self) -> float:
        ...

class Circle(Figure):

    def __init__(self, radius) -> None:
        self.radius = radius
    
    def square(self) -> float:
        import math
        return math.pi * self.radius ** 2
    def perimeter(self) -> float:
        import math
        return math.pi * self.radius * 2
