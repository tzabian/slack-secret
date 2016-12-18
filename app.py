import os

from flask import Flask, request, Response

slack_token = os.environ.get('SLACK_TOKEN')

app = Flask(__name__)


@app.route('/secret', methods=['post'])
def secret():

    token = request.values.get('token')

    if token != slack_token:
        return Response('You are not authorized to use slack-secret',
                        content_type='text/plain; charset=utf-8')

    return request.values.get('text')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
