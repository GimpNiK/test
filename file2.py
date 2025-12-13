import numpy as np
from typing import Callable,Iterable,Union

sigmoid: Callable[[float], float] = lambda x: 1/(1+np.exp(-x))

class Neuron:
    def __init__(
            self,
            weights: Union[np.ndarray,Iterable[float]],
            b: float = 0.0,
            funcAct: Callable[[float], float] = sigmoid) -> None:
        
        self.weights = np.array(weights)
        self.b = b
        self.funcAct = funcAct
    def __call__(self, *args: float) -> float:
        """Возвращает выходной сигнал нейрона"""
        return self.funcAct(np.dot(self.weights, np.array(args)) + self.b)

class Network:
    def __init__(self) -> None:
        self.h1 = Neuron([0,1],0)
        self.h2 = Neuron([0,1],0)
        self.o =  Neuron([0,1],0)
    def __call__(self, *args: float) -> float:
        return self.o(
            self.h1(*args),
            self.h2(*args)
            )
network = Network()
print(network(2,3))
