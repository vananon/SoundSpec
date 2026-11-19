"""Uso: python -m soundspec programa.soundspec [--arbol]"""
import argparse
import sys
from pathlib import Path

from .compilador import compilar_soundspec


def main(argv=None):
    ap = argparse.ArgumentParser(prog="soundspec",
                                 description="Compilador SoundSpec (léxico, sintáctico, semántico)")
    ap.add_argument("archivo", help="archivo .soundspec de entrada")
    ap.add_argument("--arbol", action="store_true", help="imprime el árbol sintáctico")
    args = ap.parse_args(argv)

    resultado = compilar_soundspec(Path(args.archivo).read_text(encoding="utf-8"))
    if resultado["fase"] != "ACEPTADO":
        print(f"Rechazado en la fase {resultado['fase']}:")
        for m in resultado["mensajes"]:
            print("  " + m)
        return 1

    print("Programa aceptado por las tres fases (léxico, sintáctico, semántico).")
    print("Tabla de símbolos:")
    for nombre, (cat, linea) in resultado["tabla"].items():
        print(f"  {nombre:<22} {cat:<8} línea {linea}")
    if args.arbol:
        print("\nÁrbol sintáctico:\n" + resultado["arbol_texto"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
