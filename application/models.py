from application import db

class Post(db.Model):

    __tablename__ = "post"
    
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    user = db.relationship('User', foreign_keys=user_id)
    #parent = db.relationship('Post', foreign_keys=parent_id)
    
    def __init__(self, message, parent_id, user_id):
        self.message = message
        self.parent_id = parent_id
        self.user_id = user_id