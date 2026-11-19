from antlr4.error.ErrorListener import ErrorListener


class ListenerErrores(ErrorListener):
    """Acumula los errores de ANTLR indicando fase, línea y columna (desde 1)."""

    def __init__(self, fase):
        super().__init__()
        self.fase = fase
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append({
            "fase": self.fase,
            "linea": line,
            "columna": column + 1,
            "mensaje": msg,
        })
