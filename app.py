from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import json

app = Flask(__name__)

# Swagger configuration
