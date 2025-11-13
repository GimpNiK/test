# 4. Класс «Фигура» (площадь, периметр).
# 9. Использовать abc для абстрактного класса.
# 6. Класс со статическим методом.

# 10. Создать класс-итератор.

# 5. Класс для сериализации объектов в JSON.


import abc
class Figure(abc.ABC):
    @abc.abstractmethod
    def square(self) -> float:
        ...
    @abc.abstractmethod
    def perimeter(self) -> float:
        ...

class Circle(Figure):

    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def square(self) -> float:
        import math
        return math.pi * self.radius ** 2
    def perimeter(self) -> float:
        import math
        return math.pi * self.radius * 2
    
    @staticmethod
    def is_valid_radius(radius: float):
        return radius >= 0
