"""Pipeline completo: léxico -> sintáctico -> semántico."""
import re

from antlr4 import ParseTreeWalker
from antlr4.tree.Tree import ParseTreeListener

from .generated.SoundSpecParser import SoundSpecParser
from .semantico import Declaraciones, Verificador
from .sintactico import analizar_sintaxis


class CoberturaReglas(ParseTreeListener):
    """Registra las reglas de la gramática (y alternativas de propiedades) usadas."""

    def __init__(self, reglas, alternativas):
        self.reglas, self.alternativas = reglas, alternativas

    def enterEveryRule(self, ctx):
        nombre = SoundSpecParser.ruleNames[ctx.getRuleIndex()]
        self.reglas.add(nombre)
        if nombre in ("trackProp", "effectProp"):
            self.alternativas.add(f"{nombre}: {ctx.start.text}")


def compilar_soundspec(cod_fuente, reglas=None, alternativas=None):
    """Ejecuta las tres fases y devuelve la fase que rechaza el programa.

    Resultado: dict con 'fase' (LÉXICO, SINTÁCTICO, SEMÁNTICO o ACEPTADO),
    'codigos' (SEM-0X), 'lineas', 'mensajes' y, si se acepta, 'tabla' y 'arbol_texto'.
    """
    resultado = analizar_sintaxis(cod_fuente)
    if not resultado["valido"]:
        fase = resultado["errores"][0]["fase"] if resultado["errores"] else "SINTÁCTICO"
        return {"fase": fase, "codigos": set(), "lineas": set(),
                "mensajes": [f"[{e['fase']}] línea {e['linea']}, columna {e['columna']}: "
                             f"{e['mensaje']}" for e in resultado["errores"]],
                "tabla": {}, "arbol_texto": None}

    tabla, errores = {}, []
    ParseTreeWalker().walk(Declaraciones(tabla, errores), resultado["arbol"])
    ParseTreeWalker().walk(Verificador(tabla, errores), resultado["arbol"])

    if reglas is not None and alternativas is not None:
        ParseTreeWalker().walk(CoberturaReglas(reglas, alternativas), resultado["arbol"])

    if errores:
        errores.sort(key=lambda e: int(re.search(r"línea (\d+)", e).group(1)))
        return {"fase": "SEMÁNTICO",
                "codigos": {re.search(r"\[(SEM-\d+)\]", e).group(1) for e in errores},
                "lineas": {int(re.search(r"línea (\d+)", e).group(1)) for e in errores},
                "mensajes": errores, "tabla": tabla, "arbol_texto": None}
    return {"fase": "ACEPTADO", "codigos": set(), "lineas": set(), "mensajes": [],
            "tabla": tabla, "arbol_texto": resultado["arbol_texto"]}
