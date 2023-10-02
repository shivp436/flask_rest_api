from flask import Flask, request, jsonify
# sqlAlchemy to abstract the SQL methods, and use them as functions, like mongoose with mongoDB
from flask_sqlalchemy import SQLAlchemy
# to serialise and deserialise objects
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)

# variable to locate the database root
basedir = os.path.abspath(os.path.dirname(__file__))

# database
# setting db uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# Product Class/model
# this syntax is because of Alchemy
# this is used for POST requests
class Product(db.Model): # .Model will give us some pre built methods for our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        
# Product schema - this is while using GET requests to fetch the data
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty') # this field tells what properties we want to return in a get request
        
# Initialise schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) # for multiple products

# Create a product
@app.route('/product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']
        
        # create Product object
        new_product = Product(name, description, price, qty)
        
        db.session.add(new_product)
        # save it to database
        db.session.commit()
        
        return product_schema.jsonify(new_product)
    
    # get all products
    all_products = Product.query.all() # this gets all the contents, no need to say SELECT * FROM Products etc...
    result = products_schema.dump(all_products) # wll take a collection of "Product" objects and convert it into JSON-like dictionary
    return jsonify(result)

# get single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# update a product
@app.route('/product/<id>', methods=['PUT']) # PUT method is used to update something on the server
def update_product(id):
    # fetch old product
    product = Product.query.get(id)
    # new values
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    # update the values
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    
    db.session.commit()
    
    return product_schema.jsonify(product)

# delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
    
# run server
if __name__ == '__main__':
    # debug enabled, since we are in development mode 
    app.run(debug = True)