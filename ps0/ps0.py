import math

print('Enter number x: ', end = '')
x = input()
try:
    x = int(x)
except:
    x = float(x)
print('Enter number y: ', end = '')
y = input()
try:
    y = int(y)
except:
    y = float(y)
print('x**y = ' + str(x**y))
logBase2 = math.log(x, 2)
if int(logBase2) == logBase2:
    logBase2 = int(logBase2)
print('log(x) = ' + str(logBase2))
