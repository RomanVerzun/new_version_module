from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers

@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'

@htmlize.register
def _(text: str)->str:
    content = html.escape(text).replace('\n', '<br/>\n')
    return f'</p>{content}</p>'

@htmlize.register
def _(n: numbers.Integral)->str:
    return f'<pre>{n}</pre>'

@htmlize.register
def _(n:bool)->str:
    return f'<pre>{n}</pre>'