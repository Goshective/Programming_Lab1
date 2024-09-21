# import re
from operator import add, sub, mul, truediv, pow, neg


# def parse_to_common(expression):
#     '''
#     Returns the list of strings, splited by numbers and operators, including brackets.

#             Parameters:
#                     expression (str): A math expression

#             Returns:
#                     parsed_ex (list[str]): list of numbers and operators
#     '''
#     tech_ex = "".join([symb for symb in expression if not symb.isspace()])
#     parsed_ex = re.split(r"([-,+,*,/,^,(,)])", tech_ex)  # except negative numbers
#     return parsed_ex

def parse_to_common(expression):
    '''
    Returns the list of strings, splited by numbers and operators, including brackets.

            Parameters:
                    expression (str): A math expression

            Returns:
                    exit_code (bool): is expression converatble into list of str
                    parsed_ex (list[str]): list of numbers and operators
    '''
    def condition():
        return (i != len(expression) - 1 and expression[i + 1].isnumeric()) \
              and (parsed_ex and not parsed_ex[-1][-1].isnumeric() or not parsed_ex)

    i = 0
    number_parts = set('.0123456789')
    operators = set('-+*/^()')
    # prev = None
    is_after_space = True
    number_adding_mod = False
    number_str = ''
    parsed_ex = []
    while i < len(expression):
        s = expression[i]
        if number_adding_mod and s not in number_parts:
            number_adding_mod = False
            parsed_ex.append(number_str)
            number_str = ''
        if s.isspace():
            is_after_space = True
            i += 1
            continue

        if s.isnumeric() or s == '.':
            if not number_adding_mod:
                number_adding_mod = True
                if s == '.':
                    return False, None

            if s == '.' and '.' in number_str:
                return False, None

            if is_after_space and parsed_ex and parsed_ex[-1][-1].isnumeric():
                return False, None # 3+10 15-6 : incorrect

            number_str += s
        elif s in operators:
            if s == '-' and condition():
                    number_adding_mod = True
                    number_str += '-' + expression[i + 1]
                    i += 1
            else:
                parsed_ex.append(s)
        else:
            return False, None # unrecognizable symbol
        
        is_after_space = False
        i += 1
    if number_adding_mod and number_str:
        parsed_ex.append(number_str)
    return True, parsed_ex


def parse_to_polish(expression):
    '''
    Returns the list of operators and numbers combining an expression in RPN.

            Parameters:
                    expression (str): A math expression

            Returns:
                    exit_code (bool): can expression be transformed in RPN
                    output (list[str, int, float]): list of operators and numbers
    '''
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "u-": 4}  # Unary minus
    associativity = {
        "+": "L",
        "-": "L",
        "*": "L",
        "/": "L",
        "^": "R",  # Right associativity for exponentiation
        "u-": "R",  # Unary minus (treated as right associative for correct placement)
    }

    output = []
    operators = []

    exit_code, parsed_ex = parse_to_common(expression)
    if not exit_code:
        return False, None

    for i, token in enumerate(parsed_ex):
        if not token:
            continue

        if token in precedence:
            while (
                operators
                and operators[-1] != "("
                and (
                    precedence[operators[-1]] > precedence[token]
                    or (precedence[operators[-1]] == precedence[token] and associativity[token] == "L")
                )
            ):
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)

        elif token == ")":
            while operators:
                op = operators.pop()
                if op != "(":
                    output.append(op)
                else:
                    break
            else:
                return False, None

        elif token == "-" and (i == 0 or parsed_ex[i - 1] in precedence or parsed_ex[i - 1] == "("):
            # Handling unary minus: if '-' is at the start or preceded by an operator or '('
            operators.append("u-")

        else:
            is_num, func = is_number(token)
            if is_num:
                output.append(func(token))
            else:
                return False, None  # not in numbers or in operators

    while operators:
        output.append(operators.pop())

    return True, output


# def is_number(s):
#     '''
#     Returns the class of the number in string if there's a number, else returns False exit code.

#             Parameters:
#                     s (str): number in a string form or any other parsed string except operator

