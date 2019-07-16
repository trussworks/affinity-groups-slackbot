import slack
from . import create_app
import app.groups_read as groups_read
import app.groups_write as groups_write
from flask import abort, request
from urllib.parse import unquote

flask_app = create_app()

PRIVATE_MESSAGE_NUDGE = 'Please direct message me to get the list or join a channel. :slightly_smiling_face:'


def slack_web_client(token=flask_app.config['SLACK_BOT_USER_TOKEN']):
    return slack.WebClient(token=token)


def _is_request_valid(form_data, verification_token, team_id):
    # TODO: fix this to use request signing rather than deprecated verification token
    return form_data['token'] == verification_token and form_data['team_id'] == team_id


def _is_private_message(form_data):
    return form_data['channel_name'] == 'directmessage'


@flask_app.route('/list', methods=['POST'])
def list_groups():
    if not _is_request_valid(request, flask_app.config['SLACK_VERIFICATION_TOKEN'], flask_app.config['SLACK_TEAM_ID']):
        abort(400)

    if not _is_private_message(request):
        return PRIVATE_MESSAGE_NUDGE

    return groups_read.get_groups_list()


@flask_app.route('/join', methods=['POST'])
def join_channel():
    form_data = request.form
    if not _is_request_valid(form_data):
        abort(400)

    if not _is_private_message(form_data):
        return PRIVATE_MESSAGE_NUDGE

    return groups_write.request_to_join_group(form_data, flask_app.config['OAUTH_URI'])


@flask_app.route('/confirm_invite', methods=['GET', 'POST'])
def confirm_invite():
    auth_code = request.args['code']
    client = slack_web_client('')

    response = client.oauth_access(
        client_id=flask_app.config['SLACK_CLIENT_ID'],
        client_secret=flask_app.config['SLACK_CLIENT_SECRET'],
        code=auth_code,
        redirect_uri=flask_app.config['REDIRECT_URI'],
    )

    oauth_token = response['access_token']
    raw_state = unquote(request.args['state'])

    return groups_write.invite_user_to_group(raw_state, oauth_token)
