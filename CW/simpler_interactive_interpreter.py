import re
import operator as op

class Interpreter:
    def input(self, expression):
        expression = list(filter(lambda x: x.strip(), re.split(r" *( |\+|-|\*|/|%|\^|=|\(|\)) *", re.sub(r"(--)+", "", expression))))
        i = 0
        while i < len(expression):
            if expression[i] == "-" and (i == 0 or expression[i-1] in list(ops) + ["("]):
                expression[i] = "UNARY_MINUS"
            i += 1
        return float(AST(expression).build().evaluate()) if expression else ""

class AST:
    def __init__(self, expression):
        self.expression = expression

    def build(self):
        depth = 0
        mult = max(prec.values())
        prev = None
        for item in self.expression:
            if item in "()":
                depth += mult * [-1, 1][item in "("]
                continue
            p = prec.get(item, float("inf")) + depth * mult
            node = Node(item, p)
            if not prev:
                pass
            elif item not in ops:
                while len(prev.children) == n_of_c.get(prev.item, 0):
                    prev = prev.parent
                prev.children.append(node)
                node.parent = prev
            elif prev.item not in ops and not prev.parent:
                prev.parent = node
                node.children = [prev]
            elif item in ops and prev.item in ops:
                prev.children.append(node)
                node.parent = prev
            else:
                while prev.precedence >= p and len(prev.children) == n_of_c.get(prev.item, 0):
                    if prev.parent:
                        prev = prev.parent
                    else: break
                else:
                    if prev.precedence != p:
                        node.children = [prev.children[-1]]
                        prev.children[-1].parent = node
                        prev.children[-1] = node
                    else:
                        prev.children.append(node)
                    node.parent = prev
                    prev = node
                    continue
                prev.parent = node
                node.children = [prev]
            prev = node
        while prev.parent: prev = prev.parent
        return prev

class Node:
    def __init__(self, item, precedence=0):
        self.item = item
        self.precedence = precedence
        self.parent = None
        self.children = []
    
    def __eq__(self, other):
        return self.item == other.item
    
    def evaluate(self):
        if self.item in ops: return float(ops[self.item](*[x.evaluate() for x in self.children]))
        try:
            return float(self.item)
        except:
            if self.parent and self.parent.item == "=" and self == self.parent.children[0]: return self.item
            return var[self.item]

def memorize(a, b):
    var[a] = var.get(b, float(b))
    return var[a]

def unary_minus(x):
    return -x

var = {}
prec = {"+":2, "-":2, "*":3, "/":3, "%":3, "^":4, "=":1, "UNARY_MINUS":5}
n_of_c = {"+":2, "-":2, "*":2, "/":2, "%":2, "^":2, "=":2, "UNARY_MINUS":1}
ops = {"+":op.add, "-":op.sub, "*":op.mul, "/":op.truediv, "%":op.mod, "^":op.pow, "=":memorize, "UNARY_MINUS":unary_minus}
