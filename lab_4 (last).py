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
        queue = list(filter(lambda x: x, re.split(r"(\+|-|\*|/|\^|=|\(|\))", re.sub(r"(--)+", "--", self.expression.replace(" ", "")))))
        i = 0
        while i < len(queue):
            if queue[i] == "-" and (i == 0 or queue[i-1] in list(ops) + ["("]):
                queue[i:i+1] = ["-1", "*"]
            i += 1
        depth = 0
        prev = None
        for item in queue:
            if item in "()":
                depth += 4 * [-1, 1][item in "("]
                continue
            p = prec.get(item, float("inf")) + depth * 4
            node = Node(item, p)
            if not prev:
                pass
            elif item not in ops:
                prev.right = node
                node.parent = prev
            elif not prev.parent:
                prev.parent = node
                node.left = prev
            else:
                while prev.precedence >= p:
                    if prev.parent:
                        prev = prev.parent
                    else: break
                else:
                    node.left = prev.right
                    prev.right.parent = node
                    prev.right = node
                    node.parent = prev
                    prev = node
                    continue
                prev.parent = node
                node.left = prev
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
        self.parent = self.left = self.right = None

    def evaluate(self):
        try:
            try: return float(var.get(self.item, self.item))
            except: return float(ops[self.item](self.left.evaluate(), self.right.evaluate()))
        except:
            return self.item

def memorize(a, b):
    var[a] = var.get(b, float(b))
    return var[a]

var = {}
prec = {"+":1, "-":1, "*":2, "/":2, "^":3, "=":4}
ops = {"+":op.add, "-":op.sub, "*":op.mul, "/":op.truediv, "^":op.pow, "=":memorize}

ast = AST("6 * x = (-y = 3)^3")
print(ast)
