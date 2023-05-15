from thefuzz import process


def search_titles(movie_title, titles_list, limit=10, rating=90):
    matches = process.extract(movie_title, titles_list, limit=50)
    matched_titles = []
    for m in matches:
        if m[1] >= rating and len(m[0]) >= len(movie_title):
            matched_titles.append(m[0])
    return matched_titles


# filtered_movies = df[df["title"].isin(matched_titles)]
# filtered_movies
