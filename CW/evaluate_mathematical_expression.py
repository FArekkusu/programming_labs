import re, operator

prec = {"+":1, "-":1, "*":2, "/":2}
ops = {"+":operator.add, "-":operator.sub, "*":operator.mul, "/":operator.truediv}

class AST:
    def __init__(self, expression):
        self.expression = expression
        self.result = self.evaluate()
    
    def evaluate(self):
        if not self.expression: return None
        queue = list(filter(lambda x: x, re.split(r"(\+|-|\*|/|\^|\(|\))", re.sub(r"(--)+", "--", self.expression.replace(" ", "")))))
        i = 0
        while i < len(queue):
            if queue[i] == "-" and (i == 0 or queue[i-1] in list(ops) + ["("]):
                if i > 0 and queue[i-1] == "(":
                    queue[i:i+1] = ["-1", "*"]
                else:
                    if queue[i+1] == "(":
                        j = find_pair(i+1, queue)
                        queue[j:j+1] = [")", ")"]
                    else:
                        queue[i+1:i+2] = [queue[i+1], ")"]
                    queue[i:i+1] = ["(", "-1", "*"]
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
        return prev.evaluate()

class Node:
    def __init__(self, item, precedence=0):
        self.item = item
        self.precedence = precedence
        self.parent = self.left = self.right = None

    def evaluate(self):
        try: return float(self.item)
        except: return float(ops[self.item](self.left.evaluate(), self.right.evaluate()))

def find_pair(x, a):
    s = 0
    for i in range(x, len(a)):
        if a[i] == "(": s += 1
        if a[i] == ")": s -= 1
        if not s: return i

def calc(expression):
    return AST(expression).result
