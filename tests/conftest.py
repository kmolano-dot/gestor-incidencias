import os
import pathlib
import re

import psycopg
import pytest
from psycopg.rows import dict_row

import app as modulo_app

URL_POR_DEFECTO = "postgresql://postgres@localhost:5432/gestor_incidencias_test"

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


def _url():
    return os.environ.get("DATABASE_URL") or URL_POR_DEFECTO


def _sentencias_del_esquema():
    lineas = []
    for linea in ESQUEMA.read_text(encoding="utf-8").splitlines():
        if any(patron.match(linea) for patron in DESCARTABLES):
            continue
        lineas.append(linea)
    return "\n".join(lineas)


@pytest.fixture(scope="session")
def url_base_datos():
    url = _url()
    os.environ["DATABASE_URL"] = url
    try:
        with psycopg.connect(url, connect_timeout=5):
            pass
    except psycopg.OperationalError as error:
        raise pytest.UsageError(
            "No se pudo conectar a PostgreSQL para ejecutar las pruebas.\n"
            f"  URL utilizada: {url}\n"
            f"  Error: {error}\n"
            "Define la variable DATABASE_URL o crea la base de pruebas con:\n"
            "  createdb gestor_incidencias_test"
        ) from error
    return url


@pytest.fixture(scope="session", autouse=True)
def esquema(url_base_datos):
    with psycopg.connect(url_base_datos, autocommit=True) as conexion:
        conexion.execute(LIMPIEZA)
        conexion.execute(_sentencias_del_esquema())
    return url_base_datos


@pytest.fixture
def conexion(url_base_datos):
    with psycopg.connect(url_base_datos, row_factory=dict_row, autocommit=True) as con:
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
