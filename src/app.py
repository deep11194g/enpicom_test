from flask import Flask
from flask import request
from flask import jsonify

import views

app = Flask(__name__)


@app.route('/dnas', methods=['POST', 'GET'])
def dnas():
    """Here `dnas` representing plural (set) of DNA"""
    if request.method == 'POST':
        response_body, status_code = views.add_dna()
    else:   # GET method
        response_body, status_code = views.find_matching_dnas()

    return jsonify(response_body), status_code


if __name__ == '__main__':
    app.run()
