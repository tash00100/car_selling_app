from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'  # Use PostgreSQL in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'buyer', 'seller', 'admin'
    contact_info = db.Column(db.String(200), nullable=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', backref=db.backref('cars', lazy=True))
    image_main = db.Column(db.String(200), nullable=False)
    image_back = db.Column(db.String(200), nullable=False)
    image_front = db.Column(db.String(200), nullable=False)
    image_engine = db.Column(db.String(200), nullable=False)
    image_side = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='available')  # 'available' or 'sold'

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_pw, role=data['role'], contact_info=data.get('contact_info'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        'id': car.id, 
        'make': car.make, 
        'model': car.model, 
        'price': car.price, 
        'description': car.description,
        'seller': car.seller.username,
        'contact_info': car.seller.contact_info,
        'image_main': car.image_main,
        'images': [car.image_back, car.image_front, car.image_engine, car.image_side],
        'status': car.status
    } for car in cars])

@app.route('/cars', methods=['POST'])
@jwt_required()
def add_car():
    data = request.get_json()
    user = get_jwt_identity()
    if user['role'] != 'seller':
        return jsonify({'message': 'Only sellers can add cars'}), 403
    
    new_car = Car(
        make=data['make'], 
        model=data['model'], 
        price=data['price'], 
        description=data.get('description', ''),
        seller_id=user['id'],
        image_main=data['image_main'],
        image_back=data['image_back'],
        image_front=data['image_front'],
        image_engine=data['image_engine'],
        image_side=data['image_side']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car added successfully'})

@app.route('/cars/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    user = get_jwt_identity()
    car = Car.query.get_or_404(car_id)
    if user['role'] != 'admin' and car.seller_id != user['id']:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
