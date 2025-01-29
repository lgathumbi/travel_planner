from app import app
from model import db, Users, Itinerary, Destination, Itinerary_Destination

with app.app_context():

    Itinerary_Destination.query.delete()
    Itinerary.query.delete()
    Users.query.delete()
    Destination.query.delete()

    user1 = Users(name = "Pauline", email = "pauline@gmail.com")
    user2 = Users(name = "Willy", email = "willy@gmail.com")
    user3 = Users(name = "Anthony", email = "anthony@gmaol.com")
    user4 = Users(name = "Lea", email = "lea@gmail.com")
    users = [user1, user2, user3, user4]

    db.session.add_all(users)

    paris = Destination(name = "Paris", location = "France")
    tokyo = Destination(name = "Tokyo", location = "Japan")
    new_york = Destination(name = "New York", location = "USA")
    london =  Destination(name = "London", location = "UK")
    destinations = [paris, tokyo, new_york, london]

    db.session.add_all(destinations)

    itinerary1 = Itinerary(title = "Pauline's European Adventure", start_date = "2025-02-01", end_date = "2025-02-10", user_id = user1.id)
    itinerary2 = Itinerary(title = "Willy's Asian Adventure", start_date = "2025-03-20", end_date = "2025-03-30", user_id = user2.id)
    itinerary3 = Itinerary(title = "Anthony's North America Adventure", start_date = "2025-04-10", end_date = "2025-04-20", user_id = user3.id)
    itinerary4 = Itinerary(title = "Lea's UK Adventure", start_date = "2025-05-25", end_date = "2025-06-03", user_id = user4.id)
    itineries = [itinerary1, itinerary2, itinerary3, itinerary4]

    db.session.add_all(itineries)

    itinerary_destination1 = Itinerary_Destination(itinerary_id = itinerary1.id, destination_id = paris.id)
    itinerary_destination2 = Itinerary_Destination(itinerary_id = itinerary1.id, destination_id = london.id)
    itinerary_destinaton3 = Itinerary_Destination(itinerary_id = itinerary2.id, destination_id = tokyo.id)
    itinerary_destination4 = Itinerary_Destination(itinerary_id = itinerary3.id, destination_id = new_york.id)
    itinerary_destination5 = Itinerary_Destination(itinerary_id = itinerary4.id, destination_id = london.id)
    itinerary_destination6 = Itinerary_Destination(itinerary_id = itinerary4.id, destination_id = paris.id)

    itinerary_destinations = [itinerary_destination1, itinerary_destination2, itinerary_destinaton3, itinerary_destination4, itinerary_destination5, itinerary_destination6]

    db.session.add_all(itinerary_destinations)

    db.session.commit()
    print("Database seeded successfully!")