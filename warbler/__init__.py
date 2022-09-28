from flask import Flask
from warbler.messages import messages

app = Flask(__name__)
app.register_blueprint(messages)