import sqlite3
from flask import request, redirect, jsonify
from miniUrl import app, get_db, shorten
from utility import validate_json, classify_user_agent


@app.route('/shorten', methods=['POST'])
def index():
    try:
        json_obj = request.get_json()
        validate_json(json_obj)
        mini_url = shorten.add_mini_url(get_db(), json_obj)
        response = {'miniUrl': mini_url}
        return jsonify(response)
    except ValueError as ex:
        if ex.message == "url":
            return error_response("Invalid url specified")
        elif ex.message == "request":
            return error_response("Invalid request format")
    except sqlite3.Error as ex:
        print(ex.message)
        return error_response("Server error"), 500


@app.route('/mini/<mini_url>', methods=['GET'])
def redirect_to_target(mini_url):
    user_agent_str = request.headers.get('User-Agent')
    device_type = classify_user_agent(user_agent_str)
    try:
        redirect_url = shorten.retrieve_url(get_db(), mini_url, device_type)
        if redirect_url is not None:
            return redirect(redirect_url)
        else:
            return error_response("No such url stored"), 404
    except sqlite3.Error:
        return error_response("Server error"), 500


@app.route('/stats', methods=['GET'])
def stats():
    try:
        return jsonify(shorten.stats(get_db()))
    except sqlite3.Error:
        return error_response("Server error"), 500


def error_response(error_msg):
    return jsonify({"Status": "Failure", "Error": error_msg})


