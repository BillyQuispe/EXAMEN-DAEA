from flask import Flask, request, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

# Conectar a SQL Server
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=sqlserver;DATABASE=MiBaseDeDatos;UID=sa;PWD=StrongPassword123'
conn = pyodbc.connect(conn_str)

# Consulta para obtener datos de la base de datos
def fetch_user_data():
    query = '''
    SELECT u.ID, u.Nombre, s.Nombre as Skill, us.Puntuacion
    FROM Usuarios u
    JOIN UsuarioSkills us ON u.ID = us.ID_Usuario
    JOIN Skills s ON us.ID_Skill = s.ID
    '''
    df = pd.read_sql(query, conn)
    return df

# Obtener los datos al inicio para no hacer la consulta en cada petición
user_data = fetch_user_data()

@app.route('/recomendacion/<string:skill>', methods=['GET'])
def recomendacion(skill):
    # Filtrar por la skill solicitada y ordenar por puntuación descendente
    filtered_data = user_data[user_data['Skill'].str.lower() == skill.lower()]
    sorted_data = filtered_data.sort_values(by='Puntuacion', ascending=False).head(5)

    # Preparar las recomendaciones
    recommendations = []
    for index, row in sorted_data.iterrows():
        recommendations.append({
            "Usuario": row["Nombre"],
            "Skill": row["Skill"],
            "Puntuacion": row["Puntuacion"]
        })

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
