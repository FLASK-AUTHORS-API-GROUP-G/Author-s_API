#helps to intialize the working with multiple instances
# We then work with appliction factory function
# it helps to organize and makes it easy to work with the code

# any extension that we work with we have to regiter it here
# Application factory function(Define the app instance within the function) helps to rellate with different 3rd party libraries
from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.authors.authors_controller import authors

def create_app():
    
    # Can't migrate before configuring
    app = Flask(__name__) #  create a variable which is an instance(acts as a local variable for the special name and it returns the variable name) ie app
    app.config.from_object('config.Config')     # access the config 
    db.init_app(app)   # intialize the db instance
    migrate.init_app(app,db)    #initialize the migrate instance
    jwt.init_app(app)
   
    
    
    # importing and registering models(they have to take the format from the parent to the least child)
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.books_model import Book
    
    
    #registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(authors)
    
    
    @app.route('/')
    def home():
        return 'Authors API for many times'
    
    
    return app  #(Helps to set up different evnionments testing )