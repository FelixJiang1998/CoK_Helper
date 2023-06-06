from Alchemy import db

class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())


class Record(BaseModel):
    __tablename__ = "record"
    app_name = db.Column(db.String(64), nullable=False)

    last_run = db.Column(db.DateTime, default=db.func.now())
    last_monster = db.Column(db.DateTime, default=db.func.now())
    last_collect = db.Column(db.DateTime, default=db.func.now())
    last_daily = db.Column(db.DateTime, default=db.func.now())
    

