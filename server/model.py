from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(
     naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True

    def to_dict(self, only=None):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if only:
            data = {key: value for key, value in data.items() if key in only}
        return data

class Users(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    itineraries = db.relationship('Itinerary', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-itineraries.user',)

    def __repr__(self):
        return f"<User {self.name}, {self.email}>"
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email")
        return email

class Itinerary(BaseModel):
    __tablename__ = "itineraries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('Users', back_populates='itineraries')
    itinerary_destinations = db.relationship('ItineraryDestination', back_populates='itinerary', cascade='all, delete-orphan')

    destinations = association_proxy('itinerary_destinations', 'destination',
                                 creator=lambda destination_obj: ItineraryDestination(destination=destination_obj))


    serialize_rules = ('-itinerary_destinations.itinerary', '-user.itineraries')

    def __repr__(self):
        return f"<Itinerary {self.title}, User {self.user_id}>"

class Destination(BaseModel):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    itinerary_destinations = db.relationship('ItineraryDestination', back_populates='destination', cascade='all, delete-orphan')

    serialize_rules = ('-itinerary_destinations.destination',)

    def __repr__(self):
        return f"<Destination {self.name}, Location {self.location}>"

    
class ItineraryDestination(BaseModel):
    __tablename__ = "itinerary_destinations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)

    itinerary = db.relationship('Itinerary', back_populates='itinerary_destinations')
    destination = db.relationship('Destination', back_populates='itinerary_destinations')

    serialize_rules = ('-itinerary.itinerary_destinations', '-destination.itinerary_destinations')

    def __repr__(self):
        return f"<ItineraryDestination Itinerary {self.itinerary_id}, Destination {self.destination_id}>"
