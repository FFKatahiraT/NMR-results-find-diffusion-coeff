#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import matplotlib.axes
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def func (x, D,b):
	return (-D*x+b)

def func1(x_new, D1, b1):
	return (-D1*x_new+b1)

def func2(x_new2, D2, b2):
	return (-D2*x_new2+b2)

def func3(x_new3,D3,b3):
	return (-D3*x_new3+b3)

gamma = 4.258
LD = 3
BD = 55
gradient, experiment, x = [], [], []
NAME_list= 'il20_293K_D_1'
NAME = str(NAME_list)
png = '.png'
NAME_png_list = NAME_list+png
NAME_png = str(NAME_png_list)
with open(NAME, 'r') as data:
	data_new = data.readlines()[26:74] 
	i =0
	while i < len(data_new):
		elements = data_new[i].strip().split('    ')
		gradient.append(float(elements[1]))
		experiment.append(float(elements[2]))
		i += 1

x=[]
i=0
while i<len(gradient):
	x.append((2.0*np.pi*gamma*gradient[i]*LD)**2*(BD - LD/3))
	i+=1
m = np.amax(experiment)
#print(m, ' amplitude maximum')
i = 0
while i < len(experiment):
	experiment[i] = np.log(experiment[i]/m)
	i+=1

popt, pcov = curve_fit(func, x, experiment)    #Аппроксимируем функцию
D, b= popt
perr = np.sqrt(np.diag(pcov))
x_new = list(x)
exp_new = list(experiment)
while perr[1]>0.0877:
	del(x_new[0])
	del(exp_new[0])
	popt, pcov = curve_fit(func1, x_new, exp_new) 
	perr = np.sqrt(np.diag(pcov))
print(len(x_new), 'x_new')
perr1=perr
D1, b1 = popt

x_new2 = list(x)
exp_new2 = list(experiment)
i=0
while i<len(x):
	exp_new2[i]=exp_new2[i]-(-D1*x[i]+b1)
	i+=1
del(x_new2[(len(x)-len(x_new)):])
del(exp_new2[(len(x)-len(exp_new)):])
popt, pcov = curve_fit(func2, x_new2, exp_new2) 
perr = np.sqrt(np.diag(pcov))
while perr[1]>0.0227:	#0.0226785
	del(x_new2[0])
	del(exp_new2[0])
	print('Allez gut?')
	if len(x_new2)<9:
		break
	try:
		popt, pcov = curve_fit(func2, x_new2, exp_new2) 
	except RuntimeError:
		print("Error - curve_fit failed")
	perr = np.sqrt(np.diag(pcov))
print(x, 'x')
print(x_new2, 'x_new2')
perr2=perr
D2, b2 = popt

x_new3 = list(x)
exp_new3 = list(experiment)
i=0
while i<len(x):
	exp_new3[i]=exp_new3[i]-(-D2*x[i]+b2)-(-D1*x[i]+b1)
	i+=1
del(x_new3[(len(x_new3)-len(x_new2)-len(x_new)):])
del(exp_new3[(len(exp_new3)-len(exp_new2)-len(x_new)):])
popt, pcov = curve_fit(func3, x_new3, exp_new3) 
perr = np.sqrt(np.diag(pcov))
D3, b3 = popt

print(D1,D2,D3, 'D\n',b1,b2,b3,'b')
plt.ylabel("experiment") #Обозначем оси
plt.xlabel('x')
plt.grid()

format1=str('data.txt')
file_name = NAME+format1
file1 = open(file_name,"w") 
i=0
while i<len(experiment):
	file1.write(str(x[i]))
	file1.write(' ')
	file1.write(str(experiment[i]))
	file1.write('\n')
	i+=1
file1.close()

plt.scatter(x, experiment, s=10, color='black') #Выводим массив точек на график
plt.scatter(x_new, exp_new, s=10, color='blue')
plt.scatter(x_new2, exp_new2, s=10, color='orange')
plt.scatter(x_new3, exp_new3, s=10, color='green')
y_sum_m=[]
i=0
while i<len(x):
	y_sum=(-D2*x[i]+b2)+(-D1*x[i]+b1)+(-D3*x[i]+b3)
	y_sum_m.append(y_sum)
	i+=1
plt.scatter(x, y_sum_m, s=10)
x_new=np.array(x_new)
popt=D1,b1
plt.plot(x_new, func1(x_new, *popt), label='1')
x_new2=np.array(x_new2)
popt=D2, b2
plt.plot(x_new2, func2(x_new2, *popt), label='2')

x_new3=np.array(x_new3)
popt=D3, b3
plt.plot(x_new3, func3(x_new3, *popt), label='3')
plt.legend(loc='best')
plt.savefig(NAME_png)

#gradient = np.arange(0, 180, 1)  #делаем функцию гладкой
#plt.plot(gradient, experiment) #Рисуем гладкую аппроксимирующую функцию
plt.show()
