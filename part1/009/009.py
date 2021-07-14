
for i in [1,2,3]:
    print(i)

for i in (1,2,3):
    print(i)



class iterNum:
    def __init__(self,begin=0,end=None,step=1):
        # 如果沒有提供end參數，則cursor與end均設為0
        if end == None:
            self.cursor = 0
            self.end = 0
        else:
            self.cursor = begin
            self.end = end
            self.step = step        
    def __iter__(self):
        return(self)       
    def __next__(self):
        if self.cursor < self.end:
            current = self.cursor
            self.cursor += self.step
            return current
        else:
            raise StopIteration()  

from collections.abc import Iterable
from collections.abc import Iterator

iter_num = iterNum(0,10,2)
isinstance(iter_num, Iterable)
isinstance(iter_num, Iterator)

next(iter_num)
next(iter_num)
next(iter_num)
next(iter_num)
next(iter_num)
next(iter_num)
isinstance(iter_num, Iterator)

class my_iterable:
    def __init__(self,begin,end,step):
        self.begin = begin
        self.end = end
        self.step = step

    def __iter__(self):
        return(iterNum(self.begin,self.end,self.step))

iterable_obj = my_iterable(0,10,4)
isinstance(iterable_obj,Iterable)
isinstance(iterable_obj,Iterator)

iterator_obj = iter(iterable_obj)
isinstance(iterator_obj,Iterator)
next(iterator_obj)
next(iterator_obj)
next(iterator_obj)
next(iterator_obj)

x = [1,2,3,4]
y = iter(x) # 獲得疊代器
y
type(y)
next(y)
next(y)
next(y)
next(y)
next(y)


s1 = (45,6,33)
iter(s1)

st1='Python'
iter(st1)

import numpy as np
a1 = np.array([1,23,4])
iter(a1)

d1 = {'aa':123,'bb':34,'cc':'python'}
isinstance(d1, Iterator)
isinstance(d1, Iterable)

d1_iter=iter(d1)
isinstance(d1_iter, Iterator)
#isinstance(d1_iter, Iterable)
next(d1_iter)
next(d1_iter)
next(d1_iter)
next(d1_iter)


def genFun():
    n = 1
    print('n = ',n)
    yield n
    n += 1
    print('n = ',n)
    yield n
    n += 1
    print('n = ',n)
    yield n

g = genFun()

i = next(g)
print(i)

i = next(g)
print(i)

def fib1(maxNum):
    index, first, second = 0, 0, 1
    Seq = []
    while index < maxNum:
        Seq.append(second)
        first, second = second, first + second
        index += 1
        return Seq

f1=fib1(5)
for i in f1:
    print(i)


def fib2(maxNum):
    index, first, second = 0, 0, 1
    while index < maxNum:
        yield second
        first, second = second, first + second
        index += 1

f2=fib2(5)
for i in f2:
    print(i)