"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ----endpoints---- :

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters_query = Character.query.all()
    results = list(map(lambda item: item.serialize(), characters_query))
    response_body = {
        "msg": "OK", 
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_characters(characters_id):
    character_query = Character.query.filter_by(id=characters_id).first()

    response_body = {
        "msg": "OK", 
        "results": character_query.serialize()
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planet.query.all()
    results = list(map(lambda item: item.serialize(), planets_query))
    response_body = {
        "msg": "OK", 
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planets(planets_id):
    planet_query = Planet.query.filter_by(id=planets_id).first()

    response_body = {
        "msg": "OK", 
        "results": planet_query.serialize()
    }

    return jsonify(response_body), 200


# ----fin endpoints---- :
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
