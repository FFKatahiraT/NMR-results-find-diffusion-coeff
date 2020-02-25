This program can find duffusion coefficients for NMR data, including gradient and experiment measurements. 
I=I[0]*exp(-D*SQR(2*PI*gamma*Gi*LD)*(BD-LD/3)*1e4) formula is used to plot a graph. 
y is I/I(0), x is SQR(2*PI*gamma*Gi*LD)*(BD-LD/3)*1e4
From the graph diffusion coefficients D could be estimated. 

This program is calculated for splitting a graph into 3 parts, every part means a separate contribution of an element.
results of the program will be in 'output' folder.
