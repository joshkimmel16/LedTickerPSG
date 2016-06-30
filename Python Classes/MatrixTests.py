from MatrixRGB import Matrix


#constructor - no data set
print ("Constructor Tests:")
test = Matrix(3,3)
test.print_matrix()

print("")

other_test = Matrix(2,2,[(0,1,(8,8,8))])
other_test.print_matrix()

print("")

#copy constructor
print("Copy construct")
third_test = other_test.copy_construct()
third_test.print_matrix()

print("")

#setdatum and getdatum
print ("Getter and Setter tests")
test.setdatum(0,0,(23,45,64))
print (test.getdatum(0,0))
test.print_matrix()

print("")

#getcolumn, getrow, get_submatrix
print ("Get column + row + submatrix")
col = test.getcolumn(0)
row = test.getrow(0)
sub = test.get_submatrix(2,2)

col.print_matrix()
print("")
row.print_matrix()
print("")
sub.print_matrix()

print("")

#setdata
print("Batch set data")
test.setdata([(1,1,(2,3,4)), (2,2,(4,5,6))])
test.print_matrix()

print("")

#Operatorequals
print ("Operator Equals")
test2 = Matrix(1,1)
test2.copy(test)
test2.print_matrix()

print("")

#concatenate
print("Concatenation")
concat = test.concatenate(test2)
concat.print_matrix()

print("")

#stack
print("Stacking")
stack = test.stack_matrix(test2)
stack.print_matrix()

print("")

#horizontal shift
print("Shift horizontally")
test.shift_horizontal(True, col)
test.print_matrix()
test.shift_horizontal(False, col)
test.print_matrix()

print("")

#vertical shift
print("Shift vertically")
test.shift_vertical(True, row)
test.print_matrix()
test.shift_vertical(False, row)
test.print_matrix()

