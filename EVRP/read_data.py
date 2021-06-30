import os
import sys as system
def read_data(file):
    with open(str(file)) as input_file:
        input_data = input_file.read().split('\n')

    OPTIMAL_VALUE = (float)(input_data[3][15:])
    NUM_VEHICLE = (int)(input_data[4][10:])
    DIMENSION = (int)(input_data[5][11:])
    STATIONS = (int)(input_data[6][10:])
    CAPACITY = (int)(input_data[7][10:])
    ENERGY_CAPACITY = (float)(input_data[8][16:])
    ENERGY_CONSUMPTION = (float)(input_data[9][20:])
    
    NODE_COORD = []
    STATION_COORD = []
    DEMAND = []
    DEPOT = ()

    #Node coordinate
    for i in range(DIMENSION):
        x = (int)(input_data[12 + i].split(" ")[1])
        y = (int)(input_data[12 + i].split(" ")[2])
        NODE_COORD.append((x, y))

    #Station coordinate 
    for i in range(STATIONS):
        x = (int)(input_data[12 + DIMENSION + i].split(" ")[1])
        y = (int)(input_data[12 + DIMENSION + i].split(" ")[2])
        STATION_COORD.append((x, y))

    #Demand for each node 
    for i in range(DIMENSION):
        DEMAND.append(input_data[12 + DIMENSION + STATIONS + i + 1].split(" ")[1])
    # print(DEMAND)
    #Depot coordinate
    DEPOT = ((input_data[75]), (input_data[76]))

    #Write file
    # os.system('touch preprocess_benchmark/' + file)
    new_file = open("preprocess_benchmark/" + file, mode="w", encoding="utf-8")
    new_file.write(str(NUM_VEHICLE) +"\n")
    new_file.write(str(DIMENSION) + "\n")
    new_file.write(str(STATIONS) + "\n")
    new_file.write(str(CAPACITY) + "\n")
    new_file.write(str(ENERGY_CAPACITY) + "\n")
    new_file.write(str(ENERGY_CONSUMPTION) + "\n")
    for i, j in NODE_COORD:
        new_file.write(str(i) + " " + str(j) + "\n")

    for i, j in STATION_COORD:
        new_file.write(str(i) + " " + str(j) + "\n")
    
    for i in DEMAND:
        new_file.write(str(i)+ "\n") 

file_name=["benchmark/E-n101-k8.evrp",
"benchmark/E-n22-k4.evrp",
"benchmark/E-n23-k3.evrp",
"benchmark/E-n30-k3.evrp",
"benchmark/E-n33-k4.evrp",
"benchmark/E-n51-k5.evrp",
"benchmark/E-n76-k7.evrp",
"benchmark/X-n1001-k43.evrp",
"benchmark/X-n143-k7.evrp",
"benchmark/X-n214-k11.evrp",
"benchmark/X-n351-k40.evrp",
"benchmark/X-n459-k26.evrp",
"benchmark/X-n573-k30.evrp",
"benchmark/X-n685-k75.evrp",
"benchmark/X-n749-k98.evrp",
"benchmark/X-n819-k171.evrp",
"benchmark/X-n916-k207.evrp",
]
for text in file_name:
    print(text)
    read_data(text)
# print(file_name[2])
# read_data(file_name[2])