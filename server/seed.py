from app import app
from model import db, Users, Itinerary, Destination, ItineraryDestination
from datetime import datetime

with app.app_context():

    ItineraryDestination.query.delete()
    Itinerary.query.delete()
    Users.query.delete()
    Destination.query.delete()

    user1 = Users(name = "Pauline", email = "pauline@gmail.com")
    user2 = Users(name = "Willy", email = "willy@gmail.com")
    user3 = Users(name = "Anthony", email = "anthony@gmaol.com")
    user4 = Users(name = "Lea", email = "lea@gmail.com")
    users = [user1, user2, user3, user4]

    db.session.add_all(users)
    db.session.commit()

    paris = Destination(name = "Paris", location = "France")
    tokyo = Destination(name = "Tokyo", location = "Japan")
    new_york = Destination(name = "New York", location = "USA")
    london =  Destination(name = "London", location = "UK")
    destinations = [paris, tokyo, new_york, london]

    db.session.add_all(destinations)
    db.session.commit()

    itinerary1 = Itinerary(
        title="Pauline's European Adventure", 
        start_date=datetime.strptime("2025-02-01", "%Y-%m-%d").date(), 
        end_date=datetime.strptime("2025-02-10", "%Y-%m-%d").date(), 
        user_id=user1.id
    )
    itinerary2 = Itinerary(
        title="Willy's Asian Adventure", 
        start_date=datetime.strptime("2025-03-20", "%Y-%m-%d").date(), 
        end_date=datetime.strptime("2025-03-30", "%Y-%m-%d").date(), 
        user_id=user2.id
    )
    itinerary3 = Itinerary(
        title="Anthony's North America Adventure", 
        start_date=datetime.strptime("2025-04-10", "%Y-%m-%d").date(), 
        end_date=datetime.strptime("2025-04-20", "%Y-%m-%d").date(), 
        user_id=user3.id
    )
    itineraries = [itinerary1, itinerary2, itinerary3]

    db.session.add_all(itineraries)
    db.session.commit()

    itinerary_destination1 = ItineraryDestination(itinerary_id = itinerary1.id, destination_id = paris.id)
    itinerary_destination2 = ItineraryDestination(itinerary_id = itinerary1.id, destination_id = london.id)
    itinerary_destinaton3 = ItineraryDestination(itinerary_id = itinerary2.id, destination_id = tokyo.id)
    itinerary_destination4 = ItineraryDestination(itinerary_id = itinerary3.id, destination_id = new_york.id)


    itinerary_destinations = [itinerary_destination1, itinerary_destination2, itinerary_destinaton3, itinerary_destination4]

    db.session.add_all(itinerary_destinations)

    db.session.commit()
    print("Database seeded successfully!")