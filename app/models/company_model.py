from app.extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companys'
   
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    full_names = db.Column(db.String(200), nullable = False)
    origin = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    author = db.relationship('Author', backref ='companys')   
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    
    
    def __init__(self, full_names, origin, description, author_id, created_at, updated_at):
        super(Company,self).__init__()
        self.full_names = full_names
        self.origin = origin
        self.description = description
        self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at
        
    def __repr__(self):
        return f'{self.full_names} {self.origin}'
    