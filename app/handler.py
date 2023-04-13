from slack import WebClient
from base64 import b64decode

from groups_read import get_groups_list
from groups_write import request_to_join_group

import os
import urllib

INVALID_REQUEST_ERROR = (
    "Sorry your request is invalid"
)

PRIVATE_MESSAGE_NUDGE = "Please direct message me to get the list or join a channel. :slightly_smiling_face:"          

def _is_request_valid(token, team_id):
    return token == os.environ["SLACK_VERIFICATION_TOKEN"] and team_id == query_team_id()


def _is_private_message(channel_name):
    return channel_name == "directmessage"


def query_team_id():
    client = WebClient(token=os.environ["SLACK_BOT_USER_TOKEN"])
    response = client.api_call(api_method="team.info")
    if not response["ok"]:
        raise AssertionError

    return response["team"]["id"]


def oauth_URI(scope, client_id, redirect_uri):
    return (
        f"https://slack.com/oauth/authorize?scope={ scope }"
        f"&client_id={ client_id }&redirect_uri={ redirect_uri }"
    )

def decode_body(body):
    decoded_body = b64decode(body).decode('utf-8')
    pairs = decoded_body.split("&")

    return dict(pair.split("=") for pair in
                    pairs)


def slack_web_client(token=os.environ["SLACK_BOT_USER_TOKEN"]):
    return WebClient(token=token)


def handler(event, _):
    print(event)
    body = decode_body(event["body"])
    print(body)

    if not _is_request_valid(body.get("token"), body.get("team_id")):
        return INVALID_REQUEST_ERROR


    if not _is_private_message(body.get("channel_name")):
        return PRIVATE_MESSAGE_NUDGE


    command = urllib.parse.unquote(body.get("command"))
    if command == "/list-groups" or command == "/test_list":
        return get_groups_list(slack_web_client())

    if command == "/join-group" or command == "/test_join":
        user_id = body.get("user_id")
        channel_name = body.get("text")
        oauth_uri = oauth_URI(
             "groups:write", os.environ["SLACK_CLIENT_SECRET"], os.environ["REDIRECT_URI"]
            )
        
        return request_to_join_group(
                slack_web_client(), user_id, channel_name, oauth_uri
            )