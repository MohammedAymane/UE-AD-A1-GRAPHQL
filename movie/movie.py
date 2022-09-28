from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# ADD THINGS HERE
#
###

# root message


@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

#####
# graphql entry points


@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200


@app.route('/graphql', methods=['POST'])
def graphql_server():
    # Tout d’abord, il nous faut charger les types déclarés dans le schéma GraphQL
    type_defs = load_schema_from_path('movie.graphql')

    # Nous devons ensuite créer les objets associés au schéma. Ici nous avons pour le moment deux types d’objets, Query et Movie.
    query = QueryType()
    movie = ObjectType('Movie')
    query.set_field('movie_with_id', r.movie_with_id)





    # Nous devons maintenant associer le resolver à la mutation déclarée dans le schéma. Nous faisons donc les modifications suivantes :
    mutation = MutationType()
    mutation.set_field('update_movie_rate', r.update_movie_rate)

    # Nous allons maintenant devoir déclarer le type actor
    actor = ObjectType('Actor')
    # Nous allons devoir attacher notre resolver à la liste des acteurs à construire dans le type Movie du schéma
    movie.set_field('actors', r.resolve_actors_in_movie)


    # Nous allons maintenant déclarer la Query pour la requete all_movies
    query.set_field('all_movies', r.all_movies)

    # Nous allons maintenant déclarer la Mutation pour la requete delete_movie
    mutation.set_field('delete_movie', r.delete_movie)

    # Nous allons maintenant déclarer la Mutation pour la requete add_movie
    mutation.set_field('add_movie', r.add_movie)

    # Nous allons maintenant déclarer la Mutation pour la requete update_movie
    mutation.set_field('update_movie', r.update_movie)

    # Enfin, la création de notre schéma exécutable.
    schema = make_executable_schema(type_defs, movie, query, mutation, actor)


    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
