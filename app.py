
from flask import Flask, request, Response, jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_cors import CORS



app = Flask(__name__)
# CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='Lolalolalolla'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    ceo = db.Column(db.String(80), nullable=False)
    cto = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    website = db.Column(db.String(80), nullable=False)
    following = db.Column(db.Integer(), nullable=False)
    donation = db.Column(db.Integer(), nullable=False)

with app.app_context():
    print("Pre flight check  " + str(app.name))
    db.create_all()    
    print("Database Initialized")

@app.route('/get_all_company', methods=['GET'])
def get_all_company():
    all_company = Company.query.all()
    result = company_schema.dump(all_company)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(password)
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = user.query.filter_by(username=username).first()

    if user:
        if bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'logged in', 'id': user.id, 'username': user.username})
        else:
            return jsonify({'message': 'wrong password'})
    else:
        return jsonify({'message': 'user not found'})

if __name__=="__main__":
    app.run(debug=True)