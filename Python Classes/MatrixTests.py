from Matrix import Matrix

test1 = Matrix(3,3,[(0,0,1), (1,1,1)])
test2 = Matrix(3,3,[(2,0,1)])

test1.shift_horizontal(False, test2)

print("result:")
test1.print_matrix()
