
#class to represent LED light matrices
#m is number of rows (=height)
#n is number of columns (=length)
class Matrix(object):

    #constructor that instantiates an (MxN) 0-matrix (optional param to include matrix indices to set)
    def __init__(self, m, n, data=None):
        
        #check for valid data
        if (not type(m) is int or not type(n) is int or m <= 0 or n <= 0):
            raise MatrixError("Invalid dimension(s)")

        self.rows = [[0]*n for x in range(m)]
        self.m = m
        self.n = n

        if (data):
            self.setdata(data)

    #get value of matrix[row][col]
    def getdatum(self, m, n):
        
        #check for valid data
        if (not type(m) is int or not type(n) is int or m < 0 or n < 0 or m > self.m-1 or n > self.n-1):
            raise MatrixError("Invalid matrix index")
        
        return self.rows[m][n]

    #set the value of matrix[row][col]
    def setdatum(self, m, n, data):
        
        #check for valid data
        if (not type(m) is int or not type(n) is int or m < 0 or n < 0 or m > self.m-1 or n > self.n-1):
            raise MatrixError("Invalid matrix index")
        if (not type(data) is int or (not data == 1 and not data == 0)):
            raise MatrixError("Invalid input data")
        
        self.rows[m][n] = data
        return True

    #method to set multiple indices in the matrix at once
    #input format: a list of 3-element tuples (m, n, data)
    def setdata(self, data):

        #check for valid data
        if (not type(data) is list):
            raise MatrixError("Input must be a list")

        for point in data:
            if (not type(point) is tuple or len(point) < 3):
                raise MatrixError("Invalid matrix index data")
            self.setdatum(point[0], point[1], point[2])

    #copy input matrix into self
    def copy(self, matrix):
        
        #check for valid data
        if (not type(matrix) is Matrix):
            raise MatrixError("Copy input must be a matrix")

        self.rows = []
        self.rows = [[0]*matrix.n for x in range(matrix.m)]

        row_count = 0
        col_count = 0
        for m in range(matrix.m):
            for n in range(matrix.n):
                self.rows[m][n] = matrix.rows[m][n]

        self.m = matrix.m
        self.n = matrix.n

    #concatenate input matrix onto self
    def concatenate(self, matrix):

        #validate inputs
        if ((not type(matrix) is Matrix) or (not matrix.m == self.m) or (not matrix.n == self.n)):
            raise MatrixError("Invalid input matrix. Matrices must have same dimensions")

        output = Matrix(self.m, self.n*2)
        col_count = 0
        for n in range(self.n):
            for m in range(self.m):
                output.rows[m][n] = self.rows[m][n]
            col_count += 1
        for n in range(matrix.n):
            for m in range(matrix.m):
                output.rows[m][col_count+n] = matrix.rows[m][n]

        return output

    #print the matrix to console
    def print_matrix(self):
        for m in range(self.m):
            row = ""
            for n in range(self.n):
                row += str(self.rows[m][n])
            print (row)
                
#error class
class MatrixError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

        
