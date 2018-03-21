from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')

db_object = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db_object.Model):
    id = db_object.Column(db_object.Integer, primary_key=True)
    username = db_object.Column(db_object.String(80), unique=True)
    email = db_object.Column(db_object.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# new user
@app.route("/register", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    db_object.session.add(User(username, email))
    db_object.session.commit()

    return jsonify("User Added")

# all users
@app.route("/users", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

# user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return jsonify((user_schema.dump(user)).data)

# update user
@app.route("/update/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db_object.session.commit()
    return jsonify("Edit details from the body")

# delete user
@app.route("/delete/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db_object.session.delete(user)
    db_object.session.commit()

    return jsonify("User deleted")

if __name__ == '__main__':
    app.run(debug=True)
