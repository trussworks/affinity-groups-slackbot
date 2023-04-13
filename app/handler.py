from slack import WebClient
from base64 import b64decode

from groups_read import get_groups_list

import time
import os

PRIVATE_MESSAGE_NUDGE = "Please direct message me to get the list or join a channel. :slightly_smiling_face:"          

def _is_request_valid(token):
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


def list_groups(channel_name):
    if not _is_private_message(channel_name):
        return PRIVATE_MESSAGE_NUDGE

    return get_groups_list(slack_web_client())
      

def handler(event, context):
    start_t = time.time()
    print(event)
    body = decode_body(event["body"])
    
    command = body.get("command")
    
    if not _is_request_valid(body.get("token"), body.get("team_id")):
        return 'this is not a valid request'
    
    if command == "%2list-groups" or command == "%2test_list":
        return list_groups(body.get("channel_name"))
    
    response = dict()
    response['duration'] = "{} ms".format(
        round(1000 * (time.time() - start_t), 2))

    log("Response", response)
    return response