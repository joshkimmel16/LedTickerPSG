import numpy

#class to represent an all-purpose matrix
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
        self.solved = False
        self.kernel = []

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
        if (not type(data) is float and not type(data) is int):
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

    ######## MATRIX SOLVING FUNCTIONS ########

    #check if given column is all zeros
    def is_col_empty(self, n, starting_row):

        #check inputs
        if (not type(n) is int or n < 0 or n > self.n-1 or not type(starting_row) is int or starting_row < 0 or starting_row > self.m-1):
            raise MatrixError("Invalid row index")

        for m in range(starting_row, self.m):
            if (not self.rows[m][n] == 0):
                return (False, m)
        return (True, -1)
                
    #check if given row is all zeros
    def is_row_empty(self, m):

        #check inputs
        if (not type(m) is int or m < 0 or m > self.m-1):
            raise MatrixError("Invalid row index")

        for n in range(self.n):
            if (not self.rows[m][n] == 0):
                return False
        return True

    #swap the given 2 rows
    def swap_rows(self, m1, m2):
        
        #check inputs
        if (not type(m1) is int or m1 < 0 or m1 > self.m-1 or not type(m2) is int or m2 < 0 or m2 > self.m-1):
            raise MatrixError("Invalid row indices")

        for n in range(self.n):
            temp = self.rows[m1][n]
            self.setdatum(m1, n, self.rows[m2][n])
            self.setdatum(m2, n, temp)
    
    #normalize given row
    def normalize_row(self, m):

        #check inputs
        if (not type(m) is int or m < 0 or m > self.m-1):
            raise MatrixError("Invalid row index")

        factor = None
        for n in range(self.n):
            if (type(factor) is int or type(factor) is float):
                self.setdatum(m,n,(self.rows[m][n])/factor)
            else:
                if (not self.rows[m][n] == 0):
                    factor = self.rows[m][n]
                    self.setdatum(m,n,1)

    #augment target row by factor multiplied by source row
    def augment_row(self, m_source, factor, m_target):

        #check inputs
        if (not type(m_source) is int or m_source < 0 or m_source > self.m-1 or not type(m_target) is int or m_target < 0 or m_target > self.m-1 or (not type(factor) is float and not type(factor) is int) or factor == 0):
            raise MatrixError("Invalid row indices")

        for n in range(self.n):
            self.setdatum(m_target, n, (self.rows[m_target][n] + factor*self.rows[m_source][n]))

    #solve the given matrix
    def solve_matrix(self):

        current_row = 0
        for n in range(self.n):
            if (current_row > self.m-1):
                break
            check = self.is_col_empty(n, current_row)
            if (not check[0]):
                if (check[1] != current_row):
                    self.swap_rows(check[1], current_row)
                self.normalize_row(current_row)
                for m in range(self.m):
                    if (not m == current_row):
                        if (not self.rows[m][n] == 0):
                            factor = (-1) * self.rows[m][n]
                            self.augment_row(current_row, factor, m)
            current_row = current_row + 1
            print("")
            self.print_matrix()

        self.solved = True

    ######## MATRIX ARITHMETIC FUNCTIONS ########

    #add 2 matrices
    def matrix_add(self, matrix):

        #check inputs
        if (not type(matrix) is Matrix or not self.m == matrix.m or not self.n == matrix.n):
            raise MatrixError("Matrices must have the same dimensions")

        result = Matrix(self.m, self.n)
        for m in range(self.m):
            for n in range(self.n):
                result.setdatum(m, n, (self.rows[m][n] + matrix.rows[m][n]))
        return result

    #multiply 2 matrices
    def matrix_multiply(self, matrix):

        #check inputs
        if (not type(matrix) is Matrix or not (self.n == matrix.m)):
            raise MatrixError("Input matrix must have appropriate dimensions")

        result = Matrix(self.m, matrix.n)
        for n in range(matrix.n):
            for m in range(self.m):
                temp = 0
                for x in range(self.n):
                    temp = temp + (matrix.rows[x][n] * self.rows[m][x])
                result.setdatum(m, n, temp)
        return result

    #raise matrix to an exponent
    def matrix_exponent(self, power):

        #check inputs
        if (not type(power) is int or power < 0):
            raise MatrixError("Only positive, non-zero integers are supported as exponent")

        if (power == 0):
            result = Matrix(self.m, self.n)
            for x in range(self.m):
                result.setdatum(m, m, 1)
            return result
        elif (power == 1):
            return self.copy_construct()
        else:
            result = self.matrix_multiply(self.copy_construct())
            for x in range(2, power):
                result = result.matrix_multiply(self.copy_construct())
            return result

    ######## KERNEL FUNCTIONS ########

    #determine whether given row contains only 0's
    def is_zero_row(self, m, end):

        if (not type(m) is int or m < 0 or m > self.m-1 or not type(end) is int or end < 1 or end > self.n):
            raise MatrixError("Invalid row index")

        check = True
        for n in range(end):
            if (not self.rows[m][n] == 0):
                check = False
        return check

    #determine whether given column contains only 0's, return non-zero indices
    def is_zero_col(self, n):

        if (not type(n) is int or n < 0 or n > self.n-1):
            raise MatrixError("Invalid column index")

        check = True
        hold = []
        for m in range(self.m):
            if (not self.rows[m][n] == 0):
                check = False
                hold.append(m)
        return (check, hold)

    #check whether the given column contains a single 1 and all 0's otherwise
    def is_dependent_col(self, n):

        #check inputs
        if (not type(n) is int or n < 0 or n > self.n-1):
            raise MatrixError("Invalid column index")

        check = False
        index = -1
        for m in range(self.m):
            if (not self.rows[m][n] == 0 and not self.rows[m][n] == 1):
                check = False
                index = -1
                break
            elif (self.rows[m][n] == 1 and check):
                check = False
                index = -1
                break
            elif (self.rows[m][n] == 1):
                test = True
                for x in range(n):
                    if (not self.rows[m][x] == 0):
                        test = False
                        break
                if (test):
                    check = True
                    index = m
            else:
                temp = 0
        return (check, index)

    #get a list of vectors in the kernel of the given matrix
    def set_kernel(self):

        #matrix must be solved to for kernel computation algorithm to work
        if (not self.solved):
            self.solve_matrix()

        self.kernel = []
        self.kernel.append(Matrix(1,self.n)) #kernel always contains the zero vector

        square = min(self.n, self.m)

        holder = []
        frees = self.n
        for a in range(frees):
            holder.append([])
            
        for n in range(self.n):
            if (self.is_zero_col(n)[0]):
                temp = Matrix(1,self.n,[(0,n,1)])
                self.kernel.append(temp)
            elif (self.is_dependent_col(n)[0]):
                temp = 0 #DO NOTHING
            else:
                holder[n-square].append((0,n,1)) #add free variable
                for y in range(self.m):
                    if (not self.rows[y][n] == 0):
                        for b in range(self.n):
                            if (not self.rows[y][b] == 0 and not b == n):
                                holder[n-square].append((0,b,(-1)*(self.rows[y][n] / self.rows[y][b])))
        for z in holder:
                if (not len(z) == 0):   
                    self.kernel.append(Matrix(1,self.n,z))
         
    #get rank and nullity of the matrix
    def get_rank_nullity(self):

        if (len(self.kernel) == 0):
            self.set_kernel()

        rank = self.n - len(self.kernel) + 1

        return (rank, len(self.kernel)-1)


    ######## DETERMINANT FUNCTIONS ########

    #test for a valid matrix index
    def check_matrix_index(self, height, index):

        #check inputs
        if (not type(height) is bool or not type(index) is int):
            raise MatrixError("Invalid parameters")

        #check against number of rows
        if (height):
            if (index < 0 or index > self.m-1):
                return False
            else:
                return True
        #check against number of columns
        else:
            if (index < 0 or index > self.n-1):
                return False
            else:
                return True

    #get any submatrix of self
    def get_submatrix_precise(self, m_start, m_finish, n_start, n_finish):

        #check inputs
        if ((not self.check_matrix_index(True, m_start)) or (not self.check_matrix_index(True, m_finish)) or (not self.check_matrix_index(False, n_start)) or (not self.check_matrix_index(False, n_finish))):
            raise MatrixError("Invalid matrix indices")
        if (m_start > m_finish or n_start > n_finish):
            raise MatrixError("Starting indices must be less than or equal to ending indices")

        rows = m_finish - m_start + 1
        columns = n_finish - n_start + 1

        result = Matrix(rows, columns)

        for x in range(m_start, m_finish+1):
            for y in range(n_start, n_finish+1):
                result.setdatum(x - m_start, y - n_start, self.rows[x][y])
        return result

    #compute the determinant of self
    def get_determinant(self):

        if (not self.m == self.n):
            raise MatrixError("Cannot compute the determinant of a non-square matrix")

        if (self.m == 1):
            return self.rows[0][0]
        elif (self.m == 2):
            return (self.rows[0][0]*self.rows[1][1] - self.rows[0][1]*self.rows[1][0])
        else:
            result = 0
            polarity = 1
            for n in range(self.n):
                scalar = self.rows[0][n]
                temp = None
                if (not n == self.n-1):
                    temp = self.get_submatrix_precise(1, self.m-1, n+1, self.n-1)
                    for col in range(n):
                        temp = self.get_submatrix_precise(1, self.m-1, n-col-1, n-col-1).concatenate(temp)
                else:
                    temp = self.get_submatrix_precise(1, self.m-1, 0, self.n-2)
                result = result + (polarity)*(scalar)*temp.get_determinant()
                polarity = (-1)*polarity
            return result

    ######## EIGENVALUE AND EIGENVECTOR FUNCTIONS ########

    #get the trace of self
    def get_trace(self):

        if (not self.m == self.n):
            raise MatrixError("Can only compute the trace of a square matrix")

        result = 0
        for m in range(self.m):
            result = result + self.rows[m][m]
        return result


    #get the eigenvalue polynomial coefficients for self
    #Le Verrier's algorithm
    def generate_characteristic_polynomial(self):

        if (not self.m == self.n):
            raise MatrixError("Can only compute eigenvalues of square matrices")

        holder = []

        #compute result vector
        result_vector = Matrix(self.m, 1)
        temp = self.copy_construct()
        for x in range(self.m):
            result_vector.setdatum(x, 0, temp.get_trace())
            temp = temp.matrix_multiply(self.copy_construct())

        #compute linear equation set
        linear_eq_set = Matrix(self.m, self.m)
        for m in range(self.m):
            for n in range(m+1):
                if (n == m):
                    linear_eq_set.setdatum(m, n, m+1)
                else:
                    val = result_vector.rows[m-1-n][0]
                    linear_eq_set.setdatum(m, n, val)

        #set up solution
        solver = linear_eq_set.concatenate(result_vector)
        solver.print_matrix()
        solver.solve_matrix()

        #extract coefficients
        holder.append(-1)
        for z in range(solver.m):
            holder.append(solver.rows[z][solver.n-1])

        return holder

    #given a set of coefficients, solve the characteristic polynomial to derive eigenvalues
    def solve_characteristic_polynomial(self, poly, keep_complex):

        #check inputs
        if (not type(poly) is list or not len(poly) == self.n+1):
            raise MatrixError("Characteristic polynomial must be an array with a length equal to the dimensions of the matrix plus 1")

        holder = list(numpy.roots(poly))

        #filter out complex roots
        if (not keep_complex):
            counter = 0
            for x in range(len(holder)):
                if (not type(counter) == numpy.float64):
                    holder.remove(holder[counter])
                else:
                    holder[counter] = float(holder[counter])
                    counter = counter + 1

        return holder
            

    #check whether the given input is an eigenvalue of self
    def verify_eigenvalue(self, eigenvalue):

        #check inputs
        if (not type(eigenvalue) is int and not type(eigenvalue) is float):
            raise MatrixError("Eigenvalue must be a real number")

        temp = Matrix(self.m, self.n)
        for y in range(self.m):
            temp.setdatum(y, y, (-1)*eigenvalue)
        current = self.matrix_add(temp)

        test = current.get_determinant()
        if (not test == 0):
            return False
        else:
            return True

    #given its eigenvalues, compute the eigenvectors of the given matrix
    #does not currently handle complex eigenvalues
    def get_eigenvectors(self, eigenvalues):

        #check inputs
        if (not self.m == self.n):
            raise MatrixError("Eigenvectors only apply to square matrices")
        if (not type(eigenvalues) is list):
            raise MatrixError("Invalid input")

        result = []
        for x in eigenvalues:
            if (not type(x) is int and not type(x) is float):
                raise MatrixError("Eigenvalues must be real numbers")

            temp = Matrix(self.m, self.n)
            for y in range(self.m):
                temp.setdatum(y, y, (-1)*x)
            current = self.matrix_add(temp)

            current.set_kernel()
            count = 0
            for z in current.kernel:
                if (not count == 0):
                    result.append(z)
                count = count + 1

        return result
            

    
    ######## TESTING FUNCTIONS ###########        

    #print the matrix to console
    def print_matrix(self):
        for m in range(self.m):
            row = ""
            for n in range(self.n):
                row += (str(self.rows[m][n])+" ")
            print (row)
             
                
#error class
class MatrixError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

        

