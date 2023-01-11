import math
start = 2
numList = [start, start, start, start, start, start, start, start, start, start]
complete = False
timer = 0

while (complete==False):
    count0, count1, count2, count3, count4, count5, count6, count7, count8, count9 = 1,1,1,1,1,1,1,1,1,1
    
    for x in range(len(numList)):
        if numList[x] == 0:
            count0+=1
            print("Count0:", count0)
        elif numList[x] == 1:
            count1+=1
            print("Count1:", count1)
        elif numList[x] == 2:
            count2+=1
            print("Count2:", count2)
        elif numList[x] == 3:
            count3+=1
            print("Count3:", count3)
        elif numList[x] == 4:
            count4+=1
            print("Count4:", count4)
        elif numList[x] == 5:
            count5+=1
            print("Count5:", count5)
        elif numList[x] == 6:
            count6+=1
            print("Count6:", count6)
        elif numList[x] == 7:
            count7+=1
            print("Count7:", count7)
        elif numList[x] == 8:
            count8+=1
            print("Count8:", count8)
        elif numList[x] == 9:
            count9+=1
            print("Count9:", count9)

    numList[0] = count0
    numList[1] = count1
    numList[2] = count2
    numList[3] = count3
    numList[4] = count4
    numList[5] = count5
    numList[6] = count6
    numList[7] = count7
    numList[8] = count8
    numList[9] = count9
    
    if count0 == (numList[0]) and count1 == (numList[1]) and count2 == (numList[2]) and count3 == (numList[3]) and count4 == (numList[4]) and count5 == (numList[5]) and count6 == (numList[6]) and count7 == (numList[7]) and count8 == (numList[8]) and count9 == (numList[9]):
        complete = True

    timer += 1
    print (numList)

print(numList)
