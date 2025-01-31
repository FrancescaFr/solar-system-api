from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_planet(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"planet '{id}' is invalid"}, 400))

    planet = Planet.query.get(id)

    if not planet:
        abort(make_response({"message": f"Planet {id} not found"}, 404))

    return planet

@planet_bp.route("", methods=["GET", "POST"])
def handle_planets():
    if request.method == "POST":
        request_body = request.get_json()
        new_planet = Planet(name=request_body["name"], 
                            description=request_body["description"],
                            flag=request_body["flag"])
        db.session.add(new_planet)
        db.session.commit()
        return make_response(f"planet {new_planet.name} successfully created!", 201)
    
    elif request.method == "GET":
        name_query = request.args.get("name")
        flag_query = request.args.get("flag")
        
        planet_query = Planet.query

        if name_query:
            planet_query = planet_query.filter_by(name=name_query)
        if flag_query:
            planet_query = planet_query.filter_by(flag=flag_query)

        planets = planet_query.all()
        planets_response = [planet.to_dict() for planet in planets]
        return jsonify(planets_response)

@planet_bp.route("/<id>", methods=["GET"])
def get_one_planet(id):
    validate_planet(id)
    planet = Planet.query.get(id)
    return {"id": planet.id, 
            "name": planet.name, 
            "description": planet.description,
            "flag": planet.flag}
