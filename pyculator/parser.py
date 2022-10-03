from decimal import Decimal
from typing import Any, Iterable, Tuple
import string

EXPR_NUMBER = 1
EXPR_OPERATOR = 2
EXPR_EQU = 4
EXPR_ENTER = 8
EXPR_EXIT = 16
EXPR_SEP = 32
EXPR_FUNC = 64
EXPR_UNKNOWN = 1024

number = string.digits + "._@%"
operator = "+-*/^!"
equ = "=<>"
enter = "([{"
eexit = ")]}"
expr_prio = ["^!", "*/", "+-"]


class Stack:
    def __init__(self) -> None:
        self.data = []

    def __len__(self):
        return len(self.data)

    @property
    def top(self):
        return self.data[-1]

    @top.setter
    def top(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop(-1)

    def pop_all(self):
        while len(self):
            yield self.pop()


def exprtype(c: str):
    if c in number:
        return EXPR_NUMBER
    elif c in operator:
        return EXPR_OPERATOR
    elif c in equ:
        return EXPR_EQU
    elif c in enter:
        return EXPR_ENTER
    elif c in eexit:
        return EXPR_EXIT
    elif c == ",":
        return EXPR_SEP
    elif c in string.ascii_letters:
        return EXPR_FUNC
    else:
        return EXPR_UNKNOWN


def getexprprio(c: str):
    for i, g in enumerate(expr_prio):
        if c in g:
            return i
    return -1


class LiteralAnalyzer:
    def __init__(self) -> None:
        pass

    def _analyze_number(self, lit: str):
        try:
            if "." not in lit:
                return int(lit, base=0)
            else:
                return Decimal(lit)
        except ValueError:
            if "@" in lit:
                num, bs = lit.split("@", 1)
                return int(num, base=int(bs))
            elif lit.endswith("%"):
                return Decimal(lit[:-1]) / 100
            raise


class Parser:
    def __init__(self) -> None:
        pass

    def _trail(self, expr: str, sym: str = ""):
        buf, buftype = "", EXPR_NUMBER
        for c in expr:
            if c == string.whitespace:
                continue
            if not buf:
                buf += c
                buftype = exprtype(c)
            else:
                if (_etype := exprtype(c)) == buftype:
                    buf += c
                else:
                    yield buf, buftype
                    buf, buftype = c, _etype
        if buf:
            yield buf, buftype

    def _rpn(self, data: Iterable[Tuple[str, int]]):
        oprts = Stack()

        for s, t in data:
            if t & EXPR_NUMBER:
                yield s, t
            elif t & EXPR_OPERATOR:
                if len(oprts) and \
                        getexprprio(oprts.top[0]) < getexprprio(s):
                    yield from oprts.pop_all()
                oprts.top = s, t

        yield from oprts.pop_all()

    def parse(self, expr: str):
        return list(self._rpn(self._trail(expr)))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.parse(*args, **kwds)