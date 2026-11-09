import time

import psycopg
import pytest
from psycopg.rows import dict_row

import app as modulo_app


def test_la_aplicacion_ya_no_guarda_en_memoria():
    assert not hasattr(modulo_app, "incidencias")
    assert not hasattr(modulo_app, "siguiente_id")


def test_la_incidencia_queda_guardada_en_la_base(crear_incidencia, url_base_datos):
    crear_incidencia(titulo="Incidencia persistida",
                     descripcion="Debe sobrevivir al proceso")
    with psycopg.connect(url_base_datos, row_factory=dict_row) as otra_conexion:
        with otra_conexion.cursor() as cursor:
            cursor.execute("SELECT titulo FROM incidencias ORDER BY id")
            titulos = [registro["titulo"] for registro in cursor.fetchall()]
    assert titulos == ["Incidencia persistida"]


def test_la_base_asigna_las_fechas(crear_incidencia, leer_incidencias):
    crear_incidencia()
    registro = leer_incidencias()[0]
    assert registro["fecha_creacion"] is not None
    assert registro["fecha_actualizacion"] is not None


def test_la_fecha_de_actualizacion_cambia_al_editar(cliente, crear_incidencia,
                                                    leer_incidencias):
    crear_incidencia()
    fecha_inicial = leer_incidencias()[0]["fecha_actualizacion"]
    time.sleep(0.01)
    cliente.post("/incidencias/1/editar", data={
        "titulo": "Titulo corregido",
        "descripcion": "Descripcion corregida",
        "prioridad": "Alta",
    })
    registro = leer_incidencias()[0]
    assert registro["fecha_actualizacion"] > fecha_inicial
    assert registro["fecha_creacion"] < registro["fecha_actualizacion"]


def test_sin_variable_de_entorno_no_hay_conexion(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError):
        modulo_app.conectar_db()
