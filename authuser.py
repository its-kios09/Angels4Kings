from pyrebase import pyrebase



# Initialize firebase
config = {
    'apiKey': "AIzaSyBPnqa2PdpSnipXI1S407rfIHFYEY4aWp8",
    'authDomain': "kingsauth-67a90.firebaseapp.com",
    'projectId': "kingsauth-67a90",
    'storageBucket': "kingsauth-67a90.appspot.com",
    'messagingSenderId': "698579119515",
    'appId': "1:698579119515:web:81f6f24d1225745278053e",
    'measurementId': "G-XHE0YBHKDH",
     'databaseURL':''
    
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
