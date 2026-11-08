def test_eliminar_incidencia_existente(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia()
    respuesta = cliente.post("/incidencias/1/eliminar")
    assert respuesta.status_code == 302
    assert leer_incidencias() == []


def test_la_incidencia_desaparece_del_listado(cliente, crear_incidencia):
    crear_incidencia(titulo="Incidencia por borrar")
    cliente.post("/incidencias/1/eliminar")
    contenido = cliente.get("/").get_data(as_text=True)
    assert "Incidencia por borrar" not in contenido
    assert "No hay incidencias registradas" in contenido


def test_eliminar_incidencia_inexistente_devuelve_404(cliente):
    respuesta = cliente.post("/incidencias/999/eliminar")
    assert respuesta.status_code == 404


def test_borrar_una_no_afecta_a_las_demas(cliente, crear_incidencia, leer_incidencias):
    crear_incidencia(titulo="Primera")
    crear_incidencia(titulo="Segunda")
    crear_incidencia(titulo="Tercera")
    cliente.post("/incidencias/2/eliminar")
    titulos = [registro["titulo"] for registro in leer_incidencias()]
    assert titulos == ["Primera", "Tercera"]


def test_no_se_puede_borrar_dos_veces(cliente, crear_incidencia):
    crear_incidencia()
    cliente.post("/incidencias/1/eliminar")
    respuesta = cliente.post("/incidencias/1/eliminar")
    assert respuesta.status_code == 404
