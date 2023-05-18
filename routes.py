from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from python_files import search
from pathlib import Path
from fastapi_htmx import htmx, htmx_init
from python_files.chartjs import SpiderChart
from python_files import recommendation
from python_files.tmdb import API_KEY, TMDB_wrapper


import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory="templates")
htmx_init(templates=Jinja2Templates(directory=Path("templates")))


df = pd.read_parquet("csv/complete.parquet")
df = df.sort_values(by="popularity", ascending=False)
similarity_matrix = recommendation.sim_matrix(df)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@router.get("/api")
def api():
    return {"api_key": API_KEY}


# @router.get("/recommendation/{movie_id}")
# def tmdb_recommendation(movie_id: int):
#     tmdb = TMDB_wrapper()
#     movie = tmdb.get_recommendations(movie_id)
#     return movie


@router.get("/recommendation/{movie_id}", response_class=HTMLResponse)
@htmx("recommendation_cards")
async def search_title(movie_id: str, request: Request):
    tmdb = TMDB_wrapper()
    recommendations = tmdb.get_recommendations(movie_id)
    ids = [x["id"] for x in recommendations]
    filtered = df[df["id"].isin(ids)]
    movies = []
    for index, row in filtered.iterrows():
        movies.append(row.to_dict())
    context = {"movies": movies, "request": request}
    return context


@router.get("/hola/", response_class=HTMLResponse)
@htmx("pruebas", "pruebas")
async def hola(request: Request):
    tmdb = TMDB_wrapper()
    context = {"request": request}
    return context


# @router.get("/hola", response_class=HTMLResponse)
# @htmx("pruebas", "pruebas")
# async def hola(request: Request):
#     movie_id = 502356
#     rec_list = recommendation.process_reccom(df, movie_id, similarity_matrix)
#     movies = recommendation.get_top_recommended_movies(df, rec_list, 5)
#     for i in range(len(movies)):
#         mov = movies[i]
#         data = mov["results"].values()
#         print(data)

#     context = {"request": request, "movies_data": movies}
#     return context


@router.get("/movie/{movie_id}", response_class=HTMLResponse)
@htmx("movie", "movie")
def movie(request: Request, movie_id: int):
    # Movie data
    movies = df[df["id"] == movie_id]
    movie = {}
    for index, row in movies.iterrows():
        movie = row.to_dict()

    # Recommendations
    rec_list = recommendation.process_reccom(df, movie_id, similarity_matrix)
    recommended_movies = recommendation.get_top_recommended_movies(df, rec_list, 6)
    recommendations = []
    for i in range(len(recommended_movies)):
        mov = recommended_movies[i]
        chart = SpiderChart()
        data = list(mov["results"].values())
        chart.data.data = data
        chart.labels.names = list(mov["results"].keys())
        chart.data.label = mov["title"]
        chart_json = chart.get()
        recommended_movie = {
            "id": mov["id"],
            "title": mov["title"],
            "chart": chart_json,
            "poster_path": mov["poster_path"],
        }
        recommendations.append(recommended_movie)

    # TMDB's recommendations
    # ----------------------------------Rellenar --------------------------------------------

    context = {
        "request": request,
        "recommendations": recommendations,
        "film_data": movie,
    }
    return context


@router.get("/trust_us", response_class=HTMLResponse)
@htmx("trustus", "trustus")
def trust_us(request: Request):
    movies_data = []
    for index, row in df.iterrows():
        if len(movies_data) < 100:
            movies_data.append(row.to_dict())
            continue
    context = {"request": request, "movies_data": movies_data}
    return context


@router.get("/search", response_class=HTMLResponse)
@htmx("searched_cards")
async def search_title(title: str, request: Request):
    matched_titles = search.search_titles(title, df["title"], rating=90)
    filtered_movies = df[df["title"].isin(matched_titles)]
    filtered_movies = filtered_movies.sort_values(by="year", ascending=False)
    movies = []
    for index, row in filtered_movies.iterrows():
        movies.append(row.to_dict())
    context = {"movies": movies}

    return context


@router.get("/filter", response_class=HTMLResponse)
@htmx("filter_yourself", "filter_yourself")
async def filter_yourself(request: Request):
    genres = set()
    for l in df["genres"]:
        for g in l:
            genres.add(g)
    genres = list(genres)
    min_year = df["year"].min()
    max_year = df["year"].max()

    context = {"genres": genres, "min_year": min_year, "max_year": max_year}
    return context
