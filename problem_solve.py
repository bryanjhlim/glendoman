import random
from pprint import pprint
import time

# TODO: Fix this, pass by reference
def reduce_equation_with_bodmas_rule(operator, equation, total):
    while operator in equation:
        idx = equation.index(operator)

        print(idx)

        # prevent division by 0
        if operator == "/":
            if equation[idx+1] == 0:
                print("Division by 0")
                return -1

        if operator == "/":
            total = equation[idx-1] / equation[idx+1]
        elif operator == "x":
            total = equation[idx-1] * equation[idx+1]
        elif operator == "+":
            total = equation[idx-1] + equation[idx+1]
        elif operator == "-":
            total = equation[idx-1] - equation[idx+1]

        equation[idx-1] = total
        del equation[idx+1]
        del equation[idx]

def generate_equation(no_operators, operators, generated_numbers):
    total = 0
    equation = []
    final_equation = []
    # we take the prime numbers from 0 - 100
    prime_nos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    prime_factorials = []

    for i in range(0, no_operators+1):
        # select number (between 0 & 100)
        num = random.randint(0, 100)
        while (num in generated_numbers):
            num = random.randint(0, 100)
            print("Duplicate", num)
            # return -1
        # select operator
        operator = operators[random.randint(0, 1)]

        print(i, num, operator)

        # prevent prime numbers if the operator is "/"
        # this will allow prime factorials division
        if operator == "/":
            print("Divide", num)
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
                    # time.sleep(3)
                    # print(num, num_temp, prime_factorials)
                    if num_temp == 1:
                        break
                print("Prime factorials", prime_factorials)
                num = prime_factorials[random.randint(0, len(prime_factorials)-1)]
                if num in generated_numbers:
                    print(num, "Duplicate prime factorial")
                    return -1
                print("Divide by", num)
                # equation[-2] = num
        prime_factorials.clear()

        equation.append(num)
        if (i < no_operators):
            equation.append(operator)
        
        print(equation)
    
    final_equation = equation.copy()

    # work on the equation here
    # follow the rule of bodmas (we only care about dmas since we don't deal with brackets and orders of powers here)
    while "/" in equation:
        div_idx = equation.index("/")
        # print(div_idx)
        # prevent division by 0
        if equation[div_idx+1] == 0:
            print("Division by 0")
            return -1
        total = equation[div_idx-1] / equation[div_idx+1]
        if equation[div_idx-1] % equation[div_idx+1] == 0:
            equation[div_idx-1] = int(total)
        else:
            equation[div_idx-1] = total
        del equation[div_idx+1]
        del equation[div_idx]
        print("After division", equation)
    while "x" in equation:
        mul_idx = equation.index("x")
        # print(mul_idx)
        total = equation[mul_idx-1] * equation[mul_idx+1]
        equation[mul_idx-1] = total
        del equation[mul_idx+1]
        del equation[mul_idx]
        print("After multiplication", equation)
    while "+" in equation:
        add_idx = equation.index("+")
        # print(add_idx)
        total = equation[add_idx-1] + equation[add_idx+1]
        equation[add_idx-1] = total
        del equation[add_idx+1]
        del equation[add_idx]
        print("After addition", equation)
    while "-" in equation:
        sub_idx = equation.index("-")
        # print(sub_idx)
        total = equation[sub_idx-1] - equation[sub_idx+1]
        equation[sub_idx-1] = total
        del equation[sub_idx+1]
        del equation[sub_idx]
        print("After subtraction", equation)
    
    if total in generated_numbers:
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
    final_equation.append("=")
    final_equation.append(total)

    while (True):
        other_num = random.randint(0, 100)
        if other_num not in generated_numbers:
            generated_numbers.append(other_num)
            final_equation.append("or")
            final_equation.append(other_num)
            break

    return final_equation

def generate_greater_less_than_equations(operators, generated_numbers):
    equation = []

    operator = operators[random.randint(0,1)]
    num = random.randint(0, 100-1)

    other_num = 0
    
    if num in generated_numbers:
        print("Duplicate GT, LT #1", num)
        return -1
    equation.append(num)
    equation.append(operator)

    num_gt = random.randint(num+1, 100)
    num_lt = random.randint(0+1, num-1)

    if num_gt in generated_numbers or num_lt in generated_numbers:
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

    # generate equations containing + and - operators only
    num_add_sub_equations = 5
    print("Generating equations containing + and - operators only")
    for num_equations in range(0, num_add_sub_equations):
        # do 2 operators for all equations
        # no_operators = random.randint(1, 2)
        no_operators = 2
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

    # generate equations containing / and x operators only
    print("Generating equations containing / and x operators only")
    for num_equations in range(0, total_equations-num_add_sub_equations):
        # no_operators = random.randint(1, 2)
        no_operators = 2
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

    sorted_numbers = []
    # for visual manual tallying if there are duplicate bugs
    all_numbers = []

    # generate the greater and less than equations
    # [26 Jan 2022] leave this after problem solving phase 1 done
    # for num_gt_lt_eq in range(0, 3):
    #     while (True):
    #         e = generate_greater_less_than_equations(equalities_inequalities, generated_numbers)
    #         if e != -1:
    #             print("Equation", e)
    #             equations.append(e)
    #             for x in e:
    #                 if isinstance(x, int):
    #                     generated_numbers.append(x)
    #             break
    #         else:
    #             print("Retry")

    for l in equations:
        for n in l:
            if isinstance(n, int):
                all_numbers.append(n)
                if n not in sorted_numbers:
                    sorted_numbers.append(n)

    # shuffle the list so that the same operations are not combined
    # [26 Jan 2022] Do this at a later stage
    # random.shuffle(equations)

    print("  \n##### START #####")
    print("  >>> Split into 3 equations per set. E.g. Set A has the 1st 3 equations, Set B has the next 3 equations. Set C has the last 3 equations. Show the equations and let baby choose the answer.")
    print("  >>> These are the equations to show. The first number in the RHS is always the correct total.")
    # pprint(equations)
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
    print("  >>> For ease of preparation, take these numbers out from the main pile\n", sorted_numbers)
    # print("For manual verification of duplicates", all_numbers)