from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import logging

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar a MongoDB
client = MongoClient("mongodb://mongodb:27017")  # Asegúrate de que 'mongodb' es el nombre del servicio en Docker
db = client["MiBaseDeDatos"]  # Nombre de tu base de datos

# Verificación de la conexión a la base de datos
try:
    # Intentar obtener una colección para verificar la conexión
    db.list_collection_names()
    logger.info("Conexión exitosa a la base de datos MongoDB.")
except Exception as e:
    logger.error(f"Error al conectar a la base de datos: {e}")

# Obtener los datos de usuarios y habilidades
def fetch_user_data():
    usuarios = db["Usuarios"].find()
    skills = db["Skills"].find()
    usuario_skills = db["UsuarioSkills"].find()
    
    # Convertir a DataFrame
    users_list = list(usuarios)
    skills_list = list(skills)
    usuario_skills_list = list(usuario_skills)
    
    # Unir la información en un solo DataFrame
    df = pd.DataFrame(usuario_skills_list)
    
    # Agregar nombres de usuarios y habilidades desde sus colecciones
    df["Nombre"] = df["ID_Usuario"].apply(lambda x: next(user["Nombre"] for user in users_list if user["ID"] == x))
    df["Skill"] = df["ID_Skill"].apply(lambda x: next(skill["Nombre"] for skill in skills_list if skill["ID"] == x))
    
    return df

# Obtener los datos al inicio para no hacer la consulta en cada petición
user_data = fetch_user_data()

# Generar matriz de usuarios con sus habilidades y puntajes para similitud de coseno
skill_matrix = user_data.pivot_table(index='Nombre', columns='Skill', values='Puntuacion', fill_value=0)
cosine_sim = cosine_similarity(skill_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=skill_matrix.index, columns=skill_matrix.index)

@app.route('/recomendacion/<string:skill>', methods=['GET'])
def recomendacion(skill):
    # Filtrar por la skill solicitada y ordenar por puntuación descendente
    filtered_data = user_data[user_data['Skill'].str.lower() == skill.lower()]
    sorted_data = filtered_data.sort_values(by='Puntuacion', ascending=False).head(5)

    # Verificar si sorted_data está vacío
    if sorted_data.empty:
        logger.warning(f"No se encontraron datos para la skill: {skill}")
        return jsonify({"mensaje": "No se encontraron usuarios con esa habilidad."}), 404

    # Preparar recomendaciones de los mejores en la habilidad solicitada
    recommendations = []
    for index, row in sorted_data.iterrows():
        recommendations.append({
            "Usuario": row["Nombre"],
            "Skill": row["Skill"],
            "Puntuacion": row["Puntuacion"]
        })

    # Buscar estudiantes similares si no hay suficientes en la habilidad solicitada
    if len(recommendations) < 5:
        top_user = sorted_data.iloc[0]['Nombre']  # Usuario con puntaje más alto en la habilidad
        similar_users = cosine_sim_df[top_user].sort_values(ascending=False).index[1:6]

        # Agregar usuarios similares con otras habilidades
        for similar_user in similar_users:
            similar_data = user_data[(user_data['Nombre'] == similar_user) & (user_data['Skill'] != skill)]
            for _, row in similar_data.iterrows():
                recommendations.append({
                    "Usuario": row["Nombre"],
                    "Skill": row["Skill"],
                    "Puntuacion": row["Puntuacion"]
                })
                if len(recommendations) >= 10:  # Limitar a 10 recomendaciones
                    break
            if len(recommendations) >= 10:
                break

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
