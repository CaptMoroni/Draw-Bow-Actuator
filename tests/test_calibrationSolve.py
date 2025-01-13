
def loadFit(inputLoad):
    lineFitLoad =  .000202*(inputLoad)^3 - 0.0149*(inputLoad)^2 + 1.35*(inputLoad) - 0.122
    return lineFitLoad

testData = [
        [922, 0],
        [-99304, 4.96],
        [-196637, 9.76],
        [-493281, 24.4]
    ]


# from matrix import *
import matrix as mat

A, B = mat.processTestData(testData)
# print(A)
# print(B)

calValues = mat.MM(mat.getInverse(A), B)
print(calValues)

a = calValues[0][0]
b = calValues[1][0]
c = calValues[2][0]
d = calValues[3][0]

print(a,b,c,d)