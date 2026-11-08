import pytest


def _datos(titulo="Titulo corregido",
           descripcion="Descripcion corregida",
           prioridad="Alta"):
    return {"titulo": titulo, "descripcion": descripcion, "prioridad": prioridad}


def test_edicion_valida_actualiza_los_datos(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia()
    respuesta = cliente.post("/incidencias/1/editar", data=_datos())
    assert respuesta.status_code == 302
    registro = leer_incidencias()[0]
    assert registro["titulo"] == "Titulo corregido"
    assert registro["descripcion"] == "Descripcion corregida"
    assert registro["prioridad"] == "Alta"


def test_la_edicion_no_cambia_el_id_ni_el_estado(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia()
    cliente.post("/incidencias/1/estado", data={"estado": "En proceso"})
    cliente.post("/incidencias/1/editar", data=_datos())
    registro = leer_incidencias()[0]
    assert registro["id"] == 1
    assert registro["estado"] == "En proceso"


@pytest.mark.parametrize(
    "datos, motivo",
    [
        (_datos(titulo=""), "titulo vacio"),
        (_datos(titulo="   "), "titulo solo espacios"),
        (_datos(descripcion=""), "descripcion vacia"),
        (_datos(titulo="A" * 151), "titulo demasiado largo"),
        (_datos(prioridad="Urgente"), "prioridad invalida"),
        ({}, "peticion sin campos"),
    ],
)
def test_datos_invalidos_devuelven_400(cliente, crear_incidencia, leer_incidencias,
                                       datos, motivo):
    crear_incidencia(titulo="Original", descripcion="Original", prioridad="Baja")
    respuesta = cliente.post("/incidencias/1/editar", data=datos)
    assert respuesta.status_code == 400, f"se esperaba 400 por {motivo}"
    registro = leer_incidencias()[0]
    assert registro["titulo"] == "Original", f"no debe cambiar con {motivo}"
    assert registro["prioridad"] == "Baja", f"no debe cambiar con {motivo}"


def test_incidencia_inexistente_devuelve_404(cliente):
    respuesta = cliente.post("/incidencias/999/editar", data=_datos())
    assert respuesta.status_code == 404


def test_solo_edita_la_incidencia_indicada(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="Primera")
    crear_incidencia(titulo="Segunda")
    cliente.post("/incidencias/2/editar", data=_datos(titulo="Segunda corregida"))
    registros = leer_incidencias()
    assert registros[0]["titulo"] == "Primera"
    assert registros[1]["titulo"] == "Segunda corregida"
