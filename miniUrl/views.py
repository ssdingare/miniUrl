from flask import request, redirect, jsonify
from miniUrl import app, get_db, shorten
from utility import *


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    shorten_url: Validates the json request, creates the shortened url and returns as json
    """
    try:
        print(app.__class__)
        json_obj = request.get_json()
        validate_json(json_obj)
        validate_urls(json_obj, app.config['MINI_URL_BASE'])
        mini_url = shorten.add_mini_url(get_db(), json_obj, app.config['MINI_URL_BASE'])
        response = { 'miniUrl': mini_url }
        return jsonify(response)
    except JsonValidationException:
        return error_response("Invalid request format")
    except UrlValidationException:
        return error_response("Invalid url specified")


@app.route('/mini/<mini_url>', methods=['GET'])
def redirect_to_target(mini_url):
    """
    redirect_to_target: Given a GET request to a mini url, identifies the device type
    of the user agent. If device is a tablet or mobile and a corresponding url is stored,
    redirects to that url. Otherwise redirects to the default url. If the mini url is not
    found in db returns 404
    @:param mini_url
    """
    user_agent_str = request.headers.get('User-Agent')
    device_type = identify_device_type(user_agent_str)
    redirect_url = shorten.retrieve_url(get_db(), mini_url, device_type)
    if redirect_url is None:
        return error_response("No such url stored"), 404
    else:
        return redirect(redirect_url)


@app.route('/stats', methods=['GET'])
def stats():
    """
    Return stats for all stored urls, including age and hit count
    """
    return jsonify(shorten.get_stats(get_db(), app.config['MINI_URL_BASE']))


def error_response(error_msg):
    return jsonify({"Status": "Failure", "Error": error_msg})
