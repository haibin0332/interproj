
import numpy as np
import matplotlib.pyplot as plt

#n_groups = 5
  
means_men = (20, 35, 30, 35, 27)  
#means_women = (25, 32, 34, 20, 25)  
test_y = 22
   
fig, ax = plt.subplots()  
#index = np.arange(n_groups)
index = (0.1, 0.2, 0.4, 0.8, 0.9)  
bar_width = 0.08
index1=0.55
  
opacity = 1 
rects1 = plt.bar(index, means_men, bar_width,alpha=opacity, color='b',label='partitions')  
#rects2 = plt.bar(index1, test_y, bar_width, alpha=opacity,color='r',label='average')  
#rects2=plt.plot(index1,"b--")
plt.axvline(index1, linewidth=4, color='black',linestyle="--")

plt.annotate('average',xy=(index1,35),xytext=(index1,35))

plt.xlabel('Group')  
plt.ylabel('Scores')  
plt.title('Scores by group and gender')  
#plt.xticks('0.4', 'A')  
plt.ylim(0,50)
plt.xlim(-1,1)
plt.legend()  

plt.grid(True)
  
plt.tight_layout()  
plt.show()

#plt.savefig('/home/hadoop/Downloads/figures/1.jpg')
