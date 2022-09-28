import json
import uuid


def all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies['movies']



def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors


# define function to resolve deleting a movie
def delete_movie(_, info, _id):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movies['movies'].remove(movie)
                newmovie = movie
                newmovies = movies
                # delete the movie from the actors list
                with open('{}/data/actors.json'.format("."), "r") as rfile:
                    actors = json.load(rfile)
                    for actor in actors['actors']:
                        if _id in actor['films']:
                            actor['films'].remove(_id)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


# define function to resolve adding a new movie with all the fields
def add_movie(_, info, _title, _director, _rating, _actors):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        # create a string id using uid
        newmovie = {
            "id": str(uuid.uuid4()),
            "title": _title,
            "director": _director,
            "rating": _rating,
        }
        movies['movies'].append(newmovie)
        # add the movie to the actors list
        with open('{}/data/actors.json'.format("."), "r") as rfile:
            actors = json.load(rfile)
            for actor in actors['actors']:
                if actor['id'] in _actors:
                    
                    actor['films'].append(newmovie['id'])
                    # save the actors list
                    with open('{}/data/actors.json'.format("."), "w") as wfile:
                        json.dump(actors, wfile)
        newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


    # define function to resolve updating a movie
def update_movie(_, info, _id, _title="null", _director="null", _rating=0):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['title'] = _title if _title!="null" else movie['title']
                movie['director'] = _director if _director!="null" else movie['director']
                movie['rating'] = _rating if _rating!=0 else movie['rating']
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

