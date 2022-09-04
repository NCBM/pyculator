from dataclasses import dataclass
from typing import List
import string

EXPR_LITERAL = 1
EXPR_OPERATOR = 2
EXPR_SUFFIX = 4
EXPR_ENTER = 8
EXPR_EXIT = 16
EXPR_UNKNOWN = 1024

literal = string.ascii_lowercase + string.digits + "._"
operator = "+-*/^!=<>"
suffix = "@%"
enter = "([{"
eexit = ")]}"


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
    else:
        return EXPR_UNKNOWN


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
            if c == " ":
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
