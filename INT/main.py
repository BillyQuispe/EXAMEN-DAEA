from flask import Flask, request, jsonify
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import numpy as np
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

app = Flask(__name__)

# Cargar los datos de ejercicios
data = pd.read_csv('exercise.csv')

# Preprocesamiento
en_stopwords = stopwords.words("english")
lemma = WordNetLemmatizer()

def clean(text):
    text = re.sub("[^A-Za-z1-9 ]", "", text)  # Elimina signos de puntuación
    text = text.lower()  # Convierte a minúsculas
    tokens = word_tokenize(text)  # Tokeniza el texto
    clean_list = [lemma.lemmatize(token) for token in tokens if token not in en_stopwords]  # Lematización y eliminación de stopwords
    return " ".join(clean_list)

# Crear columna 'Description' combinando columnas relevantes
data['Description'] = data['Exercise'] + ' ' + data['Muscle'] + ' ' + data['Descripcion']
data['Description'] = data['Description'].apply(clean)

# Vectorización de TF-IDF
vectorizer = TfidfVectorizer()
test_matrix = vectorizer.fit_transform(data['Description'])

# Entrenar modelo Word2Vec con las descripciones
descriptions_tokenized = data['Description'].apply(lambda x: word_tokenize(x))
w2v_model = Word2Vec(sentences=descriptions_tokenized, vector_size=100, window=5, min_count=1, workers=4)

# Función para expandir términos con Word2Vec
def expand_term_with_word2vec(term, top_n   =5):
    similar_terms = []
    try:
        similar_terms = [term]  # Incluir el término original
        similar_terms += [word for word, score in w2v_model.wv.most_similar(term, topn=top_n)]  # Palabras similares
    except KeyError:
        # Si no se encuentra la palabra en el vocabulario de Word2Vec
        pass
    return similar_terms

@app.route('/recomendacion/<string:termino>', methods=['GET'])
def recomendacion(termino):
    # Preprocesar el término de búsqueda
    clean_term = clean(termino)

    # Expandir términos usando Word2Vec
    expanded_terms = expand_term_with_word2vec(clean_term)

    # Vectorizar los términos expandidos y calcular la similitud
    combined_similarity = np.zeros(test_matrix.shape[0])  # Matriz para sumar las similitudes

    for term in expanded_terms:
        term_vector = vectorizer.transform([term])
        similarity = cosine_similarity(term_vector, test_matrix)[0]  # Similaridad con todos los ejercicios
        combined_similarity += similarity  # Sumar la similitud para cada término

    # Obtener los 10 ejercicios más similares
    similar_exercises = list(enumerate(combined_similarity))
    filtered_similar_exercises = [(i, score) for i, score in similar_exercises if score > 0.0]
    sorted_similar_exercises = sorted(filtered_similar_exercises, key=lambda x: x[1], reverse=True)[:10]

    # Preparar las recomendaciones
    recommendations = []
    for i, score in sorted_similar_exercises:
        recommendations.append({
            "Name": data.loc[i, "Exercise"],
            "Muscle": data.loc[i, "Muscle"],
            "Description": data.loc[i, "Descripcion"],
            "Additional Info": data.loc[i, "Additional"],
            "Score": score,
            "Description": data.loc[i, "Description"],
        })

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
