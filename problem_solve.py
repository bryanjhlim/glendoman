import random

def generate_equation(no_operators, operators, gen_num):
    total = 0
    equation = []
    final_equation = []
    # we take the prime numbers from 0 - 100
    prime_nos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    prime_factorials = []

    for i in range(0, no_operators+1):
        # select number (between 0 & 100)
        num = random.randint(0, 100)
        while (num in gen_num):
            num = random.randint(0, 100)
        # select operator
        operator = operators[random.randint(0, 1)]

        print(i, num, operator)

        # prevent prime numbers if the operator is "/"
        # this will allow prime factorials division
        if operator == "/":
            if num in prime_nos:
                print("Prime numbers have no prime factorials")
                return -1

        # if the previous operator is "/", we do prime factorials so we end up with integers, not float
        if len(equation) > 1:
            if equation[-1] == "/":
                num_temp = equation[-2]
                if num_temp <= 1:
                    print("Divide by 0 / No prime factorials")
                    return -1
                while num_temp > 0:
                    for p in range(0, len(prime_nos)-1):
                        if num_temp % prime_nos[p] == 0:
                            num_temp /= prime_nos[p]
                            prime_factorials.append(prime_nos[p])
                    # print(num, num_temp, prime_factorials)
                    if num_temp == 1:
                        break
                # print("Prime factorials", prime_factorials)
                num = prime_factorials[random.randint(0, len(prime_factorials)-1)]
                if num in gen_num:
                    print(num, "Duplicate prime factorial")
                    return -1
        prime_factorials.clear()

        equation.append(num)
        if (i < no_operators):
            equation.append(operator)
        
        print(equation)
    
    final_equation = equation.copy()

    total = 0
    op = None

    for elem in equation:
        # print(elem, total)
        # input("continue??")
        if type(elem) == int:
            if op == None:
                total = elem
            else:
                if op == '+':
                    total += elem
                elif op == '-':
                    total -= elem
                elif op == '/':
                    total /= elem
                elif op == 'x':
                    total *= elem
                else:
                    print("ERROR. No operator found.")
        elif type(elem) == str:
            if elem == '+':
                op = '+'
            elif elem == '-':
                op = '-'
            elif elem == '/':
                op = '/'
            elif elem == 'x':
                op = 'x'
            else:
                print("ERROR. No operator found.")

    if total in gen_num:
        print("Duplicate total", total)
        return -1
    
    # check if total is decimal or integer
    if isinstance(total, float):
        print("Is float")
        return -1
    # check if total is 100 and below
    if total > 100 or total < 0:
        print("Exceed card support", total)
        return -1

    if "-" in equation and "+" in equation:
        subtract_index = equation.index("-")
        addition_index = equation.index("+")
        if equation[subtract_index-1] < equation[subtract_index+1]:
            print("Negative subtotal, reordering equation", equation)
            # find + X
            # replace position with - Y
            # e.g. A - Y + X --> A + X - Y
            # A - Y + X --> A + Y - X
            final_equation[subtract_index] = equation[addition_index]
            final_equation[addition_index] = equation[subtract_index]
            final_equation[subtract_index+1] = equation[addition_index+1]
            final_equation[addition_index+1] = equation[subtract_index+1]
            print("Reodered equation", final_equation)

    gen_num.append(total)
    final_equation.append("=")

    while (True):
        other_num = random.randint(0, 100)
        if other_num not in gen_num:
            gen_num.append(other_num)
            break

    rhs = []
    rhs.append(total)
    rhs.append(other_num)

    rhs_a = rhs.pop(rhs.index(rhs[random.randint(0,1)]))
    rhs_b = rhs.pop()

    final_equation.append(rhs_a)
    final_equation.append("or")
    final_equation.append(rhs_b)
    final_equation.append("Answer is")
    final_equation.append(total)

    return final_equation

