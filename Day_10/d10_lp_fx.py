# running LP minimization problem as function for the
# target joltage and wiring buttons

from pulp import *

def run_lp(target: list, buttons: list) -> int:

# setup LP problem
    prob = LpProblem('Joltage', LpMinimize)

    #define the variables
    # use list comprehension to give each button an id
    button_ids = [i for i in range(len(buttons))]

    # build the variable dictionaries
    button_vars = LpVariable.dicts('presses_button', button_ids, lowBound=0, cat=LpInteger)

    # objective function
    # using lpSum to add all variables
    prob += (lpSum(button_vars[i] for i in button_ids), "Total number of button presses")

    # add constraints
    # loop through each indicator values (target[i])
    # and find the buttons that increment it
    for i, t in enumerate(target):
        prob += (lpSum(button_vars[j] for j in button_ids if i in buttons[j]) == t, f'Position {i} target') 
    
    # example of the output
    #  b0    b1  b2   b3    b4    b5      t
    # (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    #prob += n4 + n5 == 3, "position 0 target"
    #prob += n1 + n5 == 5, "position 1 target"
    #prob += n2 + n3 + n4 == 4, "position 2 target"
    #prob += n0 + n1 + n3 == 7, "position 3 target"

    # write problem data to LP file
    prob.writeLP('d10_fx.lp')

    # solve using PuLP's choice of solver
    prob.solve()

    # print status of solution
    print(f'Status: {LpStatus[prob.status]}')

    # print each variable with resolved values
    for v in prob.variables():
        print(f'Variable: {v.name} Value: {v.varValue}')

    # optimized objective function
    result = value(prob.objective)
    print(f'The minimum number of button presses to reach target: {result}')

    return result

def main():

    # sample problem #1
    target = [3,5,4,7]
    buttons = [[3], [1,3], [2], [2,3], [0,2], [0,1]]

    result = run_lp(target, buttons)

    print(f'The minimum number of button presses to reach target: {result}')

    expected_value = 10
    assert result == expected_value

    # sample problem #3
    target = [10,11,11,5,10,5]
    buttons = [[0,1,2,3,4], [0,3,4], [0,1,2,4,5], [1,2]]

    result = run_lp(target, buttons)

    print(f'The minimum number of button presses to reach target: {result}')

    expected_value = 11
    assert result == expected_value

    # test problem #2
    target = [13,28,20,2,28,26]
    buttons = [[1,2,3,4], [1,4,5], [2], [0,1,4,5]]

    result = run_lp(target, buttons)

    print(f'The minimum number of button presses to reach target: {result}')

    expected_value = 46
    assert result == expected_value

if __name__ == '__main__':
    main()

