import priceAnalysis
import priceAnalysis as PrA
price=[19,18,20,22,17,21]
PrA.OpenPrice(price)
PrA.ClosePrice(price)
PrA.HighPrice(price)
PrA.LowPrice(price)



#10.2
#10.2.1
import math
import cmath
math.pi
math.sin(math.pi/2)
math.ceil(3.5)
math.floor(3.5)
math.trunc(3.5)
cmath.polar(1)
cmath.phase(complex(-1.0, 0.0))

import calendar
calendar.month(2016,2)
print(calendar.month(2016,2))
calendar.isleap(2016)

import time
time.time()
time.localtime()
time.asctime()


t1=time.localtime(2000)
print(t1)
time.ctime(2000)
time.asctime(t1)

from time import strftime,strptime
t2=strptime("12/02/2016","%d/%m/%Y")
print(t2)

strftime("%d %b %y",t2)

from datetime import datetime
now = datetime.now()
now

delta =datetime(2016,2,1)-datetime(2016,1,15)
delta
now + delta

str(now)
now.strftime('%Y-%m-%d')
datetime.strptime('2016-01-01','%Y-%m-%d')

from dateutil.parser import parse
parse('01-01-2016',dayfirst=True)
parse('2016-01-01')
parse('10')

#10.3
L1=list([123,23,[4,5,6],'abc'])
L1

L2=list()
L2

L2.append('python')
L2
L2.extend([123,'price',7,8,9])
L2

L2.append([123,'price',7,8,9])
L2

L1+['python','price',78]
L1
L1+=['python','price',78]
L1

L1.insert(4,88)
L1
L1.pop()
L1

L1.remove('python')
L1.remove('PYTHON')

L1.count('PYTHON')
L1.pop(3)
L1

tu1=tuple((123,45,6,7,8,'python'))
type(tu1)
tu1

tu2=123,6,7,8,'python'
type(tu2)
tu3=(3,4,5,"python")
type(tu3)
tu4=(2,)
type(tu4)

a=[34,78.9,True,"python","finance"]
type(a)
b=tuple(a)
b
type(b)
c=tuple('python')
c

tu5=(tu1,tu2,tu3,tu4)
tu5
type(tu5)

a[0:2:4]
b[2:4]
len(c)
len(tu5)
tu5[0][3]
tu5[2]
tu5[2][3]

list2=[]
for i in tu5:
	list2.append(i)
	print('tuple:',i)

list2

tu6=(3**2,4*5,56/4,False)
tu6
max(tu6)
min(tu6)
tu7=tu4+tu6
tu7 
tu4 
tu6 
tu6*3
tu6


r1=range(5)
type(r1)

len(r1)
print(r1)
r1[0:3]

list1=list(r1)
list1

tuple1=tuple(range(2,16,3))
tuple1

list2=list(range(2,-9,-2))
list2

r1*2


st1='Finance in python'
st1

st2="stock price of Alibaba Group Holding Ltd"
st2

st3="""'beauty' of Python"""
st3

st4=str(123456)
st4
len(st3)
st1[1:6]
st1[1:6:2]

st5='py'+'thon'
st5
st4[0:2]+' '+'price'+' '+st4[2:]

GeogeSoros="""I’m only rich because I know when I’m wrong, I basically have survived\
        by recognizing my mistakes."""
GeogeSoros.split()
GeogeSoros
'234,456,345'.split(',')
'234,456,345'.split(',',maxsplit=1)
'234,456,345'.split('3')
GeogeSoros.split(',',2)

GeogeSoros="""I’m only rich because I know when I’m wrong, I basically have survived by recognizing my mistakes."""
split_GS=GeogeSoros.split() #句子以空格進行分割
count_GS={} #創建空字典
for i in split_GS: #對分割後的字串去除標點‘，’或者‘.’
	if ',' in i:
		split_GS.remove(i);
		split_GS.append(i.split(',')[0])
	if '.' in i:
		split_GS.remove(i);
		split_GS.append(i.split('.')[0])

for j in split_GS:
	count_GS[j]=split_GS.count(j)
   
count_GS   #單詞作為字典的key，詞頻作為字典相應key的value

