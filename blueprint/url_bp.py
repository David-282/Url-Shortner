from flask import request, jsonify, redirect
from flask import Blueprint
from services.url_services import get_short_code, get_original_url, get_url_stats

url_blueprint = Blueprint("url", __name__)


@url_blueprint.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    result= get_short_code(data["original_url"])
    return jsonify(result),201


@url_blueprint.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    original_url = get_original_url(short_code)
    return redirect(original_url, code=302)


@url_blueprint.route("/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    result = get_url_stats(short_code)
    return jsonify(result), 200