#!/usr/bin/env bash
# Genera el lexer y el parser de ANTLR en soundspec/generated/.
# Uso: ./scripts/generar_parser.sh   (requiere Java 11+)
set -euo pipefail
cd "$(dirname "$0")/.."

JAR="antlr-4.13.2-complete.jar"
if [ ! -f "$JAR" ]; then
  curl -L -o "$JAR" "https://www.antlr.org/download/$JAR"
fi

java -jar "$JAR" -Dlanguage=Python3 -listener \
  -o soundspec/generated -Xexact-output-dir \
  grammar/SoundSpecLexer.g4 grammar/SoundSpecParser.g4

# El archivo __init__.py convierte la carpeta en un paquete importable.
touch soundspec/generated/__init__.py
echo "Parser generado en soundspec/generated/"
