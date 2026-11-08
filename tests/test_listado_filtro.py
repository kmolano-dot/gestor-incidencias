import pytest


def test_listado_vacio_responde_200(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200


def test_listado_vacio_muestra_mensaje(cliente):
    contenido = cliente.get("/").get_data(as_text=True)
    assert "No hay incidencias registradas" in contenido


@pytest.fixture
def tres_estados(cliente, crear_incidencia):
    crear_incidencia(titulo="Incidencia pendiente")
    crear_incidencia(titulo="Incidencia en proceso")
    crear_incidencia(titulo="Incidencia resuelta")
    cliente.post("/incidencias/2/estado", data={"estado": "En proceso"})
    cliente.post("/incidencias/3/estado", data={"estado": "Resuelta"})


def test_sin_filtro_muestra_todas(cliente, tres_estados):
    contenido = cliente.get("/").get_data(as_text=True)
    assert "Incidencia pendiente" in contenido
    assert "Incidencia en proceso" in contenido
    assert "Incidencia resuelta" in contenido


@pytest.mark.parametrize(
    "estado, visible, ocultas",
    [
        ("Pendiente", "Incidencia pendiente",
         ["Incidencia en proceso", "Incidencia resuelta"]),
        ("En proceso", "Incidencia en proceso",
         ["Incidencia pendiente", "Incidencia resuelta"]),
        ("Resuelta", "Incidencia resuelta",
         ["Incidencia pendiente", "Incidencia en proceso"]),
    ],
)
def test_filtro_muestra_solo_el_estado_pedido(cliente, tres_estados,
                                              estado, visible, ocultas):
    contenido = cliente.get("/", query_string={"estado": estado}).get_data(as_text=True)
    assert visible in contenido
    for oculta in ocultas:
        assert oculta not in contenido


def test_filtro_todos_muestra_las_tres(cliente, tres_estados):
    contenido = cliente.get("/", query_string={"estado": "Todos"}).get_data(as_text=True)
    assert "Incidencia pendiente" in contenido
    assert "Incidencia en proceso" in contenido
    assert "Incidencia resuelta" in contenido


def test_filtro_invalido_se_comporta_como_todos(cliente, tres_estados):
    contenido = cliente.get("/", query_string={"estado": "Inventado"}).get_data(as_text=True)
    assert "Incidencia pendiente" in contenido
    assert "Incidencia en proceso" in contenido
    assert "Incidencia resuelta" in contenido
