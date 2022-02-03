import os
from azure.storage.blob import BlobServiceClient


class Config(object):
    SECRET_KEY = os.environ.get('secrteKey5H') or "ohe#%DWM^&5ERASbF_(DSA!@$>^WSGssaf"
    SQLALCHEMY_BINDS = {
        'sellerdb' : "sqlite:///databases/seller.db",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # UPLOAD_FOLDER = "C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\images\products"


def get_client():
    conn_str = "DefaultEndpointsProtocol=https;AccountName=learn10sg;AccountKey=AHTtAU6SOIzK7jqLwgyVm88BTyqNgduQkc6jPXj30RWgPOAh7TGzdTGYfKxSSlU1mq9a9H/14ZltDPJJMSfxJQ==;EndpointSuffix=core.windows.net" # retrieve the connection string from the environment variable
    container = "cnt1"
    blob_service_client = BlobServiceClient.from_connection_string(conn_str = conn_str)
    container_service_client = blob_service_client.get_container_client(container=container)
    container_service_client.get_container_properties()
    return container_service_client
