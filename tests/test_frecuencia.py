"""Pruebas de la utilidad de frecuencias; no requieren el parser generado."""
import importlib.util
import math
import re
from pathlib import Path

# Se extrae `frecuencia` del módulo sin importar los archivos generados por ANTLR.
src = (Path(__file__).resolve().parent.parent / "soundspec" / "semantico.py").read_text(encoding="utf-8")
ns = {}
exec(re.search(r"SEMITONO = .*?\n\n\ndef frecuencia.*?\n\n\n", src, re.S).group(0), ns)
frecuencia = ns["frecuencia"]


def test_a4_es_440():
    assert math.isclose(frecuencia("A4"), 440.0)


def test_limites_audibles():
    assert frecuencia("E0") >= 20
    assert frecuencia("D#0") < 20
    assert frecuencia("B8") <= 20000


def test_enarmonicos():
    assert math.isclose(frecuencia("C#4"), frecuencia("Db4"))
