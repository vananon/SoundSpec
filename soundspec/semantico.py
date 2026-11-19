"""Fase 3: análisis semántico (tabla de símbolos y dos recorridos del árbol).

Pasada 1 (Declaraciones): registra track/effect/mix y detecta SEM-01.
Pasada 2 (Verificador):   detecta SEM-02 a SEM-06.
"""
from fractions import Fraction

from .generated.SoundSpecParserListener import SoundSpecParserListener

SEMITONO = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ALTERACION = {'': 0, '#': 1, 'b': -1}


def frecuencia(nota):
    """Frecuencia en Hz de una nota como 'C#4' (A4 = 440 Hz, MIDI 69)."""
    midi = 12 * (int(nota[-1]) + 1) + SEMITONO[nota[0]] + ALTERACION[nota[1:-1]]
    return 440 * 2 ** ((midi - 69) / 12)


class Declaraciones(SoundSpecParserListener):
    """Pasada 1: llena la tabla {nombre: (categoría, línea)} y detecta SEM-01."""

    def __init__(self, tabla, errores):
        self.tabla, self.errores = tabla, errores

    def declarar(self, token, categoria):
        if token.text in self.tabla:
            cat, linea = self.tabla[token.text]
            self.errores.append(
                f"[SEM-01] línea {token.line}: '{token.text}' ya fue declarado "
                f"como {cat} en la línea {linea}.")
        else:
            self.tabla[token.text] = (categoria, token.line)

    def enterTrackDecl(self, ctx):
        self.declarar(ctx.ID().symbol, 'track')

    def enterEffectDecl(self, ctx):
        self.declarar(ctx.ID().symbol, 'effect')

    def enterMixRule(self, ctx):
        self.declarar(ctx.ID(0).symbol, 'mix')


class Verificador(SoundSpecParserListener):
    """Pasada 2: detecta SEM-02 a SEM-06."""

    def __init__(self, tabla, errores):
        self.tabla, self.errores = tabla, errores

    def enterNoteList(self, ctx):
        total = Fraction(0)
        for item in ctx.noteItem():
            nota = item.NOTE().getText()
            linea = item.start.line
            f = frecuencia(nota)
            if not 20 <= f <= 20000:
                self.errores.append(
                    f"[SEM-03] línea {linea}: la nota {nota} ({f:.2f} Hz) "
                    f"está fuera del rango audible.")
            duracion = item.FRACTION().getText()
            num, den = map(int, duracion.split('/'))
            if num == 0 or den == 0:
                # La nota no se suma al compás porque su duración no es válida
                self.errores.append(
                    f"[SEM-06] línea {linea}: la nota {nota} tiene una "
                    f"duración inválida ({duracion}).")
            else:
                total += Fraction(num, den)
        if total.denominator != 1:
            self.errores.append(
                f"[SEM-04] línea {ctx.start.line}: las duraciones suman "
                f"{total} de compás; falta {1 - total % 1}.")

    def enterMixRule(self, ctx):
        ids, linea = ctx.ID(), ctx.start.line
        fuente = ids[1].getText()
        if fuente not in self.tabla:
            self.errores.append(
                f"[SEM-02] línea {linea}: la pista '{fuente}' no ha sido declarada.")
        elif self.tabla[fuente][0] != 'track':
            self.errores.append(
                f"[SEM-05] línea {linea}: '{fuente}' fue declarado como "
                f"{self.tabla[fuente][0]}, pero la fuente de un mix debe ser un track.")
        for efecto in ids[2:]:
            nombre = efecto.getText()
            if nombre not in self.tabla:
                self.errores.append(
                    f"[SEM-02] línea {linea}: el efecto '{nombre}' no ha sido declarado.")
            elif self.tabla[nombre][0] != 'effect':
                self.errores.append(
                    f"[SEM-05] línea {linea}: '{nombre}' fue declarado como "
                    f"{self.tabla[nombre][0]}, pero la cadena de un mix solo admite effects.")
