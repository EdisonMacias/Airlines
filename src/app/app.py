from flask import Flask

app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"
