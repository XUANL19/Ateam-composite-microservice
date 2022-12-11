from flask import Flask, Response, request
from flask_cors import CORS
import json
from typing import *
import requests

app = Flask(__name__)
CORS(app)

BLOG_PROPS = {
    'microservice': 'blog microservice',
    'api': 'http://localhost:5012/blognumber'
}

COMMENT_PROPS = {
    'microservice': 'comment microservice',
    'api': 'http://localhost:5013/commentnumber'
}


def get_user_blognum_and_commentnum(username):
    blog_response = requests.get(BLOG_PROPS['api'], params={
        'username': username
    })
    blog_data = blog_response.text

    comment_response = requests.get(COMMENT_PROPS['api'], params={
        'username': username
    })
    comment_data = comment_response.text

    result = {
        'blognum': blog_data,
        'commentnum': comment_data
    }
    print(result)
    return Response(json.dumps(result, default=str), status=200, content_type="application/json")


@app.route('/getuseraction', methods=['GET'])
def get_user_action():
    if request.method != 'GET':
        status_code = 405
        return Response(f"{status_code} - wrong method!", status=status_code, mimetype="application/json")
    # req_data = request.get_json()
    username = request.args.get('username')
    response = get_user_blognum_and_commentnum(username)
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5014)