from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token


auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')

# Author registration

@auth.route('/register',methods=['POST'])       #decorator to point tp oint to the blueprint    Methods for creating a new user
def register_author():
    data = request.json                 #variable to store the requets
    
    # storing request values and keep track of them
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    bio = data.get('bio','')
    
    
    # reducing redundancy ie reputation and empty values ie checking for null values.
    #validation of the incoming requets. and it works with the constraints
    
    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({
            'error':'All fields are required'
        }),HTTP_400_BAD_REQUEST
    
    if len(password)<8:   #to check the length of the password passed in.
        return jsonify({'error':'The password is short. Enter atleast 8 Characters'}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error': 'Enter a valid email'}), HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first() is not None:         #
        return jsonify({'error':'The email address is already used, Please select another'}), HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({'error':'This contact is already in use, Please use another contact'}), HTTP_409_CONFLICT
    
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') #hashing the password ie crypotology.
        
        # creating new author instance with the hashed password
        
        new_author = Author(
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        email=email,
        contact=contact,
        bio=bio,
        
        )
        
        db.session.add(new_author)
        db.session.commit()
        
        #keeping track of the author name
        author_name =new_author.author_info()
        
        if author_name is None:
            author_name = " Author"
            
            # retruning the instance 
        return jsonify({
            'message': author_name  + ' has been successfully craeted as an ' , #new_author.type,
            'user':{
                'id':new_author.id,
                'first_name':new_author.first_name,
                'last_name':new_author.last_name,
                'email':new_author.email,
                'contact':new_author.contact,
                'bio':new_author.bio,
                'created_at':new_author.created_at,
            }
        }),HTTP_201_CREATED
        
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    #user login
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    try:
        if not password or not email:
            return jsonify({
                'Message': 'Email and Password are required'
            }), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email=email).first()
        
        if author:
            
            is_correct_password = bcrypt.check_password_hash(author.password,password)
            refresh_token = create_refresh_token(identity=author.id)
            
            
            
            
            if is_correct_password:
                  # has to be unique ie pass in the identity.
                
                access_token = create_access_token(identity=str(author.id))
                refresh_token = create_refresh_token(identity=str(author.id))

                return jsonify({
                    'author':{
                        'id':author.id,
                        'username':author.author_info(),
                        'email':author.email,
                        'access_token':access_token,
                        'refresh_token':refresh_token,
                       
                    },
                    'message':'Login successful'
                }),HTTP_200_OK
                
            else:
                return jsonify({
                    'Message':'Invalid email password'
                }), HTTP_401_UNAUTHORIZED
        
        else:
            return jsonify({
                'Message': 'Invalid email address'
            }), HTTP_401_UNAUTHORIZED
    
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
        
    # refreshing Token
        
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())  
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token':access_token})


