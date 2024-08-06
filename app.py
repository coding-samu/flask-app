from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import time
import psycopg2
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/mydatabase'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

def wait_for_db():
    while True:
        try:
            # Controlla se la connessione al database funziona
            conn = psycopg2.connect(
                dbname='mydatabase',
                user='postgres',
                password='postgres',
                host='db'
            )
            conn.close()
            break
        except OperationalError:
            print("Database not ready yet, waiting...")
            time.sleep(5)  # Aumenta il tempo di attesa a 5 secondi

@app.before_first_request
def create_tables():
    wait_for_db()  # Assicurati che il DB sia pronto
    db.create_all()
    print("Tables created!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
