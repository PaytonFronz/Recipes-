from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
from flask import flash

class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_mins = data['under_30_mins']
        self.instructions = data['instructions']
        self.description = data['description']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def create_recipe(cls, data):

        query = "INSERT INTO recipes (name, under_30_mins, instructions, description, date, user_id) VALUES (%(name)s, %(under_30_mins)s, %(instructions)s,%(description)s,%(date)s, %(user_id)s);"

        return MySQLConnection('recipes_schema').query_db(query, data)
    
    @classmethod
    def get_all_recipes(cls):
        
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"

        results = MySQLConnection('recipes_schema').query_db(query)

        recipes = []

        for item in results:
            recipe = Recipe(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):

        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'

        result = MySQLConnection('recipes_schema').query_db(query, data)[0]

        recipe = Recipe(result)

        user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],
            }

        recipe.user = User(user_data)

        return recipe
    
    @staticmethod
    def recipe_validation(data):
        is_valid = True

        if len(data['name']) < 1 or len(data['name']) > 100:
            is_valid = False
            flash("please enter a valid name for your recipe!")   

        if len(data['instructions']) < 1 or len(data['instructions']) > 100:
            is_valid = False
            flash("Instructions should be 1 to 100 characters in length!")
        
        if len(data['description']) < 1 or len(data['description']) > 100:
            is_valid = False
            flash("Description should be 1 to 100 characters in length!")
            
        if len(data['date']) != 10:
            is_valid = False
            flash('Please provide a valid date')
        
        # if data['under_30_mins'] == None:
        #     is_valid = False
        #     flash('Please provide a valid selection')
    
        # if data['under_30_mins'] != "Yes" and data['under_30_mins']!= "No" :
        #     is_valid = False
        #     flash('Please provide a valid selection')
        
        
        return is_valid

    @classmethod
    def edit_recipe(cls, data):

        query = 'UPDATE recipes SET name = %(name)s, under_30_mins = %(under_30_mins)s, instructions = %(instructions)s, description = %(description)s, date = %(date)s WHERE id = %(id)s;'
        
        MySQLConnection('recipes_schema').query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):

        query='DELETE FROM recipes WHERE id = %(id)s;'

        return MySQLConnection('recipes_schema').query_db(query, data)
