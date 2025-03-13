from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db, bcrypt

from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token

# authors blueprint
authors = Blueprint('authors', __name__,url_prefix='/api/v1/authors')

        
# Get all authors 
@authors.get('/all')
@jwt_required()
def get_all_authors():
    
    try:
        
        all_author = Author.query.all()
        
        authors_data = []
        
        for author in all_author:
            author_info ={
                'id':author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username': author.author_info(),
                'email': author.email,
                'contact':author.contact,
                'created_at': author.created_at,
                'companys':[],
                'books':[]
                
            }
            
            if hasattr(author,'books'):   #check if the attribute has the data we want to access.
                author_info['books'] = [{   #use a list
                    'id': book.id,
                    'title':book.title,
                    'price':book.price,
                    'genre':book.genre,
                    'description':book.description,
                    'publication_date': book.publication_date,
                    'image':book.image,
                    'created_at': book.created_at
                }for book in author.books]
                
            if hasattr(author,'companys'):
                author_info['companys']= [{
                    'id':company.id,
                    'full_names':company.full_names,
                    'origin':company.origin,
                    } for company in author.companys]
                        
            authors_data.append(author_info)
            
        return jsonify({
                'message': 'All authors retrived successfully',
                'total_authors':len(authors_data),
                'author': authors_data
                
            }),HTTP_200_OK
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
# Getting author by ID

@authors.get('/authors/<int:id>')
@jwt_required()
def get_author(id):
    
    try:
        
        authors = Author.query.filter_by(id=id).first()
        
        books = []
        companys = []
        
        
            
        if hasattr(authors,'books'):   #check if the attribute has the data we want to access.
            books = [{   #use a list
                'id': book.id,
                'title':book.title,
                'price':book.price,
                'genre':book.genre,
                'description':book.description,
                'publication_date': book.publication_date,
                'image':book.image,
                'created_at': book.created_at
                }for book in authors.books]
                
        if hasattr(authors,'companys'):
                companys= [{
                    'id':company.id,
                    'full_names':company.full_names,
                    'origin':company.origin,
                    } for company in authors.companys]
                        
        
            
        return jsonify({
                'message': 'Author details retrived successfully',
                
                'author':{
                    'id':authors.id,
                    'first_name': authors.first_name,
                    'last_name': authors.last_name,
                    'username': authors.author_info(),
                    'email': authors.email,
                    'contact':authors.contact,
                    'bio': authors.bio,
                    'created_at': authors.created_at,
                    'companys': companys,
                    'books': books
                }
                
            }),HTTP_200_OK
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
        
# Updating author details

@authors.route('/edit/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_author_details(id):
    
    try:
        
        current_author = get_jwt_identity()
        logined_in_author = Author.query.filter_by(id=current_author).first()
        
        
        #  get authpor by id
        author = Author.query.filter_by(id=id).first()
        
        if not author:
            return jsonify({
                'error':'Author not found'
            }), HTTP_400_BAD_REQUEST
            
        # elif author.id!= current_author:
        #     return jsonify({
        #         'error': 'You are not authorized to update the details'
        #     })
            
            
        else:
            first_name = request.get_json().get('first_name',author.first_name)
            last_name =  request.get_json().get('last_name',author.last_name)
            contact =  request.get_json().get('contact',author.contact)
            email =  request.get_json().get('email',author.email)
            bio =  request.get_json().get('bio',author.bio)
            
            if 'password' in request.json:
                hashed_password = bcrypt.generate_password_hash(request.json.get('password'))
                author.password = hashed_password
                
            if email != author.email and Author.query.filter_by(email=email).first():
                return jsonify({
                    'error':'Email already in use'
                }), HTTP_409_CONFLICT
                
                
            if contact != author.contact and Author.query.filter_by(contact=contact).first():
                return jsonify({
                    'error':'Contact already in use'
                }), HTTP_409_CONFLICT
                
                
                
            author.first_name = first_name
            author.last_name = last_name
            author.contact = contact
            author.email = email
            author.bio = bio
            
            
            db.session.commit()
            
            author_name = author.author_info()
            
            return jsonify({
                'message':author_name + "'s details have been successfully updated",
                'author':{
                    'id':author.id,
                    'first_name':author.first_name,
                    'last_name':author.last_name,
                    'email':author.email,
                    'contact':author.contact,
                    'bio':author.bio,
                    'created_at':author.created_at,
            }
            })
            
         
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_404_NOT_FOUND

# deleting a user by id

@authors.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    
    try:
        
        current_author = get_jwt_identity()
        logined_in_author = Author.query.filter_by(id=current_author).first()
        
        
        #  get author by id
        author = Author.query.filter_by(id=id).first()
        
        if not author:
            return jsonify({
                'error':'Author not found'
            }), HTTP_400_BAD_REQUEST
            
        elif author.id!= current_author:
            return jsonify({
                'error': 'You are not authorized to delete the details'
            }), HTTP_403_FORBIDDEN
            
            
        else:
          
          
          #loop to delete the user associated with companys
          for company in author.companys:
              db.session.delete(company)
            
            #loop to delete the user associated with books
          for book in author.books:
              db.session.delete(book)
            
            
        db.session.delete(author)
        db.session.commit()
            
            
        return jsonify({
                'message':'Author deleted succesfully',
                
            })
            
         
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_404_NOT_FOUND


