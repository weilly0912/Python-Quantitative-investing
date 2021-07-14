
a = 7; b = 8

a.__add__(b)

a.__add__(b).__sub__(1)

# Section 5.1
7 + 8

a = 3
b = 4
a + b

# Section 5.1.1
3+2.0 # 加法

3-2.0 # 減法

3*2.0 # 乘法

3**2.0 # 求冪

3/2.0 # 除法

3//2.0 # 整除

3%2.0 # 取模

True+2.0 # 布 林 型 值 與 浮 點 數 相 加 ， True 代 表 整 數 1

False//2.0 # 布 林 型 值 與 浮 點 數 取商數 ， False 代 表 整 數 0

a=2+3j
b=3+5j
a+b

'Python'+'Quant'
'Python'*4

# Section 5.1.2
a=3
b=4
b+=a
b

# Section 5.1.3
a=30
b=30
a!=b
True==1

s1=set([1,2,3,4])
s2=set([3,2,4,1])
s1==s2 

# Section 5.1.4
True and False

False or True

a=32.5

bool(a)

a and 34

a or 34

not a

b=0

bool(b)

b and a

b or 1

False and True

0 and 33

# Section 5.1.5
a=2

b=2

a==b

id(a)

id(b)

a is b

a is not b

b=50

id(b)

id(a)

a is b

a is not b

c=[2,3,4]

id(c)

d=[2,3,4]

id(d)

c is d

c==d

'a' is 'A'

True is 1

id(True)

id(1)

# Section 5.1.6
a=2

b=[3,4,2]

c={2,3,4}

d=(2,4,5)

a in b

a in c

a in d

'2' in b

'2' in c

'2' in d

e='abc2'

a not in e

'2' not in e

# Section 5.1.7
2+3*5

6>=3**5

# Section 5.2
sum([6,2.0]) # 求 序 列 元 素 之 和

pow(6,2) # 冪 運 算

divmod(6,2) # 整 除 與 取 模

(6//2,6%2)

abs(-6) #求 -6 的 絶 對 值

all([3>2,6<9])

all([2,3,5,6,7])

any([2,3,5,6,7])

any([]) 

max(6,9) 

max([2,3,5,6,7])

min(6,9)

min([2,3,5,6,7])

round(3.84,1)