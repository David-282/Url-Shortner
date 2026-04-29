from datetime import datetime, timezone

from database import db


class Url(db.Model):
    __tablename__ = "urls"


    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text,nullable=False)
    no_of_visits = db.Column(db.Integer,default=0)
    generated_url = db.Column(db.String(10),nullable=False,unique=True)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
