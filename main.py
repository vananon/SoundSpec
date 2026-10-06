import sys
from fractions import Fraction
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

try:
    from grammar.SoundSpecLexer import SoundSpecLexer
    from grammar.SoundSpecParser import SoundSpecParser
    from grammar.SoundSpecParserListener import SoundSpecParserListener
except ImportError:
    print("Error: No se encontraron los archivos generados por ANTLR en 'grammar/'.")
    print("Por favor, ejecuta los comandos de generación primero.")
    sys.exit(1)

class ListenerErrores(ErrorListener):
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

def analizar_sintaxis(cod_fuente):
    lexer = SoundSpecLexer(InputStream(cod_fuente))
    errores_lexicos = ListenerErrores("LÉXICO")
    lexer.removeErrorListeners()
    lexer.addErrorListener(errores_lexicos)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

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

SEMITONO = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ALTERACION = {'': 0, '#': 1, 'b': -1}

def frecuencia(nota):
    midi = 12 * (int(nota[-1]) + 1) + SEMITONO[nota[0]] + ALTERACION[nota[1:-1]]
    return 440 * 2 ** ((midi - 69) / 12)

class Declaraciones(SoundSpecParserListener):
    def __init__(self, tabla, errores):
        self.tabla, self.errores = tabla, errores

    def declarar(self, token, categoria):
        if token.text in self.tabla:
            cat, linea = self.tabla[token.text]
            self.errores.append(f"[SEM-01] línea {token.line}: '{token.text}' ya fue declarado como {cat} en la línea {linea}.")
        else:
            self.tabla[token.text] = (categoria, token.line)

    def enterTrackDecl(self, ctx):  self.declarar(ctx.ID().symbol, 'track')
    def enterEffectDecl(self, ctx): self.declarar(ctx.ID().symbol, 'effect')
    def enterMixRule(self, ctx):    self.declarar(ctx.ID(0).symbol, 'mix')

class Verificador(SoundSpecParserListener):
    def __init__(self, tabla, errores):
        self.tabla, self.errores = tabla, errores

    def enterNoteList(self, ctx):
        total = Fraction(0)
        for item in ctx.noteItem():
            nota = item.NOTE().getText()
            linea = item.start.line
            f = frecuencia(nota)
            if not 20 <= f <= 20000:
                self.errores.append(f"[SEM-03] línea {linea}: la nota {nota} ({f:.2f} Hz) está fuera del rango audible.")
            duracion = item.FRACTION().getText()
            num, den = map(int, duracion.split('/'))
            if num == 0 or den == 0:
                self.errores.append(f"[SEM-06] línea {linea}: la nota {nota} tiene una duración inválida ({duracion}).")
            else:
                total += Fraction(num, den)
        if total.denominator != 1:
            self.errores.append(f"[SEM-04] línea {ctx.start.line}: las duraciones suman {total} de compás; falta {1 - total % 1}.")

    def enterMixRule(self, ctx):
        ids, linea = ctx.ID(), ctx.start.line
        fuente = ids[1].getText()
        if fuente not in self.tabla:
            self.errores.append(f"[SEM-02] línea {linea}: la pista '{fuente}' no ha sido declarada.")
        elif self.tabla[fuente][0] != 'track':
            self.errores.append(f"[SEM-05] línea {linea}: '{fuente}' fue declarado como {self.tabla[fuente][0]}, pero la fuente de un mix debe ser un track.")
        for efecto in ids[2:]:
            nombre = efecto.getText()
            if nombre not in self.tabla:
                self.errores.append(f"[SEM-02] línea {linea}: el efecto '{nombre}' no ha sido declarado.")
            elif self.tabla[nombre][0] != 'effect':
                self.errores.append(f"[SEM-05] línea {linea}: '{nombre}' fue declarado como {self.tabla[nombre][0]}, pero la cadena de un mix solo admite effects.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.snd>")
        return

    archivo = sys.argv[1]
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            cod_fuente = f.read()
    except FileNotFoundError:
        print(f"Error: no se pudo abrir el archivo '{archivo}'.")
        return

    print(f"--- Compilando {archivo} ---")
    resultado = analizar_sintaxis(cod_fuente)
    
    errores_totales = []
    
    if not resultado["valido"]:
        for e in resultado["errores"]:
            errores_totales.append(f"[{e['fase']}] línea {e['linea']}, columna {e['columna']}: {e['mensaje']}")
    else:
        tabla = {}
        ParseTreeWalker().walk(Declaraciones(tabla, errores_totales), resultado["arbol"])
        ParseTreeWalker().walk(Verificador(tabla, errores_totales), resultado["arbol"])
        
        def extract_line(e):
            try:
                return int(e.split("línea ")[1].split(":")[0])
            except Exception:
                return 0
        
        errores_totales.sort(key=extract_line)

    if errores_totales:
        print("Errores encontrados:")
        print("\n".join(errores_totales))
    else:
        print("Compilación exitosa. Sin errores léxicos, sintácticos ni semánticos.")

if __name__ == '__main__':
    main()
