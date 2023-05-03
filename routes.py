from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory='templates')

df = pd.read_parquet('csv/popular.parquet')

@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)

@router.get('/hola', response_class=HTMLResponse)
def hola(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('provisional.html', context)

@router.get('/movie/{movie_id}', response_class=HTMLResponse)
def movie(request: Request, movie_id: int):
    # film = movies_dic[movie_id]
    movies = df[df['id'] == movie_id]
    movie = {}
    for index, row in movies.iterrows():
        movie = row.to_dict()
    context = {'request': request, 'film_data': movie}
    return templates.TemplateResponse('movie.html', context)

@router.get('/anna')
def anna():
    return {'Anna': 'más fea y le salen callos en la cara'}

@router.get('/alex')
def alex():
    return {'Alex': 'Te quiero', 'dónde?': 'bien lejos'}