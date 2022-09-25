from marshmallow import Schema, fields


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    director_id = fields.Int()


movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)


class DirectorsSchema(Schema):
    id = fields.Int()
    name = fields.Str()


director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)


class GenresSchema(Schema):
    id = fields.Int()
    name = fields.Str()


genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)
