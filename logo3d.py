import sys
from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import visitor

'''
Programa pricipal, incialitzem el parser, lexer i visitor, obtenim el nom del
programa a executar dels arguments, i si hi ha, la funció pricipal més els arguemnts.
'''

input_stream = FileStream(sys.argv[1], encoding='utf-8')

lexer = logo3dLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = logo3dParser(token_stream)
tree = parser.program()

name = "main"
args = []
if len(sys.argv) > 2:
    name = sys.argv[2]
    i = 3
    n = len(sys.argv)
    while i < n:
        args.append(float(sys.argv[i]))
        i += 1

visitor = visitor(name, args)
visitor.visit(tree)
