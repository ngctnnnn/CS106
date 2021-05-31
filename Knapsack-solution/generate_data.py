import random
folder_name = [
		"00Uncorrelated",
		"01WeaklyCorrelated",
		"02StronglyCorrelated",
		"03InverseStronglyCorrelated",
		"04AlmostStronglyCorrelated",
		"05SubsetSum",
		"06UncorrelatedWithSimilarWeights",
		"07SpannerUncorrelated",
		"08SpannerWeaklyCorrelated",
		"09SpannerStronglyCorrelated",
		"10MultipleStronglyCorrelated",
		"11ProfitCeiling",
		"12Circle"
	]
for name in folder_name:
    for i in range(1, 9):
        print('"', end ='')
        rand = random.randint(0, 1)
        if rand >= 0.5:
            print("data/" + name + "/" + str(i) + "/R01000/s0" + str(random.randint(10, 100)), end = '')
        else:
            print("data/" + name + "/" + str(i) + "/R10000/s0" + str(random.randint(10, 100)), end = '')
        print('",')