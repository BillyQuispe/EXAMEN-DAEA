from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import redis
import json

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar a MongoDB
client = MongoClient("mongodb://mongodb:27017")  # Asegúrate de que 'mongodb' es el nombre del servicio en Docker
db = client["MiBaseDeDatos"]  # Nombre de tu base de datos

# Conectar a Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Verificación de la conexión a la base de datos
try:
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

# Vectorizar los nombres de las habilidades
skills = user_data['Skill'].unique()
vectorizer = TfidfVectorizer()
vectorizer.fit(skills)
skill_vectors = vectorizer.transform(skills)
skill_sim_matrix = cosine_similarity(skill_vectors)

@app.route('/recomendacion/<string:skill>', methods=['GET'])
def recomendacion(skill):
    # Intentar obtener los datos de Redis
    cached_result = redis_client.get(skill)
    if cached_result:
        logger.info(f"Usando datos en caché para la habilidad: {skill}")
        recommendations = json.loads(cached_result)
        return jsonify(recommendations)

    # Filtrar por la skill solicitada y ordenar por puntuación descendente
    filtered_data = user_data[user_data['Skill'].str.lower() == skill.lower()]
    sorted_data = filtered_data.sort_values(by='Puntuacion', ascending=False).head(10)

    # Preparar recomendaciones de los mejores en la habilidad solicitada
    recommendations = []
    for index, row in sorted_data.iterrows():
        recommendations.append({
            "Usuario": row["Nombre"],
            "Skill": row["Skill"],
            "Puntuacion": row["Puntuacion"]
        })

    # Extraer la última palabra de la habilidad solicitada
    last_word = skill.split('_')[-1]

    # Calcular similitud de texto para encontrar habilidades similares basadas en la última palabra
    similar_skills = [s for s in skills if last_word.lower() in s.lower() and s.lower() != skill.lower()]

    # Buscar habilidades similares
    similar_recommendations = []
    for similar_skill in similar_skills:
        similar_data = user_data[user_data['Skill'].str.lower() == similar_skill.lower()]
        similar_data_sorted = similar_data.sort_values(by='Puntuacion', ascending=False).head(10)
        for index, row in similar_data_sorted.iterrows():
            similar_recommendations.append({
                "Usuario": row["Nombre"],
                "Skill": row["Skill"],
                "Puntuacion": row["Puntuacion"]
            })
            if len(similar_recommendations) >= 10:
                break
        if len(similar_recommendations) >= 10:
            break

    # Combinar recomendaciones
    recommendations.extend(similar_recommendations)

    # Almacenar las recomendaciones en Redis
    redis_client.set(skill, json.dumps(recommendations))
    logger.info(f"Datos para la habilidad {skill} almacenados en caché.")

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
