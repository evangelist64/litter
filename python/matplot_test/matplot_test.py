import matplotlib as mpl
mpl.use('TkAgg')
import os,sys
import matplotlib.pyplot as plt
import numpy as np
import time
import threading

os.chdir(os.path.dirname(sys.argv[0]))

X1 = range(0, 50)
Y1 = [num**2 for num in X1] # y = x^2
X2 = [0, 1]
Y2 = range(50, 100) # y = x
Fig = plt.figure(figsize=(8,4))                      # Create a `figure' instance
Ax = Fig.add_subplot(211)               # Create a `axes' instance in the figure
Ax.plot(X1, Y1)                 # Create a Line2D instance in the axes
Ax2 = Fig.add_subplot(212)
Ax2.plot(X1,Y2)
Fig.savefig("test.jpg")
plt.show()
