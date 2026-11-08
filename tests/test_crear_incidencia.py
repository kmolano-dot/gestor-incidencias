import pytest


def test_crear_incidencia_valida_redirige(crear_incidencia):
    respuesta = crear_incidencia()
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"] == "/"


def test_crear_incidencia_guarda_los_datos(crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="Error 500 al guardar",
                     descripcion="La pagina falla al enviar el formulario",
                     prioridad="Alta")
    registros = leer_incidencias()
    assert len(registros) == 1
    assert registros[0]["titulo"] == "Error 500 al guardar"
    assert registros[0]["descripcion"] == "La pagina falla al enviar el formulario"
    assert registros[0]["prioridad"] == "Alta"


def test_incidencia_nueva_queda_en_estado_pendiente(crear_incidencia, leer_incidencias):
    crear_incidencia()
    assert leer_incidencias()[0]["estado"] == "Pendiente"


def test_identificadores_son_consecutivos(crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="Primera")
    crear_incidencia(titulo="Segunda")
    crear_incidencia(titulo="Tercera")
    assert [registro["id"] for registro in leer_incidencias()] == [1, 2, 3]


def test_se_eliminan_los_espacios_sobrantes(crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="   Fallo con espacios   ",
                     descripcion="   Descripcion con espacios   ")
    registro = leer_incidencias()[0]
    assert registro["titulo"] == "Fallo con espacios"
    assert registro["descripcion"] == "Descripcion con espacios"


def test_la_incidencia_aparece_en_el_listado(cliente, crear_incidencia):
    crear_incidencia(titulo="Fallo visible en el listado")
    contenido = cliente.get("/").get_data(as_text=True)
    assert "Fallo visible en el listado" in contenido


def test_titulo_de_150_caracteres_es_valido(crear_incidencia, leer_incidencias):
    respuesta = crear_incidencia(titulo="A" * 150)
    assert respuesta.status_code == 302
    assert len(leer_incidencias()) == 1


@pytest.mark.parametrize(
    "titulo, descripcion, prioridad, motivo",
    [
        ("", "Descripcion valida", "Media", "titulo vacio"),
        ("   ", "Descripcion valida", "Media", "titulo solo espacios"),
        ("Titulo valido", "", "Media", "descripcion vacia"),
        ("Titulo valido", "   ", "Media", "descripcion solo espacios"),
        ("A" * 151, "Descripcion valida", "Media", "titulo demasiado largo"),
        ("Titulo valido", "Descripcion valida", "Urgente", "prioridad invalida"),
        ("Titulo valido", "Descripcion valida", "", "prioridad vacia"),
        ("Titulo valido", "Descripcion valida", "media", "prioridad en minuscula"),
    ],
)
def test_datos_invalidos_devuelven_400(crear_incidencia, leer_incidencias,
                                       titulo, descripcion, prioridad, motivo):
    respuesta = crear_incidencia(titulo=titulo,
                                 descripcion=descripcion,
                                 prioridad=prioridad)
    assert respuesta.status_code == 400, f"se esperaba 400 por {motivo}"
    assert leer_incidencias() == [], f"no debe guardarse la incidencia con {motivo}"


def test_peticion_sin_campos_devuelve_400(cliente, leer_incidencias):
    respuesta = cliente.post("/incidencias", data={})
    assert respuesta.status_code == 400
    assert leer_incidencias() == []
