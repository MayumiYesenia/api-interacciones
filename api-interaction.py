from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}}, supports_credentials=True)

# Conexión a la base de datos
db = mysql.connector.connect(
    host="database-proyecto.c45ddxrq8nnm.us-east-1.rds.amazonaws.com",
    user="admin",
    password="database-proyecto",
    database="imagenes"
)
cursor = db.cursor(dictionary=True)

# Rutas para las imágenes favoritas
@app.route("/favorite_images", methods=["GET"])
def get_favorite_images():
    query = "SELECT * FROM imagenes_favoritas"
    cursor.execute(query)
    favorite_images = cursor.fetchall()
    return jsonify(favorite_images)

@app.route("/favorite_image/<int:id>", methods=["GET"])
def get_favorite_image(id):
    query = "SELECT * FROM imagenes_favoritas WHERE id = %s"
    cursor.execute(query, (id,))
    favorite_image = cursor.fetchone()
    if favorite_image:
        return jsonify(favorite_image)
    else:
        return jsonify({"error": "Imagen favorita no encontrada"}), 404

@app.route("/favorite_image", methods=["POST"])
def create_favorite_image():
    data = request.json
    if "nombre" in data and "url" in data:
        query = "INSERT INTO imagenes_favoritas (nombre, url, descripcion) VALUES (%s, %s, %s)"
        values = (data["nombre"], data["url"], data.get("descripcion", ""))
        cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "Imagen favorita creada exitosamente"}), 201
    else:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

@app.route("/favorite_image/<int:id>", methods=["PUT"])
def update_favorite_image(id):
    data = request.json
    if "nombre" in data or "url" in data or "descripcion" in data:
        updates = []
        values = []
        if "nombre" in data:
            updates.append("nombre = %s")
            values.append(data["nombre"])
        if "url" in data:
            updates.append("url = %s")
            values.append(data["url"])
        if "descripcion" in data:
            updates.append("descripcion = %s")
            values.append(data["descripcion"])

        query = "UPDATE imagenes_favoritas SET " + ", ".join(updates) + " WHERE id = %s"
        values.append(id)
        cursor.execute(query, tuple(values))
        db.commit()
        return jsonify({"message": "Imagen favorita actualizada exitosamente"}), 200
    else:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

@app.route("/favorite_image/<int:id>", methods=["DELETE"])
def delete_favorite_image(id):
    query = "DELETE FROM imagenes_favoritas WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    if cursor.rowcount > 0:
        return jsonify({"message": "Imagen favorita eliminada exitosamente"}), 200
    else:
        return jsonify({"error": "Imagen favorita no encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
