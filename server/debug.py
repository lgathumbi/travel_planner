from app import app
from model import db, Users, Itinerary, Destination, ItineraryDestination

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
