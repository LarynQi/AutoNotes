from flask import Flask

app_instance = Flask(__name__)

from application import transcription
