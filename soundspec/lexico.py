"""Fase 1: análisis léxico."""
from antlr4 import InputStream

from .errores import ListenerErrores
from .generated.SoundSpecLexer import SoundSpecLexer


def tokenizar(cod_fuente):
    """Devuelve (lista de (TOKEN, lexema), errores léxicos)."""
    lexer = SoundSpecLexer(InputStream(cod_fuente))
    errores = ListenerErrores("LÉXICO")
    lexer.removeErrorListeners()
    lexer.addErrorListener(errores)
    tokens = [(lexer.symbolicNames[t.type], t.text) for t in lexer.getAllTokens()]
    return tokens, errores.errores
