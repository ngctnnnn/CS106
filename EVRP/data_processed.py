import sys
import os
import numpy as np

inp = 0

folder_name = "X-n143-k7"

with open(folder_name + "/" + "plot_2.py", "w+") as output:
    output.write('import numpy as np\nimport matplotlib.pyplot as plt\n')
    output.write('\nmean = [')

for i in range(0, 5000):
    sum, cnt = 0, 0
    arr = []
    for inp in range(10):
        with open(folder_name + "/" + folder_name + "-rand" + str(inp) +".txt") as input_file:
            data = input_file.read().split('\n') 

        _, x, __, ___ = data[i].split(" ")
        arr.append((float)(x))
    
    mean = np.mean(arr)
    dev = np.std(arr)

    with open(folder_name + "/plot_2.py", 'a') as output_file:
        if i == 4999:
            output_file.write('{}]\n'.format(mean))
        else:
            output_file.write('{}, '.format(mean))

with open(folder_name + "/plot_2.py", 'a') as output:
    output.write('\ndev = [')

for i in range(0, 5000):
    sum, cnt = 0, 0
    arr = []
    for inp in range(10):
        with open(folder_name + "/" + folder_name + "-rand" + str(inp) +".txt") as input_file:
            data = input_file.read().split('\n') 

        _, x, __, ___ = data[i].split(" ")
        arr.append((float)(x))
    
    mean = np.mean(arr)
    dev = np.std(arr)

    with open(folder_name + "/plot_2.py", 'a') as output_file:
        if i == 4999:
            output_file.write('{}]\n'.format(dev))
        else:
            output_file.write('{}, '.format(dev))
     
# os.system('python3 ' + folder_name + '/plot.py')