from array import array
import math

class Vector2d:
    __match_args__ = ('x', 'y')
    __slots__ =('__x', '__y')
    typecode = 'd'

    def __init__(self, x:int=332131543, y:int=352445243) -> None:
        self.__x = float(x)
        self.__y = float(y)
    
    def __iter__(self):
        return (i for i in (self.__x, self.__y))
    
    def __repr__(self) -> str:
        class_name = type(self).__name__
        self.__x_ = 10
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self) -> str:
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        return math.hypot(self.__x, self.__y)
    
    def __bool__(self):
        return bool(abs(self))
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
import timeit

setup_code = '''
from __main__ import Vector2d
'''

test_code = '''
for _ in range(100000000):
    Vector2d()
'''

# Измеряем время выполнения
execution_time = timeit.timeit(setup=setup_code, stmt=test_code, number=1)
import time
time.sleep(20)

print(f"Время создания 10 миллионов экземпляров: {execution_time} секунд")