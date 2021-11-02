from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def create_user(cls, data):

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);"

        return MySQLConnection('recipes_schema').query_db(query, data)

    @classmethod
    def get_user_by_info(cls, data):
    
        query = "SELECT * from users WHERE email = %(email)s"


        results = MySQLConnection('recipes_schema').query_db(query,data)
        print(results)
        print
        users = []

        for line in results:
            users.append(User(line))
        
        return users

    @staticmethod
    def validate_user(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 2 or len(data['first_name']) > 100:
            is_valid = False
            flash('Enter valid first name!')

        if len(data['last_name']) < 2 or len(data['last_name']) > 100:
            is_valid = False
            flash('Enter valid last name!')
        
        if len(User.get_user_by_info(data)) > 0:
            is_valid = False
            flash('Name and email is registered already!')

        if not email_regex.match(data['email']):
            is_valid = False
            flash('Enter valid email!')
        
        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash('Enter valid password!')


        return is_valid

