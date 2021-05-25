#!/usr/bin/env python
'''
this program is used to plot every hand gesture and record which hand gesture it is
'''
import pandas as pd
import matplotlib.pyplot as plt


hand_data=pd.read_csv('handLog9.csv',header=0)
# result_data=pd.read_excel('result.xlsx',header=0)

print("Sample num is: \t",int(len(hand_data)/21))

# print(hand_data[:21])
# print(result_data[0:5])
def PlotGesture(x, y, accnum, j):
    """
    function plot hand gesture
    """
    # prepare line data 
    L1_x = x[0:5]
    L1_y = y[0:5]
    L2_x = [x[0]] + x[5:9]
    L2_y = [y[0]] + y[5:9]
    L3_x = x[9:13]
    L3_y = y[9:13]
    L4_x = x[13:17]
    L4_y = y[13:17]
    L5_x = [x[0]] + x[17:21]
    L5_y = [y[0]] + y[17:21]
    L6_x = x[5:18:4]
    L6_y = y[5:18:4]

    ax = plt.gca()                                  # Get the current axis information
    ax.xaxis.set_ticks_position('top')              # Move the X axis to the top
    ax.invert_yaxis()                               # Reverse Y axis

    plt.title(str(j)+': AccNum: ' + str(accnum))
    plt.plot(L1_x, L1_y, marker='o', mec='r', mfc='g')
    plt.plot(L2_x, L2_y, marker='o', mec='r', mfc='g')
    plt.plot(L3_x, L3_y, marker='o', mec='r', mfc='g')
    plt.plot(L4_x, L4_y, marker='o', mec='r', mfc='g')
    plt.plot(L5_x, L5_y, marker='o', mec='r', mfc='g')
    plt.plot(L6_x, L6_y, marker='o', mec='r', mfc='g')


    plt.draw()
    plt.pause(1)                
    plt.close()

# lists to record the data label
samplenum = []
accnum  = []
label  = []             # -1 for not valid
                        #  0 for extended hand gesture 
                        #  1 for close hand gesture 
                        #  2 for scissor gesture 
                        #  3 for Ok pose hand gesture 
                        #  4 for spiderman pose hand
                        #  5 for gun gesture 
                        #  6 for others                     

# reason  = []            # 1 for not accnum==0, 2 for data lose, 3 for not gun gesture, 0 for gun gesture
# new_result = []       # 1 for gun gesture，0 for not gun gesture          


# each time label 100 samples
beginNo = 1100
Labelthem = True
Invalidnum = 0
for j in range(beginNo, min(100+beginNo, int(len(hand_data)/21))):   
# for j in range(int(len(hand_data)/21)):   
    # list to store point position
    x = []
    y = []
    # z = []
    TemAccNum = int(hand_data[j*21:j*21+1]['AccNo'])
    accnum.append(TemAccNum)
    samplenum.append(j)

    # read x and y list
    for i in range(21):
        x.append(float(hand_data[j*21+i : j*21+i+1]['x']))
        y.append(float(hand_data[j*21+i : j*21+i+1]['y']))
    
    if not(all(x) and all(y)):
        label.append(-1)
        print("Invailid sample")
        Invalidnum += 1
        continue
        
    # plot
    PlotGesture(x, y, TemAccNum,j)     
    if (Labelthem):
        a = input(''' 
        -1 for not valid
         0 for extended hand gesture 
         1 for close hand gesture 
         2 for scissor gesture 
         3 for Ok pose hand gesture 
         4 for spiderman pose hand
         5 for gun gesture  
         6 for others      
        ''')

        label.append(a)           #record result

print("sum Invalidnum is:\t", Invalidnum)

if (Labelthem):
    df = pd.DataFrame({'samplenum' : samplenum, 'accnum' : accnum, 'label' : label})

    df.to_excel('result.xlsx', sheet_name='Sheet1')

# transfer data to another excel file "result_backup.xlsx" after program stop

