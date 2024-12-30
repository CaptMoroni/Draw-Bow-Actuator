print(5)

def processTestData(testData):
    A = []
    B = []
    for line in testData:
        x = line[0]
        y = line[1]
        A.append([x**3, x**2, x, 1])
        B.append([y])
    return A, B

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def get_cofactor(matrix, i, j):
    """Gets the cofactor of a matrix element."""
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


def adjoint(matrix):
    """Calculates the adjoint of a matrix."""
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sign = (-1) ** (i + j)
            adj[j][i] = sign * getMatrixDeternminant(get_cofactor(matrix, i, j))
    return adj

def getInverse(matrix):
    adj = adjoint(matrix)
    det = getMatrixDeternminant(matrix)
    inverse = []
    temp = []
    for vector in adj:
        for x in vector:
            temp.append(x/det)
        inverse.append(temp)
        temp = []
    return inverse

def MM(a,b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)
    return c