import os
import slack
from flask import Flask

def query_team_id(slack_bot_token):
    client = slack.WebClient(token=slack_bot_token)
    response = client.api_call(
        api_method='team.info'
    )
    assert response['ok']

    return response['team']['id']

def oauth_URI(scope, client_id, redirect_uri):
    return f'https://slack.com/oauth/authorize?scope={ scope }'\
        f'&client_id={ client_id }&redirect_uri={ redirect_uri }'

def create_app(config=None):
    app = Flask(__name__)
    app.config['SLACK_BOT_USER_TOKEN'] = os.environ['SLACK_BOT_USER_TOKEN']
    app.config['SLACK_CLIENT_ID'] = os.environ['SLACK_CLIENT_ID']
    app.config['SLACK_CLIENT_SECRET'] = os.environ['SLACK_CLIENT_SECRET']
    app.config['SLACK_VERIFICATION_TOKEN'] = os.environ['SLACK_VERIFICATION_TOKEN']
    app.config['REDIRECT_URI'] = os.environ['REDIRECT_URI']

    app.config['SLACK_TEAM_ID'] = query_team_id(app.config['SLACK_BOT_USER_TOKEN'])
    app.config['OAUTH_URI'] = oauth_URI('groups:write', \
        app.config['SLACK_CLIENT_ID'], app.config['REDIRECT_URI'])

    return app
