# 4. Класс «Фигура» (площадь, периметр).
# 9. Использовать abc для абстрактного класса.
# 6. Класс со статическим методом.
# 5. Класс для сериализации объектов в JSON.
# 10. Создать класс-итератор.



import abc
class Figure(abc.ABC):
    @abc.abstractmethod
    def square(self) -> float:
        ...
    @abc.abstractmethod
    def perimeter(self) -> float:
        ...

class Circle(Figure):
    radius: float
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

class Json:
    def __new__(cls,obj):
        data = {}
        for key,value in obj.__dict__.items():
            if not key.startswith("_"):
                data[key] = value
        return data

class FigureIterator:
    def __init__(self, figures):
        self._figures = figures
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._figures):
            figure = self._figures[self._index]
            self._index += 1
            return figure
        raise StopIteration
    
circle = Circle(10)
print(Json(circle))
circles = [Circle(5), Circle(10), Circle(15)]
iterator = FigureIterator(circles)
for circle in iterator:
    print(f"Радиус: {circle.radius}, Площадь: {circle.square():.2f}")