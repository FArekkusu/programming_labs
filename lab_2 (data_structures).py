from operator import *
import re

def calculate(expression):
    expression = expression.split()[::-1]
    stack, operators = [], {"+":add, "-":sub, "*":mul, "/":truediv, "^":pow}
    for i in range(len(expression)):
        stack.append(expression.pop())
        if stack[-1] in operators:
            o, s, f = stack.pop(), float(stack.pop()), float(stack.pop())
            stack.append(operators[o](f, s))
    return float(stack[-1])

def postfix(infix):
    infix = filter(lambda x: x, re.split(r"(\+|-|\*|/|\^|\(|\))", infix))
    o, s, p = [], [], {"(":1, "^":2, "*":3, "/":3, "+":4, "-":4}
    for i in infix:
        if i.isdigit(): o.append(i)
        elif i == ")":
            while s[-1] != "(": o.append(s.pop())
            s.pop()
        else:
            while len(s) and p[s[-1]] <= p[i] and s[-1] != "(": o.append(s.pop())
            s.append(i)
    return " ".join(o + s[::-1])