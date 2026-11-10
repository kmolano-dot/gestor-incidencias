import os
import pathlib
import re
from contextlib import contextmanager

import psycopg
import pytest
from psycopg.conninfo import conninfo_to_dict
from psycopg.rows import dict_row

import app as modulo_app

BASE_DE_PRUEBAS = "gestor_incidencias_test"

ESQUEMA = pathlib.Path(__file__).resolve().parents[1] / "database" / "gestor_incidencias.sql"

DESCARTABLES = (
    re.compile(r"^\s*\\"),
    re.compile(r"^\s*SET\s+\w+\s*=", re.IGNORECASE),
    re.compile(r"^\s*SELECT\s+pg_catalog\.set_config", re.IGNORECASE),
    re.compile(r"^\s*ALTER\s+(TABLE|FUNCTION)\s+.*OWNER\s+TO\s+.*;\s*$", re.IGNORECASE),
)

LIMPIEZA = """
DROP TABLE IF EXISTS public.incidencias CASCADE;
DROP FUNCTION IF EXISTS public.actualizar_fecha_incidencia() CASCADE;
"""


def _url_pruebas():
    url = os.environ.get("TEST_DATABASE_URL", "").strip()
    if not url:
        raise pytest.UsageError(
            f"Define TEST_DATABASE_URL con la conexión a {BASE_DE_PRUEBAS}."
        )

    try:
        parametros = conninfo_to_dict(url)
    except (psycopg.ProgrammingError, ValueError):
        raise pytest.UsageError(
            "TEST_DATABASE_URL no contiene una cadena de conexión válida de PostgreSQL."
        ) from None

    if parametros.get("dbname") != BASE_DE_PRUEBAS:
        raise pytest.UsageError(f"TEST_DATABASE_URL debe apuntar a {BASE_DE_PRUEBAS}.")
    return url


@contextmanager
def _conexion_pruebas(url):
    try:
        conexion = psycopg.connect(url, autocommit=True, connect_timeout=5)
    except (psycopg.Error, ValueError):
        raise pytest.UsageError(
            "No se pudo conectar a la base de pruebas. "
            "Revisa TEST_DATABASE_URL y comprueba que PostgreSQL esté disponible."
        ) from None

    with conexion:
        try:
            base_actual = conexion.execute("SELECT pg_catalog.current_database()").fetchone()
        except psycopg.Error:
            raise pytest.UsageError(
                "No se pudo confirmar el destino de la conexión de pruebas."
            ) from None
        if base_actual != (BASE_DE_PRUEBAS,):
            raise pytest.UsageError(
                f"La conexión de pruebas debe llegar a {BASE_DE_PRUEBAS}."
            )
        yield conexion


def _sentencias_del_esquema():
    lineas = []
    for linea in ESQUEMA.read_text(encoding="utf-8").splitlines():
        if any(patron.match(linea) for patron in DESCARTABLES):
            continue
        lineas.append(linea)
    return "\n".join(lineas)


@pytest.fixture(scope="session")
def url_base_datos():
    url = _url_pruebas()
    with pytest.MonkeyPatch.context() as entorno:
        entorno.setenv("DATABASE_URL", url)
        yield url


@pytest.fixture(scope="session", autouse=True)
def esquema(url_base_datos):
    with _conexion_pruebas(url_base_datos) as conexion:
        conexion.execute(LIMPIEZA)
        conexion.execute(_sentencias_del_esquema())
    return url_base_datos


@pytest.fixture
def conexion(url_base_datos):
    with _conexion_pruebas(url_base_datos) as con:
        con.row_factory = dict_row
        yield con


@pytest.fixture
def cliente(conexion):
    modulo_app.app.config.update(TESTING=True)
    _vaciar(conexion)
    with modulo_app.app.test_client() as cliente_pruebas:
        yield cliente_pruebas
    _vaciar(conexion)


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
def leer_incidencias(conexion):
    def _leer():
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM incidencias ORDER BY id")
            return cursor.fetchall()

    return _leer


def _vaciar(conexion):
    conexion.execute("TRUNCATE incidencias RESTART IDENTITY CASCADE")
