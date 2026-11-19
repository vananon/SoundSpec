"""Fase 2: análisis sintáctico (la fase léxica se ejecuta primero)."""
from antlr4 import InputStream, CommonTokenStream

from .errores import ListenerErrores
from .generated.SoundSpecLexer import SoundSpecLexer
from .generated.SoundSpecParser import SoundSpecParser


def analizar_sintaxis(cod_fuente):
    """Valida toda la entrada. No realiza comprobaciones semánticas."""
    lexer = SoundSpecLexer(InputStream(cod_fuente))
    errores_lexicos = ListenerErrores("LÉXICO")
    lexer.removeErrorListeners()
    lexer.addErrorListener(errores_lexicos)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    # Un carácter rechazado por el lexer no debe desaparecer silenciosamente.
    if errores_lexicos.errores:
        return {"valido": False, "errores": errores_lexicos.errores,
                "arbol": None, "arbol_texto": None}

    tokens.seek(0)
    parser = SoundSpecParser(tokens)
    errores_sintacticos = ListenerErrores("SINTÁCTICO")
    parser.removeErrorListeners()
    parser.addErrorListener(errores_sintacticos)
    arbol = parser.program()
    valido = parser.getNumberOfSyntaxErrors() == 0
    return {
        "valido": valido,
        "errores": errores_sintacticos.errores,
        "arbol": arbol if valido else None,
        "arbol_texto": arbol.toStringTree(recog=parser) if valido else None,
    }
