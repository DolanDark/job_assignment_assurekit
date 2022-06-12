import pyrebase


firebase_config = {
  "apiKey": "AIzaSyC6izH7bqmq-EQY6JbhFPRxFIGzMZWrLK8",
  "authDomain": "akash-test-338618.firebaseapp.com",
  "projectId": "akash-test-338618",
  "storageBucket": "akash-test-338618.appspot.com",
  "messagingSenderId": "217507775389",
  "appId": "1:217507775389:web:75533c3b53d8fa81f4e574",
  "databaseURL": ""
  }

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

email = "test@gmail.com"
password = "testtest123"

# new_user = auth.create_user_with_email_and_password(email, password)
# uid = new_user['localId']

logging_in = auth.sign_in_with_email_and_password(email, password)
print(logging_in)