#class to represent LED light matrices (where each LED takes an RGB value)
#m is number of rows (=height)
#n is number of columns (=length)
class Matrix(object):

    #constructor that instantiates an (MxN) 0-matrix (optional param to include matrix indices to set)
    def __init__(self, m, n, data=None):
        
        #check for valid data
        if (not type(m) is int or not type(n) is int or m <= 0 or n <= 0):
            raise MatrixError("Invalid dimension(s)")

        self.rows = [[(0,0,0)]*n for x in range(m)]
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

    #get matrix representing the given column of self
    def getcolumn(self, n):

        #check for valid data
        if (not type(n) is int or n < 0 or n > self.n-1):
            raise MatrixError("Invalid column index")

        output = Matrix(self.m, 1)
        for m in range(self.m):
            output.setdatum(m, 0, self.rows[m][n])

        return output

    #get matrix representing the given row of self
    def getrow(self, m):

        #check for valid data
        if (not type(m) is int or m < 0 or m > self.m-1):
            raise MatrixError("Invalid row index")

        output = Matrix(1, self.n)
        for n in range(self.n):
            output.setdatum(0, n, self.rows[m][n])

        return output

    #return submatrix of self given row and column indices
    #submatrix is computed from top left
    def get_submatrix(self, m, n):

        #check inputs
        if (not type(m) is int or m < 0 or not type(n) is int or n < 0):
            raise MatrixError("Invalid matrix index")

        row_bound = self.m if (m >= self.m) else m
        col_bound = self.n if (n >= self.n) else n

        output = Matrix(row_bound, col_bound)
        for x in range(row_bound):
            for y in range(col_bound):
                output.setdatum(x, y, self.rows[x][y])
        return output

    #get_bits - DOES THIS MAKE SENSE

    #copy_constructor
    def copy_construct(self):

        output = Matrix(self.m, self.n)
        for m in range(self.m):
            for n in range(self.n):
                output.setdatum(m, n, self.rows[m][n])
        return output

    #set the value of matrix[row][col]
    def setdatum(self, m, n, data):
        
        #check for valid data
        if (not type(m) is int or not type(n) is int or m < 0 or n < 0 or m > self.m-1 or n > self.n-1):
            raise MatrixError("Invalid matrix index")
        if (not type(data) is tuple or not len(data) >= 3 or not (data[0] >= 0 and data[0] <= 255) or not (data[1] >= 0 and data[1] <= 255) or not (data[2] >= 0 and data[2] <= 255)):
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
        self.rows = [[(0,0,0)]*matrix.n for x in range(matrix.m)]

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
        if ((not type(matrix) is Matrix) or (not matrix.m == self.m)):
            raise MatrixError("Invalid input matrix. Matrices must have same height")

        output = Matrix(self.m, self.n+matrix.n)
        col_count = 0
        for n in range(self.n):
            for m in range(self.m):
                output.rows[m][n] = self.rows[m][n]
            col_count += 1
        for n in range(matrix.n):
            for m in range(matrix.m):
                output.rows[m][col_count+n] = matrix.rows[m][n]

        return output

    #stack self on top of input matrix
    def stack_matrix(self, matrix):

        #validate inputs
        if ((not type(matrix) is Matrix) or (not matrix.n == self.n)):
            raise MatrixError("Invalid input matrix. Matrices must have same number of columns")

        output = Matrix(self.m+matrix.m, self.n)
        row_count = 0
        for m in range(self.m):
            for n in range(self.n):
                output.rows[m][n] = self.rows[m][n]
            row_count += 1
        for m in range(matrix.m):
            for n in range(matrix.n):
                output.rows[row_count+m][n] = matrix.rows[m][n]

        return output

    #replace left/rightmost n columns with input
    def shift_horizontal(self, left, new_col):

        #validate inputs
        if (not type(left) is bool or not type(new_col) is Matrix or (not self.m == new_col.m)):
            raise MatrixError("Invalid inputs. Matrices must have the same height")

        shift_factor = self.n - new_col.n
        if (shift_factor <= 0):
            #replace the old matrix entirely
            self.copy(new_col)
            return
        else:
            #shift columns to the left
            if (left):
                output = Matrix(self.m, shift_factor)
                for m in range(self.m):
                    for n in range(new_col.n,self.n):
                        output.setdatum(m, n-new_col.n, self.rows[m][n])
                self.copy(output.concatenate(new_col))
            #shift columns to the right
            else:
                output = Matrix(new_col.m, new_col.n)
                output.copy(new_col)
                temp = Matrix(self.m, shift_factor)
                for m in range(self.m):
                    for n in range(shift_factor):
                        temp.setdatum(m, n, self.rows[m][n])
                self.copy(output.concatenate(temp))

    #replace top/bottom n rows with input
    def shift_vertical(self, bottom, new_rows):

        #validate inputs
        if (not type(bottom) is bool or not type(new_rows) is Matrix or (not self.n == new_rows.n)):
            raise MatrixError("Invalid inputs. Matrices must have the same number of columns")

        shift_factor = self.m - new_rows.m
        if (shift_factor <= 0):
            #replace the old matrix entirely
            self.copy(new_rows)
            return
        else:
            #shift columns up
            if (bottom):
                output = Matrix(shift_factor, self.n)
                for n in range(self.n):
                    for m in range(new_rows.m,self.n):
                        output.setdatum(m-new_rows.m, n, self.rows[m][n])
                self.copy(output.stack_matrix(new_rows))
            #shift columns down
            else:
                output = Matrix(new_rows.m, new_rows.n)
                output.copy(new_rows)
                temp = Matrix(shift_factor, self.n)
                for n in range(self.n):
                    for m in range(shift_factor):
                        temp.setdatum(m, n, self.rows[m][n])
                self.copy(output.stack_matrix(temp))

    #logical functions - WHAT TO PUT HERE????

    #print the matrix to console
    def print_matrix(self):
        for m in range(self.m):
            row = ""
            for n in range(self.n):
                row += "("
                row += str(self.rows[m][n][0])
                row += ","
                row += str(self.rows[m][n][1])
                row += ","
                row += str(self.rows[m][n][2])
                row += ")"
            print (row)
             
                
#error class
class MatrixError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

        
