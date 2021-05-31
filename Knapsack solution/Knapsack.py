import numpy as np
import data
import sys
class Knapsack01Problem:
    def __init__(self, file_number):

        # initialize instance variables:
        self.items = []
        self.maxCapacity = 0
        self.file_name = ""


        self.file_number = file_number
        # initialize the data:
        self.__initData(self.file_number)



    def __len__(self):
        #return: the total number of items defined in the problem
        return len(self.items)

    def __initData(self, file_number):
        
        inp = data.input_data()

        #Read files
        with open(inp[self.file_number] + ".kp") as level_file:
            rows = level_file.read().split('\n')

        print(rows[0])

        number_of_items = (int)(rows[1])
        self.items = []
        self.file_name = inp[self.file_number - 1]

        for i in range(4, number_of_items + 5 - 1):
            x = rows[i].split(" ")[0]
            y = rows[i].split(" ")[1]
            self.items.append(((int)(x), (int)(y)))

        self.maxCapacity = (int)(rows[2])

    def get_file_name(self):
        return self.file_name

    def getValue(self, zeroOneList):

        totalWeight = totalValue = 0


        for i in range(len(zeroOneList)):
            value, weight = self.items[i]

            if totalWeight + weight <= self.maxCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value

        return totalValue

    def printItems(self, zeroOneList):

        totalWeight = totalValue = 0
        values, weights = [], []

        for i in range(len(zeroOneList)):
            value, weight = self.items[i]
            weights.append(value)
            values.append(weight)
            if totalWeight + weight <= self.maxCapacity:
                if zeroOneList[i] > 0:
                    totalWeight += weight
                    totalValue += value
        #             print("weight = {}, value = {}, accumulated weight = {}, accumulated value = {}".format(weight, value, totalWeight, totalValue))
        # print("- Total weight = {}, Total value = {}".format(totalWeight, totalValue))
        return totalWeight, totalValue, self.maxCapacity, weights, values

def main():
    
    knapsack = Knapsack01Problem()

    randomSolution = np.random.randint(2, size=len(knapsack))
    print("Random Solution = ", end = '')
    print(randomSolution)
    knapsack.printItems(randomSolution)


if __name__ == "__main__":
    main()