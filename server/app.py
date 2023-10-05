#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

import pdb


class Index(Resource):
    def get(self):
        return {"message": "Welcome!"}


class ClearSession(Resource):
    def delete(self):
        session["page_views"] = None
        session["user_id"] = None

        return {}, 204


class Signup(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get("username")
        password = json_data.get("password")

        if not username or not password:
            return {"message": "Username and password are required."}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "Username already exists."}

        new_user = User(username=username, _password_hash=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        
        user_id = session['user_id']
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        return {}, 204
        

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get("username")
        pwd = json_data.get("password")
        user = User.query.filter(User.username == username).first()

        if username and pwd:
            session["user_id"] = user.id
            return user.to_dict(), 200


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return [], 204


api.add_resource(Index, "/")
api.add_resource(ClearSession, "/clear", endpoint="clear")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
