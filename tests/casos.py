"""Plan de validación: (id, categoría, descripción, código, fase esperada, códigos SEM, línea)."""
from pathlib import Path

ESTRELLITA = (Path(__file__).resolve().parent.parent / "examples" / "estrellita.soundspec"
              ).read_text(encoding="utf-8")

A = "ACEPTADO"
CASOS = [
    # --- Aceptación ---
    ("A01", "Aceptación", "Pista con las tres propiedades",
     "track Bajo { bpm: 120; wave: SAWTOOTH; notes: [C2:1/4, E2:1/4, G2:1/2]; }", A, set(), None),
    ("A02", "Aceptación", "Notas sin «:», sostenidos y bemoles",
     "track Alt { notes: [C#4 1/2, Db4 1/4, Bb3 1/4]; }", A, set(), None),
    ("A03", "Aceptación", "Efecto con delay y decay",
     "effect Eco { delay: 300ms; decay: 0.85; }", A, set(), None),
    ("A04", "Aceptación", "Mix con cadena de dos efectos",
     "track M { wave: SINE; }\neffect Eco { delay: 80ms; }\neffect Sala { decay: 0.3; }\nmix S = M -> Eco -> Sala;",
     A, set(), None),
    ("A05", "Aceptación", "Mix declarado antes que su pista",
     "mix S = M;\ntrack M { bpm: 90; }", A, set(), None),
    ("A06", "Aceptación", "Duraciones que completan dos compases",
     "track Larga { notes: [C4 3/2, G4 1/2]; }", A, set(), None),
    ("A07", "Aceptación", "Comentarios y propiedades en otro orden",
     "// comentario\ntrack T { wave: TRIANGLE; bpm: 100; } // fin", A, set(), None),
    ("A08", "Aceptación", "Frontera inferior audible: E0 (20.60 Hz)",
     "track Grave { notes: [E0 1/1]; }", A, set(), None),
    ("A09", "Aceptación", "Onda SQUARE y nota más aguda B8 (7902 Hz)",
     "track Agudo { wave: SQUARE; notes: [B8 1/1]; }", A, set(), None),
    # --- Léxico ---
    ("L01", "Léxico", "Carácter no reconocido «@»", "track T { bpm: 120; } @", "LÉXICO", set(), None),
    ("L02", "Léxico", "Identificador con tilde", "track Atmósfera { bpm: 120; }", "LÉXICO", set(), None),
    ("L03", "Léxico", "Símbolo «$» dentro de una lista", "track T { notes: [C4 $1/1]; }", "LÉXICO", set(), None),
    # --- Sintáctico ---
    ("S01", "Sintáctico", "Programa vacío", "", "SINTÁCTICO", set(), None),
    ("S02", "Sintáctico", "«=» en lugar de «:»", "track T { bpm = 120; }", "SINTÁCTICO", set(), None),
    ("S03", "Sintáctico", "Falta «;»", "track T { bpm: 120 }", "SINTÁCTICO", set(), None),
    ("S04", "Sintáctico", "Falta «}»", "effect E { delay: 300ms;", "SINTÁCTICO", set(), None),
    ("S05", "Sintáctico", "Falta coma entre notas", "track T { notes: [C4 1/2 D4 1/2]; }", "SINTÁCTICO", set(), None),
    ("S06", "Sintáctico", "Lista de notas vacía", "track T { notes: []; }", "SINTÁCTICO", set(), None),
    ("S07", "Sintáctico", "Bloque de efecto vacío", "effect E { }", "SINTÁCTICO", set(), None),
    ("S08", "Sintáctico", "«->» sin efecto", "mix S = T -> ;", "SINTÁCTICO", set(), None),
    ("S09", "Sintáctico", "bpm con decimal", "track T { bpm: 120.5; }", "SINTÁCTICO", set(), None),
    ("S10", "Sintáctico", "delay sin unidad ms", "effect E { delay: 300; }", "SINTÁCTICO", set(), None),
    ("S11", "Sintáctico", "Texto sobrante después del programa",
     "track T { bpm: 120; } sobrante", "SINTÁCTICO", set(), None),
    # --- Semántico ---
    ("E01", "Semántico", "track y effect con el mismo nombre",
     "track M { bpm: 90; }\neffect M { decay: 0.5; }", "SEMÁNTICO", {"SEM-01"}, 2),
    ("E02", "Semántico", "Pista fuente no declarada", "mix S = Guitarra;", "SEMÁNTICO", {"SEM-02"}, 1),
    ("E03", "Semántico", "Efecto no declarado en la cadena",
     "track M { bpm: 90; }\nmix S = M -> Reverb;", "SEMÁNTICO", {"SEM-02"}, 2),
    ("E04", "Semántico", "Nota bajo 20 Hz: D#0 (19.45 Hz)",
     "track G { notes: [D#0 1/1]; }", "SEMÁNTICO", {"SEM-03"}, 1),
    ("E05", "Semántico", "Compás incompleto (3/4)",
     "track M { notes: [C4 1/4, D4 1/4, E4 1/4]; }", "SEMÁNTICO", {"SEM-04"}, 1),
    ("E06", "Semántico", "Fuente del mix es un effect",
     "effect E { delay: 80ms; }\nmix S = E;", "SEMÁNTICO", {"SEM-05"}, 2),
    ("E07", "Semántico", "Cadena del mix contiene un track",
     "track M { bpm: 90; }\nmix S = M -> M;", "SEMÁNTICO", {"SEM-05"}, 2),
    ("E08", "Semántico", "Duración con denominador 0",
     "track M { notes: [C4 1/0, D4 1/1]; }", "SEMÁNTICO", {"SEM-06"}, 1),
    ("E09", "Semántico", "Duración con numerador 0",
     "track M { notes: [C4 0/4, D4 1/1]; }", "SEMÁNTICO", {"SEM-06"}, 1),
    ("E10", "Semántico", "Varios errores en un mismo programa",
     "track M { notes: [C0 1/4]; }\neffect M { decay: 0.5; }\nmix S = X -> M;",
     "SEMÁNTICO", {"SEM-01", "SEM-02", "SEM-03", "SEM-04", "SEM-05"}, None),
    # --- Integración ---
    ("I01", "Integración", "Programa completo «Estrellita» (42 notas)", ESTRELLITA, A, set(), None),
]
