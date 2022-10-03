from pyculator import parser

p = parser.Parser()
a = parser.LiteralAnalyzer()

r1 = p("11@19 + 23.5 - 0o46 / 44^2 + 8%")

print(r1)

for lit, t in r1:
    if t == parser.EXPR_NUMBER:
        print(a._analyze_number(lit))