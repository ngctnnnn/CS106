x = mean
y = [i for i in range(0, 5000)]
error = dev 

e1=[]
for i in range(len(dev)):
    e1.append(x[i]+dev[i])
e2=[]
for i in range(len(dev)):
    e2.append(x[i]-dev[i])


plt.xlabel("Generations")
plt.ylabel("Average best fitness")
plt.fill_between(y, e1, e2, color='paleturquoise')
plt.plot(y, x, color='g')


plt.xlim(-20, 5000)
plt.ylim(400, 500)

plt.show()