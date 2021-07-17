import os
import sys

os.system('rm -rf output.txt')

with open("output.csv", 'w+') as output_file:
    output_file.write('')

file_name = ['E-n22-k4', 'E-n23-k3', 'E-n30-k3', 'E-n33-k4', 'E-n51-k5', 'E-n76-k7', 'E-n101-k8', 'X-n143-k7']

final = 4999

final_ans = []

for file in file_name:
    for i in range(10):
        with open(file + "/" + file + "-rand" + str(i) + ".txt") as input_file:
            output = input_file.read().split('\n')
        
        x, y, z, t = output[final].split(" ")
        final_ans.append(x)

    with open("output.csv", 'a') as output_file:
        # output_file.write('{}\n'.format(file))
        for i in final_ans:
            output_file.write('{}, '.format(i))
        output_file.write('\n')
    final_ans = []