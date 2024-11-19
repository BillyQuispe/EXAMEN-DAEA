from flask import Flask, request, jsonify
from pymongo import MongoClient
from pyspark.sql import SparkSession
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import logging

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar a MongoDB
client = MongoClient("mongodb://mongodb:27017")  # Asegúrate de que 'mongodb' es el nombre del servicio en Docker
db = client["MiBaseDeDatos"]  # Nombre de tu base de datos

# Configurar Spark
spark = SparkSession.builder \
    .appName("RecomendacionUsuarios") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Verificación de la conexión a la base de datos
try:
    db.list_collection_names()
    logger.info("Conexión exitosa a la base de datos MongoDB.")
except Exception as e:
    logger.error(f"Error al conectar a la base de datos: {e}")

# Obtener los datos de usuarios y habilidades
def fetch_user_data():
    usuarios = list(db["Usuarios"].find())
    skills = list(db["Skills"].find())
    usuario_skills = list(db["UsuarioSkills"].find())
    
    # Crear DataFrames de Spark
    usuarios_df = spark.createDataFrame(usuarios)
    skills_df = spark.createDataFrame(skills)
    usuario_skills_df = spark.createDataFrame(usuario_skills)
    
    # Unir la información en un solo DataFrame de Spark
    df = usuario_skills_df.join(usuarios_df, usuario_skills_df["ID_Usuario"] == usuarios_df["ID"], "inner") \
                          .join(skills_df, usuario_skills_df["ID_Skill"] == skills_df["ID"], "inner") \
                          .select(usuario_skills_df["ID"], "ID_Usuario", "ID_Skill", "Puntuacion", "Nombre", "Skill")
    
    return df

# Obtener los datos al inicio para no hacer la consulta en cada petición
user_data = fetch_user_data()

# Convertir DataFrame de Spark a pandas para usar en similitud de cosenos
user_data_pd = user_data.toPandas()

# Generar matriz de usuarios con sus habilidades y puntajes para similitud de coseno
skill_matrix = user_data_pd.pivot_table(index='Nombre', columns='Skill', values='Puntuacion', fill_value=0)
cosine_sim = cosine_similarity(skill_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=skill_matrix.index, columns=skill_matrix.index)

@app.route('/recomendacion/<string:skill>', methods=['GET'])
def recomendacion(skill):
    filtered_data = user_data_pd[user_data_pd['Skill'].str.lower() == skill.lower()]
    sorted_data = filtered_data.sort_values(by='Puntuacion', ascending=False).head(5)

    if sorted_data.empty:
        logger.warning(f"No se encontraron datos para la skill: {skill}")
        return jsonify({"mensaje": "No se encontraron usuarios con esa habilidad."}), 404

    recommendations = []
    for index, row in sorted_data.iterrows():
        recommendations.append({
            "Usuario": row["Nombre"],
            "Skill": row["Skill"],
            "Puntuacion": row["Puntuacion"]
        })

    if len(recommendations) < 5:
        top_user = sorted_data.iloc[0]['Nombre']
        similar_users = cosine_sim_df[top_user].sort_values(ascending=False).index[1:6]

        for similar_user in similar_users:
            similar_data = user_data_pd[(user_data_pd['Nombre'] == similar_user) & (user_data_pd['Skill'] != skill)]
            for _, row in similar_data.iterrows():
                recommendations.append({
                    "Usuario": row["Nombre"],
                    "Skill": row["Skill"],
                    "Puntuacion": row["Puntuacion"]
                })
                if len(recommendations) >= 10:
                    break
            if len(recommendations) >= 10:
                break

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
