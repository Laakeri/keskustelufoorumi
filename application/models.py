from application import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    message = db.Column(db.Text, nullable=False)
    def __init__(self, message, parent):
        self.message = message
        self.parent = parent
        
