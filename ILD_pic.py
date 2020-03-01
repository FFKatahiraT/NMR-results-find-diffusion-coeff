#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
from os import path
import itertools

marker = itertools.cycle((',', '+', '.', 'o', '*', '<', 'v')) 
gamma = 4.258
LD = 3
BD = 55
print('=======================================================================')
print('THIS IS PROGRAM MAKE A GRAPH, WHERE I(G) IS SHOWN')
print('PLEASE, PUT THIS PROGRAM TO FOLDER WITH DATA, THAT YOU WANT TO HANDLE')
print('ACCEPTIBLE DATA FORMAT: il[concenctration]_[temperature]K_D_[number_of_peak]')
print('FOR EXAMPLE: il20_293K_D_1')
print('A GRAPH WILL BE IN THE "OUTPUT" FOLDER')
print('=======================================================================')
concenctration=input('concenctration(%): ')
temperature=['293','303','313','323','333','343','353']
number_of_peak=['1','2','3']
if path.exists('output')==False:
	os.mkdir('output')
save_path='output/'
nop_count=0
while nop_count<len(number_of_peak):
	plt.ylabel("I(x)/I(0)")
	plt.semilogy()
	plt.xlabel('x')
	plt.grid()
	temp_count=0
	while temp_count<len(temperature):
		gradient, experiment, x = [], [], []
		NAME_list= str('il')+str(concenctration)+str('_')+str(temperature[temp_count])+str('K_D_')+str(number_of_peak[nop_count])
		with open(NAME_list, 'r') as data:
			data_new = data.readlines()[26:74] 
			i =0
			while i < len(data_new):
				elements = data_new[i].strip().split('    ')
				gradient.append(float(elements[1]))
				experiment.append(float(elements[2]))
				i += 1
		i=0
		while i<len(gradient):
			x.append(((2.0*np.pi*gamma*gradient[i]*LD)**2*(BD - LD/3))/10**11)
			i+=1
		m = np.amax(experiment)
		i = 0
		while i < len(experiment):
			experiment[i] = experiment[i]/m
			i+=1
		plt.scatter(x, experiment, marker = marker.next(), label=temperature[temp_count])
		temp_count+=1
	
	IL=str('% Ionic liquid peak ')
	plt.title(str(concenctration)+IL+str(number_of_peak[nop_count]))
	plt.legend(loc='best')
	plt.savefig(save_path+str(concenctration)+IL+str(number_of_peak[nop_count])+'.svg', format='svg')
	plt.close()
	nop_count+=1
#gradient = np.arange(0, 180, 1)  #делаем функцию гладкой
#plt.plot(gradient, experiment) #Рисуем гладкую аппроксимирующую функцию
