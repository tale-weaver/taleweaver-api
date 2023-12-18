from flask import send_from_directory, request
from flask import current_app as app
from flask_restful import Resource


class StaticImage(Resource):
    def get(self, filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
