"""Gestor de incidencias de software: aplicación Flask con PostgreSQL."""

import os

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)


def conectar_db():
    """Abre una conexión a PostgreSQL usando configuración externa."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Falta definir la variable de entorno DATABASE_URL")
    return psycopg.connect(database_url, row_factory=dict_row, connect_timeout=5)


# Muestra la interfaz principal y permite filtrar las incidencias por estado.
@app.get("/")
def inicio():
    filtro_estado = request.args.get("estado", "Todos")
    estados_validos = ("Todos", "Pendiente", "En proceso", "Resuelta")
    if filtro_estado not in estados_validos:
        filtro_estado = "Todos"

    with conectar_db() as conexion:
        with conexion.cursor() as cursor:
            if filtro_estado == "Todos":
                cursor.execute(
                    "SELECT id, titulo, descripcion, prioridad, estado "
                    "FROM incidencias ORDER BY id"
                )
            else:
                cursor.execute(
                    "SELECT id, titulo, descripcion, prioridad, estado "
                    "FROM incidencias WHERE estado = %s ORDER BY id",
                    (filtro_estado,),
                )
            resultados = cursor.fetchall()

    return render_template(
        "index.html",
        incidencias=resultados,
        filtro_estado=filtro_estado,
    )


# Registra una nueva incidencia.
@app.post("/incidencias")
def crear_incidencia():
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    prioridad = request.form.get("prioridad", "")

    if not titulo or not descripcion:
        return "El título y la descripción son obligatorios", 400
    if len(titulo) > 150:
        return "El título no puede superar 150 caracteres", 400
    if prioridad not in ("Baja", "Media", "Alta"):
        return "La prioridad seleccionada no es válida", 400

    with conectar_db() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO incidencias (titulo, descripcion, prioridad) "
                "VALUES (%s, %s, %s)",
                (titulo, descripcion, prioridad),
            )
    return redirect(url_for("inicio"))


# Actualiza el estado de una incidencia existente.
@app.post("/incidencias/<int:incidencia_id>/estado")
def actualizar_estado(incidencia_id):
    nuevo_estado = request.form.get("estado", "")
    if nuevo_estado not in ("Pendiente", "En proceso", "Resuelta"):
        return "Estado no válido", 400

    with conectar_db() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE incidencias SET estado = %s WHERE id = %s RETURNING id",
                (nuevo_estado, incidencia_id),
            )
            encontrada = cursor.fetchone()

    if encontrada is None:
        return "Incidencia no encontrada", 404
    return redirect(url_for("inicio"))


# Borra una incidencia por su identificador.
@app.post("/incidencias/<int:incidencia_id>/eliminar")
def eliminar_incidencia(incidencia_id):
    with conectar_db() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM incidencias WHERE id = %s RETURNING id",
                (incidencia_id,),
            )
            encontrada = cursor.fetchone()

    if encontrada is None:
        return "Incidencia no encontrada", 404
    return redirect(url_for("inicio"))


# Edita el título, la descripción y la prioridad de una incidencia.
@app.post("/incidencias/<int:incidencia_id>/editar")
def editar_incidencia(incidencia_id):
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    prioridad = request.form.get("prioridad", "")

    if not titulo or not descripcion:
        return "Título y descripción obligatorios", 400
    if len(titulo) > 150:
        return "El título no puede superar 150 caracteres", 400
    if prioridad not in ("Baja", "Media", "Alta"):
        return "Prioridad no válida", 400

    with conectar_db() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE incidencias "
                "SET titulo = %s, descripcion = %s, prioridad = %s "
                "WHERE id = %s RETURNING id",
                (titulo, descripcion, prioridad, incidencia_id),
            )
            encontrada = cursor.fetchone()

    if encontrada is None:
        return "Incidencia no encontrada", 404
    return redirect(url_for("inicio"))


# Comprueba que el servicio Flask responda (sin verificar la base de datos).
@app.get("/salud")
def verificar_salud():
    return jsonify({"estado": "ok", "servicio": "Flask"})
