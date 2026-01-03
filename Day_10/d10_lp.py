# manually try a few problems

from pulp import *

# sample #1
prob = LpProblem('Joltage', LpMinimize)

#define the variables
n0 = LpVariable('button #0 presses', 0, None, LpInteger)
n1 = LpVariable('button #1 presses', 0, None, LpInteger)
n2 = LpVariable('button #2 presses', 0, None, LpInteger)
n3 = LpVariable('button #3 presses', 0, None, LpInteger)
n4 = LpVariable('button #4 presses', 0, None, LpInteger)
n5 = LpVariable('button #5 presses', 0, None, LpInteger)

# objective function
prob += n0 + n1 + n2 + n3 + n4 + n5, "total number of button presses"

#  b0    b1  b2   b3    b4    b5      t
# (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# constraints
prob += n4 + n5 == 3, "position 0 target"
prob += n1 + n5 == 5, "position 1 target"
prob += n2 + n3 + n4 == 4, "position 2 target"
prob += n0 + n1 + n3 == 7, "position 3 target"

# write problem data to LP file
prob.writeLP('d10.lp')

# solve using PuLP's choice of solver
prob.solve()

# print status of solution
print(f'Status: {LpStatus[prob.status]}')

# print each variable with resolved values
for v in prob.variables():
    print(f'Variable: {v.name} Value: {v.varValue}')

# optimized objective function
print(f'The minimum number of button presses to reach target: {value(prob.objective)}')

# sample #3
prob = LpProblem('Joltage', LpMinimize)

#define the variables
n0 = LpVariable('button #0 presses', 0, None, LpInteger)
n1 = LpVariable('button #1 presses', 0, None, LpInteger)
n2 = LpVariable('button #2 presses', 0, None, LpInteger)
n3 = LpVariable('button #3 presses', 0, None, LpInteger)

# objective function
prob += n0 + n1 + n2 + n3, "total number of button presses"

#  b0            b1          b2     b3        t
# (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
# constraints
prob += n0 + n1 + n2 == 10, "position 0 target"
prob += n0 + n2 + n3 == 11, "position 1 and 2 target"
# prob += n0 + n2 + n3 == 11, "position 2 target"
prob += n0 + n1 == 5, "position 3 target"
prob += n0 + n1 + n2 == 10, "position 4 target"
prob += n2 == 5, "position 5 target"

# write problem data to LP file
prob.writeLP('d10.lp')

# solve using PuLP's choice of solver
prob.solve()

# print status of solution
print(f'Status: {LpStatus[prob.status]}')

# print each variable with resolved values
for v in prob.variables():
    print(f'Variable: {v.name} Value: {v.varValue}')

# optimized objective function
print(f'The minimum number of button presses to reach target: {value(prob.objective)}')

# test problem #2
prob = LpProblem('Joltage', LpMinimize)

#define the variables
n0 = LpVariable('button #0 presses', 0, None, LpInteger)
n1 = LpVariable('button #1 presses', 0, None, LpInteger)
n2 = LpVariable('button #2 presses', 0, None, LpInteger)
n3 = LpVariable('button #3 presses', 0, None, LpInteger)

# objective function
prob += n0 + n1 + n2 + n3, "total number of button presses"

#  b0          b1    b2   b3        t
# (1,2,3,4) (1,4,5) (2) (0,1,4,5) {13,28,20,2,28,26}
# constraints
prob += n3 == 13, "position 0 target"
prob += n0 + n1 + n3 == 28, "position 1 target"
prob += n0 + n2 == 20, "position 2 target"
prob += n0 == 2, "position 3 target"
prob += n0 + n1 + n3 == 28, "position 4 target"
prob += n1 + n3 == 26, "position 5 target"

# write problem data to LP file
prob.writeLP('d10.lp')

# solve using PuLP's choice of solver
prob.solve()

# print status of solution
print(f'Status: {LpStatus[prob.status]}')

# print each variable with resolved values
for v in prob.variables():
    print(f'Variable: {v.name} Value: {v.varValue}')

# optimized objective function
print(f'The minimum number of button presses to reach target: {value(prob.objective)}')
