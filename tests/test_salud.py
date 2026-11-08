def test_salud_responde_200(cliente):
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200


def test_salud_devuelve_json_esperado(cliente):
    respuesta = cliente.get("/salud")
    assert respuesta.get_json() == {"estado": "ok", "servicio": "Flask"}


def test_salud_tiene_content_type_json(cliente):
    respuesta = cliente.get("/salud")
    assert respuesta.content_type.startswith("application/json")