#             Returns:
#                     exit_code (bool): is string can be converted into the number
#                     type (int, float, None): type of number in string
#     '''
#     # Int is:
#     #  - Only numbers that do NOT start with 0 (protect padded number strings)
#     #  - Exactly 0
#     re_int = re.compile(r"(^[1-9]+\d*$|^0$)")
#     is_int = re_int.match(s)
#     # Float is:
#     #  - Only numbers but with exactly 1 dot.
#     #  - The dot must always be followed number numbers
#     re_float = re.compile(r"(^\d+\.\d+$|^\.\d+$)")
#     is_float = re_float.match(s)
#     return (False, None) if not (is_int or is_float) else (True, int) if is_int else (True, float)

def is_number(s):
    '''
    Returns the class of the number in string if there's a number, else returns False exit code.

            Parameters:
                    s (str): number in a string form or any other parsed string except operator

            Returns:
                    exit_code (bool): is string can be converted into the number
                    type (int, float, None): type of number in string
    '''
    try:
        int(s)
        return True, int
    except:
        try:
            float(s)
            return True, float
        except:
            return False, None
    return False, None


def is_operator(s):
    '''
    Returns the fact of string being a math operator.

            Parameters:
                    s (str): any parsed string

            Returns:
                    ret (bool): is s an operator
    '''
    return s in set("+-/*^")


def calculate_polish(p_ex):
    '''
    Returns the result of calculation of RPN expression.

            Parameters:
                    p_ex (list[float, int, str]): RPN expression

            Returns:
                    exit_code (bool): is expression correct
                    res (float, int): final result of calculating RPN expression
    '''
    res_stack = []
    dct_operations = {"+": add, "-": sub, "*": mul, "/": truediv, "^": pow, 'u-': neg}
    for obj in p_ex:
        if isinstance(obj, str):
            if res_stack:
                b = res_stack.pop()
            else:
                return False, None

            if res_stack:
                a = res_stack.pop()
            else:
                return False, None

            res = dct_operations[obj](a, b)
            res_stack.append(res)
        else:
            res_stack.append(obj)
    return True, res_stack[-1]


def correct_input_loop():
    '''
    Manages the correct input process

            Returns:
                    exit_code (bool): is user quiting calculator
                    polish_expression (list[int, float, str]): RPN expression
    '''
    exit_code = False
    while not exit_code:
        print("Выражение некорректно, повторите ввод: (q - выход)")
        expression = input()
        if expression == "q":
            return True, None
        exit_code, polish_expression = parse_to_polish(expression)
    return False, polish_expression


def main():
    '''Manages the main loop of program and calling functions'''

    while True:
        print("Введите выражение: (q - выход)")
        expression = input()
        if expression == "q":
            return

        exit_code, polish_expression = parse_to_polish(expression)
        if not exit_code:
            is_quit, polish_expression = correct_input_loop()
            if is_quit:
                return

        print(polish_expression)

        exit_code, result = calculate_polish(polish_expression)
        while not exit_code:
            is_quit, polish_expression = correct_input_loop()
            if is_quit:
                return
            exit_code, result = calculate_polish(polish_expression)

        print(f"Ответ: {result}")


if __name__ == "__main__":
    main()
    print("Завершение программы.")

"""
(3 + 5) * 10 - 17*2
46

17.6 * 3^(12/3 - 0) + ((1 - 2) + 66/6))
17.6 * 3^(12/3 - 0) + ((1 - 2) + 66/6)
1435.6

1+5-6+9
9

10-1-2-3-4-(0-1-2-3-4)+(0-1-2-3-4)
0

0-1-2-3-4
-10

-1-2-3-4
-10

-1 + (-2) + (-3) + (-4) * (-5 + 6)
-10

print(is_number('17.6')[1]('17.6'))
print(calculate_polish([1, 5, 6, 9, '+', '-', '+']))

print(new_parse_to_common('(3 + 5) * 10 - 17*2'))
print(new_parse_to_common('(3 + a) * 10 - 17*2'))
print(new_parse_to_common('(3 +    5)  * 10 - 17^     2 * (-1 + 3)'))
print(new_parse_to_common('(3 + 5) * 10 - 17*2 + 0.2345'))
print(new_parse_to_common('(3 + 5) * 10 - 17*2 +.023'))
print(new_parse_to_common('(3 + 5) * 10 - 17*2+-+-+-((()())()()())'))
"""
