import pytest


@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Resuelta"])
def test_estados_validos_se_guardan(cliente, crear_incidencia, leer_incidencias, estado):
    crear_incidencia()
    respuesta = cliente.post("/incidencias/1/estado", data={"estado": estado})
    assert respuesta.status_code == 302
    assert leer_incidencias()[0]["estado"] == estado


@pytest.mark.parametrize("estado", ["Cerrada", "pendiente", "", "EN PROCESO"])
def test_estado_invalido_devuelve_400(cliente, crear_incidencia, leer_incidencias, estado):
    crear_incidencia()
    respuesta = cliente.post("/incidencias/1/estado", data={"estado": estado})
    assert respuesta.status_code == 400
    assert leer_incidencias()[0]["estado"] == "Pendiente"


def test_incidencia_inexistente_devuelve_404(cliente):
    respuesta = cliente.post("/incidencias/999/estado", data={"estado": "Resuelta"})
    assert respuesta.status_code == 404


def test_solo_cambia_la_incidencia_indicada(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="Primera")
    crear_incidencia(titulo="Segunda")
    cliente.post("/incidencias/2/estado", data={"estado": "Resuelta"})
    registros = leer_incidencias()
    assert registros[0]["estado"] == "Pendiente"
    assert registros[1]["estado"] == "Resuelta"