def generate_greater_less_than_equations(operators, gen_num):
    equation = []

    operator = operators[random.randint(0,1)]
    num = random.randint(0, 100-1)

    other_num = 0
    
    if num in gen_num:
        print("Duplicate GT, LT #1", num)
        return -1
    equation.append(num)
    equation.append(operator)

    num_gt = random.randint(num+1, 100)
    num_lt = random.randint(0+1, num-1)

    if num_gt in gen_num or num_lt in gen_num:
        print("Duplicate GT, LT #2", num_lt, num_gt)
        return -1

    if operator == ">":
        num = num_gt
        other_num = num_lt
    elif operator == "<":
        num = num_lt
        other_num = num_gt

    equation.append(other_num)
    equation.append("or")
    equation.append(num)

    return equation

if __name__ == "__main__":
    # phase 1
    operators = ["+", "-", "x", "/"]
    # phase 2
    equalities_inequalities = [">", "<", "=", "!="]
    # phase 3 (in order): i.e. sequences 1st, simple algebra last
    # sequences: arithmetic progression, geometric progression
    math_patterns = ["sequences", "greater_less_than", "equalities_inequalities", "number_personality", "fractions", "simple_algebra"]

    # this will contain the list of equations to check for collision
    # we want to avoid collision because we don't want to keep changing cards
    # ideally we will have 3 bins of 3 equations with unique cards (total of 9 equations a day)
    equations = []

    # prevent duplicates for ease of all sets preparation in advance
    generated_numbers = []

    # total equations = 9
    total_equations = 9

    random.seed()
    
    num_add_sub_equations = 6

    # generate the x and / first to reduce chance of duplicate
    # generate equations containing x and / operators only
    print("Generating equations containing x and / operators only")
    for num_equations in range(0, total_equations-num_add_sub_equations):
        no_operators = random.randint(1, 2)
        # no_operators = 2
        print("no_operators", no_operators)
        while (True):
            e = generate_equation(no_operators, operators[2:4], generated_numbers)
            if e != -1:
                print("Equation", e)
                equations.append(e)
                # add numbers in equation to generated_numbers
                for x in e:
                    if isinstance(x, int):
                        generated_numbers.append(x)
                break
            else:
                print("> Retry")

    # generate equations containing + and - operators only
    print("Generating equations containing + and - operators only")
    for num_equations in range(0, num_add_sub_equations):
        # do 2 operators for all equations
        no_operators = random.randint(1, 2)
        # no_operators = 2
        print("no_operators", no_operators)
        while (True):
            e = generate_equation(no_operators, operators[0:2], generated_numbers)
            if e != -1:
                print("Equation", e)
                equations.append(e)
                # add numbers in equation to generated_numbers
                for x in e:
                    if isinstance(x, int):
                        generated_numbers.append(x)
                break
            else:
                print("> Retry")

    sorted_numbers = []
    # for visual manual tallying if there are duplicate bugs
    all_numbers = []

    # shift the x and / equations to the last set, so that baby can warm up with + and - on first 2 sets
    equations.append(equations.pop(0))
    equations.append(equations.pop(0))
    equations.append(equations.pop(0))

    for l in equations:
        for n in l:
            if isinstance(n, int):
                all_numbers.append(n)
                if n not in sorted_numbers:
                    sorted_numbers.append(n)

    print("  \n##### START #####")
    print("  >>> Split into 3 equations per set. E.g. Set A has the 1st 3 equations, Set B has the next 3 equations. Set C has the last 3 equations. Show the equations and let baby choose the answer.")
    print("  >>> HOW TO READ: The equations are read as 'A PLUS B EQUALS C'.")
    print("  >>> There is a need to be consistent and accurate. Don't vary your manner of speech among 'The answer is', 'equals' and 'equals to'. Stick to one and keep using it.")
    print("  >>> These are the different set of equations to show.")
    count_set = 0
    for e in equations:
        e_str = ""
        if count_set % 3 == 0:
            print("\t>> [Set", int(count_set / 3 + 1), "\b]")
        for element in e:
            e_str += str(element) + " "
        print("\t   " + e_str)
        count_set += 1
    sorted_numbers.sort()
    # all_numbers.sort()
    print("  >>> For ease of preparation, take these numbers out from the main pile. You may sort the numbers in ascending order after for ease of keeping & setting up the next time.\n", sorted_numbers)
    # print("For manual verification of duplicates", all_numbers)
