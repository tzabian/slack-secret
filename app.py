import os
import requests

from requests.auth import HTTPBasicAuth
from flask import Flask, request, Response

slack_token = os.environ.get('SLACK_TOKEN')
ttl = os.environ.get('SECRET_TTL', 259200)  # 3 days
secret_user = os.environ.get('SECRET_USER')
secret_pass = os.environ.get('SECRET_PASS')

SECRET_BASE = "https://onetimesecret.com"
SECRET_LINK = "{}/secret/".format(SECRET_BASE)
SECRET_SHARE = "{}/api/v1/share".format(SECRET_BASE)

app = Flask(__name__)


@app.route('/secret', methods=['post'])
def secret():

    token = request.values.get('token')
    text = request.values.get('text')

    if token != slack_token:
        return Response('You are not authorized to use slack-secret',
                        content_type='text/plain; charset=utf-8')

    d = {'secret': text, 'ttl': ttl}
    r = requests.post(SECRET_SHARE, data=d, auth=HTTPBasicAuth(secret_user, secret_pass))

    return Response("{}{}".format(SECRET_LINK, r.json().get('secret_key')))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
