import pymongo
import flask_restful
from flask_restful import reqparse


MONGO_HOST = '10.5.1.160'
MONGO_PORT = 32768
MONGO_USER = 'jef'
MONGO_PASS = 'jeflovespython'


class Mongo:
    def __init__(self, host=None, port=None, user=None, password=None):
        self.host = host and host or '127.0.0.1'
        self.port = port and port or 27017
        self.user = user or None
        self.password = password or None

    def __enter__(self):
        self.mongo_clitnt = self.user and pymongo.MongoClient(f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/') or pymongo.MongoClient(f'mongodb://{self.host}:{self.port}/')
        return self.mongo_clitnt

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.mongo_clitnt.close()


def load_payload():
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        col.insert_many(payload).inserted_ids
        print('OK')


def delete_all():
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        col.delete_many({})
        print('OK')


def count_mongo(q):
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        return col.count(q) or None


def find_mongo(q):
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        return [x for x in col.find(q, {'_id': 0})]


def insert_mongo(q):
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        cur = col.insert_one(q)
        return cur.inserted_id and True or False


def delete_mongo(q):
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        col.delete_one(q)
        return True


def update_mongo(f, u):
    with Mongo(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS) as mc:
        db = mc.jef_db
        col = db.us_capitals
        r = col.update_one(f, {'$set': u})
        return r.modified_count and True or False



app = flask.Flask(__name__)
api = flask_restful.Api(app)


@app.route('/')
def root_page():
    return 'This is the HOMEPAGE.'


class Allusers(flask_restful.Resource):
    def get(self):
        return find_mongo({}), 200


class User(flask_restful.Resource):
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('age')
        parser.add_argument('occupation')
        args = parser.parse_args()
        print(args)

        if find_mongo({'name': name}):
            return f'User with name {name} already exist.', 400

        user_payload = {
            'name': name,
            'age': args.get('age'),
            'occupation': args.get('occupation'),
        }
        insert_mongo(user_payload)
        return find_mongo({'name': name}), 201

    def get(self, name):
        q = {'name': name}
        if count_mongo(q):
            return find_mongo(q), 200
        return 'User not found', 404

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('age')
        parser.add_argument('occupation')
        arges = parser.parse_args()

        origin_age = find_mongo({'name': name})[-1].get('age')
        origin_occupation = find_mongo({'name': name})[-1].get('occupation')
        input_payload = {
            'age': arges.get('age') or origin_age,
            'occupation': arges.get('occupation') or origin_occupation,
        }
        f = {'name': name}
        u = input_payload
        if count_mongo(f):
            update_mongo(f, u)
            return 'User modified.', 200
        return 'User not found.', 404

    def delete(self, name):
        if count_mongo({'name': name}):
            delete_mongo({'name': name})
            return 'User deleted!', 200
        else:
            return 'User not found.', 404


class UserCount(flask_restful.Resource):
    def get(self):
        return {'count': count_mongo({})}


api.add_resource(Allusers, '/api/v1.0/allusers')
api.add_resource(User, '/api/v1.0/user/<string:name>')
api.add_resource(UserCount, '/api/v1.0/usercount')

payload = [
    {
        'name': 'jef',
        'age': 18,
        'occupation': 'full-stack Python developer',
    },
    {
        'name': 'joy',
        'age': 16,
        'occupation': 'advanced ERP consultant',
    },
    {
        'name': 'rex',
        'age': 39,
        'occupation': 'general manager',
    },
    {
        'name': 'alex',
        'age': 56,
        'occupation': 'AI guru',
    }
]


if __name__ == '__main__':
    app.run(debug=True)