''.join(['a','b','c','d'])
','.join(['a','b','c','d'])
'A'.join(['a','b','c','d'])

'Finance'.islower()
'Finance'.lower()
'Stock price analysis'.title()
'Stockprice'.upper()
'Stockprice'.upper().title()
'the price is high.'.capitalize( )
st2 = "stock price of Alibaba Group Holding Ltd"
st2.capitalize( )
st2[0:4].capitalize( )+st2[4:]

'stock stocK Stock Stock,stock'.count('stock')
'stock stocK Stock Stock,stock'.lower().count('stock')

TAIEX1={'Date':'02-Mar-2015','Open':3332.7,'High':3336.8,'Low':3298.7,'Close':3336.3}
TAIEX2=dict({'Date':'02-Mar-2015','Open':3332.7,'High':3336.8,'Low':3298.7,'Close':3336.3})
TAIEX3=dict(Date='02-Mar-2015',Open=3332.7,High=3336.8,Low=3298.7,Close=3336.3)
TAIEX4=dict([('Date','02-Mar-2015'),('Open',3332.7),('High',3336.8),('Low',3298.7),('Close',3336.3)])
TAIEX5=dict(zip(['Date','Open','High','Low','Close'],['02-Mar-2015',3332.7,3336.8,3298.7,3336.3]))
TAIEX1==TAIEX2==TAIEX3==TAIEX4==TAIEX5

TAIEX1.items()
TAIEX1.keys()
TAIEX1.values()

TAIEX_keys=TAIEX1.keys()
type(TAIEX_keys)
TAIEX_keysList=list(TAIEX_keys)
TAIEX_keysList
TAIEX_keysList[2]

for v in TAIEX1.values():
	if type(v)==float:
		v-=20
		print((v+20,v))
	else:
		print(v,type(v))   

TAIEX1['Open']
TAIEX1.get('Open')

for key in TAIEX1.keys():
	if type(TAIEX1[key])==float:
		TAIEX1[key]+=100000
		print(key,':',TAIEX1.get(key))

TAIEX1.update(Open=2332.7,High=2336.8,Low=2298.7,Close=2336.3)
TAIEX1

TAIEX1['index']='taiex'
TAIEX1

del TAIEX1['Date']
'Date' in TAIEX1
TAIEX1

TAIEX2=TAIEX1.copy()
TAIEX2.clear()
TAIEX1
TAIEX2

set1=set([20,50,60,34,'python'])
set1
list1=[2,3,4,5,3,2,67]
set2=set(list1)
set2

fset1=frozenset([23,56,'python'])
fset1
set3={'Open','Close','High','Low'}
type(set3)

set1.add('finance')
set1
set1.remove(20)
set1
fset1.add(3)
len(set3)
len(fset1)


list2=[23.1,24,24.3,22.9]
d=dict()
j=0
for i in set3:
	d[i]=list2[j]
	j+=1

d


set1={20,30,5,6,7}
set2={2,3,5,7,8}

#聯集運算
set1.union(set2),set1|set2

#交集運算
set1.intersection(set2),set1 & set2
({5, 7}, {5, 7})

#差集運算
set1.difference(set2),set1 - set2
({6, 20, 30}, {6, 20, 30})

#對稱差集運算
set1.symmetric_difference(set2),set1 ^ set2
({2, 3, 6, 8, 20, 30}, {2, 3, 6, 8, 20, 30})

#{1,2,3}是否屬於{1,2,3}的子集判斷
{1,2,3}<={1,2,3}
True

#{1,2,3}是否屬於{1,2,3,'python'}真子集判斷
{1,2,3}<{1,2,3,'python'}

#包含關系判斷
{1,2,3,'python'}.issuperset({1,2,3})

#有無交集判斷
{5,6,7}.isdisjoint({})


#有無交集判斷
{5,6,7}.isdisjoint({5})

{2,3,4,7,8,9}.intersection({2,3,4,6}).intersection({3,4,9})
{2,3,4,7,8,9}&{2,3,4,6}&{3,4,9}
{2,3,4,7,8,9}- {2,8}|{708,100,245}