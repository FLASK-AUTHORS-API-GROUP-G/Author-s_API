from app.extensions import db
from datetime import datetime

class Book (db.Model):
    
    __tablename__ = 'books'
    
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(100), nullable = False)
    image = db.Column(db.String(100), nullable = False)  
    no_of_pages = db.Column(db.Integer, nullable = False)
    price_unit = db.Column(db.Integer, default= 'Ugx')  
    publication_date = db.Column(db.Date, default = datetime.now())
    isbn = db.Column(db.String(100), nullable = True, unique = True)
    genre = db.Column(db.String(50), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id') )
    company_id = db.Column(db.Integer, db.ForeignKey('companys.id'))
    author = db.relationship('Author', backref= 'books')
    company =db.relationship('Company', backref ='books')
    created_at = db.Column(db.DateTime,default =datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    
    
    def __init__(self, title,price,isbn, descrpition, image, no_of_pages, price_unit, publication_date, gener, author_id, company_id):
        super(Book,self).__init__()
        self.title = title
        self.price = price
        self.isbn = isbn
        self.description = descrpition
        self.iamge = image
        self.no_of_pages = no_of_pages
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.gener = gener
        self.author_id = author_id
        self.company_id = company_id
        
        
    def __repr__(self):
        return f'Book {self.title}'
    
    
    
    