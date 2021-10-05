from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///manytomany1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Associate Table
subs = db.Table('subs',
    db.Column('product_id',db.Integer, db.ForeignKey('product.product_id')),
    db.Column('vendor_id',db.Integer, db.ForeignKey('vendor.vendor_id')),
    )


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    vendors = db.relationship("Vendor", secondary=subs, back_populates="products")


class Vendor(db.Model):
    vendor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    products = db.relationship("Product", secondary=subs, back_populates="vendors")


# Add New vendor
@app.route('/vendor', methods=['POST'])
def add_vendor():

    data = request.get_json()
    new_vendor = Vendor(name = data['name'])
    db.session.add(new_vendor)
    db.session.commit()
    return jsonify({'message':'New vendor Created'}), 200


# Add new Product
@app.route('/product', methods=['POST'])
def add_product():

    data = request.get_json()
    new_product = Product(product_name = data['product_name'])

    vendor = db.session.query(Vendor).filter_by(vendor_id="4").first()

    db.session.add(new_product)

    new_product.vendors.append(vendor)

    db.session.commit()
    return jsonify({'message':'New Product Created'}), 200


# Get All vendor
@app.route('/vendor', methods=['GET'])
def get_all_vendor():

    alldata = Vendor.query.all()
    if not alldata:
        return jsonify({'message':'No Data found'}), 404

    output = []
    for data in alldata:
        vendore_data = {}
        vendore_data['id'] = data.vendor_id
        vendore_data['name'] = data.name
        vendore_data['product'] = get_product(data)
        output.append(vendore_data)

    return jsonify({'data':output}), 200


#Get One vendor
@app.route("/vendor/<id>", methods=['GET'])
def get_one_vendor(id):
    data = Vendor.query.filter_by(vendor_id=id).first()
    if not data:
        return jsonify({'message':'No Data found'}), 404

    vendor_data = {}
    vendor_data['id'] = data.vendor_id
    vendor_data['name'] = data.name
    vendor_data['products'] = get_product(data)
    return jsonify({'data':vendor_data})


def get_product(data):

    if not data.products:
        return None

    output=[]
    for data in data.products:
        product_data = {}
        product_data['product id'] = data.product_id
        product_data['product name'] = data.product_name
        output.append(product_data)

    return output





#Get One Product
@app.route("/product/<id>", methods=['GET'])
def get_one_product(id):
    data = Product.query.filter_by(product_id=id).first()
    print(data)
    print(data.vendors)
    if not data:
        return jsonify({'message':'No Data found'}), 404

    product_data = {}
    product_data['id'] = data.product_id
    product_data['name'] = data.product_name
    product_data['Vendor'] = get__vendor(data)
    return jsonify({'data':product_data})


# Get All product
@app.route('/product', methods=['GET'])
def get_all_product():

    alldata = Product.query.all()
    if not alldata:
        return jsonify({'message':'No Data found'}), 404

    output = []
    for data in alldata:
        product = {}
        product['id'] = data.product_id
        product['name'] = data.product_name
        product['vendor'] = get__vendor(data)
        output.append(product)

    return jsonify({'data':output}), 200


def get__vendor(data):
    if not data:
        return None
    output=[]
    for data in data.vendors:
        vendor_data = {}
        vendor_data['vendor id'] = data.vendor_id
        vendor_data['vendor name'] = data.name
        output.append(vendor_data)
    return output



if __name__ == '__main__':

    app.run(debug=True)












# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///manytomany.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# #Associate Table
# subs = db.Table('subs',
#     db.Column('vendor_id',db.Integer, db.ForeignKey('vendor.vendor_id')),
#     db.Column('product_id',db.Integer, db.ForeignKey('product.product_id')),
#     )


# class Vendor(db.Model):
#     vendor_id = db.Column(db.Integer, primary_key=True)
#     vendor_name = db.Column(db.String(20))
#     vendorr = db.relationship('Product', secondary=subs, backref=db.backref('vendddor', lazy = 'dynamic'))


# class Product(db.Model):
#     product_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))



# # Add New product
# @app.route('/product', methods=['POST'])
# def add_product():

#     data = request.get_json()
#     new_product = Product(name = data['name'])

#     vendor = db.session.query(Vendor).filter_by(vendor_id="3").first()

#     db.session.add(new_product)

#     new_product.vendddor.append(vendor)

#     db.session.commit()
#     return jsonify({'message':'New product Created'}), 200


# # Add new Vendor
# @app.route('/vendor', methods=['POST'])
# def add_vendor():

#     data = request.get_json()
#     new_vendor = Vendor(vendor_name = data['vendor_name'])
#     db.session.add(new_vendor)
#     db.session.commit()
#     return jsonify({'message':'New Vendor Created'}), 200




# # Get All Products
# @app.route('/product', methods=['GET'])
# def get_all_products():

#     alldata = Product.query.all()

#     if not alldata:
#         return jsonify({'message':'No Data found'}), 404

#     output = []
#     for data in alldata:
#         product_data = {}
#         product_data['id'] = data.product_id
#         product_data['name'] = data.name
#         product_data['vendor'] = get_vendor(data)
#         output.append(product_data)

#     return jsonify({'data':output}), 200



# #Get One Product
# @app.route("/product/<id>", methods=['GET'])
# def get_one_product(id):
#     data = Product.query.filter_by(product_id=id).first()
#     print(data)
#     print(data.vendddor[0])
#     if not data:
#         return jsonify({'message':'No Data found'}), 404

#     product_data = {}
#     product_data['id'] = data.product_id
#     product_data['name'] = data.name
#     product_data['vendor'] = get_vendor(data)
#     return jsonify({'data':product_data})


# def get_vendor(data):

#     if not data:
#         return None
#     try:
#         vendor = data.vendddor[0]
#     except:
#         return None

#     vendor_data = {}
#     vendor_data['vendor id'] = vendor.vendor_id
#     vendor_data['vendor name'] = vendor.vendor_name

#     return vendor_data





# #Get One Vendor
# @app.route("/vendor/<id>", methods=['GET'])
# def get_one_vendor(id):
#     data = Vendor.query.filter_by(vendor_id=id).first()
#     print(data)
#     print(data.vendddor[0])
#     if not data:
#         return jsonify({'message':'No Data found'}), 404

#     vendor_data = {}
#     vendor_data['id'] = data.vendor_id
#     vendor_data['name'] = data.vendor_name
#     vendor_data['product'] = get_one_product(data)
#     return jsonify({'data':vendor_data})


# # Get All vendor
# @app.route('/vendor', methods=['GET'])
# def get_all_vendor():

#     alldata = Vendor.query.all()

#     if not alldata:
#         return jsonify({'message':'No Data found'}), 404

#     output = []
#     for data in alldata:
#         vendor = {}
#         vendor['id'] = data.vendor_id
#         vendor['name'] = data.vendor_name
#         vendor['product'] = get_one_product(data)
#         output.append(vendor)

#     return jsonify({'data':output}), 200


# def get_one_product(data):

#     if not data:
#         return None
#     try:
#         product = data.vendddor[0]
#     except:
#         return None

#     product_data = {}
#     product_data['product id'] = product.product_id
#     product_data['product name'] = product.name

#     return product_data



# if __name__ == '__main__':

#     app.run(debug=True)
