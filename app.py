# app.py
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from serialization import movies_schema, movie_schema, directors_schema, director_schema, genres_schema, genre_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
JSON_AS_ASCII = False
JSONIFY_PRETTYPRINT_REGULAR = True
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        genre_key = request.args.get("genre_id")
        director_key = request.args.get("director_id")

        if director_key and genre_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key) and
                                                    Movie.genre_id == int(genre_key)).all()

        elif genre_key:
            result = db.session.query(Movie).filter(Movie.genre_id == int(genre_key)).all()
            print(result)
        elif director_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key)).all()
            print(result)


        else:
            result = db.session.query(Movie).all()
        if result:
            print(result)
            return movies_schema.dump(result), 200
        else:
            return jsonify({"ValueError": "id not found"})

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return jsonify({"ValueError": 'Movie_id not found'})
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def patch(self, uid):
        movie = db.session.query(Movie).get(uid)
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director" in req_json:
            movie.genre_id = req_json.get("genre_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return jsonify({"ValueError": 'Movie_id not found'})

        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_drirectors = db.session.query(Director).all()
        return directors_schema.dump(all_drirectors), 200


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = db.session.query(Director).get(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = db.session.query(Genre).get(uid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404


if __name__ == '__main__':
    app.run(debug=True)
