from MatrixRegular import Matrix

#testa = Matrix(2,2,[(0,0,1), (0,1,1), (1,0,1)])
#testb = Matrix(2,1,[(0,0,1)])
#result = testb.matrix_multiply(testa)
#result.print_matrix()

#test = Matrix(3,2,[(0,0,5), (0,1,3), (1,0,2), (1,1,1), (2,0,1), (2,1,4)])
#test.print_matrix()
#test.solve_matrix()

#test1 = Matrix(2,3,[(0,0,6), (0,1,1), (0,2,2), (1,0,3), (1,1,4), (1,2,5)])
#test1.print_matrix()
#test1.solve_matrix()
#test1.set_kernel()
#test1.print_matrix()
#for x in test1.kernel:
    #print("Vector "+str(x))
    #x.print_matrix()

#test1 = Matrix(2,3,[(0,0,1), (1,1,1), (0,2,3), (1,2,4)])
#test1.print_matrix()
#test1.set_kernel()
#for x in test1.kernel:
    #print("Vector "+str(x))
    #x.print_matrix()

#print (test1.get_rank_nullity())

#test2 = Matrix(2,4,[(0,0,1), (0,3,1)])
#test2.print_matrix()
#test2.set_kernel()
#for x in test2.kernel:
    #print("Vector "+str(x))
    #x.print_matrix()

#test4 = Matrix(2,4,[(0,0,1), (0,3,0.5), (1,2,1), (1,3,1.5)])
#test4.print_matrix()
#test4.set_kernel()
#for x in test4.kernel:
    #print("Vector "+str(x))
    #x.print_matrix()


#test5 = Matrix(3,3,[(0,0,1),(0,1,2),(0,2,3),(1,0,4),(1,1,5),(1,2,6),(2,0,7),(2,1,8),(2,2,9)])
#result = test5.get_determinant()
#print(str(result))

#test6 = Matrix(2,2,[(0,0,2),(0,1,1),(1,0,1),(1,1,2)])
#test6.print_matrix()
#print (test6.verify_eigenvalue(1))
#print (test6.verify_eigenvalue(3))
#print (test6.verify_eigenvalue(4))
#result = test6.get_eigenvectors([1,3])
#for x in result:
    #print("Vector:")
    #x.print_matrix()

#test7 = Matrix(2,2,[(0,0,2),(0,1,1),(1,0,1),(1,1,2)])
#result = test7.matrix_exponent(3)
#result.print_matrix()

#test8 = Matrix(2,2,[(0,0,2),(0,1,1),(1,0,1),(1,1,2)])
#result = test8.generate_characteristic_polynomial()
#print (result)

poly = [1,0,1]
test = Matrix(2,2)
holder = test.solve_characteristic_polynomial(poly, False)
print (holder)


