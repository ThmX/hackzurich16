import matplotlib.pyplot as plt
import numpy as np

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 
gray = (207/255, 207/255, 207/255)
fs=14

for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.) 


def plot(x, y, title, xlab, ylab, fname=""):

	if(type(x) == type([]) and type(y) == type([])):
		min_y = min(y[0])
		max_y = max(y[0])
		for i in range(len(x)):
			min_y = min(min_y, min(y[i]))
			max_y = max(max_y, max(y[i]))
			plt.plot(x[i], y[i], "o-", color=tableau20[2*i], linewidth=2.)
			plt.hold(True)
		extent = max_y - min_y
	else:
		plt.plot(x, y, "o-", color=tableau20[0], linewidth=2.)
		min_y = y.min()
		max_y = y.max()
		extent = max_y - min_y


	ax = plt.gca()


	ax.set_ylim(min_y - 0.1*extent, max_y + 0.1*extent)
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
	            labelbottom="on", left="off", right="off", labelleft="on")
	plt.xticks(fontsize=fs, horizontalalignment="left")
	plt.yticks(fontsize=fs, horizontalalignment="left", x=-0.1, transform=ax.get_yaxis_text1_transform(0)[0])
	plt.grid()
	ax.xaxis.grid(False)
	ax.yaxis.grid(linestyle="-", linewidth=0.5, color=gray)
	ax.set_axisbelow(True)

	x_low, x_up = ax.axes.get_xlim()
	y_low, y_up = ax.axes.get_ylim()

	title2 = plt.text(-0.1, 1.10, title, fontsize=fs+2, weight="bold", ha='left', transform=ax.transAxes)
	ylabel = plt.text(-0.1, 1.05, ylab, fontsize=fs, family="sans-serif", transform=ax.transAxes)
	xlabel = plt.text(0, -0.10, xlab, fontsize=fs, transform=ax.transAxes)

	if(fname):
		plt.savefig(fname)
	else:
		plt.show()