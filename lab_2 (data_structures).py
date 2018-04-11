from operator import *
import re

def calculate(exp):
    exp = exp.split()[::-1]
    stack, ops = [], {"+":add, "-":sub, "*":mul, "/":truediv, "^":pow}
    for i in range(len(exp)):
        stack.append(exp.pop())
        if stack[-1] in ops:
            o, s, f = stack.pop(), float(stack.pop()), float(stack.pop())
            stack.append(ops[o](f, s))
    return float(stack[-1])

def postfix(infix):
    infix = filter(lambda x: x, re.split(r"(\+|-|\*|/|\^|\(|\))", infix.replace(" ", "")))
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
