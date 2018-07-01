from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, api, Resource, User