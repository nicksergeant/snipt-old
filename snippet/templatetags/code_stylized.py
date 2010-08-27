from django import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

def code_stylized(value):
    # Stylize the code.
    code_stylized = highlight(value.code, get_lexer_by_name(value.lexer, encoding='UTF-8'), HtmlFormatter())
    return code_stylized

register.filter('code_stylized', code_stylized)
