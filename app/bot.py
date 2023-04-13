from urllib.parse import unquote

from slack import WebClient

from app.groups_read import get_groups_list
from app.groups_write import invite_user_to_group, request_to_join_group


def slack_web_client(token=current_app.config["SLACK_BOT_USER_TOKEN"]):
    return WebClient(token=token)


def list_groups():
    form_data = request.form
    if not _is_request_valid(
        form_data,
        current_app.config["SLACK_VERIFICATION_TOKEN"],
        current_app.config["SLACK_TEAM_ID"],
    ):
        abort(400)

    if not _is_private_message(form_data):
        return PRIVATE_MESSAGE_NUDGE

    return get_groups_list(slack_web_client())


def join_channel():
    form_data = request.form
    if not _is_request_valid(
        form_data,
        current_app.config["SLACK_VERIFICATION_TOKEN"],
        current_app.config["SLACK_TEAM_ID"],
    ):
        abort(400)

    if not _is_private_message(form_data):
        return PRIVATE_MESSAGE_NUDGE

    return request_to_join_group(
        slack_web_client(), form_data, current_app.config["OAUTH_URI"]
    )


def confirm_invite():
    auth_code = request.args["code"]
    client = slack_web_client("")

    response = client.oauth_access(
        client_id=current_app.config["SLACK_CLIENT_ID"],
        client_secret=current_app.config["SLACK_CLIENT_SECRET"],
        code=auth_code,
        redirect_uri=current_app.config["REDIRECT_URI"],
    )

    oauth_token = response["access_token"]
    raw_state = unquote(request.args["state"])

    # Permissions note:
    # This must be a user token (xoxp) from a user who is already in the private channel.
    return invite_user_to_group(
        slack_web_client(oauth_token), slack_web_client(), raw_state
    )
