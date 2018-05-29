import re
import operator as op

class AST:
    def __init__(self, expression=""):
        self.expression = expression
        self.root = None

    def __repr__(self):
        return "[ {} ]  =  {}".format(self.expression, self.evaluate()) if self.expression else "Missing expression"

    def build(self):
        if not self.expression: return None
        exp = list(filter(lambda x: x.strip(), re.split(r" *( |\+|-|\*|/|\^|=|IF|\(|\)) *", re.sub(r"(--)+", "", self.expression))))
        i = 0
        while i < len(exp):
            if exp[i] == "-" and (i == 0 or exp[i-1] in list(ops) + ["("]):
                exp[i:i+1] = ["-1", "*"]
            i += 1
        depth = 0
        mult = max(prec.values())
        prev = None
        for item in exp:
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

    def evaluate(self):
        self.root = self.build()
        return self.root.evaluate() if self.root else None

class Node:
    def __init__(self, item, precedence=0):
        self.item = item
        self.precedence = precedence
        self.parent = None
        self.children = []

    def evaluate(self):
        try:
            try: return float(var.get(self.item, self.item))
            except: return float(ops[self.item](*[x.evaluate() for x in self.children]))
        except:
            return self.item

def memorize(a, b):
    var[a] = var.get(b, float(b))
    return var[a]

def check(a, b, c):
    return b if a else c

var = {}
prec = {"+":1, "-":1, "*":2, "/":2, "^":3, "=":4, "IF":5}
n_of_c = {"+":2, "-":2, "*":2, "/":2, "^":2, "=":2, "IF":3}
ops = {"+":op.add, "-":op.sub, "*":op.mul, "/":op.truediv, "^":op.pow, "=":memorize, "IF":check}

ast = AST("IF IF (x = (1 - 1)) 1 0 IF 0 5 3 IF 1 (2^3 * -(2 + 16 * x)) 10")

# IF {IF (x = 0) THEN 1 ELSE 0}
# THEN {IF 0 THEN 5 ELSE 3}
# ELSE {IF 1 THEN -16 ELSE 10}

print(ast)
