import pandas as pd
import pandas as pd
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
    return similitud


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


def description_similarity_dic(title_id, similarity_matrix, id_list):
    title_idx = id_list.index(title_id)
    title_row = list(similarity_matrix[title_idx])
    similarity_dict = dict(enumerate(title_row))
    return similarity_dict


def sacar_puntuaciones_completo(df, kw_list, genero, actores, director, año, sim_dict):
    results_list = []
    i = 0
    for index, row in df.iterrows():
        keywords_p = compararListas(kw_list, row["keywords"])  # Sobre 10
        genres_p = compararListas(genero, row["genres"])  # Sobre 10
        cast_p = compararListas(actores, row["cast"])  # Sobre 10
        years_p = similitud_anios(int(año), int(row["year"]), 0.11)  # Sobre 1
        director_p = compararListas(director, row["director"])  # Sobre 10
        description_p = sim_dict[i]  # sobre 1
        # kw * 0.35; genres * 0.15; cast * 0.05; years * 0.5; director * 0.1; description * 3

        labels = [keywords_p, genres_p, cast_p, years_p, director_p, description_p]
        values = [0.35, 0.15, 0.05, 0.5, 0.1, 3]
        points = sum(list(map(lambda x, y: x * y, labels, values)))
        results = {
            "keywords": keywords_p,
            "genres": genres_p,
            "cast": cast_p,
            "years": years_p * 10,
            "director": director_p,
            "description": description_p * 10,
        }
        results_list.append((row["id"], points, results))
        i += 1
    return results_list


def process_reccom(df, movie_id, similarity_matrix):
    # sacar_puntuaciones_completo(df, kw_list, genero, actores, director, año, sim_dict)
    movies = df[df["id"] == movie_id]
    for index, row in movies.iterrows():
        movie = row.to_dict()

    sim_dict = description_similarity_dic(movie_id, similarity_matrix, list(df["id"]))
    list_res = sacar_puntuaciones_completo(
        df,
        movie["keywords"],
        movie["genres"],
        movie["cast"],
        movie["director"],
        movie["year"],
        sim_dict,
    )
    list_res.sort(key=lambda x: x[1], reverse=True)
    return list_res


def get_top_recommended_movies(
    df: pd.DataFrame, recommendations_list: list, limit: int
):
    def search_points(rec_list: list, id: int, limit: int):
        for i in range(1, limit + 1):
            m = rec_list[i]
            if m[0] == id:
                return (recommendations_list[i][1], recommendations_list[i][2])
        return None, None

    filtered_results = [x[0] for x in recommendations_list][1 : limit + 1]
    filtered_df = df[df["id"].isin(filtered_results)]
    movies = []
    for idx, row in filtered_df.iterrows():
        movie = row.to_dict()
        points, results = search_points(recommendations_list, movie["id"], limit)
        movie["points"] = points
        movie["results"] = results
        movies.append(movie)
    return movies
