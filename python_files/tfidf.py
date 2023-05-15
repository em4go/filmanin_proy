from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math


def sim_matrix(df):
    description_list = df["description"]
    # Crea una instancia del vectorizador TF-IDF
    tfidf = TfidfVectorizer()
    # Transforma las descripciones en una matriz de términos y documentos (DTM)
    dtm = tfidf.fit_transform(description_list)
    # Calcula la similitud coseno entre todas las películas
    similarity_matrix = cosine_similarity(dtm)
    # title_index_dic = {}
    # for index, id in enumerate(df['id']):
    #     title_index_dic[id] = index
    return similarity_matrix


def description_similarity(title_id, similarity_matrix, id_list):
    title_idx = id_list.index(title_id)
    title_row = list(similarity_matrix[title_idx])
    similarity_list = list(enumerate(title_row))
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    return similarity_list


def process_similarity(df, title_id):
    similarity_matrix = sim_matrix(df)
    sim_list = description_similarity(title_id, similarity_matrix, list(df["id"]))
    lista = []
    for i in range(1, 1000):
        index = sim_list[i][0]
        id = df["id"][index]
        lista.append(id)

    filtered = df[df["id"].isin(lista)]
    filtered["tfidf"] = [sim_list[index][1] for index in range(1000)]

    movies = []
    for index, row in filtered.iterrows():
        movie = row.to_dict()
        movie["tfidf"] = sim_list[index][1]
        movies.append(movie)


def get_description_recomenndations(
    similarity_dic: dict[float:str], title_row: list[str], limit: int = 100
):
    title_row.sort(reverse=True)
    recommendations = []
    for i in range(limit):
        similarity = title_row[i]
        recommendations.append(similarity_dic[similarity])

    return recommendations


def compararString(str1, str2):
    if str1 == str2:
        return 10
    else:
        return 0


def compararListas(lista1, lista2):
    try:
        if len(lista1) == 0 or len(lista2) == 0:
            return 0
        set1 = set(lista1)
        set2 = set(lista2)
        if set1.issubset(set2):
            return 10
        else:
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            jaccard_similarity = len(intersection) / len(union)
            score = jaccard_similarity * 10
        return score
    except:
        return 0


def similitud_anios(anio1, anio2, k):
    # Calcular la diferencia de años entre los dos valores
    diferencia = abs(anio1 - anio2)
    # Calcular la similitud utilizando la fórmula exponencial
    similitud = math.exp(-k * diferencia)
    # Returns a number between 0 and 1 (1 means is the same year)
    return similitud


def sacarPuntuaciones(df, kw_list, genero, actores, director, año):
    dicResults = {}
    for index, row in df.iterrows():
        puntuacion = 0
        puntuacion += (compararListas(kw_list, row["keywords"])) * 0.4
        puntuacion += (compararListas(genero, row["genres"])) * 0.3  # 0.7
        puntuacion += (compararListas(actores, row["cast"])) * 0.1  # 0.8
        puntuacion += (compararListas(director, row["director"])) * 0.1  # 0.9
        puntuacion += similitud_anios(int(año), int(row["year"]), 0.8)  # gives up to 1p
        dicResults[row["title"]] = puntuacion
    return dicResults


if __name__ == "__main__":
    df = pd.read_parquet("../csv/popular.parquet")
    df["year"] = df["year"].astype("int")
