from typing import Set

from talon import Module, Context, actions

mod = Module()
mod.list('letter',   desc='The spoken phonetic alphabet')
mod.list('symbol',   desc='All symbols from the keyboard')
mod.list('arrow',    desc='All arrow keys')
mod.list('number',   desc='All number keys')
mod.list('modifier', desc='All modifier keys')
mod.list('special',  desc='All special keys')

@mod.capture
def modifiers(m) -> Set[str]:
    "One or more modifier keys"

@mod.capture
def arrow(m) -> str:
    "One directional arrow key"

@mod.capture
def number(m) -> str:
    "One number key"

@mod.capture
def letter(m) -> str:
    "One letter key"

@mod.capture
def symbol(m) -> str:
    "One symbol key"

@mod.capture
def special(m) -> str:
    "One special key"

@mod.capture
def any(m) -> str:
    "Any one key"

@mod.capture
def key(m) -> str:
    "A single key with optional modifiers"

ctx = Context()

ctx.lists['self.modifier'] = {
    'command': 'cmd',
    'control': 'ctrl',   'troll':   'ctrl',
    'shift':   'shift',  'sky':     'shift',
    'alt':     'alt',    'option':  'alt',
}

ctx.lists['self.arrow'] = {
    'left':  'left',
    'right': 'right',
    'up':    'up',
    'down':  'down',
}

ctx.lists['self.number'] = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

ctx.lists['self.letter'] = {
    'air': 'a',
    'bat': 'b',
    'cap': 'c',
    'drum': 'd',
    'each': 'e',
    'fine': 'f',
    'gust': 'g',
    'harp': 'h',
    'sit': 'i',
    'jury': 'j',
    'crunch': 'k',
    'look': 'l',
    'made': 'm',
    'near': 'n',
    'odd': 'o',
    'pit': 'p',
    'quench': 'q',
    'red': 'r',
    'sun': 's',
    'trap': 't',
    'urge': 'u',
    'vest': 'v',
    'whale': 'w',
    'plex': 'x',
    'yank': 'y',
    'zip': 'z',
}

ctx.lists['self.symbol'] = {
    'back tick': '`',
    'comma': ',',
    'dot': '.', 'period': '.',
    'semi': ';', 'semicolon': ';',
    'quote': "'",
    'L square': '[', 'left square': '[', 'square': '[',
    'R square': ']', 'right square': ']',
    'forward slash': '/', 'slash': '/',
    'backslash': '\\',
    'minus': '-', 'dash': '-',
    'equals': '=',
    'plus': '+',
    'question mark': '?',
    'tilde': '~',
    'bang': '!', 'exclamation point': '!',
    'dollar': '$', 'dollar sign': '$',
    'down score': '_', 'under score': '_',
    'colon': ':',
    'paren': '(', 'L paren': '(', 'left paren': '(',
    'R paren': ')', 'right paren': ')',
    'brace': '{', 'left brace': '{',
    'R brace': '}', 'right brace': '}',
    'angle': '<', 'left angle': '<', 'less than': '<',
    'rangle': '>', 'R angle': '>', 'right angle': '>', 'greater than': '>',
    'star': '*', 'asterisk': '*',
    'pound': '#', 'hash': '#', 'hash sign': '#', 'number sign': '#',
    'percent': '%', 'percent sign': '%',
    'caret': '^',
    'at sign': '@',
    'and sign': '&', 'ampersand': '&', 'amper': '&',
    'pipe': '|',
    'dubquote': '"', 'double quote': '"',
}

simple_keys = [
    'tab', 'escape', 'enter', 'space',
    'home', 'pageup', 'pagedown', 'end',
]
alternate_keys = {
    'delete': 'backspace', 'junk': 'backspace',
    'forward delete': 'delete',
}
keys = {k: k for k in simple_keys}
keys.update(alternate_keys)
ctx.lists['self.special'] = keys

@ctx.capture(rule='{self.modifier}+')
def modifiers(m):
    return set(m.modifier)

@ctx.capture(rule='{self.arrow}')
def arrow(m) -> str:
    return m.arrow

@ctx.capture(rule='{self.number}')
def number(m):
    return m.number

@ctx.capture(rule='{self.letter}')
def letter(m):
    return m.letter

@ctx.capture(rule='{self.special}')
def special(m):
    return m.special

@ctx.capture(rule='{self.symbol}')
def symbol(m):
    return m.symbol

@ctx.capture(rule='(<self.arrow> | <self.number> | <self.letter> | <self.special>)')
def any(m) -> str:
    for name in ('arrow', 'number', 'letter', 'special'):
        value = m.get(name)
        if value is not None:
            return value
    raise AttributeError(f'No key found in capture: {m}')

@ctx.capture(rule='[<self.modifiers>] <self.any>')
def key(m) -> str:
    key = m.any
    mods = m.get('modifiers', None)
    if mods:
        mods = '-'.join(mods[0])
        key = f'{mods}-{key}'
    return key

ctx.commands = {
    'go <self.arrow>': lambda m: actions.key(m.arrow),
    '<self.number>': lambda m: actions.key(m.number),
    '<self.letter>': lambda m: actions.key(m.letter),
    '<self.symbol>': lambda m: actions.key(m.symbol),
    '<self.special>': lambda m: actions.key(m.special),
    '<self.key>': lambda m: actions.key(m.key),
}
