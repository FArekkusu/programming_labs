import re, copy
import operator as op

class Interpreter:
    def input(self, expression):
        expression = list(filter(lambda x: x.strip(), re.split(r" *( |\+|-|\*|/|%|\^|=>|=|\(|\)) *", re.sub(r"(--)+", "", expression))))
        i = 0
        while i < len(expression):
            if expression[i] == "-" and (i == 0 or expression[i-1] in list(ops) + ["("]):
                expression[i] = "UNARY_MINUS"
            i += 1
        if "=>" in expression: AST(expression).parse_func(); return ""
        else: return float(AST(expression).build().evaluate()) if expression else ""

class AST:
    def __init__(self, expression):
        self.expression = expression

    def build(self):
        depth = chain = 0
        mult = max(prec.values())
        prev = None
        for item in self.expression:
            if item in "()":
                depth += mult * [-1, 1][item in "("]
                continue
            if item == "=": chain += 1; depth += mult
            elif prev and prev.parent and prev.parent.item != "=": depth -= chain * mult; chain = 0
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
            elif prev.item in funcs and not prev.parent:
                prev.children.append(node)
                node.parent = prev
            elif item in ops and prev.item in ops and prev.item not in funcs:
                prev.children.append(node)
                node.parent = prev
            else:
                while prev.precedence >= p and len(prev.children) == n_of_c.get(prev.item, 0):
                    if prev.parent:
                        prev = prev.parent
                    else:
                        break
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

    def parse_func(self):
        i = self.expression.index("=>")
        left, right = self.expression[:i], self.expression[i+1:]
        v = left[2:]
        assert left[0] == "fn"
        assert left[1] not in var
        assert len(v) == len(set(v))
        assert all(x.isalpha() for x in v)
        assert set(v) == set(filter(lambda x: x.isalpha(), right))
        self.expression = right
        name, args = left[1], v
        funcs[name] = (self.build(), args)
        prec[name] = 5
        n_of_c[name] = len(args)
        ops[name] = name

class Node:
    def __init__(self, item, precedence=0):
        self.item = item
        self.precedence = precedence
        self.parent = None
        self.children = []
    
    def __eq__(self, other):
        return self.item == other.item
    
    def eval_custom_func(self):
        d = {funcs[self.item][1][i]:self.children[i].evaluate() for i in range(len(self.children))}
        root = copy.deepcopy(funcs[self.item][0])
        def BST(node):
            if node.item in d: node.item = d[node.item]
            for x in node.children: BST(x)
        BST(root)
        return root.evaluate()
    
    def evaluate(self):
        if self.item in funcs:
            assert len(self.children) == n_of_c[self.item]
            return float(self.eval_custom_func())
        if self.item in ops: return float(ops[self.item](*[x.evaluate() for x in self.children]))
        try:
            return float(self.item)
        except:
            if self.parent and self.parent.item == "=" and self == self.parent.children[0]: return self.item
            return var[self.item]

def memorize(a, b):
    assert a not in funcs
    var[a] = var.get(b, float(b))
    return var[a]

def unary_minus(x):
    return -x

var = {}
funcs = {}
prec = {"+": 2, "-": 2, "*": 3, "/": 3, "%": 3, "^": 4, "=": 1, "UNARY_MINUS":5}
n_of_c = {"+": 2, "-": 2, "*": 2, "/": 2, "%": 2, "^": 2, "=": 2, "UNARY_MINUS":1}
ops = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv, "%":op.mod, "^": op.pow, "=": memorize, "UNARY_MINUS":unary_minus}
