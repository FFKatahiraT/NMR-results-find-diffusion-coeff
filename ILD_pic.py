#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path
import itertools

def save_file():
	file1 = open(save_path+file_name,"w") 
	i=0
	while i<len(x) :
		file1.write(str(x[i])+str('    ')+str(experiment[i]))
		file1.write('\n')
		i+=1

def delete_file():
	os.remove(save_path+file_name)

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
format1=str('_raw_data.txt')

nop_count=0
while nop_count<len(number_of_peak):
	temp_count=0
	while temp_count<len(temperature):
		plt.ylabel("I(x)/I(0)")
		plt.semilogy()
		plt.xlabel('x')
		plt.grid()
		gradient, experiment, x = [], [], []
		while True:
			NAME_list= str('il')+str(concenctration)+str('_')+str(temperature[temp_count])+str('K_D_')+str(number_of_peak[nop_count])
			file_name = NAME_list+format1
			print(temperature[temp_count],number_of_peak[nop_count])
			try:	
				with open(NAME_list, 'r') as data:
					data_new = data.readlines()[26:] 
					del(data_new[data_new.index('\n'):])
					i =0
					while i < len(data_new):
						elements = data_new[i].strip().split('    ')
						gradient.append(float(elements[1]))
						experiment.append(float(elements[2]))
						i += 1
				break
			except IOError:
				print(temperature[temp_count],number_of_peak[nop_count], ' does not exist')
				temp_count+=1
		i=0
		while i<len(gradient):
			x.append(((2.0*np.pi*gamma*gradient[i]*LD)**2*(BD - LD/3)/10**11))
			i+=1
		m = np.amax(experiment)
		i = 0
		while i < len(experiment):
			experiment[i] = experiment[i]/m
			if experiment[i]<=0.0:
				print(experiment[i], ' del')
				experiment.pop(i)
				x.pop(i)
			i+=1
		save_file()
		plt.scatter(x, experiment, marker = marker.next(), label=temperature[temp_count])
		temp_count+=1
	
	IL=str('% Ionic liquid peak ')
	plt.title(str(concenctration)+IL+str(number_of_peak[nop_count]))
	plt.legend(loc='best')
	plt.show()
	DelBP=raw_input('Delete bad points? [press any key] - Yes, [n] - No ')
	while True:
		if DelBP!='n':
			plt.ylabel("I(x)/I(0)")
			plt.semilogy()
			plt.xlabel('x')
			plt.grid()
			experiment, x = [], []
			while True:
				temp_count=temperature.index(raw_input('Which temperature you want to hangle?:	'))
				NAME_list= str('il')+str(concenctration)+str('_')+str(temperature[temp_count])+str('K_D_')+str(number_of_peak[nop_count])
				file_name = NAME_list+format1
				print(file_name, ' file_name')
				try:
					with open(save_path+file_name, 'r') as data:
						data_new = data.readlines() 
						i =0
						while i < len(data_new):
							elements = data_new[i].strip().split('    ')
							x.append(float(elements[0]))
							experiment.append(float(elements[1]))
							i += 1
					break
				except IOError:
					print(file_name, ' does not exist')
			Del_quantity=int(raw_input('How many points do you want to remove?:	'))
			del(x[len(x)-Del_quantity:len(x)])
			del(experiment[len(experiment)-Del_quantity:len(experiment)])
			plt.scatter(x, experiment, label=temperature[temp_count])
			plt.legend(loc='best')
			plt.show()
			delete_file()
			save_file()
			DelBP=raw_input('Continue processing? [press any key] - Yes, [n] - No')
		else:
			break
	temp_count=0
	while temp_count<len(temperature):
		plt.scatter(x, experiment, marker = marker.next(), label=temperature[temp_count])
		temp_count+=1	
	temp_count=0
	while temp_count<len(temperature):
		plt.ylabel("I(x)/I(0)")
		plt.semilogy()
		plt.xlabel('x')
		plt.grid()
		experiment, x = [], []
		while True:
			NAME_list= str('il')+str(concenctration)+str('_')+str(temperature[temp_count])+str('K_D_')+str(number_of_peak[nop_count])
			file_name = NAME_list+format1
			try:
				with open(save_path+file_name, 'r') as data:
					data_new = data.readlines() 
					i =0
					while i < len(data_new):
						elements = data_new[i].strip().split('    ')
						x.append(float(elements[0]))
						experiment.append(float(elements[1]))
						i += 1
				break
			except IOError:
				print(file_name, ' does not exist')
				temp_count+=1
		save_file()
		plt.scatter(x, experiment, marker = marker.next(), label=temperature[temp_count])
		temp_count+=1
	plt.savefig(save_path+str(concenctration)+IL+str(number_of_peak[nop_count])+'.svg', format='svg')
	plt.close()
	nop_count+=1
#gradient = np.arange(0, 180, 1)  #делаем функцию гладкой
#plt.plot(gradient, experiment) #Рисуем гладкую аппроксимирующую функцию
