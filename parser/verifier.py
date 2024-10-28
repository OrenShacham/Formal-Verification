import copy

import parser
import models
import z3
import re


def calculate_wlp(post_condition, code):
    """ given a loopless list (or singular) of code, and a post_condition (boolean expression)
    this function calculates the weakest liberal precondition necessary for that postcondition after the code runs
    :param post_condition: Boolean Expression
    :param code: instruction or list of instructions
    :return: None
    """
    if isinstance(code, list):
        for i in reversed(code):
            calculate_wlp(post_condition, i)
    elif code is None:
        return
    elif 'variable' in dir(code):
        calculate_assignment_wlp(post_condition,code)
    elif 'if_true' in dir(code):
        calculate_if_wlp(post_condition, code)
    return


def calculate_if_wlp(post_condition, code):
    """ given an If block of code and a wanted postcondition, this function calculates the wlp necessary
    :param post_condition: condition (comparison or boolean expression)
    :param code: If block
    :return: None
    """
    leftcond = parse_as_condition("a<b && a<b")
    leftcond.left = code.condition
    leftcond.right = copy.deepcopy(post_condition)
    calculate_wlp(leftcond.right, code.if_true)
    rightcond = parse_as_condition("a<b && a<b")
    rightcond.left = copy.deepcopy(code.condition)
    condition_negation(rightcond.left)
    rightcond.right = copy.deepcopy(post_condition)
    calculate_wlp(rightcond.right, code.if_false)
    post_condition.left = leftcond
    post_condition.right = rightcond
    post_condition.op = "||"
    return


def condition_negation(cond):
    """ given a condition (comparison or boolean expression) this function negates it in place
    :param cond:
    :return:
    """
    if cond.op in ["<", "<=", ">=", ">", "=", "!="]:
        cond.op = neg_op(cond.op)
        return
    if cond.op == "&&":
        cond.op = "||"
    else:
        cond.op = "&&"
    condition_negation(cond.left)
    condition_negation(cond.right)
    return


def neg_op(op):
    if op == "<":
        return ">="
    elif op == "<=":
        return ">"
    elif op == ">=":
        return "<"
    elif op == ">":
        return "<="
    elif op == "=":
        return "!="
    elif op == "!=":
        return "="
    print("not a legal op")
    return ""


def calculate_assignment_wlp(post_condition, assignment):
    replace_id_with_exp(post_condition, assignment.variable, assignment.value)
    return


def replace_id_with_exp(obj, iden, new):  # replaces all instances of id[=Identifier(name='...')] with new
    for i in attribute_list(obj):  # for each attribute
        j = getattr(obj, i)
        if j == iden:  # replace it if it's the variable
            setattr(obj, i, new)
        elif '__dataclass_fields__' in dir(j):  # call recursively if applicable
            replace_id_with_exp(j, iden, new)
    return


def attribute_list(obj):
    l = dir(obj)
    m = [x for x in l if x[0] != '_']
    return m


def parse_as_condition(s):
    return parser.program.parse_or_raise("if " + s + """ then {
        skip;
    } else
        skip;
    end
    """)[0].condition


def test_condition(cond):
    """
    given a condition it tests if that condition is satisfiable with z3
    :param cond:
    :return:
    """
    variables = find_variables_envelope(cond)
    a = [i for i in range(len(variables))]
    b = list(variables)
    for i in range(len(a)):
        a[i] = z3.Int(b[i])
    solver = z3.Solver()
    s = exp_to_string(cond, b)
    eval("solver.add(" + s + ")")
    return solver.check()


def find_variables_envelope(obj):
    names = set()
    find_variables_rec(obj, names)
    return names


def find_variables_rec(obj, names):
    for i in attribute_list(obj):  # for each attribute
        j = getattr(obj, i)
        if i == 'name':  # add it if it's a name
            names.add(obj.name)
        elif '__dataclass_fields__' in dir(j):  # call recursively if applicable
            find_variables_rec(j, names)
    return


def exp_to_string(exp, a):
    if exp is None:
        return ""
    if isinstance(exp, int):
        return str(exp)
    attributes = attribute_list(exp)
    if 'name' in attributes:
        return "a[" + str(a.index(exp.name)) + "]"
    if 'op' in attributes:
        if exp.op == "&&":
            return "z3.And(" + exp_to_string(exp.left, a) + ", " + exp_to_string(exp.right, a) + ")"
        elif exp.op == "||":
            return "z3.Or(" + exp_to_string(exp.left, a) + ", " + exp_to_string(exp.right, a) + ")"
        else:
            return "(" + exp_to_string(exp.left, a) + " " + op_to_z3op(exp.op) + " " + exp_to_string(exp.right, a) + ")"
    return 'default'


def op_to_z3op(op):
    if op == '=':
        return '=='
    return op


def verify_code(code,postcondition):
    """given code and a desired postcondition, returns weather the postcondition is always satisfied
    :param code: str
    :param postcondition: str
    :return:
    """
    cond = parse_as_condition(postcondition)
    calculate_wlp(cond, code)
    condition_negation(cond)
    s = test_condition(parse_as_condition("1>0"))
    k = test_condition(cond)
    if k == s:  # if we found a way for the post_condition to not be satisfied, that means the code isn't valid
        return False
    else:
        return True




"""def toz3(cond, a):
    
    :param cond: the condition in model
    :param a: the list of z3 variables
    :return: a z3 condition
   
    if cond.op == '||':
        return z3.Or(toz3(cond.left, a), toz3(cond.right, a))
    elif cond.op == '&&':
        return z3.And(toz3(cond.left, a), toz3(cond.right, a))
    elif cond.op in ["<", "<=", ">=", ">", "=", "!="]:
        
    return"""
