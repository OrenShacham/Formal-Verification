import parser
import models
import z3
import re


def loopless_verifier(cond,code):
    for i in reversed(code):
        x = 6
    return 0


def calculate_wlp(post_condition, code):
    if 'variable' in dir(code):
        calculate_assignment_wlp(post_condition,code)
    elif 'if_true' in dir(code):
        calculate_if_wlp(post_condition,code)
    return


def calculate_if_wlp(post_condition, code): #  TODO: figure out deep copies
    leftcond = parse_as_condition("a<b && a<b")
    leftcond.left = code.condition
    leftcond.right = calculate_wlp(post_condition,code.if_true)
    rightcond = parse_as_condition("a<b && a<b")
    rightcond.left = "placeholder"  #  TODO: figure out negation
    rightcond.right = calculate_wlp(post_condition,code.if_false)
    post_condition.left = leftcond
    post_condition.right = rightcond
    post_condition.op = "||"
    return


def calculate_assignment_wlp(post_condition, assignment):
    replace_id_with_exp(post_condition, assignment.variable, assignment.value)
    return


def find_closing_par(s, ind):
    counter = 1
    if ~s[ind].equals("("):
        print("false index given")
        return -1
    while ind < len(s):
        if s[ind].equals('('):
            counter += 1
        elif s[ind].equals(')'):
            counter -= 1
            if counter == 0:
                return ind
        ind += 1
    print("no closing parenthesis found, illegal string given")
    return -1


def replace_id_with_exp(obj, id, new):  # replaces all instances of id[=Identifier(name='...')] with new
    for i in attribute_list(obj):  # for each attribute
        j = getattr(obj, i)
        if j == id:  # replace it if it's the variable
            setattr(obj, i, new)
        elif '__dataclass_fields__' in dir(obj):  # call recursively if applicable
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
