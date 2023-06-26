from flask import Flask, render_template, current_app
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import googlemaps
import os
import json
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	bootstrap.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app