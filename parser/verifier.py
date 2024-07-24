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


def replace_id_with_exp(obj, id, new):  # replaces all instances of id[=Identifier(name='...')] with new
    for i in attribute_list(obj):  # for each attribute
        j = getattr(obj, i)
        if j == id:  # replace it if it's the variable
            setattr(obj, i, new)
        elif '__dataclass_fields__' in dir(j):  # call recursively if applicable
            replace_id_with_exp(j, id, new)
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
