from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
from google.protobuf.json_format import MessageToJson





def get_movie_by_id(id):
   # get movie by id using graphql query
   query = """
   query {
       movie_with_id(_id: "%s") {
           id
           title
           rating
           actors{firstname}
           director
           }
       }
   """ % id
   url = 'http://localhost:3001/graphql'
   r = requests.post(url, json={'query': query})
   return r.json()


def get_booking_by_id(stub,id):
    return stub.getBooking(id)

def get_list_movies():
   # get movie by id using graphql query
   query = """
   query {
       all_movies {
           id
           title
           rating
           actors
           directors
           }
       }
   """
   url = 'http://localhost:3001/graphql'
   r = requests.post(url, json={'query': query})
   return r.json()



app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# create user endpoints according to the API specification
# get all users
@app.route("/users", methods=['GET'])
def get_users():
   return make_response(jsonify(users),200)

# get user by id
@app.route("/users/<string:user_id>", methods=['GET'])
def get_user(user_id):
   for user in users:
       if user["id"] == user_id:
           return make_response(jsonify(user),200)
   raise NotFound("User with id {} not found".format(user_id))

# post user
@app.route("/users", methods=['POST'])
def post_user():
   user = request.json
   # check if user already exists
   for u in users:
       if u["id"] == user["id"]:
           raise NotFound("User with id {} already exists".format(user["id"]))
   users.append(user)
   return make_response(jsonify(user),201)


   # remove user
@app.route("/users/<string:user_id>", methods=['DELETE'])
def delete_user(user_id):
   for user in users:
       if user["id"] == user_id:
           users.remove(user)
           return make_response(jsonify(user),200)
   raise NotFound("User with id {} not found".format(user_id))

   # update user
@app.route("/users/<string:user_id>", methods=['PUT'])
def put_user(user_id):
   user = request.json
   for u in users:
       if u["id"] == user_id:
           users.remove(u)
           users.append(user)
           return make_response(jsonify(user),200)
   raise NotFound("User with id {} not found".format(user_id))


   # get bookings for a user by user id using the booking service
@app.route("/users/<string:user_id>/bookings", methods=['GET'])
def get_user_bookings(user_id):
   # check if user exists
   for user in users:
       if user["id"] == user_id:
         #   get bookings for user
           with grpc.insecure_channel('localhost:3002') as channel: ## WITH GRPC
                bookingStub = booking_pb2_grpc.BookingStub(channel)
                booking = MessageToJson(get_booking_by_id(bookingStub, booking_pb2.userId(userid=user_id)))
           channel.close()
           return make_response(json.loads(booking),200)
   raise NotFound("User with id {} not found".format(user_id))
   

# get movies for a user by user booking using the booking and movie services
@app.route("/users/<string:user_id>/movies", methods=['GET'])
def get_user_movies(user_id):
   # check if user exists
   for user in users:
       if user["id"] == user_id:
           # get bookings for user
           movies = []
           with grpc.insecure_channel('localhost:3002') as channel: ## WITH GRPC
                bookingStub = booking_pb2_grpc.BookingStub(channel)
                booking = get_booking_by_id(bookingStub, booking_pb2.userId(userid=user_id))
           channel.close()
           # get movies for all bookings
           for b in booking.dates:
                     for s in b.movies:
                        print(s)
                        movies.append(get_movie_by_id(s))
           return make_response(jsonify(movies),200)
   raise NotFound("User with id {} not found".format(user_id))



@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"





if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
