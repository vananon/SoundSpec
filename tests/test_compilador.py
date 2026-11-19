import pytest

pytest.importorskip(
    "soundspec.generated.SoundSpecParser",
    reason="Genera el parser primero: ./scripts/generar_parser.sh")

from soundspec import compilar_soundspec  # noqa: E402
from tests.casos import CASOS  # noqa: E402


@pytest.mark.parametrize("cid,cat,desc,codigo,fase,codigos,linea", CASOS,
                         ids=[c[0] for c in CASOS])
def test_caso(cid, cat, desc, codigo, fase, codigos, linea):
    r = compilar_soundspec(codigo)
    assert r["fase"] == fase, r["mensajes"]
    if codigos:
        assert r["codigos"] == codigos, r["mensajes"]
    if linea is not None:
        assert linea in r["lineas"], r["mensajes"]
