import firebase_admin
from firebase_admin import firestore, App
import google.cloud.firestore

firebase: App
client: google.cloud.firestore.Client


def init_firebase():
    global firebase, client

    firebase = firebase_admin.initialize_app()
    client = firestore.client()
