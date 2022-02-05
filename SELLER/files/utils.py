import sqlite3
import secrets
import os
from unittest import result
from .models import Seller
from files import db, config
from flask_login import current_user



def dbquery(query, data):
    dbAddress = config.PRODUCT_DATABASE
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()


def saveProdImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    return imageName


def saveShopImage(formImage):
    randonHex = secrets.token_hex(8)
    _, fileExe = os.path.splitext(formImage.filename)
    imageName = randonHex +  fileExe
    container_client = config.get_client()
    container_client.upload_blob(imageName, formImage)
    return imageName


def add_seller(form):
    shopLogo = saveShopImage(form.shopLogo.data)
    new_seller = Seller(
                        fname = form.sellerFirstName.data,\
                        lname = form.sellerLastName.data,\
                        email = form.email.data,\
                        password = form.pswd.data,\
                        address = form.address.data,\
                        city = form.city.data, \
                        state = form.state.data, \
                        pin = form.pin.data, \
                        shopName= form.shopName.data, \
                        shopLogo = get_image_url(shopLogo)
                        )
    db.session.add(new_seller)
    db.session.commit()


def add_product(form):
    productImage = saveProdImage(form.productPhoto.data)
    connection = sqlite3.connect(config.PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = """ INSERT INTO products 
                (productName, 
                productType, 
                productPhoto, 
                productDesc, 
                productPrice, 
                shopName, 
                sellerID, 
                sellerAddress,
                sellerEmail)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """
    data =  (
            form.productName.data,\
            form.productType.data,\
            get_image_url(productImage),\
            form.productDesc.data,\
            int(form.productPrice.data),\
            current_user.shopName,\
            int(current_user.id),\
            current_user.address,\
            current_user.email,\
            )
    cursor.execute(query, data)
    connection.commit()
    connection.close()


def get_image_url(image_name):
    container_client = config.get_client()
    logo_url = container_client.get_blob_client(blob = image_name).url
    return logo_url


def get_products_details(current_user_id: int):
    cursor = config.get_cursor()
    query = "SELECT * FROM products WHERE sellerID = (?)"
    data = (current_user_id, )
    cursor.execute(query, data)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],

        })
    return prods


def get_this_product(current_user_id: int, data):
    cursor = config.get_cursor()
    data = "%{0}%".format(data)
    query = "SELECT * FROM products\
            WHERE\
            (sellerID = {}) AND (\
            ProductName LIKE '{}' OR\
            productType LIKE '{}' OR\
            productDesc LIKE '{}')\
            ORDER BY productName, productType, productDesc"\
            .format(current_user_id, data, data, data, data, data)
    cursor.execute(query)
    results = cursor.fetchall()
    prods = []
    for result in results:
        prods.append({
            "prod_id" : result[0],
            "prod_name" : result[1],
            "prod_type" : result[2],
            "prod_img" : result[3],
            "prod_desc": result[4], 
            "prod_price": result[5],
            "prod_shop": result[6],
            "seller_id" : result[7],
            "prod_seller" : result[8]
        })
    return prods

def update_order_status(action):
        query = " UPDATE orders SET status = ? WHERE id = ?"
        data = (str(action[0]), int(action[1]),)
        dbquery(query, data)


def get_all_orders():
    connection = sqlite3.connect(config.PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT \
                products.productName, \
                products.productPhoto, \
                orders.buyerName, \
                orders.buyerEmail,\
                orders.id,\
                orders.status,\
                orders.productID,\
                orders.orderTime,\
                orders.buyeAdd\
            FROM products INNER JOIN orders ON products.sellerID = orders.sellerID\
            WHERE orders.sellerID = (?) AND orders.productID = products.id AND orders.status <> 'Received' AND orders.status <> 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    orders = []
    for result in results:
        orders.append({
                    "productName" : result[0],
                    "productPhoto" : result[1],
                    "buyerName" : result[2],
                    "buyerEmail" : result[3],
                    "orderId" : result[4],
                    "status" : result[5],
                    "productID" : result[6],
                    "orderTime" : result[7],
                    "buyerAdd" : result[8]
                    })
    return orders


def get_orders_history():
    print("\n\n\n\n")
    connection = sqlite3.connect(config.PRODUCT_DATABASE)
    cursor = connection.cursor()
    query = "SELECT \
                products.productName, \
                products.productPhoto, \
                orders.buyerName, \
                orders.buyerEmail,\
                orders.id,\
                orders.status,\
                orders.productID,\
                orders.orderTime,\
                orders.buyeAdd\
            FROM products INNER JOIN orders ON products.sellerID = orders.sellerID\
            WHERE orders.sellerID = (?) AND orders.productID = products.id AND orders.status = 'Received' OR orders.status = 'Cancelled'"
    data = (int(current_user.id), )
    cursor.execute(query, data)
    results = cursor.fetchall()
    orders = []
    for result in results:
        orders.append({
                    "productName" : result[0],
                    "productPhoto" : result[1],
                    "buyerName" : result[2],
                    "buyerEmail" : result[3],
                    "orderId" : result[4],
                    "status" : result[5],
                    "productID" : result[6],
                    "orderTime" : result[7],
                    "buyerAdd" : result[8]
                    })
    print(orders)
    return orders