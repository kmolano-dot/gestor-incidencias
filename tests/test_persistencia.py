import pytest

import app as modulo_app

pytestmark = pytest.mark.skip(
    reason="pendiente: requiere la integracion de Flask con PostgreSQL"
)


@pytest.mark.postgres
def test_la_incidencia_no_se_guarda_en_memoria(crear_incidencia):
    crear_incidencia()
    assert modulo_app.incidencias == []


@pytest.mark.postgres
def test_la_base_asigna_la_fecha_de_creacion(crear_incidencia, leer_incidencias):
    crear_incidencia()
    assert leer_incidencias()[0]["fecha_creacion"] is not None


@pytest.mark.postgres
def test_la_fecha_de_actualizacion_cambia_al_editar(cliente, crear_incidencia,
                                                    leer_incidencias):
    crear_incidencia()
    fecha_inicial = leer_incidencias()[0]["fecha_actualizacion"]
    cliente.post("/incidencias/1/editar", data={
        "titulo": "Titulo corregido",
        "descripcion": "Descripcion corregida",
        "prioridad": "Alta",
    })
    assert leer_incidencias()[0]["fecha_actualizacion"] > fecha_inicial
