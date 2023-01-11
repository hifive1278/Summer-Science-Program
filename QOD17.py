# import math
# start = 1
# numList = [start, start, start, start, start, start, start, start, start]
# num0, num1, num2, num3, num4, num5, num6, num7, num8, num9 = False

# while (num0==False or num1 == False or num2==False or num3 == False or num4==False or num5 == False or num6==False or num7 == False or num8 == False or num9 == False):
#     count0, count1, count2, count3, count4, count5, count6, count7, count8, count9 = 0
    
#     for x in range(len(numList)):
#         if numList[x] == 0:
#             count0+=1
#         elif numList[x] == 1:
#             count1+=1
#         elif numList[x] == 2:
#             count2+=1
#         elif numList[x] == 3:
#             count3+=1
#         elif numList[x] == 4:
#             count4+=1
#         elif numList[x] == 5:
#             count5+=1
#         elif numList[x] == 6:
#             count6+=1
#         elif numList[x] == 7:
#             count7+=1
#         elif numList[x] == 8:
#             count8+=1
#         elif numList[x] == 9:
#             count9+=1

#     if count0 != (numList[0] + 1):
#         num0 = False
#         numList[0] = count0
#     elif count1 != (numList[1] + 1):
#         num1 = False
#         numList[1] = count1
#     elif count2 != (numList[2] + 1):
#         num2 = False
#         numList[2] = count2
#     elif count3 != (numList[3] + 1):
#         num3 = False
#         numList[3] = count3
#     elif count4 != (numList[4] + 1):
#         num4 = False
#         numList[4] = count4
#     elif count5 != (numList[5] + 1):
#         num5 = False
#         numList[5] = count5
#     elif count6 != (numList[6] + 1):
#         num6 = False
#         numList[6] = count6
#     elif count7 != (numList[7] + 1):
#         num7 = False
#         numList[7] = count7
#     elif count8 != (numList[8] + 1):
#         num8 = False
#         numList[8] = count8
#     elif count9 != (numList[9] + 1):
#         num9 = False
#         numList[9] = count9
#     else:
#         num0, num1, num2, num3, num4, num5, num6, num7, num8, num9 = True

# print(numList)

# import math
# start = 3
# numList = [start, start, start, start, start, start, start, start, start, start]
# complete = False
# timer = 0

# while (complete==False):
#     count0, count1, count2, count3, count4, count5, count6, count7, count8, count9 = 0,0,0,0,0,0,0,0,0,0
    
#     for x in range(len(numList)):
#         if numList[x] == 0:
#             count0+=1
#             print("Count0:", count0)
#         elif numList[x] == 1:
#             count1+=1
#             print("Count1:", count1)
#         elif numList[x] == 2:
#             count2+=1
#             print("Count2:", count2)
#         elif numList[x] == 3:
#             count3+=1
#             print("Count3:", count3)
#         elif numList[x] == 4:
#             count4+=1
#             print("Count4:", count4)
#         elif numList[x] == 5:
#             count5+=1
#             print("Count5:", count5)
#         elif numList[x] == 6:
#             count6+=1
#             print("Count6:", count6)
#         elif numList[x] == 7:
#             count7+=1
#             print("Count7:", count7)
#         elif numList[x] == 8:
#             count8+=1
#             print("Count8:", count8)
#         elif numList[x] == 9:
#             count9+=1
#             print("Count9:", count9)

#     if count0 != (numList[0] + 1):
#         numList[0] = count0
#     elif count1 != (numList[1] + 1):
#         numList[1] = count1
#     elif count2 != (numList[2] + 1):
#         numList[2] = count2
#     elif count3 != (numList[3] + 1):
#         numList[3] = count3
#     elif count4 != (numList[4] + 1):
#         numList[4] = count4
#     elif count5 != (numList[5] + 1):
#         numList[5] = count5
#     elif count6 != (numList[6] + 1):
#         numList[6] = count6
#     elif count7 != (numList[7] + 1):
#         numList[7] = count7
#     elif count8 != (numList[8] + 1):
#         numList[8] = count8
#     elif count9 != (numList[9] + 1):
#         numList[9] = count9
#     else:
#         complete = True

#     timer += 1
#     print (numList)

# print(numList)



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