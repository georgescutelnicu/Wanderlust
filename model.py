from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint


db = SQLAlchemy()

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    continent = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    budget = db.Column(db.String(10), CheckConstraint("budget IN ('affordable', 'moderate', 'expensive')"))

    eating_out = db.Column(db.Integer, CheckConstraint('eating_out >= 0 AND eating_out <= 5'))
    sightseeing = db.Column(db.Integer, CheckConstraint('sightseeing >= 0 AND sightseeing <= 5'))
    activities = db.Column(db.Integer, CheckConstraint('activities >= 0 AND activities <= 5'))
    shopping = db.Column(db.Integer, CheckConstraint('shopping >= 0 AND shopping <= 5'))
    nightlife = db.Column(db.Integer, CheckConstraint('nightlife >= 0 AND nightlife <= 5'))
    museums = db.Column(db.Integer, CheckConstraint('museums >= 0 AND museums <= 5'))
    kid_friendly = db.Column(db.Integer, CheckConstraint('kid_friendly >= 0 AND kid_friendly <= 5'))

    beaches = db.Column(db.Integer, CheckConstraint('beaches >= 0 AND beaches <= 5'))
    skiing = db.Column(db.Integer, CheckConstraint('skiing >= 0 AND skiing <= 5'))
    diving = db.Column(db.Integer, CheckConstraint('diving >= 0 AND diving <= 5'))
    camping = db.Column(db.Integer, CheckConstraint('camping >= 0 AND camping <= 5'))
    hiking = db.Column(db.Integer, CheckConstraint('hiking >= 0 AND hiking <= 5'))
    cycling = db.Column(db.Integer, CheckConstraint('cycling >= 0 AND cycling <= 5'))
    sailing = db.Column(db.Integer, CheckConstraint('sailing >= 0 AND sailing <= 5'))

    romantic = db.Column(db.Integer, CheckConstraint('romantic >= 0 AND romantic <= 5'))
    photography = db.Column(db.Integer, CheckConstraint('photography >= 0 AND photography <= 5'))

    popular_attractions = db.Column(db.String(500), nullable=True)
    picture = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        data = {'id': getattr(self, "id"),
                'continent': getattr(self, "continent"),
                'country': getattr(self, "country"),
                'city': getattr(self, "city"),
                'budget': getattr(self, "budget"),
                'ratings': ({column.name: getattr(self, column.name) for column in self.__table__.columns
                            if isinstance(column.type, db.Integer) and column.name != 'id'}),
                'description': getattr(self, "description"),
                'popular_attractions': getattr(self, "popular_attractions"),
                'picture': getattr(self, "picture")
                }

        return data