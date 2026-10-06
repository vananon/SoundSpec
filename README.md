# SoundSpec

SoundSpec es un lenguaje de dominio específico (DSL) diseñado para la síntesis y composición musical algorítmica. Permite definir pistas musicales, efectos de audio y mezclas (mix) mediante una sintaxis estructurada y fácil de leer.

## Integrantes
- Vanessa Barrientos Villalta - U202413287
- Matias Javier Del Castillo Mendoza - U202411305
- Vivianne Fatima Ríos Hasegawa - U202410135

## Requisitos
- Python 3.x
- Java (necesario únicamente para generar el parser con ANTLR)
- Las dependencias de Python listadas en `requirements.txt`. Instalar con:
  ```bash
  pip install -r requirements.txt
  ```

## Generación del Parser (ANTLR)
Si modificas los archivos `.g4` en la carpeta `grammar/`, debes regenerar los analizadores usando el archivo `.jar` de ANTLR:

```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 grammar/SoundSpecLexer.g4
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -listener grammar/SoundSpecParser.g4
```

## Ejecución del Driver
Para analizar un código fuente escrito en SoundSpec, ejecuta el driver `main.py` pasando el archivo `.snd` por argumento:

```bash
python main.py ejemplos/ejemplo_valido.snd
```

## Tabla de Errores Semánticos

| Código | Error | Regla |
|---|---|---|
| **SEM-01** | Identificador redeclarado | Cada `track`, `effect` y `mix` tiene un nombre único. |
| **SEM-02** | Referencia no declarada | La pista y los efectos de un `mix` deben estar declarados. |
| **SEM-03** | Nota fuera de rango | 20 Hz ≤ frecuencia ≤ 20 000 Hz. |
| **SEM-04** | Compás incompleto | Las duraciones de `notes` deben completar compases enteros. |
| **SEM-05** | Categoría incorrecta | La fuente en `mix` debe ser un `track` y la cadena solo admite `effect`. |
| **SEM-06** | Duración inválida | El numerador y denominador de la duración deben ser mayores que 0. |

## Ejemplo de Salida Real

**Ejecución con código válido:**
```bash
> python main.py ejemplos/ejemplo_valido.snd
--- Compilando ejemplos/ejemplo_valido.snd ---
Compilación exitosa. Sin errores léxicos, sintácticos ni semánticos.
```

**Ejecución con errores (`ejemplo_errores.snd`):**
```bash
> python main.py ejemplos/ejemplo_errores.snd
--- Compilando ejemplos/ejemplo_errores.snd ---
Errores encontrados:
[SEM-04] línea 2: las duraciones suman 1/4 de compás; falta 3/4.
[SEM-01] línea 3: 'Pista1' ya fue declarado como track en la línea 1.
[SEM-03] línea 3: la nota C0 (16.35 Hz) está fuera del rango audible.
[SEM-06] línea 3: la nota C0 tiene una duración inválida (1/0).
[SEM-05] línea 5: 'Efecto1' fue declarado como effect, pero la fuente de un mix debe ser un track.
[SEM-02] línea 5: el efecto 'NoDeclarado' no ha sido declarado.
```
