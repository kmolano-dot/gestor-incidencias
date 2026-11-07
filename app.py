
#
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

# Almacenamiento temporal hasta integrar PostgreSQL.
incidencias = []
siguiente_id = 1


# Muestra la interfaz principal.
@app.get("/")
def inicio():
    # Obtener el estado seleccionado en el filtro.
    filtro_estado = request.args.get("estado", "Todos")
    estados_validos = (
        "Todos", "Pendiente", "En proceso", "Resuelta"
    )
    if filtro_estado not in estados_validos:
        filtro_estado = "Todos"
    # Mostrar todas las incidencias o filtrar por estado.
    if filtro_estado == "Todos":
        resultados = incidencias
    else:
        resultados = [
            incidencia
            for incidencia in incidencias
            if incidencia["estado"] == filtro_estado
        ]

    return render_template(
        "index.html",
        incidencias=resultados,
        filtro_estado=filtro_estado
    )
# Registra una nueva incidencia.
@app.post("/incidencias")
def crear_incidencia():
    global siguiente_id
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    prioridad = request.form.get("prioridad", "")
    if not titulo or not descripcion:
        return "El título y la descripción son obligatorios", 400
    if len(titulo) > 150:
        return "El título no puede superar 150 caracteres", 400
    if prioridad not in ("Baja", "Media", "Alta"):
        return "La prioridad seleccionada no es válida", 400
    nueva_incidencia = {
        "id": siguiente_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "Pendiente"
    }
    incidencias.append(nueva_incidencia)
    siguiente_id += 1
    return redirect(url_for("inicio"))
# Actualizar el estado de una incidencia.
@app.post("/incidencias/<int:incidencia_id>/estado")
def actualizar_estado(incidencia_id):
    nuevo_estado = request.form.get("estado", "")
    estados_validos = ("Pendiente", "En proceso", "Resuelta")
    if nuevo_estado not in estados_validos:
        return "Estado no válido", 400
    for incidencia in incidencias:
        if incidencia["id"] == incidencia_id:
            incidencia["estado"] = nuevo_estado
            return redirect(url_for("inicio"))
    return "Incidencia no encontrada", 404

# Borrar una incidencia por su identificador.
@app.post("/incidencias/<int:incidencia_id>/eliminar")
def eliminar_incidencia(incidencia_id):

    for incidencia in incidencias:
        if incidencia["id"] == incidencia_id:
            incidencias.remove(incidencia)
            return redirect(url_for("inicio"))
    return "Incidencia no encontrada", 404

# Editar los datos de una incidencia.
@app.post("/incidencias/<int:incidencia_id>/editar")
def editar_incidencia(incidencia_id):

    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    prioridad = request.form.get("prioridad", "")
    # Validar la información recibida.
    if not titulo or not descripcion:
        return "Título y descripción obligatorios", 400
    if len(titulo) > 150:
        return "El título no puede superar 150 caracteres", 400
    if prioridad not in ("Baja", "Media", "Alta"):
        return "Prioridad no válida", 400
    # Buscar y actualizar la incidencia.
    for incidencia in incidencias:
        if incidencia["id"] == incidencia_id:
            incidencia["titulo"] = titulo
            incidencia["descripcion"] = descripcion
            incidencia["prioridad"] = prioridad
            return redirect(url_for("inicio"))
    return "Incidencia no encontrada", 404
# Comprueba que el servicio esté funcionando.
@app.get("/salud")
def verificar_salud():
    return jsonify({
        "estado": "ok",
        "servicio": "Flask"
    })