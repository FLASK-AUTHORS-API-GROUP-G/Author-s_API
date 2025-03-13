from app.extensions import db
from datetime import datetime


class Author(db.Model):
    __tablename__ = 'authors'      # declare a variable name and assign it a name different from the default name
                                 #so that we enable  customizing so that the name has to 
   
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    contact = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    image = db.Column(db.String(255), nullable = True) 
    bio = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime, default =datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

    def _init_(self,first_name,last_name,contact, email, password, bio,created_at, updated_at, image):
        super(Author, self).__init__()
        self.first_name= first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image
        self.bio = bio
        self.created_at = created_at
        self.updated_at = updated_at
            
    def author_info(self):
        if self.first_name and self.last_name:
            
            return(f' {self.first_name} {self.last_name} ')   
        
        return None