import os
import slack
from groups_read import get_groups_list
from flask import abort, Flask, jsonify, request
from urllib.parse import unquote

app = Flask(__name__)
client_id = os.environ['SLACK_CLIENT_ID']
client_secret = os.environ['SLACK_CLIENT_SECRET']
oauth_scope = os.environ['SLACK_BOT_SCOPE']
private_message_nudge = 'Please direct message me to get the list or join a channel. :slightly_smiling_face:'


def _is_request_valid(request):
    # TODO: fix this to use request signing rather than deprecated verification token
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


def _is_private_message(request):
    return request.form['channel_name'] == 'directmessage'


@app.route('/list', methods=['POST'])
def list_groups():
    if not _is_request_valid(request):
        abort(400)
    
    if not _is_private_message(request):
        return private_message_nudge
    
    return get_groups_list(request)

