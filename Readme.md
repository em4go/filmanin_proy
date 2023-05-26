# Filmanin: movie recommendation system web app

## Description

Filmanin is a web app made for a college subject. It is a movie recommendation system that uses the TMDB dataset. It is made with Python and FastAPI. It doesn't offer any kind of authentication or authorization. It is just a simple web app to try the recommendation system. It is deployed in Google Cloud and you can try it [here](https://filmanin-tvbgmeeqta-od.a.run.app/). It is deployed in a free tier so it may take a while to load.
The web doesn't allow the user to watch the movies, it just shows the user the information about the movie and the recommendations.

## Installation

Use docker to try Filmanin locally.

```bash
docker compose -f docker-compose.development.yaml up --build
```

## Usage

### `/trust_us` route

This route is used to search the movie you want to get recommendations from. It returns a list of movies whose title is similar to the one you searched. Once you select the movie you want, it will redirect you to the `/movie/{movie_id}` route.

### `/movie/{movie_id}` route

This route is used to get the recommendations of the movie you selected in the `/trust_us` route. It shows some basic information about the movie and a list of movies whose content and information is similar to the one you selected. Once you select the movie you want, it will redirect you to the `/movie/{movie_id}` route and so on.

## Configuration

To configure the web app you have to create a `.env.development` file in the root directory of the project. The `.env.development` file must contain the API key for TMDB. You can get the API key [here](https://www.themoviedb.org/settings/api). This file must contain the following:

```bash
API_KEY='your_api_key'
```

## License

Still not decided.

## Contributing

The project is not open to contributions. It was made for a college subject and it is not going to be maintained.

## Author: Ernesto Martínez Gómez

- [Linkedin](https://www.linkedin.com/in/ernesto-mart%C3%ADnez-g%C3%B3mez-98244b1b4/)

- [GitHub](https://github.com/em4go)
