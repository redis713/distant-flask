from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGBLOB
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()

listener_programs = db.Table(
    "listener_programs",

    db.Column(
        "listener_id",
        db.Integer,
        db.ForeignKey("listener.id"),
        primary_key=True
    ),

    db.Column(
        "program_id",
        db.Integer,
        db.ForeignKey("programs.id"),
        primary_key=True
    )
)


class Listener(db.Model):
    __tablename__ = "listener"
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    job =db.Column(db.String(1024), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    institution = db.Column(db.String(255), nullable=True)

    programs = db.relationship(
        "Program",
        secondary=listener_programs,
        back_populates="listeners"
    )

    def __repr__(self):
        return f"<Listener {self.lastname} {self.firstname}>"


class Program(db.Model):
    __tablename__ = "programs"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False, unique=True)

    listeners = db.relationship("Listener", secondary=listener_programs, back_populates="programs")

    def __repr__(self):
        return f"<Program {self.title}>"