from flask import Flask, Response, request
from flask_cors import CORS
import json
from typing import *
import requests

app = Flask(__name__)
CORS(app)

BLOG_PROPS = {
    'microservice': 'blog microservice',
    # 'api': 'http://localhost:5012/'
    'api': 'http://34.201.55.17:5012/'
}

BLOG_NUMBER_PROPS = {
    'microservice': 'blog microservice',
    # 'api': 'http://localhost:5012/blognumber'
    'api': 'http://34.201.55.17:5012/blognumber'
}

COMMENT_PROPS = {
    'microservice': 'comment microservice',
    # 'api': 'http://localhost:5013/'
    'api': 'http://54.147.113.194:5013/'
}

COMMENT_BYUSER_PROPS = {
    'microservice': 'comment microservice',
    # 'api': 'http://localhost:5013/commentnumber'
    'api': 'http://54.147.113.194:5013/commentnumber'
}


def get_user_blognum_and_commentnum(username):
    blog_response = requests.get(BLOG_NUMBER_PROPS['api'], params={
        'username': username
    })
    blog_data = blog_response.text

    comment_response = requests.get(COMMENT_BYUSER_PROPS['api'], params={
        'username': username
    })
    comment_data = comment_response.text

    result = {
        'blognum': blog_data,
        'commentnum': comment_data
    }
    print(result)
    return Response(json.dumps(result, default=str), status=200, content_type="application/json")


def get_allposts_and_commentnum():
    allposts_response = requests.get(BLOG_PROPS['api'] + 'allposts')
    allposts = allposts_response.json()
    for each in allposts:
        blog_id = str(each['unique_blog_id'])
        commentnum = requests.get(COMMENT_PROPS['api'] + 'posts/' + blog_id + '/getcommentsnum').text
        each['commentnum'] = commentnum  
    return allposts


def get_mypost_and_commentnum(username):
    myposts_response = requests.get(BLOG_PROPS['api'] + username + '/myposts')
    myposts = myposts_response.json()
    for each in myposts:
        blog_id = str(each['unique_blog_id'])
        commentnum = requests.get(COMMENT_PROPS['api'] + 'posts/' + blog_id + '/getcommentsnum').text
        each['commentnum'] = commentnum
    return myposts


def get_single_post(blog_id):
    singlepost_response = requests.get(BLOG_PROPS['api'] + 'posts/' + blog_id)
    singlepost = singlepost_response.json()
    commentnum = requests.get(COMMENT_PROPS['api'] + 'posts/' + blog_id + '/getcommentsnum').text
    singlepost['commentnum'] = commentnum
    return singlepost


@app.route('/getuseraction', methods=['GET'])
def get_user_actions():
    if request.method != 'GET':
        status_code = 405
        return Response(f"{status_code} - wrong method!", status=status_code, mimetype="application/json")
    # req_data = request.get_json()
    username = request.args.get('username')
    response = get_user_blognum_and_commentnum(username)
    return response


@app.route('/getmypostinfo', methods=['GET'])
def get_mypost_info():
    username = request.args.get("username")
    result = get_mypost_and_commentnum(username)
    return Response(json.dumps(result, default=str), status=200, content_type="application/json")


@app.route('/getallpostsinfo', methods = ['GET'])
def get_allposts_info():
    result = get_allposts_and_commentnum()
    return Response(json.dumps(result, default=str), status=200, content_type="application/json")


@app.route('/singlepostinfo/<blog_id>', methods = ['GET'])
def get_single_post_info(blog_id):
    result = get_single_post(str(blog_id))
    return Response(json.dumps(result, default=str), status=200, content_type="application/json")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5014)
