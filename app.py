from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields
import sqlalchemy
import os
import datetime
import jwt
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='Lolalolalolla'
db = SQLAlchemy(app)
load_dotenv()

jwt_sec = os.getenv("JWT_SECRET")


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    ceo = db.Column(db.String(80), nullable=False)
    cto = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    website = db.Column(db.String(80), nullable=False)
    following = db.Column(db.Integer(), nullable=False)
    donation = db.Column(db.Integer(), nullable=False)

class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    ceo = fields.Str(required=True)
    cto = fields.Str(required=True)
    address = fields.Str(required=True)
    email = fields.Str(required=True)
    website = fields.Str(required=True)
    following = fields.Int(required=True)
    donation = fields.Int(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

company_schema = CompanySchema()
company_schemas = CompanySchema(many=True)


with app.app_context():
    print("Pre flight check  " + str(app.name))
    db.create_all()    
    print("Database Initialized")

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/token', methods=['POST'])
def token_gen():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and username=="admin_mon":
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'username': username,'isAdmin':'true', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, jwt_sec, algorithm="HS256")
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'wrong pass or your are not admin'}),403
    else:
        return jsonify({'message': 'user not found'}),404



@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(password)
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    try:    
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}),200
    except IntegrityError:
        return jsonify({'message': 'User already exists'}),403

@app.route('/add_company', methods=['POST'])
def add_company():
    
    data = request.get_json()
    jwt_1 = data.get('jwt')
    admin_token = data.get('admin_token')
    name = data.get('name')
    ceo = data.get('ceo')
    cto = data.get('cto')
    address = data.get('address')
    email = data.get('email')
    website = data.get('website')
    following = data.get('following')
    donation = data.get('donation')
    new_company = Company(name=name, ceo=ceo, cto=cto, address=address, email=email, website=website, following=following, donation=donation)
    try:
        jwt_decode = jwt.decode(jwt_1, jwt_sec, algorithms="HS256")
    except jwt.exceptions.DecodeError as e:
        print(e)
        return jsonify({'message': 'JWT NOT GOOD '}),418
    if jwt_decode is not None:
        if jwt_decode['isAdmin'] == 'true':
            try:
                db.session.add(new_company)
                db.session.commit()
                return jsonify({'message': 'Company added successfully'}),200
            except IntegrityError as e:
                print(e)
                return jsonify({'message': 'Company is already there'}),403
        else:
            return jsonify({'message': 'You are not admin'}),403
    return jsonify({'message': 'You are not admin'}),403
    



@app.route('/get_company/<id>', methods=['GET'])
def get_company(id):
    company = Company.query.get(id)
    result =  company_schema.dump(company)
    return jsonify(result)

@app.route('/get_all_company', methods=['GET'])
def get_all_company():
    all_company = Company.query.all()
    result = company_schemas.dump(all_company)
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user:
        if bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'logged in', 'id': user.id, 'username': user.username}),200
        else:
            return jsonify({'message': 'wrong password'}),403
    else:
        return jsonify({'message': 'user not found'}),404

if __name__=="__main__":
    app.run(debug=True)