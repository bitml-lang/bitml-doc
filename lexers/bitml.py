# -*- coding: utf-8 -*-
"""
   
    Lexer for BitML language, based on Pygments Lisp lexer-

    :copyright: Copyright 2019 Stefano Lande
    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, include, bygroups, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Literal, Error

from pygments.lexers.python import PythonLexer

__all__ = ['BitmlLexer']


class BitmlLexer(RegexLexer):
    name = 'BitML'
    aliases = ['BITML', 'bitml']
    filenames = ['*.bitml', '*.rkt']

    # list of known keywords and builtins taken form vim 6.4 scheme.vim
    # syntax file.
    keywords = (
        'pre','sum','->','putrevealif','put','revealif','reveal','split','withdraw','after','auth','tau',
        'btrue','band','bor','bnot','b=','b!=','b<','b<=','b+','b-','bsize','pred','between','strategy',
        'b-if','do-reveal','do-auth','not-destory','do-destory','state','check-liquid','check','has-more-than','check-query'
    )
    builtins = ('*')

    # valid names for identifiers
    # well, names can only not consist fully of numbers
    # but this should be good enough for now
    valid_name = r'[\w!$%&*+,/:<=>?@^~|-]+'

    tokens = {
        'root': [
            # the comments
            # and going to the end of the line
            (r';.*$', Comment.Single),
            # multi-line comment
            (r'#\|', Comment.Multiline, 'multiline-comment'),
            # commented form (entire sexpr folliwng)
            (r'#;\s*\(', Comment, 'commented-form'),
            # signifies that the program text that follows is written with the
            # lexical and datum syntax described in r6rs
            (r'#!r6rs', Comment),

            # whitespaces - usually not relevant
            (r'\s+', Text),

            # numbers
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            # support for uncommon kinds of numbers -
            # have to figure out what the characters mean
            # (r'(#e|#i|#b|#o|#d|#x)[\d.]+', Number),

            # strings, symbols and characters
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"'" + valid_name, String.Symbol),
            (r"#\\([()/'\"._!§$%& ?=+-]|[a-zA-Z0-9]+)", String.Char),

            # constants
            (r'(#t|#f)', Name.Constant),

            # special operators
            (r"('|#|`|,@|,|\.)", Operator),

            # highlight the keywords
            ('(%s)' % '|'.join(re.escape(entry) + ' ' for entry in keywords),
             Keyword),

            # first variable in a quoted string like
            # '(this is syntactic sugar)
            (r"(?<='\()" + valid_name, Name.Variable),
            (r"(?<=#\()" + valid_name, Name.Variable),

            # highlight the builtins
            ("(?<=\()(%s)" % '|'.join(re.escape(entry) + ' ' for entry in builtins),
             Name.Builtin),

            # the remaining functions
            (r'(?<=\()' + valid_name, Name.Function),
            # find the remaining variables
            (valid_name, Name.Variable),

            # the famous parentheses!
            (r'(\(|\))', Punctuation),
            (r'(\[|\])', Punctuation),
        ],
        'multiline-comment': [
            (r'#\|', Comment.Multiline, '#push'),
            (r'\|#', Comment.Multiline, '#pop'),
            (r'[^|#]+', Comment.Multiline),
            (r'[|#]', Comment.Multiline),
        ],
        'commented-form': [
            (r'\(', Comment, '#push'),
            (r'\)', Comment, '#pop'),
            (r'[^()]+', Comment),
        ],
    }