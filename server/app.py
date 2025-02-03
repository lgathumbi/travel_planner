import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api
from model import db, Users, Itinerary, Destination, ItineraryDestination
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Travel Itinerary Service</h1>"

@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "GET":
        users = Users.query.all()
        users_dict = [user.to_dict(only=("id", "name", "email")) for user in users]
        return jsonify(users_dict), 200

    elif request.method == "POST":
        data = request.get_json()
        try:
            user = Users(
                name=data["name"],
                email=data["email"]
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
           return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>', methods=["PATCH", "PUT", "DELETE"])
def user_detail(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method in ["PATCH", "PUT"]:
        data = request.get_json()
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return jsonify(user.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200                
        
@app.route('/itineraries', methods=["GET", "POST"])
def itineraries():
    if request.method == "GET":
        itineraries = Itinerary.query.all()
        itineraries_dict = [itinerary.to_dict(only=("id", "title", "start_date", "end_date", "user_id")) for itinerary in itineraries]
        return jsonify(itineraries_dict), 200

    elif request.method == "POST":
        data = request.get_json()
        try:
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            itinerary = Itinerary(
                title=data["title"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                user_id=data["user_id"]
            )
            db.session.add(itinerary)
            db.session.commit()
            return jsonify(itinerary.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/itineraries/<int:itinerary_id>', methods=["PATCH", "PUT", "DELETE"])
def itinerary_detail(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404

    if request.method in ["PATCH", "PUT"]:
        data = request.get_json()
        if "title" in data:
            itinerary.title = data["title"]
        if "start_date" in data:
            itinerary.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        if "end_date" in data:
            itinerary.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        db.session.commit()
        return jsonify(itinerary.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(itinerary)
        db.session.commit()
        return jsonify({"message": "Itinerary deleted successfully"}), 200
               
@app.route('/destinations', methods=["GET", "POST"])
def destinations():
    if request.method == "GET":
        destinations = Destination.query.all()
        destinations_dict = [destination.to_dict(only=("id", "name", "location")) for destination in destinations]
        return jsonify(destinations_dict), 200

    elif request.method == "POST":
        data = request.get_json()
        try:
            destination = Destination(
                name=data["name"],
                location=data["location"]
            )
            db.session.add(destination)
            db.session.commit()
            return jsonify(destination.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/destinations/<int:destination_id>', methods=["PATCH", "PUT", "DELETE"])
def destination_detail(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    if request.method in ["PATCH", "PUT"]:
        data = request.get_json()
        if "name" in data:
            destination.name = data["name"]
        if "location" in data:
            destination.location = data["location"]
        db.session.commit()
        return jsonify(destination.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message": "Destination deleted successfully"}), 200

        
@app.route('/itinerary_destinations', methods=["GET", "POST"])
def handle_itinerary_destinations():
    if request.method == "GET":
        try:
            itinerary_destinations = ItineraryDestination.query.all()
            itinerary_destinations_dict = [
                itinerary_destination.to_dict() for itinerary_destination in itinerary_destinations
            ]
            return jsonify(itinerary_destinations_dict), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    elif request.method == "POST":
        data = request.get_json()
        try:
            itinerary_destinations = ItineraryDestination(
                itinerary_id=data["itinerary_id"],
                destination_id=data["destination_id"]
            )
            db.session.add(itinerary_destinations)
            db.session.commit()
            return jsonify(itinerary_destinations.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
@app.route('/itinerary_destinations/<int:itinerary_destination_id>', methods=["DELETE"])
def delete_itinerary_destination(itinerary_destination_id):
    itinerary_destination = ItineraryDestination.query.get(itinerary_destination_id)
    if not itinerary_destination:
        return jsonify({"error": "Itinerary-Destination link not found"}), 404

    db.session.delete(itinerary_destination)
    db.session.commit()
    return jsonify({"message": "Itinerary-Destination link deleted successfully"}), 200        

if __name__ == "__main__":
    app.run(port=5555, debug=True)
