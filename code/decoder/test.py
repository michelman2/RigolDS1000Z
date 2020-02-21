#### adding folder paths to python path
import os
import sys
file_adder_script_path = "../"
sys.path.append(os.path.abspath(file_adder_script_path))
import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")
### end of setting up the environment



import numpy as np
from matplotlib import pyplot as plt
from matplotlib import figure



x = np.arange(start=0 , stop=2*np.pi*10 , step=0.1)
y = np.sin(x)

ffty = np.fft.fft(y)
y2 = np.abs(ffty)
# print(len(y2))
# print(len(x))
fig , a = plt.subplots(2,2)

a[0][0].plot(x , y)
a[1][0].plot(x , y2)
plt.show()