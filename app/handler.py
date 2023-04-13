from slack import WebClient
from base64 import b64decode

import logging
import time
import json

logger = logging.getLogger() 
logger_level = logging.INFO  
logger.setLevel(logger_level)

# structured logging                     
def log(msg="", data=None, level='info'):
    j = json.dumps(data) if data else "" 
    s = (msg + " " + j).strip()          
    getattr(logger, level)(s)           


def query_team_id(slack_bot_token):
    client = slack.WebClient(token=slack_bot_token)
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
    decoded_body = b64decode(body).decode('ascii')
    pairs = decoded_body.split("&")
    return dict(pair.split("=") for pair in
                    pairs)
      

def handler(event, context):
    start_t = time.time()
    body = decode_body(event["body"])
    print(body)
    # command = body.get("command")
    # # command starts with %2 for some reason
    # sanitized_command = 

    client = WebClient(token='token')
    
    response = dict()
    response['duration'] = "{} ms".format(
        round(1000 * (time.time() - start_t), 2))

    log("Response", response)
    return response