import pytest

import app as modulo_app


@pytest.fixture
def cliente():
    modulo_app.app.config.update(TESTING=True)
    _reiniciar_estado()
    with modulo_app.app.test_client() as cliente_pruebas:
        yield cliente_pruebas
    _reiniciar_estado()


@pytest.fixture
def crear_incidencia(cliente):
    def _crear(titulo="Fallo en el inicio de sesion",
               descripcion="El formulario no permite ingresar",
               prioridad="Media"):
        return cliente.post(
            "/incidencias",
            data={
                "titulo": titulo,
                "descripcion": descripcion,
                "prioridad": prioridad,
            },
        )

    return _crear


@pytest.fixture
def leer_incidencias():
    def _leer():
        return [dict(registro) for registro in modulo_app.incidencias]

    return _leer


def _reiniciar_estado():
    modulo_app.incidencias.clear()
    modulo_app.siguiente_id = 1
