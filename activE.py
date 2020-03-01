#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from os import path
import itertools

def func(TRev, Di, Coeff):
	return Di*np.exp(-Coeff*TRev)

marker = itertools.cycle((',', '<', '>')) 
print('=======================================================================')
print('THIS IS PROGRAM MAKE AN ARRENIUS PLOTS OF DIFFUSION COEFFICIENTS')
print('PUT THIS PROGRAM TO FOLDER WITH DATA, THAT YOU WANT TO HANDLE')
print('ACCEPTIBLE DATA FORMAT: il[concentration]_[temperature]K_D_[number_of_peak]data.txt')
print('FOR EXAMPLE: il20_293K_D_1data.txt')
print('A GRAPH AND ACTIVATION ENERGY WILL BE IN THE "OUTPUT" FOLDER')
print('=======================================================================')
concentration=input('concentration(%): ')
temperature=['293','303','313','323','333','343','353']
number_of_peak=input('Peak Number(int): ')
if path.exists('output')==False:
	os.mkdir('output')
save_path='output/'
DC_list, DC_err_list, TRev = [[],[],[]], [[],[],[]], [[],[],[]]
countline=0
while countline<7:
	temp_count=0
	while temp_count<len(temperature):
		NAME_list= str('il')+str(concentration)+str('_')+str(temperature[temp_count])+str('K_D_')+str(number_of_peak)+str('data.txt')
		with open(save_path+NAME_list, 'r') as data:
			data_new = data.readlines()[countline:countline+1]
			elements = data_new[0].strip().split(' +- ')
			DC_list[countline/3].append(float(elements[0]))
			#DC_err_list.append(float(elements[1]))	#This feature is coming soon!
		TRev[countline/3].append(1000/float(temperature[temp_count]))
		temp_count+=1
	countline+=3
plt.ylabel("D ($m^2 s^{-2}$)")
plt.semilogy()
plt.xlabel('1000T$^{-1}$ (K$^{-1}$)')
plt.grid()
file_name = str('RESULTS_Ea_D')+str(number_of_peak)+str('.txt')
file1 = open(save_path+file_name,"w")
countline=0
while countline<7:
	while 1==1:
		try:
			delindex=DC_list[countline/3].index(0)
		except ValueError:
		 	print('break!')
		 	break
		del(DC_list[countline/3][delindex])
		del(TRev[countline/3][delindex])
	#print(TRev[countline/3], ' TRev', countline/3)
	#print(DC_list[countline/3], ' DC_list', countline/3)
	popt, pcov = curve_fit(func, TRev[countline/3], DC_list[countline/3])
	TRev[countline/3]=np.array(TRev[countline/3])
	print(popt, ' popt')
	E_a=popt
	label=str('D')+str(countline/3+1)+str(': ')+str(' Ea=')+str(round((popt[1]*8.31), 1))+str(' kJ/mol')
	plt.scatter(TRev[countline/3],DC_list[countline/3],marker = marker.next(), label=label)
	plt.plot(TRev[countline/3], func(TRev[countline/3], *popt))
	file1.write(str('D')+str(countline/3+1)+str('=')+str(popt[0])+str(' m^2s^-1	Ea=')+str(popt[1]*8.31)+str(' kJ/mol\n'))
	del(popt, pcov)
	#perr = np.sqrt(np.diag(pcov)) 
	countline+=3
IL=str('% Ionic liquid ARRENIUS PLOTS peak ')
plt.title(str(concentration)+IL+str(number_of_peak))
plt.legend(loc='best')
plt.savefig(save_path+str('ARRENIUS_')+str(concentration)+IL+str(number_of_peak)+'.svg', format='svg')