# storing all functions used for performing the different authentication process of log in and log out.
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.user import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token

auth = Blueprint('auth', __name__, url_prefix ='/api/v1/auth')

#User registration 
@auth.route('/register', methods = ['POST'])
def register_user():
    data = request.get_json()
    name = data.get ('name')
    role = data.get('role', 'client').lower()
    password = data.get ('password')
    email = data.get('email')

    if role not in ['admin', 'client']:
        return jsonify({'error': 'Invalid role'}), HTTP_400_BAD_REQUEST
    
    if not name or not email or not password:
       return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    
    if len(password) < 8:
        return jsonify({"error": "Password is too short. Enter atleast 8 characters"})
    
    if not validators.email(email):
        return jsonify({"error": "Enter a valid email"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "This email address is already in use, please select another"}), HTTP_409_CONFLICT


    try:
        hashed_password = bcrypt.generate_password_hash(password) #hashing the password
        
        #creating a new user
        new_user = User(name,password=hashed_password,email=email)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        db.session.rollback()
        
        #keeping track of the author name
        user_name =new_user.user_info()
        
        return jsonify({
            'message': user_name + ' has been successfully craeted as a '+ role, 
            'user':{
                'name':new_user.name,
                'email':new_user.email,
                'role': new_user.role,
                'created_at':new_user.created_at,
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

        user = User.query.filter_by(email=email).first()
        
        if User:
            
            is_correct_password = bcrypt.check_password_hash(user.password,password)
            refresh_token = create_refresh_token(identity=user.id)


            if is_correct_password:
            
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))

                return jsonify({
                    'user':{
                        'id':user.id,
                        'user_name':user.user_info(),
                        'email':user.email,
                        'access_token':access_token,
                        'refresh_token':refresh_token
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
    
    



