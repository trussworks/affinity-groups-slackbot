import os
import slack
from groups_read import get_groups_list
from groups_write import *
from flask import abort, Flask, jsonify, request
from urllib.parse import unquote

app = Flask(__name__)
client_id = os.environ['SLACK_CLIENT_ID']
client_secret = os.environ['SLACK_CLIENT_SECRET']
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


@app.route('/join', methods=['POST'])
def join_channel():
    if not _is_request_valid(request):
        abort(400)
    
    if not _is_private_message(request):
        return private_message_nudge

    return request_to_join_group(request)


@app.route('/confirm_invite', methods=['GET', 'POST'])
def confirm_invite():
    auth_code = request.args['code']
    client = slack.WebClient(token='')

    response = client.oauth_access(
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code,
        redirect_uri=redirect_uri,
    )

    oauth_token = response['access_token']
    raw_state = unquote(request.args['state'])

    return invite_user_to_group(raw_state, oauth_token)

