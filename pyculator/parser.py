from dataclasses import dataclass
from typing import Iterable, List, Tuple
import string

EXPR_LITERAL = 1
EXPR_OPERATOR = 2
EXPR_SUFFIX = 4
EXPR_ENTER = 8
EXPR_EXIT = 16
EXPR_SEP = 32
EXPR_EQU = 64
EXPR_UNKNOWN = 1024

literal = string.ascii_lowercase + string.digits + "._"
operator = "+-*/^!"
equ = "=<>"
suffix = "@%"
enter = "([{"
eexit = ")]}"
expr_prio = [suffix, "^!", "*/", "+-"]


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


def exprtype(c: str):
    if c in literal:
        return EXPR_LITERAL
    elif c in operator:
        return EXPR_OPERATOR
    elif c in suffix:
        return EXPR_SUFFIX
    elif c in enter:
        return EXPR_ENTER
    elif c in eexit:
        return EXPR_EXIT
    elif c == ",":
        return EXPR_SEP
    elif c in equ:
        return EXPR_EQU
    else:
        return EXPR_UNKNOWN


def getexprprio(c: str):
    for i, g in enumerate(expr_prio):
        if c in g:
            return i
    return -1


@dataclass
class ParsedCell:
    oprt: str
    oprds: List[str]


class Parser:
    def __init__(self) -> None:
        pass

    def _trail(self, expr: str, sym: str = ""):
        buf, buftype = "", EXPR_LITERAL
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
            if t == EXPR_LITERAL:
                yield s, t
            elif t & (EXPR_OPERATOR | EXPR_SUFFIX):
                if len(oprts) == 0 or \
                        getexprprio(oprts.top[0]) >= getexprprio(s):
                    oprts.top = s, t
                else:
                    yield s, t

        while len(oprts) != 0:
            yield oprts.pop()